from odoo import models


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _message_post_after_hook(self, message, msg_vals):
        self.env['chat.bot'].reply_from_bot(self, msg_vals)
        return super(MailThread, self)._message_post_after_hook(message, msg_vals)