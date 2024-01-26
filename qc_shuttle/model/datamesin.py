from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta

class DataMesinProduksi(models.Model):
    _name = 'data.mesin.produksi'
    _description = 'Mesin Produksi'


    # Relasi ke model blok.mesin (blok.py)
    # untuk menampilkan data blok, yang nantinya bisa digunakan untuk melakukan filter data mesin.
    # menggunakan "domain" untuk menampilkan data mesin berdasarkan blok.
    blok_id = fields.Many2one('blok.mesin', string='Blok')

    # Relasi ke model line.mesin.produksi (line.py)
    # untuk menampilkan data line, yang nantinya bisa digunakan untuk melakukan filter data mesin.
    # menggunakan "domain" untuk menampilkan mesin berdasarkan line.
    line_id= fields.Many2one('line.mesin.produksi', string='Deret')

    # Relasi ke model hr.department untuk mengambil data divisi.
    divisi_id   = fields.Many2one('hr.department', string="Divisi")

    # Relasi ke model kode.kain (kodekain.py) untuk menampilkan kode kain pada masing masing mesin.
    kodekain = fields.Many2one('kode.kain',string="Kode Kain")

    nomor_mesin = fields.Char("Nomor Mesin")
    mesin = fields.Char(string="Mesin")

    # Digunakan apabila ingin menambahkan gambar pada form.
    image = fields.Binary("Image", help="Select image here")

    # Relasi ke model hr.employee untuk menampilkan data karyawan.
    operator = fields.Many2one('hr.employee', string='Operator')
    
    tanggal_snap = fields.Datetime(string="Tanggal Snap", default=fields.Datetime.now)
    
    rpm       = fields.Integer(string='RPM')
    state = fields.Selection([('draft','Kosong'),
                    ('start','Proses Naik Beam'),
                    ('progress','Mesin Jalan'),
                    ('done', 'Turun Beam'), 
                    ('cancel', 'Cancelled')], 
                    string="Status Mesin", 
                    readonly=True, 
                    copy=False, 
                    default='draft',
                    track_visibility='onchange', widget='statusbar',
                    statusbar_colors='{"success": "green", "failed": "red", "canceled": "red"}',)  

    # Tombol Kosong  
    def action_draft(self):
        self.write({'state': 'draft'})
    # Tombol Proses Naik Beam
    def action_start(self):
        self.write({'state': 'start'})    
    # Tombol Mesin Jalan
    def action_progress(self):
        self.write({'state': 'progress'})
   # Tombol Turun Beam
    def action_done(self):
        self.write({'state': 'done'})
    # Tombol Cancel
    def action_cancel(self):
        self.write({'state': 'cancel'})   

    success_header = fields.Boolean(
        compute="_compute_success_header", 
        string='Header', 
        help='This field will be marked if all tests have succeeded.')

    # depends = menampilkan sebuah kondisi berdasarkan field / parameter tertentu.
    @api.depends('nomor_mesin', 'state')
    def _compute_success_header(self):
        for record in self:
            if record.nomor_mesin and record.state == 'done':
                record.success_header = True
            else:
                record.success_header = False    

    color = fields.Integer(string="Colour", default=11)
    
    # Membuat ID dari record  
    def name_get(self):
        result = []
        for record in self:
            nomor_mesin = record.nomor_mesin 
            result.append((record.id, nomor_mesin))
        return result    

    date_planned_start = fields.Date(string="Tanggal Mulai", default=fields.Date.context_today)
    
    @api.depends('date_planned_start', 'state')
    def _compute_date_start(self):
        for record in self:
            if record.state == 'start':
                record.date_planned_start = fields.Date.today()
            else:
                record.date_planned_start = False

