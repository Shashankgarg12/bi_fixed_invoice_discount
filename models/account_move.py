from odoo import models, fields, api
from odoo.tools.misc import formatLang


class AccountMove(models.Model):
    _inherit = 'account.move'

    fixed_discount = fields.Monetary(
        string="Fixed Discount",
        currency_field='currency_id'
    )

    def _compute_tax_totals(self):
        for move in self:
            if not move.is_invoice(include_receipts=True):
                super()._compute_tax_totals()
                continue

            if not hasattr(move, 'fixed_discount'):
                super()._compute_tax_totals()
                continue

            if not move.fixed_discount:
                super()._compute_tax_totals()
                continue

            base_lines = move.invoice_line_ids.filtered(
                lambda l: l.display_type == 'product'
            )

            discount = move.fixed_discount or 0.0
            total_base = sum(l.price_unit * l.quantity for l in base_lines)

            base_line_values = []

            for line in base_lines:
                vals = line._convert_to_tax_base_line_dict()

                if discount and total_base:
                    line_base = line.price_unit * line.quantity
                    share = (line_base / total_base) * discount
                    vals['price_unit'] -= share / (vals['quantity'] or 1.0)

                base_line_values.append(vals)

            kwargs = {
                'base_lines': base_line_values,
                'currency': move.currency_id,
            }

            move.tax_totals = self.env['account.tax']._prepare_tax_totals(**kwargs)
