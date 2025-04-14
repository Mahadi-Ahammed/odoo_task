from odoo import models, fields, api

class BayVistaUser(models.Model):
    _name = 'bay.vista.user'
    _description = 'Bay Vista Users'
    
    name = fields.Char(string="Full Name", required=True)
    email = fields.Char(string="Email", required=True, unique=True)
    password = fields.Char(string="Password", required=True)
    role = fields.Selection([
        ('buyer', 'Buyer'),
        ('owner', 'Owner'),
        ('admin', 'Admin'),
    ], string="Role", required=True, default='buyer')

    image = fields.Binary(string="Profile Picture")
    
    # Address details
    street = fields.Char(string="Street")
    city = fields.Char(string="City")
    zip_code = fields.Char(string="ZIP Code")
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string='State')
    odoo_user_id = fields.Many2one('res.users', string="Linked Odoo User", ondelete="cascade")


    @api.model
    def create(self, vals):
        """Create a custom user and securely link it with Odoo's authentication system (res.users)."""

        # Step 1: Create an associated partner record
        partner = self.env['res.partner'].create({
            'name': vals.get('name'),
            'email': vals.get('email'),
        })
        
        # Step 2: Create the Odoo user
        odoo_user = self.env['res.users'].with_context({'no_reset_password': True}).create({
            'name': vals.get('name'),
            'login': vals.get('email'),
            'partner_id': partner.id,
            'role_sync': vals.get('role')  # Sync role in res.users
        })

        # Step 3: Securely set the password using the Change Password Wizard
        password_wizard = self.env['change.password.wizard'].create({})
        password_change = self.env['change.password.user'].create({
            'wizard_id': password_wizard.id,
            'user_id': odoo_user.id,
            'new_passwd': vals.get('password'),
            'user_login': vals.get('email'),
        })
        password_change.change_password_button()

        # Step 4: Link the created Odoo user with the BayVistaUser model
        vals['odoo_user_id'] = odoo_user.id

        # Step 5: Sync role in both models
        odoo_user.sudo().write({'role_sync': vals.get('role')})

        return super(BayVistaUser, self).create(vals)

    def write(self, vals):
        """Ensure the role update in `bay.vista.user` also updates `res.users`."""
        res = super(BayVistaUser, self).write(vals)
        if 'role' in vals and self.odoo_user_id:
            self.odoo_user_id.sudo().write({'role_sync': vals.get('role')})
        return res

