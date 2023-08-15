{
  'name': 'Template Qc',
  'author': 'Hendrikus',
  'version': '14.0',
  'depends': [
    'base',
    'web',
  ],
  'data': [
    "security/ir.model.access.csv",
    'views/menu.xml',
    'views/assets.xml',
    'views/qc_rapier.xml',
    'views/qc_ajl.xml',
  ],
  'qweb': [
    'static/src/xml/widget_qc_template.xml',
  ],
  'sequence': 1,
  'auto_install': False,
  'installable': True,
  'application': True,
  'category': '- Arkademy Part 1',
  'summary': 'Catat Penjualan Sederhana',
  'license': 'OPL-1',
  'website': 'https://www.arkana.co.id/',
  'description': '-'
}