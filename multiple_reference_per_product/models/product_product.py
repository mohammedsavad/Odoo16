from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = 'product.template'

    ref_ids = fields.One2many('product.multy.references', 'product_id')


    def action_create_reference(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Multiple Reference',
            'res_model': 'product.multy.references',
            'view_mode': 'tree,form',
            'domain': [('product_id.id', '=', self.id)],
            'context': {
                'default_product_id': self.id
            }
        }


class ProductProduct(models.Model):
    _inherit = 'product.product'


    def action_create_reference(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Multiple Reference',
            'res_model': 'product.multy.references',
            'view_mode': 'tree,form',
            'domain': [('product_id.id', '=', self.product_tmpl_id.id)],
            'context': {
                'default_product_id': self.product_tmpl_id.id
            }
        }
