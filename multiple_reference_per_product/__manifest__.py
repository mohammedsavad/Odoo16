{
    'name': 'Multiple Reference Per Product',
    'version': '16.0.1.0.0',
    'summary': 'Maintain multiple reference codes for a single product or product variant',
    'description': """
        Maintain multiple reference codes for a single product or product variant 
        with which you can easily filter them out from the product menu. 
        Also manage between different codes as default codes for the product.
    """,
    'depends': [
        'base', 'product'
    ],
    'data': [
        'views/product_product.xml',
        'views/product_references.xml',
        'views/product_search.xml',
        'security/ir.model.access.csv'
    ],
    'author': 'Savad',
    'website': 'example.com',
    'category': 'sales',
    'installable': True,
    'license': 'LGPL-3'
}