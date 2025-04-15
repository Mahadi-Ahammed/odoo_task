from odoo.addons.mail.controllers.thread import ThreadController
from odoo import http
from odoo.http import request
from markupsafe import Markup
from odoo.addons.mail.models.discuss.mail_guest import add_guest_to_context
from werkzeug.exceptions import NotFound
from odoo.addons.mail.tools.discuss import Store


class CustomThreadController(ThreadController):
    @http.route("/mail/message/update_content", methods=["POST"], type="json", auth="public")
    @add_guest_to_context
    def mail_message_update_content(self, message_id, body, attachment_ids, attachment_tokens=None, partner_ids=None, **kwargs):
        guest = request.env["mail.guest"]._get_guest_from_context()
        guest.env["ir.attachment"].browse(attachment_ids)._check_attachments_access(attachment_tokens)
        message = request.env["mail.message"]._get_with_access(message_id, "create", **kwargs)
        if not message:
            raise NotFound()
        # sudo: mail.message - access is checked in _get_with_access and _is_message_editable
        message = message.sudo()
        body = Markup(body) if body else body  # may contain HTML such as @mentions
        guest.env[message.model].browse([message.res_id])._message_update_content(
            message, body=body, attachment_ids=attachment_ids, partner_ids=partner_ids
        )
        return Store(message, for_current_user=True).get_result()