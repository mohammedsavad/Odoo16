odoo.define('sales_dashboard.dashboard_action', function (require){
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var QWeb = core.qweb;
    var rpc = require('web.rpc');
    var ajax = require('web.ajax');
    var SalesDashBoard = AbstractAction.extend({
        template: 'SalesDashboard',
        init: function(parent, context) {
           this._super(parent, context);
        },
        events :{
            'change #data_filter': 'fech_data',
        },
        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                var model = 'sale.order';
                var domain = []
                var fields = [];
                rpc.query({
                    model: model,
                    method: 'search_read',
                    args: [domain, fields],
                }).then(function (data){
                    self.sale_oders = data
                    self.render_dashboards()
                })
            });
        },
        sale_oders:[],
        order_by_team :[],
        sales_by_memeber:[],
        filter_id:0,
        data_id:0,
        render_dashboards: function(){
            var self = this
            $('#container-wrapper').html('')
            $('#card-container').hide()
            rpc.query({
                route: `/sale_dashboard/${this.filter_id}`,
                params: {}
                }).then(function(data){
                    var id_counter = 0
                    data.forEach(element => {
                        $('#container-wrapper').html($('#container-wrapper').html() +`
                        <div class="accordion-item col-md-6">
                            <h2 class="accordion-header" id="heading${id_counter}">
                            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapse${id_counter}" aria-expanded="true" aria-controls="collapse${id_counter}">
                                ${element['name']}
                            </button>
                            </h2>
                            <div id="collapse${id_counter}" class="accordion-collapse collapse" aria-labelledby="heading${id_counter}" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <div class="card text-center" id="container-wrapper" >
                                    <div class="card-header">
                                    <ul class="nav nav-tabs card-header-tabs">
                                        <li class="nav-item">
                                        <a class="nav-link active" aria-current="true" id="nav-hed" href="#">Quotations</a>
                                        </li>
                                    </ul>
                                    </div>
                                    <div class="card-body">
                                    <div class="container" id="table-container">
                                        <table class="table">
                                            <thead>
                                                <tr>
                                                    <th scope="col">#</th>
                                                    <th scope="col">Name</th>
                                                    <th scope="col">customer</th>
                                                    <th scope="col">State</th>
                                                    <th scope="col">Invoice Status</th>
                                                    <th scope="col">Amount</th>
                                                </tr>
                                            </thead>
                                            <tbody id="tbody-${id_counter}">
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                            </div>
                            </div>
                        </div>
                        <div class="accordion-item col-md-6">
                            <canvas id="myChart"></canvas>
                        </div>
                        `);
                    var counter = 1
                    var order_data = element['data']
                    if (self.filter_id == 0){
                        $('#card-container').show()
                    }
                    $('#title-01').text('$'+element['total_quotation']);
                    $('#title-02').text('$'+element['total_sales']);
                    $('#title-03').text('$'+element['invoiced_amount']);
                    order_data.forEach(rec => {
                        $(`#tbody-${id_counter}`).append(`
                            <tr>
                                <th scope="row">${counter}</th>
                                <td><a href="/web#id=${rec['id']}&menu_id=178&cids=1&action=296&model=sale.order&view_type=form">${rec['name']}</a></td>
                                <td>${rec['state']}</td>
                                <td>${rec['customer']}</td>
                                <td>${rec['state']}</td>
                                <td>${rec['invoice_status']}</td>
                                <td>$${rec['total']}</td>
                            </tr>
                        `);
                        counter +=1
                    });
                    id_counter += 1
                    })
                });
        },
        fech_data: function(){
            this.filter_id = $('#data_filter').val()
            this.render_dashboards()
        }
    })
    core.action_registry.add('sale_dashboard_tags', SalesDashBoard);
    return SalesDashBoard;
})

