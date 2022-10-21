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
            'click .options': 'fech_data',
            'change #data_filter': 'fech_data' 
        },
        start: function() {
            var self = this;
            this.set("title", 'Dashboard');
            return this._super().then(function() {
                self.render_dashboards()
            });
        },
        sale_oders:[],
        order_by_team :[],
        sales_by_memeber:[],
        filter_id:0,
        date:0,
        render_dashboards: function(){
            var self = this
            $('#container-wrapper').html('')
            rpc.query({
                route: `/sale_dashboard/${this.filter_id}/${this.date}`,
                params: {}
                }).then(function(res){
                    var id_counter = 0
                    var data = res['data']
                    var labels = []
                    var names = []
                    data.forEach(element => {
                        $('#container-wrapper').html($('#container-wrapper').html() +`
                        <div class="accordion-item">
                            <h2 class="accordion-header" id="heading${id_counter}">
                            <button class="accordion-button" data-id=${id_counter} type="button" data-bs-toggle="collapse" data-bs-target="#collapse${id_counter}" aria-expanded="true" aria-controls="collapse${id_counter}">
                                ${element['name']}
                            </button>
                            </h2>
                            <div id="collapse${id_counter}" class="accordion-collapse collapse" aria-labelledby="heading${id_counter}" data-bs-parent="#accordionExample">
                            <div class="accordion-body">
                                <div class="card text-center">
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
                        `);
                    names.push(element['name'])
                    labels.push(data[id_counter]['sales'])
                    id_counter += 1
                    })
                    $('#title-01').text('$'+res['total_quotation']);
                    $('#title-02').text('$'+res['total_sales']);
                    $('#title-03').text('$'+res['invoiced_amount']);
                    self.load_chart('Total Sales',labels,names)
                    $('.accordion-button').click(function (e) {
                        var this_id = $(this).data('id')
                        $('#title-01').text('$'+data[this_id]['quotations']);
                        $('#title-02').text('$'+data[this_id]['sales']);
                        $('#title-03').text('$'+data[this_id]['invoiced']);
                        var orders = data[this_id]['data']
                        var counter = 1
                        $(`#tbody-${this_id}`).html('')
                        orders.forEach(element => {
                            $(`#tbody-${this_id}`).append(`
                            <tr>
                                <th scope="row">${counter}</th>
                                <td><a href="/web#id=${element['id']}&menu_id=178&cids=1&action=296&model=sale.order&view_type=form">${element['name']}</a></td>
                                <td>${element['state']}</td>
                                <td>${element['invoice_status']}</td>
                                <td>$${element['total']}</td>
                            </tr>
                        `);
                        counter += 1
                        });
                        labels = ['quotations','sales','invoiced']
                        names = [data[this_id]['quotations'],data[this_id]['sales'],data[this_id]['invoiced']]
                        var string = $(this).text()
                        self.myChart.destroy();
                        self.load_chart(string,names,labels)
                    });
                    $('.options').click(function (e) { 
                        self.filter_id = $(this).data('id')
                        console.log($(this).data('id'))
                    });
                });
        },
        render_table: function(){
            var self = this
            $('#container-wrapper').html('')
            $('#container-wrapper').append('<ul class="list-group list-group-flush " id="product-list"></ul>')

            rpc.query({
                route: `/sale_dashboard/${self.filter_id}/${this.date}`,
                params: {}
                }).then(function(res){
                    var labels = []
                    var datas = []
                    $('#product-list').html('')
                    res.data.forEach(element => {
                        $('#product-list').append(`
                            <li class="list-group-item"><a href="/web#id=${element['product_id']}&cids=1&menu_id=178&action=161&model=product.product&view_type=form">
                            ${element['name']}</a></li>
                        `);
                        labels.push(element['name'])
                        datas.push(element['rp'])
                    });
                    self.load_chart('Top Products',datas,labels)
                })
        },
        fech_data: function(){
            console.log("working")
            this.date =$('#data_filter').val()
            console.log(this.date)
            this.myChart.destroy();
            if ((this.filter_id == 3) || (this.filter_id == 4)){
                this.render_table()
            }
            else{
                this.render_dashboards()
            }
        },
        myChart:'',
        load_chart: function(label,data,labels){
            var data = {
               labels: labels,
               datasets: [{
                    label : label,
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgb(255, 99, 132)',
                    data: data
                }]
            };
            var config = {
                type: 'bar',
                data: data,
                options: {}
            };
            this.myChart = new Chart(
                document.getElementById('myChart'),
                config
            );
        }
    })
    core.action_registry.add('sale_dashboard_tags', SalesDashBoard);
    return SalesDashBoard;
})
