from odoo import models, fields, api

class ChatBot(models.AbstractModel):
    _name = 'chat.bot'
    _description = 'Chat Bot Model'

    def reply_from_bot(self, record, values, command=None):
        bot_id = self.env['ir.model.data']._xmlid_to_res_id("test_prec.bot_partner")
        if len(record) != 1 or values.get("author_id") == bot_id or values.get("message_type") != "comment" and not command:
            return
        if bot_id in values.get('partner_ids', []) or self._is_bot_in_private_channel(record):
            body = values.get("body", "").replace(u'\xa0', u' ').strip().lower().strip(".!")
            answer = self._get_answer(record, body, values, command)
            if answer:
                message_type = 'comment'
                subtype_id = self.env['ir.model.data']._xmlid_to_res_id('mail.mt_comment')
                record.with_context(mail_create_nosubscribe=True).sudo().message_post(body=answer, author_id=bot_id, message_type=message_type, subtype_id=subtype_id)

    def _is_bot_in_private_channel(self, record):
        bot_id = self.env['ir.model.data']._xmlid_to_res_id("test_prec.bot_partner")
        if record._name == 'discuss.channel' and record.channel_type == 'chat':
            return bot_id in record.with_context(active_test=False).channel_partner_ids.ids
        return False

    def _get_answer(self, record, body, values, command):
        return "you said: " + body + " and I am a bot"

    @api.model
    def search_odoobot_channel(self):
        odoobot_partner_id = self.env['ir.model.data']._xmlid_to_res_id("test_prec.bot_partner")
        odoobot_name = self.env['res.partner'].browse(odoobot_partner_id).name
        current_user = self.env.user.partner_id
        bot_channels = self.env['discuss.channel'].search([('channel_partner_ids','in', [odoobot_partner_id]),('channel_type','=','chat')])
        channel = bot_channels.filtered(lambda c: current_user in c.channel_partner_ids)
        if not channel:
            channel = self.env['discuss.channel'].create({
                'name': '#{},{}'.format(odoobot_name, current_user.name),
                'channel_type': 'chat',
                'channel_partner_ids': [(4, odoobot_partner_id), (4, current_user.id)]
            })
        return channel.id



