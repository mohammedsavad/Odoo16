from odoo import models, fields, _


class MultipleReferences(models.Model):
    _name = 'product.multy.references'
    _description = 'Multiple References'
    _rec_name = 'product_code'

    product_code = fields.Char('reference', required=True)
    product_id = fields.Many2one('product.template', required=True)

    def action_set_default(self):
        self.product_id.default_code = self.product_code
        message = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Updated'),
                'message': 'Default Reference Updated',
                'sticky': False,
            }
        }
        return message
    _sql_constraints = [
        ('check_percentage', 'unique(product_code)',
         "Internal Reference Should Be Unique")
    ]