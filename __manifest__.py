{
    'name': 'Fixed Invoice Discount',
    'version': '17.0.1.0.0',
    'summary': 'Apply fixed discount on invoice total',
    'category': 'Accounting',
    'author': 'Shashank Garg',
    'depends': ['account'],
    'data': [
        'views/account_move_view.xml',
    ],

    'installable': True,
    'application': False,
    "pre_init_hook":  "pre_init_check",
}
