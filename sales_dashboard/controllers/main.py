from odoo import http
from odoo.http import request


class FilterController(http.Controller):

    @http.route('/sale_dashboard/<int:filter_id>', csrf=False, type='json')
    def filter(self, filter_id):
        context = []
        if filter_id == 4:
            query = """
            SELECT product_id , COUNT(product_id) as rp
            FROM sale_order_line GROUP BY product_id 
            order by rp desc  limit 10
            """
            request.env.cr.execute(query)
            data = request.env.cr.dictfetchall()
            for rec in data:
                rec['data'] = []
                product_id = request.env['product.product'].search([
                    ('id', '=', rec['product_id'])
                ])
                if product_id.name:
                    rec['name'] = product_id.product_tmpl_id.name
                else:
                    rec['name']
                context.append(rec)
        elif filter_id == 0:
            sales_team = request.env['crm.team'].search([])
            for rec in sales_team:
                order_data = request.env['sale.order'].search([
                    ('team_id', '=', rec.id)
                ])
                orders = []
                total_quotation = 0
                total_sales = 0
                invoiced_amount = 0
                for order in order_data:
                    if order.state == 'draft':
                        total_quotation += order.amount_total
                    elif order.state == 'send':
                        total_quotation += order.amount_total
                    elif order.state == 'sale':
                        total_sales += order.amount_total
                    if order.invoice_status == 'invoiced':
                        invoiced_amount += order.amount_total
                    data = {
                        'id': order.id,
                        'name': order.name,
                        'state': order.state,
                        'invoice_status': order.invoice_status,
                        'customer': order.partner_id.name,
                        'total': order.amount_total,
                    }
                    orders.append(data)
                data = {
                    'total_quotation': total_quotation,
                    'total_sales': total_sales,
                    'invoiced_amount': invoiced_amount,
                    'data': orders,
                    'filter_id': filter_id,
                    'id': rec.id,
                    'name': rec.name,
                    'team_lead': rec.user_id,
                    'invoiced_target': rec.invoiced_target,
                }
                context.append(data)

        elif filter_id == 1:
            team_members = request.env['crm.team.member'].search([])
            for rec in team_members:
                order_data = request.env['sale.order'].search([
                    ('user_id', '=', rec.id)
                ])
                orders = []
                for order in order_data:
                    data = {
                        'id': order.id,
                        'name': order.name,
                        'state': order.state,
                        'invoice_status': order.invoice_status,
                        'customer': order.partner_id.name,
                        'total': order.amount_total,
                    }
                    orders.append(data)
                data = {
                    'data': orders,
                    'filter_id': filter_id,
                    'id': rec.id,
                    'name': rec.user_id.name
                }
                context.append(data)
        elif filter_id == 2:
            query = """
                SELECT partner_id, COUNT(partner_id) as rep_count
                FROM sale_order GROUP BY partner_id 
                order by rep_count desc  limit 10 """
            request.env.cr.execute(query)
            data = request.env.cr.dictfetchall()
            for rec in data:
                rec['data'] = []
                sale_id = request.env['sale.order'].search([
                    ('partner_id', '=', rec['partner_id'])
                ])
                for order in sale_id:
                    temp = {
                        'id': order.id,
                        'name': order.name,
                        'state': order.state,
                        'invoice_status': order.invoice_status,
                        'customer': order.partner_id.name,
                        'total': order.amount_total,
                    }
                    rec['data'].append(temp)
                    rec['name'] = temp['customer']
                context.append(rec)
        elif filter_id == 3:
            query = """
                        SELECT product_id , COUNT(product_id) as rp
                        FROM sale_order_line GROUP BY product_id 
                        order by rp limit 10
                        """
            request.env.cr.execute(query)
            data = request.env.cr.dictfetchall()
            for rec in data:
                rec['data'] = []
                product_id = request.env['product.product'].search([
                    ('id', '=', rec['product_id'])
                ])
                if product_id.name:
                    rec['name'] = product_id.product_tmpl_id.name
                else:
                    rec['name']
                context.append(rec)
        elif filter_id == 5:
            order_status = ['draft', 'sent', 'sale', 'done', 'cancel']
            data = {}
            for item in order_status:
                sale_id = request.env['sale.order'].search([
                    ('state', '=', item)
                ])
                data['name'] = item
                data['data'] = []
                for order in sale_id:
                    temp = {
                        'id': order.id,
                        'name': order.name,
                        'state': order.state,
                        'invoice_status': order.invoice_status,
                        'customer': order.partner_id.name,
                        'total': order.amount_total,
                    }
                    data['data'].append(temp)
                context.append(data)
                data = {}
        elif filter_id == 6:
            invoice_status = ['upselling', 'invoiced', 'to invoice', 'no']
            data = {}
            for item in invoice_status:
                sale_id = request.env['sale.order'].search([
                    ('invoice_status', '=', item)
                ])
                data['name'] = item
                data['data'] = []
                for order in sale_id:
                    temp = {
                        'id': order.id,
                        'name': order.name,
                        'state': order.state,
                        'invoice_status': order.invoice_status,
                        'customer': order.partner_id.name,
                        'total': order.amount_total,
                    }
                    data['data'].append(temp)
                context.append(data)
                data = {}
        return context
