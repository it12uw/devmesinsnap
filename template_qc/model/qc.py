from odoo import  api, models, fields, _


class SnapQc(models.Model):
    _name = 'snap.qc'
    _description = 'Snap Qc'
    
    putus_lusi = fields.Integer('Putus Lusi')
    putus_pakan = fields.Integer('Putus Pakan')
    bendera_merah = fields.Integer('Bendera Merah')
    bendera_biru = fields.Integer('Bendera Biru')
    hb = fields.Integer('Habis Beam & Beam Baru')
    oh = fields.Integer('Over Houle')
    lain_lain = fields.Integer('Lain-lain')
    hasil = fields.Integer('Resume',)
    # untuk Rapir 
    # naik_beam = fields.Integer(string="Naik Beam Baru")
    # troble_mekanik = fields.Integer(string="Troble Mekanaik")
    # troble_elektrik = fields.Integer(string='Trobel Elektrik')
    # troble_kualitas = fields.Integer(string="Troble Kualitas")
    # tunggu_beam_cucuk = fields.Integer(string="Tunggu Bema/Cucuk")
    # tunggu_konfirmasi = fields.Integer(string='Tunggu Konfirmasi')
    # pakan_habis = fields.Integer(string='Pakan Habis')
    hasil_total = fields.Float(compute='resume',string='Hasil Presentasi',readonly=True,store=True)
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
            ('13',_('13')),
			], string= "Line")
    # per_line = fields.Integer()
    total = fields.Integer(string="Total Mesin", compute='tot',readonly=True,store=True )
    total_snap = fields.Integer(string="Hasil Snap",compute='tambah',readonly=True,store=True)
    shift = fields.Selection([
        ('A',_('A')),
        ('B',_('B')),
        ('C',_('C')),
    ],string="Shift")
    tgl = fields.Datetime(string="Tanggal Snap",default=fields.Datetime.now,readonly=True)
    tot_mesin_jln = fields.Float(string="Total Mesin Jalan", compute='total_mesin', readonly=True,store=True)
    
    @api.depends('line')
    def tot(self):
        for a in self:
            if a.line == '1':
                a.total = 50
            elif a.line == '2':
                a.total = 50
            elif a.line == '3':
                a.total = 50
            elif a.line == '4':
                a.total = 50
            elif a.line == '5':
                a.total = 50
            elif a.line == '6':
                a.total = 42
            elif a.line == '7':
                a.total = 42
            elif a.line == '8':
                a.total = 42
            elif a.line == '9':
                a.total = 42
            elif a.line == '10':
                a.total = 42    
            elif a.line == '11':
                a.total = 18
            elif a.line == '12':
                a.total = 36
            elif a.line == '13':
                a.total = 36
            else:
                a.total = 550
         
                
    @api.depends('line','shift')
    def resume(self):
        for res in self:
            if res.line:
                res.hasil_total = res.total_snap / res.total
            else:
                res.hasil_total = 0
               
       
    @api.depends('line','shift')         
    def tambah(self):
        for tam in self:
            if tam.line:
                tam.total_snap = tam.putus_pakan + tam.putus_lusi + tam.bendera_merah + tam.bendera_biru + tam.hb + tam.oh + tam.lain_lain
            else:
                tam.total_snap = 0
    
    
    @api.depends('line','shift')
    def total_mesin(self):
        for tot in self:
            if tot.line:
                # mesin = tot.total_snap/tot.total
                tot.tot_mesin_jln = (tot.total - tot.total_snap)/ tot.total
            else:
                tot.tot_mesin_jln = 0
    