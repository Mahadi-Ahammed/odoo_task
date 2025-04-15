from odoo import http
from odoo.http import request

class BayVistaUserProfile(http.Controller):

    @http.route('/bay_vista_user/<model("bay.vista.user"):user>', type='http', auth='user', website=True)
    def profile(self, user, **kwargs):
        can_edit = (user.odoo_user_id.id == request.env.user.id)
        values = {
            'user_profile': user,
            'can_edit': can_edit,
        }
        return request.render('bayvista_realestate.user_profile_page', values)

    @http.route('/bay_vista_user/update_profile', type='json', auth='user', methods=['POST'])
    def update_profile(self, **post):
        # Only allow update if the user_id sent matches the current logged in user.
        user_id = post.get('user_id')
        if not user_id or int(user_id) != request.env.user.id:
            return {"error": "You can only update your own profile."}
        # Search for the bay.vista.user record linked to the current logged-in user.
        bay_user = request.env['bay.vista.user'].sudo().search([
            ('odoo_user_id', '=', request.env.user.id)
        ], limit=1)
        if not bay_user:
            return {"error": "User not found."}

        update_vals = {
            'name': post.get('name'),
            'email': post.get('email'),
            'street': post.get('street'),
            'city': post.get('city'),
            'zip_code': post.get('zip_code'),
            # Optionally, update country and state if provided:
            'country_id': int(post.get('country_id')) if post.get('country_id') else False,
            'state_id': int(post.get('state_id')) if post.get('state_id') else False,
        }
        bay_user.sudo().write(update_vals)
        return {"status": "success"}
