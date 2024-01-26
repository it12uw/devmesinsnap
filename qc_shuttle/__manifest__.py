{
  'name': 'Snap QC Shuttle',
  'version': '1.0.',
  'author': 'Steven Morison',
  'summary': 'Quality Control Shuttle',
  'author': 'Steven Morison, stevenmorizon123@gmail.com',
  'category': 'Manufacture',
  'depends': ['base', 'web', 'mesin_unggul', 'web_responsive'],
  'data': [
    'security/ir.model.access.csv',
    'views/view_layout_shuttle.xml',
    'views/view_data_mesin.xml',
    'views/view_snap_qc.xml',
    'views/view_snap_qc_pop_up.xml',
    'views/assets.xml',
    'report/report_menu.xml',
    'report/report_qc_shuttle.xml',
  ],

  'qweb': [
        "static/src/xml/qc_shuttle_template.xml",
    ],

  'auto_install': False,
  'installable': True,
  'application': True,
}
