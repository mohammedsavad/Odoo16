from odoo import http
from odoo.http import request


class FilterController(http.Controller):

    @http.route('/sale_dashboard/<int:filter_id>/<int:date_id>', csrf=False, type='json')
    def filter(self, filter_id, date_id):
        context = {}
        inner_context = []
        if filter_id == 4:
            if date_id == 0:
                query = """
                    SELECT product_id , COUNT(product_id) as rp
                    FROM sale_order_line GROUP BY product_id 
                    order by rp desc  limit 10
                    """
            elif date_id == 1:
                query = """
                    SELECT product_id , COUNT(product_id) as rp
                    FROM sale_order_line
                    WHERE Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                    AND Extract(Week FROM create_date) = Extract(Week FROM DATE(NOW())) AND
                    Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                    GROUP BY product_id 
                    order by rp desc  limit 10
                    """
            else:
                query = """
                    SELECT product_id , COUNT(product_id) as rp
                    FROM sale_order_line
                    WHERE Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                    AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                    GROUP BY product_id 
                    order by rp desc  limit 10"""
            request.env.cr.execute(query)
            data = request.env.cr.dictfetchall()
            for rec in data:
                rec['data'] = []
                product_id = request.env['product.product'].search([
                    ('id', '=', rec['product_id'])
                ])
                rec['name'] = product_id.product_tmpl_id.name
                inner_context.append(rec)
            context = {'data': inner_context}
        elif filter_id == 0:
            total_quotation = 0
            total_sales = 0
            invoiced_amount = 0
            totals = []
            sales_team = request.env['crm.team'].search([])
            fetched_data = self.fetch_order_data(date_id)
            for rec in sales_team:
                if date_id == 0:
                    query = f"""
                        SELECT amount_total,state,invoice_status,name 
                        FROM sale_order 
                        WHERE team_id = '{rec.id}'
                        """
                elif date_id == 1:
                    query = f"""
                        SELECT amount_total,state,invoice_status,name 
                        FROM sale_order 
                        WHERE team_id = '{rec.id}'
                        AND Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                        AND Extract(Week FROM create_date) = Extract(Week FROM DATE(NOW())) 
                        AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                        """
                else:
                    query = f"""
                       SELECT amount_total,state,invoice_status,name 
                       FROM sale_order 
                       WHERE team_id = '{rec.id}'
                       AND Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                       AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                       """
                request.env.cr.execute(query)
                order_data = request.env.cr.fetchall()
                orders = []
                quotations = 0
                sales = 0
                invoiced = 0
                _totals = []
                for order in order_data:
                    if order[1] == 'draft':
                        quotations += order[0]
                    elif order[1] == 'send':
                        quotations += order[0]
                    elif order[1] == 'sale':
                        sales += order[0]
                    if order[2] == 'invoiced':
                        invoiced += order[0]
                    data = {
                        'name': order[3],
                        'state': order[1],
                        'invoice_status': order[2],
                        'total': order[0],
                    }
                    orders.append(data)
                totals.append(_totals)
                inner_context.append({
                    'name': rec.name,
                    'id': rec.id,
                    'quotations': quotations,
                    'sales': sales,
                    'invoiced': invoiced,
                    'data': orders
                })
            context = {
                'total_quotation': fetched_data[0],
                'total_sales': fetched_data[1],
                'invoiced_amount': fetched_data[2],
                'data': inner_context,
                'filter_id': filter_id,
            }

        elif filter_id == 1:
            team_members = request.env['crm.team.member'].search([])
            fetched_data = self.fetch_order_data(date_id)
            for rec in team_members:
                # order_data = request.env['sale.order'].search([
                #     ('user_id', '=', rec.user_id.id)
                # ])
                if date_id == 0:
                    query = f"""
                        SELECT amount_total,state,invoice_status,name 
                        FROM sale_order 
                        WHERE user_id = '{rec.user_id.id}'
                        """
                elif date_id == 1:
                    query = f"""
                        SELECT amount_total,state,invoice_status,name 
                        FROM sale_order 
                        WHERE user_id = '{rec.user_id.id}'
                        AND Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                        AND Extract(Week FROM create_date) = Extract(Week FROM DATE(NOW())) 
                        AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                        """
                else:
                    query = f"""
                       SELECT amount_total,state,invoice_status,name 
                       FROM sale_order 
                       WHERE user_id = '{rec.user_id.id}'
                       AND Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                       AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                       """
                request.env.cr.execute(query)
                order_data = request.env.cr.fetchall()
                orders = []
                quotations = 0
                sales = 0
                invoiced = 0
                _totals = []
                for order in order_data:
                    if order[1] == 'draft':
                        quotations += order[0]
                    elif order[1] == 'send':
                        quotations += order[0]
                    elif order[1] == 'sale':
                        sales += order[0]
                    if order[2] == 'invoiced':
                        invoiced += order[0]
                    data = {
                        'name': order[3],
                        'state': order[1],
                        'invoice_status': order[2],
                        'total': order[0],
                    }
                    orders.append(data)
                inner_context.append({
                    'name': rec.name,
                    'id': rec.id,
                    'quotations': quotations,
                    'sales': sales,
                    'invoiced': invoiced,
                    'data': orders
                })
            context = {
                'total_quotation': fetched_data[0],
                'total_sales': fetched_data[1],
                'invoiced_amount': fetched_data[2],
                'data': inner_context,
                'filter_id': filter_id,
            }
        elif filter_id == 2:
            if date_id == 0:
                query = """
                    SELECT partner_id, COUNT(partner_id) as rep_count
                    FROM sale_order GROUP BY partner_id 
                    order by rep_count desc  limit 10 """
            elif date_id == 1:
                query = """
                    SELECT partner_id, COUNT(partner_id) as rep_count
                    FROM sale_order GROUP BY partner_id 
                    WHERE Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                    AND Extract(Week FROM create_date) = Extract(Week FROM DATE(NOW())) 
                    AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                    order by rep_count desc  limit 10 """
            else:
                query = """
                    SELECT partner_id, COUNT(partner_id) as rep_count
                    FROM sale_order GROUP BY partner_id 
                    WHERE Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                    AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                    order by rep_count desc  limit 10 """
            request.env.cr.execute(query)
            data = request.env.cr.dictfetchall()
            for rec in data:
                orders = []
                quotations = 0
                sales = 0
                invoiced = 0
                rec['data'] = []
                order_data = request.env['sale.order'].search([
                    ('partner_id', '=', rec['partner_id'])
                ])
                partner_name = ''
                for order in order_data:
                    partner_name = order.partner_id.name
                    if order.state == 'draft':
                        quotations += order.amount_total
                    elif order.state == 'send':
                        quotations += order.amount_total
                    elif order.state == 'sale':
                        sales += order.amount_total
                    if order.invoice_status == 'invoiced':
                        invoiced += order.amount_total
                    data = {
                        'id': order.id,
                        'name': order.name,
                        'state': order.state,
                        'invoice_status': order.invoice_status,
                        'customer': order.partner_id.name,
                        'total': order.amount_total,
                    }
                    orders.append(data)
                inner_context.append({
                    'name': partner_name,
                    'id': rec['partner_id'],
                    'quotations': quotations,
                    'sales': sales,
                    'invoiced': invoiced,
                    'data': orders
                })
                fetched_data = self.fetch_order_data(date_id)
            context = {
                'total_quotation': fetched_data[0],
                'total_sales': fetched_data[1],
                'invoiced_amount': fetched_data[2],
                'data': inner_context,
                'filter_id': filter_id,
            }
        elif filter_id == 3:
            if date_id == 0:
                query = """
                    SELECT product_id , COUNT(product_id) as rp
                    FROM sale_order_line GROUP BY product_id 
                    order by rp limit 10
                    """
            elif date_id == 1:
                query = """
                    SELECT product_id , COUNT(product_id) as rp
                    FROM sale_order_line
                    WHERE Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                    AND Extract(Week FROM create_date) = Extract(Week FROM DATE(NOW())) AND
                    Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                    GROUP BY product_id 
                    order by rp limit 10
                    """
            else:
                query = """
                    SELECT product_id , COUNT(product_id) as rp
                    FROM sale_order_line
                    WHERE Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                    AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                    GROUP BY product_id 
                    order by rp limit 10"""
            request.env.cr.execute(query)
            data = request.env.cr.dictfetchall()
            for rec in data:
                product_id = request.env['product.product'].search([
                    ('id', '=', rec['product_id'])
                ])
                rec['name'] = product_id.product_tmpl_id.name
                inner_context.append(rec)
            context = {'data': inner_context}
        elif filter_id == 5:
            order_status = ['draft', 'sent', 'sale']
            for item in order_status:
                if date_id == 0:
                    query = f"""
                        SELECT amount_total,state,invoice_status,name 
                        FROM sale_order 
                        WHERE state = '{item}'
                        """
                elif date_id == 1:
                    query = f"""
                        SELECT amount_total,state,invoice_status,name 
                        FROM sale_order 
                        WHERE state = '{item}'
                        AND Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                        AND Extract(Week FROM create_date) = Extract(Week FROM DATE(NOW())) 
                        AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                        """
                else:
                    query = f"""
                       SELECT amount_total,state,invoice_status,name 
                       FROM sale_order 
                       WHERE state = '{item}'
                       AND Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                       AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                       """
                request.env.cr.execute(query)
                order_data = request.env.cr.fetchall()
                orders = []
                quotations = 0
                sales = 0
                invoiced = 0
                for order in order_data:
                    if order[1] == 'draft':
                        quotations += order[0]
                    elif order[1] == 'send':
                        quotations += order[0]
                    elif order[1] == 'sale':
                        sales += order[0]
                    if order[2] == 'invoiced':
                        invoiced += order[0]
                    data = {
                        'name': order[3],
                        'state': order[1],
                        'invoice_status': order[2],
                        'total': order[0],
                    }
                    orders.append(data)
                inner_context.append({
                    'name': item,
                    'id': item,
                    'quotations': quotations,
                    'sales': sales,
                    'invoiced': invoiced,
                    'data': orders
                })
                fetched_data = self.fetch_order_data(date_id)
            context = {
                'total_quotation': fetched_data[0],
                'total_sales': fetched_data[1],
                'invoiced_amount': fetched_data[2],
                'data': inner_context,
                'filter_id': filter_id,
            }

        elif filter_id == 6:
            invoice_status = ['upselling', 'invoiced', 'to invoice', 'no']
            for item in invoice_status:
                if date_id == 0:
                    query = f"""
                        SELECT amount_total,state,invoice_status,name 
                        FROM sale_order 
                        WHERE invoice_status = '{item}'
                        """
                elif date_id == 1:
                    query = f"""
                        SELECT amount_total,state,invoice_status,name 
                        FROM sale_order 
                        WHERE invoice_status = '{item}'
                        AND Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                        AND Extract(Week FROM create_date) = Extract(Week FROM DATE(NOW())) 
                        AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                        """
                else:
                    query = f"""
                       SELECT amount_total,state,invoice_status,name 
                       FROM sale_order 
                       WHERE invoice_status = '{item}'
                       AND Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                       AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                       """
                request.env.cr.execute(query)
                order_data = request.env.cr.fetchall()
                orders = []
                quotations = 0
                sales = 0
                invoiced = 0
                for order in order_data:
                    if order[1] == 'draft':
                        quotations += order[0]
                    elif order[1] == 'send':
                        quotations += order[0]
                    elif order[1] == 'sale':
                        sales += order[0]
                    if order[2] == 'invoiced':
                        invoiced += order[0]
                    data = {
                        'name': order[3],
                        'state': order[1],
                        'invoice_status': order[2],
                        'total': order[0],
                    }
                    orders.append(data)
                inner_context.append({
                    'name': item,
                    'id': item,
                    'quotations': quotations,
                    'sales': sales,
                    'invoiced': invoiced,
                    'data': orders
                })
                fetched_data = self.fetch_order_data(date_id)
            context = {
                'total_quotation': fetched_data[0],
                'total_sales': fetched_data[1],
                'invoiced_amount': fetched_data[2],
                'data': inner_context,
                'filter_id': filter_id,
            }
        return context

    def fetch_order_data(self, date_id):
        total_quotation = 0
        total_sales = 0
        invoiced_amount = 0
        # order_data = request.env['sale.order'].search([])
        if date_id == 0:
            query = f"""
                SELECT amount_total,state,invoice_status,name 
                FROM sale_order 
                """
        elif date_id == 1:
            query = f"""
                SELECT amount_total,state,invoice_status,name 
                FROM sale_order 
                WHERE Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
                AND Extract(Week FROM create_date) = Extract(Week FROM DATE(NOW())) 
                AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
                """
        else:
            query = f"""
               SELECT amount_total,state,invoice_status,name 
               FROM sale_order 
               WHERE Extract(MONTH FROM create_date) = Extract(MONTH FROM DATE(NOW()))
               AND Extract(Year FROM create_date) = Extract(Year FROM DATE(NOW()))
               """
        request.env.cr.execute(query)
        order_data = request.env.cr.fetchall()
        for order in order_data:
            if order[1] == 'draft':
                total_quotation += order[0]
            elif order[1] == 'send':
                total_quotation += order[0]
            elif order[1] == 'sale':
                total_sales += order[0]
            if order[2] == 'invoiced':
                invoiced_amount += order[0]
        return [total_quotation, total_sales, invoiced_amount]
