from odoo import http
from odoo.http import request

class PropertiesController(http.Controller):


    @http.route('/properties', type='http', auth="user", website=True)
    def properties(self, **kwargs):
        property_filter = kwargs.get('filter')
    
        
        domain = []
        if property_filter == 'sale':
            domain.append(('property_for', '=', 'sale'))
        elif property_filter == 'rent':
            domain.append(('property_for', '=', 'rent'))
        
        

        properties_records = request.env['bay.vista.property'].sudo().search(domain)
        properties_list = []

        for prop in properties_records:
            
            address_parts = []
            if prop.street: address_parts.append(prop.street)
            if prop.city: address_parts.append(prop.city)
            if prop.state_id: address_parts.append(prop.state_id.name)
            if prop.zip_code: address_parts.append(prop.zip_code)
            if prop.country_id: address_parts.append(prop.country_id.name)
            full_address = ", ".join(address_parts)

        
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'bay.vista.property'),
                ('res_id', '=', prop.id),
                ('res_field', '=', 'property_image')
            ], limit=1)

            properties_list.append({
                'id': prop.id,
                'name': prop.name,
                'full_address': full_address,
                'property_for': prop.property_for,
                'attachment_id': attachment.id if attachment else False,
                'number_bed': prop.number_bed,
                'number_bath': prop.number_bath,
                'square_feet': prop.square_feet,
            })

        return request.render('bayvista_realestate.properties_page', {
            'properties': properties_list,
            'current_filter': property_filter or 'all',
        })

    @http.route('/properties/details/<model("bay.vista.property"):prop>', type='http', auth='user', website=True)
    def details_property(self, prop, **kwargs):
        images_ids = []

        # --- 1. Include the main property image (if exists) ---
        if prop.property_image:
            # Look for an existing attachment for the property main image
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', prop._name),
                ('res_id', '=', prop.id),
                ('res_field', '=', 'property_image'),
            ], limit=1)
            if not attachment:
                # Create a new attachment record if one doesn't exist
                attachment = request.env['ir.attachment'].sudo().create({
                    'name': f'{prop.name} - Main Image',
                    'res_model': prop._name,
                    'res_id': prop.id,
                    'res_field': 'property_image',
                    'type': 'binary',
                    'datas': prop.property_image,
                })
            images_ids.append(attachment.id)

        # --- 2. Process each record in image_ids (One2many field) ---
        for image_rec in prop.image_ids:
            # Search for an existing attachment record for the image_rec's binary field.
            attachment = request.env['ir.attachment'].sudo().search([
                ('res_model', '=', 'property.image'),
                ('res_id', '=', image_rec.id),
                ('res_field', '=', 'image'),
            ], limit=1)
            if not attachment:
                # If not found, create an attachment record provided that there is image data.
                if getattr(image_rec, 'image', False):
                    attachment = request.env['ir.attachment'].sudo().create({
                        'name': image_rec.name or f'{prop.name} - Additional Image',
                        'res_model': 'property.image',
                        'res_id': image_rec.id,
                        'res_field': 'image',
                        'type': 'binary',
                        'datas': image_rec.image,
                    })
            images_ids.append(attachment.id if attachment else False)

        current_prop_user = request.env['bay.vista.user'].sudo().search([
            ('odoo_user_id', '=', request.env.user.id)
        ], limit=1)
        
        reviews = prop.sudo().review_ids
        values = {
            'prop': prop,
            'images': images_ids,
            'current_prop_user': current_prop_user,
            'reviews' : reviews,
        }
        return request.render('bayvista_realestate.property_details', values)
    
    
    @http.route('/property/submit_review', type='json', auth='user', methods=['POST'])
    def submit_review(self, **post):
        property_id = post.get('property_id')
        property_user_id = post.get('property_user_id')
        comment = post.get('comment')
        rating = post.get('rating', 0)
        
        if not (property_id and property_user_id and comment):
            return {"error": "Missing required fields."}
        
        # Create the review record in the property.review model
        review = request.env['property.review'].sudo().create({
            'property_id': int(property_id),
            'property_user_id': int(property_user_id),
            'comment': comment,
            'rating': int(rating),
        })
        
        return {"success": True, "review_id": review.id}
