from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta


class LineMesinProduksi(models.Model):
    _name='line.mesin.produksi'
    _description='Line Mesin Produksi'


    line = fields.Selection([
			('1',_('1')),
			('2',_('2')),
			('3',_('3')),
            ('4',_('4')),
			('5',_('5')),
			('6',_('6')),
            ('7',_('7')),
			('8',_('8')),
			('9',_('9')),
            ('10',_('10')),
			('11',_('11')),
			('12',_('12')),
            ('Baru','Baru'),
			], string= "Line")
            
    blok= fields.Many2one('blok.mesin', string='Blok')
    total_mesin = fields.Integer(string="Total Mesin", compute='_compute_totalmesin',readonly=True,store=True )
    mesin_ids = fields.Many2many('data.mesin.produksi', string='Data Mesin', store=True)

    data_mesin_ids = fields.One2many('data.mesin.produksi', 'line_id', 'Mesin')
    
    @api.depends('line')
    def _compute_totalmesin(self):
        for a in self:
            if a.line == 'Baru':
                 a.total_mesin = 6
            elif a.line == '1':
                a.total_mesin = 50
            elif a.line == '2':
                a.total_mesin = 50
            elif a.line == '3':
                a.total_mesin = 50
            elif a.line == '4':
                a.total_mesin = 50
            elif a.line == '5':
                a.total_mesin = 50
            elif a.line == '6':
                a.total_mesin = 34
            elif a.line == '7':
                a.total_mesin = 33
            elif a.line == '8':
                a.total_mesin = 32
            elif a.line == '9':
                a.total_mesin = 34
            elif a.line == '10':
                a.total_mesin = 34    
            elif a.line == '11':
                a.total_mesin = 35
            elif a.line == '12':
                a.total_mesin = 61
            else:
                a.total_mesin = 519
    
    def name_get(self):
        result = []

        for record in self:
            line = record.line 
            result.append((record.id, line))
        return result            


    def action_open_mesin(self):
        return {
            'name': 'Mesin Produksi',
            'view_mode': 'kanban',
            'res_model': 'data.mesin.produksi',
            'view_id': self.env.ref('custom_mesin.view_kanban_status').id,
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
