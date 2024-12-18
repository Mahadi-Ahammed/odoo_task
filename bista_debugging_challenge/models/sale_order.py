from collections import defaultdict
from datetime import timedelta

from markupsafe import Markup

from odoo import api, fields, models, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
from odoo.fields import Command
from odoo.osv import expression
from odoo.tools import float_compare, float_is_zero, format_date, groupby
from odoo.tools.translate import _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    area_manager_id = fields.Many2one('res.partner', string='Area Manager')

    @api.model
    def create(self, vals):
        if self.env.user.partner_id.is_area_manager:
            vals.update({'area_manager_id': self.env.user.id})
        res = super(SaleOrder, self).create(vals)
        return res
    
    #inherit create invoice function
    def _create_invoices(self, grouped=False, final=False):
        res = super(SaleOrder, self)._create_invoices(grouped, final)
        if self.env.user.partner_id.is_area_manager and self.area_manager_id.id != self.env.user.id and self.amount_total > 10000:
            raise UserError('You are not allowed to create invoice for this order as you are not the area manager of this customer.')
        return res

    


    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        if self.env.user.partner_id.is_area_manager and self.area_manager_id.id != self.env.user.partner_id.id and self.amount_total > 10000:
            raise UserError('You are not allowed to confirm this order as you are not the area manager of this customer.')
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # override create function
    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        return res

    # override write function
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        return res
    

    # override invoice line create function
    def _prepare_invoice_line(self, **optional_values):
        """Prepare the values to create the new invoice line for a sales order line.

        :param optional_values: any parameter that should be added to the returned invoice line
        :rtype: dict
        """
        self.ensure_one()

        res = {
            'display_type': self.display_type or 'product',
            'sequence': self.sequence,
            'name': self.env['account.move.line']._get_journal_items_full_name(self.name, self.product_id.display_name),
            'product_id': self.product_id.id,
            'product_uom_id': self.product_id.uom_po_id.id,
            'quantity': self.product_uom_qty,
            'discount': 15.00,
            'price_unit': self.product_id.list_price,
            'tax_ids': [Command.set(self.tax_id.ids)],
            'sale_line_ids': [Command.link(self.id)],
            'is_downpayment': self.is_downpayment,
        }
        self._set_analytic_distribution(res, **optional_values)
        downpayment_lines = self.invoice_lines.filtered('is_downpayment')
        if self.is_downpayment and downpayment_lines:
            res['account_id'] = downpayment_lines.account_id[:1].id
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # override create function
    @api.model
    def create(self, vals):
        res = super(StockQuant, self).create(vals)
        return res

    # override write function
    def write(self, vals):
        res = super(StockQuant, self).write(vals)
        return res
    

    
    def _get_inventory_move_values(self, qty, location_id, location_dest_id, package_id=False, package_dest_id=False):
        """ Called when user manually set a new quantity (via `inventory_quantity`)
        just before creating the corresponding stock move.

        :param location_id: `stock.location`
        :param location_dest_id: `stock.location`
        :param package_id: `stock.quant.package`
        :param package_dest_id: `stock.quant.package`
        :return: dict with all values needed to create a new `stock.move` with its move line.
        """
        self.ensure_one()
        if self.env.context.get('inventory_name'):
            name = self.env.context.get('inventory_name')
        elif fields.Float.is_zero(qty, precision_rounding=self.product_uom_id.rounding):
            name = _('Product Quantity Confirmed')
        else:
            name = _('Product Quantity Updated')
        if self.user_id and self.user_id.id != SUPERUSER_ID:
            name += f' ({self.user_id.display_name})'

        return {
            'name': name,
            'product_id': self.product_id.id,
            'product_uom': self.product_id.uom_po_id.id,
            'product_uom_qty': qty,
            'company_id': self.company_id.id or self.env.company.id,
            'state': 'confirmed',
            'location_id': location_id.id,
            'location_dest_id': location_dest_id.id,
            'restrict_partner_id':  self.owner_id.id,
            'is_inventory': True,
            'picked': True,
            'move_line_ids': [(0, 0, {
                'product_id': self.product_id.id,
                'product_uom_id': self.product_id.uom_po_id.id,
                'quantity': 1,
                'location_id': location_id.id,
                'location_dest_id': location_dest_id.id,
                'company_id': self.company_id.id or self.env.company.id,
                'lot_id': self.lot_id.id,
                'package_id': package_id.id if package_id else False,
                'result_package_id': package_dest_id.id if package_dest_id else False,
                'owner_id': self.owner_id.id,
            })]
        }


class ManagerCommissionLine(models.TransientModel):
    _name = 'manager.commission.report.line'
    _description = 'Manager Commission Report Line'

    product_id = fields.Many2one('product.template', string='Product')
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    quantity = fields.Float(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    subtotal = fields.Float(string='Subtotal')
    commission = fields.Float(string='Commission')
    manager_commission_report_id = fields.Many2one('manager.commission.report.line', string='Manager Commission Report')


class ManagerCommissionReport(models.TransientModel):
    _name = 'manager.commission.report'
    _description = 'Manager Commission Report'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    manager_id = fields.Many2one('res.users', string='Area Manager')
    commission_line_ids = fields.One2many('manager.commission.report.line', 'manager_commission_report_id', string='Commission Lines')

    def action_generate_report(self):
        self.ensure_one()
        if self.start_date > self.end_date:
            raise UserError('End Date should be greater than Start Date.')
        if self.manager_id:
            orders = self.env['sale.order'].search([('area_manager_id', '=', self.manager_id.id), ('date_order', '<=', self.start_date), ('date_order', '>=', self.end_date)])
        else:
            orders = self.env['sale.order'].search([('date_order', '>=', self.start_date), ('date_order', '<=', self.end_date)])
        commission_lines = []
        for order in orders:
            for line in order.order_line:
                commission_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'subtotal': line.price_subtotal,
                    'commission': line.price_subtotal * 0.05,
                }))
            self.commission_line_ids = commission_lines

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'manager.commission.report',
            'view_mode': 'form',
            'target': 'new',
        }