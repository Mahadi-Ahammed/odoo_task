from odoo import models, fields, api
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class Property(models.Model):
    _name = 'bay.vista.property'
    _description = 'Bay Vista Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Property Name", required=True)
    address = fields.Text(string="Address")
    number_bed = fields.Integer(string="Number of Bedrooms")
    number_bath = fields.Integer(string="Number of Bathrooms")
    square_feet = fields.Float(string="Square Feet", tracking=True)
    property_for = fields.Selection([
        ('sale', 'Sale'),
        ('rent', 'Rent')
    ], string="Property For", required=True, tracking=True)

    image_ids = fields.One2many('property.image', 'property_id', string="Property Images")
    facilities = fields.Text(string="Facilities & Features")
    property_image = fields.Binary(string="Property Picture")
    
    # Address details
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    zip_code = fields.Char(string="ZIP Code")
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string='State')

    latitude = fields.Float(string="Latitude", readonly=True)
    longitude = fields.Float(string="Longitude", readonly=True)
    
    # Biling details
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    sale_price = fields.Float(string="Sale Price")
    offer = fields.Float(string="Offer")
    offer_price = fields.Float(string="Offer Price", compute='_compute_offer_price', store=True)
    offer_price_date_expire_date = fields.Date(string="Offer Expire Date")

    rent_price = fields.Float(string="Rent Price")
    booking_price = fields.Float(string="Booking Price")

    @api.depends('offer', 'sale_price')
    def _compute_offer_price(self):
        """ Compute the offer price based on the sale price and offer percentage """
        for record in self:
            if record.offer:
                record.offer_price = record.sale_price - (record.sale_price * (record.offer / 100))
            else:
                record.offer_price = 0.0

    # Property stage
    stage_id = fields.Many2one(
        'property.stage', 
        string="Stage",
        group_expand='_read_group_stage_ids'
    )

    stage_name = fields.Char(string="Stage Name", related='stage_id.name', store=True)

    def _get_lat_long(self):
        """ Fetch latitude and longitude based on the full address """
        full_address = f"{self.street or ''}, {self.city or ''}, {self.state_id.name or ''}, {self.zip_code or ''}, {self.country_id.name or ''}".strip()
        geolocator = Nominatim(user_agent="odoo_bayvista")
        try:
            location = geolocator.geocode(full_address, timeout=20)
            if location:
                return location.latitude, location.longitude
        except GeocoderTimedOut:
            return 0.0, 0.0
        return 0.0, 0.0

    @api.model
    def create(self, vals):
        """ Override create to auto-fetch latitude and longitude """
        record = super(Property, self).create(vals)
        if record.street or record.city or record.zip_code or record.state_id or record.country_id:
            lat, long = record._get_lat_long()
            record.write({'latitude': lat, 'longitude': long})

        if not record.stage_id: 
            stage = self.env['property.stage'].search([('sequence', '=', 1)], limit=1)
            if stage:
                record.stage_id = stage.id
        return record

    def write(self, vals):
        """ Override write to auto-update latitude and longitude """
        res = super(Property, self).write(vals)
        if 'street' in vals or 'city' in vals or 'zip_code' in vals or 'state_id' in vals or 'country_id' in vals:
            lat, long = self._get_lat_long()
            super(Property, self).write({'latitude': lat, 'longitude': long})
        return res

    def _read_group_stage_ids(self, stages, domain):
        """ Override to ensure all stages are available for grouping """
        stage_ids = stages.sudo()._search([], order=stages._order)
        return stages.browse(stage_ids)

