from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class BlokMesin(models.Model):
    _name='blok.mesin'
    _description='Blok Mesin Produksi'

    blok = fields.Char(string='Nama Blok')
    jumlah_mesin_perblok = fields.Integer(string="Jumlah Mesin")
    
    #Relasi ke model line.mesin.produksi (line.py) 
    line= fields.Many2many('line.mesin.produksi', string='Deret')

    # Relasi ke model data.mesin.produksi 
    # untuk menampilkan jumlah mesin yang ada pada masing-masing blok.
    mesin_ids = fields.Many2many('data.mesin.produksi', string='Data Mesin', store=True)


    total_mesin_aktif = fields.Integer(string='Total Mesin Aktif', compute='_compute_total_mesin_aktif')

    # Menghitung jumlah mesin yang aktif dengan kondisi pada field state = start, progress, done
    @api.depends('mesin_ids.state')
    def _compute_total_mesin_aktif(self):
        for record in self:
            aktif_mesin_ids = record.mesin_ids.filtered(lambda mesin: mesin.state in ('start', 'progress', 'done'))
            record.total_mesin_aktif = len(aktif_mesin_ids)
    
    # Buat ID record data blok
    def name_get(self):
        result = []
        for record in self:
            blok_name = record.blok
            result.append((record.id, blok_name))
        return result
    
    @api.model
    def create(self, vals):
        blok_mesin = super(BlokMesin, self).create(vals)
        return blok_mesin



