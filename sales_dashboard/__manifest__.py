{
    'name': 'Sales Dashboard V16',
    'version': '16.0.1.0.0',
    'summary': '',
    'description':
    """sales dashboard with the following features,
            Sales by sales team
            Sales by sales person
            Top 10 customers
            Lowest selling products
            Highest selling products
            Order status
            Invoice status
            """,
    'depends': [
        'base', 'sale_management'
    ],
    'data': [
        'views/sales_dashboard.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'sales_dashboard/static/src/xml/sales_dashboard.xml',
            'https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js',
            'sales_dashboard/static/src/js/sales_dashboard.js',
            'sales_dashboard/static/src/css/style.css'
        ]
    },
    'author': 'Savad',
    'website': 'example.com',
    'category': 'sales',
    'installable': True,
    'license': 'LGPL-3'
}