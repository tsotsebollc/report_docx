# -*- coding: utf-8 -*-
{
    'name': 'Report DOCX - Odoo Word Report Generator',
    'version': '15.0.1.0.1',
    'summary': 'Generate dynamic DOCX reports in Odoo 15',
    'description': """
        📝 **Report DOCX - Professional Word Report Generator for Odoo 15**
        
        This module enables the generation of Microsoft Word (DOCX) reports within Odoo 15. 
        Fully integrated with Odoo’s reporting engine, it allows businesses to create 
        customizable and dynamic Word reports easily.

        **✨ Features:**
        - Generate professional DOCX reports directly from Odoo
        - Fully customizable and template-based Word documents
        - Export reports just like PDF and XLSX
        - Works with any Odoo model (Sales, Invoices, HR, etc.)
        - Supports dynamic data and styling with Python-docx
        - API-ready for automation

        **👨‍💻 Support & Documentation:**
        - Installation guide and user manual included
        - Free updates and bug fixes for 12 months
        - Dedicated email support

        💡 **Ideal for:** Accounting, Sales, HR, Invoicing, Logistics, and more!
    """,
    'category': 'Reporting',
    'author': 'Purevdorj.M',
    'maintainer': 'TsoTseBoSS LLC',
    'website': 'https://safety-tech.mn/',
    'license': 'OPL-1',  # If selling on Odoo App Store, use 'OPL-1'
    'price': 5.00,  # Set your selling price here
    'currency': 'USD',
    'images': ['static/description/banner.png'],  # Add a banner for marketing
    "external_dependencies": {"python": ["python-docx"]},
    "depends": ["base", "web"],
    "data": [],
    "demo": ["demo/report.xml"],
    "installable": True,
    "application": True,
    "assets": {
        "web.assets_backend": [
            "report_docx/static/src/js/report/action_manager_report.esm.js",
        ],
    },
}
