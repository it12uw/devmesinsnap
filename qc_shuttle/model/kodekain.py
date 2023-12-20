from odoo import models, fields, api, _

class KodeKain(models.Model):
    _name = 'kode.kain'
    _description = 'Kode Kain'

    kode_kain = fields.Char(string='Kode Kain')
    
    # Membuat id untuk record data kodekain
    def name_get(self):
            result = []
            for record in self:
                kode_kain = record.kode_kain 
                result.append((record.id, kode_kain))
            return result    
    