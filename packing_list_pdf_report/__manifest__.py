# -*- coding: utf-8 -*-
{
    "name": "PACKING LIST PDF REPORT ",
    "summary": """ PACKING LIST PDF Report """,
    "description": """ """,
    "author": "Prixgen Tech Solutions Pvt. Ltd.",
    "company": "Prixgen Tech Solutions Pvt. Ltd.",
    "website": "https://www.prixgen.com",
    "module_type": "official",
    "category": "Inventory",
    "version": "19.0.0.2",
    "license": "LGPL-3",
    "depends": [
        "base",
        "web",
        "sale",
        "l10n_in",
        "sale_stock",
        "account",
        'mail',
        'amardeep_custom_fields',
    ],
    "data": [
        "reports/packing_list.xml",
        "reports/header_footer.xml",

    ],
    'auto_install': False,
    'installable' : True,
    'application': True,
}