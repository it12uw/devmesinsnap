from odoo import  api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from datetime import datetime, timedelta
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime
from odoo.tools.misc import format_date

class SnapQc(models.Model):
    _name = 'snap.qc'
    _description = 'Snap Qc' 
    _date_name = 'date_planned_start'

    
    # Relasi ke model hr.department
    divisi_id   = fields.Many2one('hr.department', string="Divisi")

    # Relasi ke model blok.mesin (blok.py)
    blok_id = fields.Many2one('blok.mesin', string='Blok')

    # Relasi ke model line.mesin.produksi (line.py)
    line_id= fields.Many2one('line.mesin.produksi', string='Line')

    # Relasi ke model hr.employee
    operator = fields.Many2one('hr.employee', string='Operator')

    # Relasi ke model snap.qc.line (child class)
    snap_qc_line = fields.One2many('snap.qc.line', 'snap_qc_id')

    # Relasi ke model kode.kain (kodekain.py)
    kodekain = fields.Many2one('kode.kain',string="Kode Kain")
    
    # Relasi ke model data.mesin.produksi (datamesin.py)
    # mesin_produksi_id = fields.Many2many('data.mesin.produksi', string='Data Mesin', store=True)
    kanban_color = fields.Integer(string="Color")
                                                    
    tanggal_snap = fields.Date(string="Tanggal Snap", default=fields.Date.context_today)
    
    # Relasi ke model data.mesin.produksi (datamesin.py)
    nomor_mesin = fields.Many2one('data.mesin.produksi', string="Mesin")

    mesin = fields.Char(string="Mesin", readonly=True)
    putus_pakan=fields.Boolean(string='Putus Pakan')
    putus_lusi = fields.Boolean(string="Putus Lusi")
    naik_beam = fields.Boolean(string="Naik Beam")
    hb = fields.Boolean(string="Habis Beam/Beam Baru")
    troble_kualitas = fields.Boolean(string="Trouble Kualitas")
    tunggu_beam_cucuk = fields.Boolean(string="Tunggu Beam/Cucuk")
    pick_finding = fields.Boolean(string="Pick Finding")
    troble_mekanik = fields.Boolean(string="Trouble Mekanik")
    troble_elektrik = fields.Boolean(string="Trouble Elektrik")
    tunggu_konfirmasi = fields.Boolean(string="Tunggu Konfirmasi")
    preventif = fields.Boolean(string="Preventif")
    pakan_habis = fields.Boolean(string="Pakan Habis")
    ambrol = fields.Boolean(string="Ambrol")
    dedel=fields.Boolean(string="Dedel")  
    rantas=fields.Boolean(string="Rantas")  
    oh = fields.Boolean(string="Over Houle")    
    bendera_merah = fields.Boolean(string=" Bendera Merah")
    bendera_biru = fields.Boolean(string="Bendera Biru") 
    rpm = fields.Integer(string='RPM')
    keterangan = fields.Char(string="Lain Lain")
    lain_lain  =  fields.Text(string="Keterangan")
    jam_snap = fields.Datetime(string='Jam', default=fields.Datetime.now)
    
    #Relasi ke model line.mesin.produksi  (line.py) 
    # untuk mengambil data total mesin  melalui field line_id
    total_mesin = fields.Integer(related='line_id.total_mesin', store=True)
    presentasi_total = fields.Float(compute='_compute_presentasi_total', string="Hasil Presentasi")

    # Fungsi Compute untuk menampilkan presentasi total dari mesin
    @api.depends('total_mesin')
    def _compute_presentasi_total(self):
        for res in self:
            if res.line_id:
                res.presentasi_total = res.total_snap / res.total_mesin
            else:
                res.presentasi_total = 0 

    total_mesin_jalan = fields.Float(string='Total Mesin Jalan', compute='_compute_total_mesin_jalan', store=True)
    
    @api.depends('snap_qc_line', 'total_mesin')
    def _compute_total_mesin_jalan(self):
        for record in self:
            total_mesin = record.total_mesin or 0
            total_mesin_diperiksa = len(record.snap_qc_line)
            total_mesin_jalan = total_mesin - total_mesin_diperiksa

            if total_mesin > 0:
                record.total_mesin_jalan = (total_mesin_jalan / total_mesin)
            else:
                record.total_mesin_jalan = 0

    total_snap=fields.Integer(string="Total Snap", compute='_compute_total_snap')  

    @api.depends('snap_qc_line.putus_pakan', 'snap_qc_line.putus_lusi', 'snap_qc_line.ambrol', 'snap_qc_line.dedel', 'snap_qc_line.rantas', 'snap_qc_line.preventif', 'snap_qc_line.oh', 'snap_qc_line.naik_beam', 'snap_qc_line.hb', 'snap_qc_line.bendera_merah', 'snap_qc_line.lain_lain')
    def _compute_total_snap(self):
        for record in self:
            total_snap = 0
            for line in record.snap_qc_line:
                total_snap += 1 if line.putus_pakan else 0
                total_snap += 1 if line.putus_lusi else 0
                total_snap += 1 if line.ambrol else 0
                total_snap += 1 if line.dedel else 0
                total_snap += 1 if line.rantas else 0
                total_snap += 1 if line.preventif else 0
                total_snap += 1 if line.oh else 0
                total_snap += 1 if line.naik_beam else 0
                total_snap += 1 if line.hb else 0
                total_snap += 1 if line.bendera_merah else 0
                total_snap += 1 if line.lain_lain else 0

            record.total_snap = total_snap   


    # Onchange = kodekain akan berubah mengikuti nomor_mesin
    @api.onchange('nomor_mesin')
    def onchange_nomor_mesin(self):
         if self.nomor_mesin:
            self.kodekain = self.nomor_mesin.kodekain
    
    shift = fields.Selection([
        ('1', 'Shift A'),
        ('2', 'Shift B'),
        ('3', 'Shift C')
    ], string='Shift')
    
    putaran = fields.Selection([
            ('1', 'Putaran 1'),
            ('2', 'Putaran 2'),
            ('3', 'Putaran 3')
        ], string='Putaran')
    
    state    = fields.Selection([
            ('draft','Draft'),
            ('start','Confirmed'),
            ('progress','In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')], 
            string="Status", readonly=True,copy=False, default="draft",track_visibility='onchange', widget='statusbar')
    
    # Tombol Draft
    def action_draft(self):
        self.write({'state': 'draft'}) 
    # Tombol start
    def action_start(self):
        self.write({'state': 'start'})    
    # Tombol Progres
    def action_progress(self):
        self.write({'state': 'progress'})
    # Tombol Done
    def action_done(self):
        self.write({'state': 'done'})
    # Tombol Cancel
    def action_cancel(self):
        self.write({'state': 'cancel'})             
    
    # Id Record Data
    def name_get(self):
        result = [] 
        for record in self:
            name = record.name 
            result.append((record.id, name))
        return result 
    
    name = fields.Char('Snap Reference', copy=False, readonly=True,default='New')
    priority = fields.Selection(
        PROCUREMENT_PRIORITIES, string='Priority', default='0', index=True)    
    PROCUREMENT_PRIORITIES = [
        ('0', 'Low'),
        ('1', 'High'),
    ]
    
    # Kode Untuk Sequence QC/SHTL/0000
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('snap.qc.sequence') or 'New'
        return super(SnapQc, self).create(vals)
    
    date_planned_start = fields.Datetime(
        'Snap Date',
        copy=False,
        default=lambda self: fields.Datetime.now(),
        help="Date at which you plan to start the Snap.",
        index=True,
    )
    
    date_planned_finished = fields.Datetime(
        'Selesai Snap',
        default=lambda self: fields.Datetime.now() + timedelta(hours=8),
        compute='_compute_date_planned_finished',
        help="Date at which you plan to finish the Snap.",
        copy=False
    )
    
    date_deadline = fields.Datetime(
        'Deadline',
        copy=False ,
        store=True,
        compute='_compute_date_deadline',
        inverse='_set_date_deadline',
        help="Informative date allowing to define when the quality control should be processed at the latest to finish on time."
    )
    
    @api.depends('date_planned_start')
    def _compute_date_deadline(self):
        for record in self:
            if record.date_planned_start:
                record.date_deadline = record.date_planned_start + timedelta(hours=8)
    
    def _set_date_deadline(self):
        for record in self:
            if record.date_planned_start:
                record.date_deadline = record.date_planned_start + timedelta(hours=8)

    @api.model
    def _get_default_date_planned_finished(self):
        if self.env.context.get('default_date_planned_start'):
            return fields.Datetime.to_datetime(self.env.context.get('default_date_planned_start')) + timedelta(hours=8)
        return datetime.now() + timedelta(hours=8)
    
    @api.depends('date_planned_start')
    def _compute_date_planned_finished(self):
        for record in self:
            if record.date_planned_start:
                record.date_planned_finished = record.date_planned_start + timedelta(hours=8)  
            
    #Tombol Buka Form Checklist QC Shuttle 
    # def buka_form_qc(self):
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'name': 'Form Checklist QC Shuttle',
    #             'res_model': 'snap.qc.line',
    #             'view_mode': 'form',
    #             'view_id': self.env.ref('qc_shuttle.snap_qc_pop_up_form').id,
    #             'target': 'new',
    #             'context': {
    #                 'default_snap_qc_id': self.id,
    #                 'default_nomor_mesin': self.nomor_mesin.id if self.nomor_mesin else False,
    #                 'default_kodekain': self.kodekain.id,
    #                 'default_putus_lusi': self.putus_lusi,
    #                 'default_putus_pakan': self.putus_pakan,
    #                 'default_bendera_merah': self.bendera_merah,
    #                 'default_ambrol': self.ambrol,
    #                 'default_dedel': self.dedel,
    #                 'default_hb': self.hb,
    #                 'default_naik_beam': self.naik_beam,
    #                 'default_oh': self.oh,
    #                 'default_preventif': self.preventif,
    #                 'default_keterangan': self.keterangan,
    #             },
    #         }
    
    total_putus_lusi = fields.Integer(string='Total Putus Lusi', compute='_compute_total_putus_lusi')
    total_putus_pakan = fields.Integer(string='Total Putus Pakan', compute='_compute_total_putus_pakan')
    total_bendera_merah = fields.Integer(string='Total Bendera Merah', compute='_compute_total_bendera_merah')
    total_ambrol = fields.Integer(string='Total Ambrol', compute='_compute_total_ambrol')
    total_dedel = fields.Integer(string='Total Dedel', compute='_compute_total_dedel')
    total_hb = fields.Integer(string='Total Habis Beam/Beam Baru', compute='_compute_total_hb')
    total_naik_beam = fields.Integer(string='Total Naik Beam', compute='_compute_total_naik_beam')
    total_oh = fields.Integer(string='Total Over Houle', compute='_compute_total_oh')
    total_preventif = fields.Integer(string='Total Preventif', compute='_compute_total_preventif')
    total_lain_lain = fields.Char(string='Total Lain Lain', compute='_compute_total_lain_lain')

    @api.depends('snap_qc_line.putus_lusi')
    def _compute_total_putus_lusi(self):
        for record in self:
            record.total_putus_lusi = sum(record.snap_qc_line.mapped('putus_lusi'))

    @api.depends('snap_qc_line.putus_pakan')
    def _compute_total_putus_pakan(self):
        for record in self:
            record.total_putus_pakan = sum(record.snap_qc_line.mapped('putus_pakan'))

    @api.depends('snap_qc_line.bendera_merah')
    def _compute_total_bendera_merah(self):
        for record in self:
            record.total_bendera_merah = sum(record.snap_qc_line.mapped('bendera_merah'))

    @api.depends('snap_qc_line.ambrol')
    def _compute_total_ambrol(self):
        for record in self:
            record.total_ambrol = sum(record.snap_qc_line.mapped('ambrol'))

    @api.depends('snap_qc_line.dedel')
    def _compute_total_dedel(self):
        for record in self:
            record.total_dedel = sum(record.snap_qc_line.mapped('dedel'))

    @api.depends('snap_qc_line.hb')
    def _compute_total_hb(self):
        for record in self:
            record.total_hb = sum(record.snap_qc_line.mapped('hb'))

    @api.depends('snap_qc_line.naik_beam')
    def _compute_total_naik_beam(self):
        for record in self:
            record.total_naik_beam = sum(record.snap_qc_line.mapped('naik_beam'))

    @api.depends('snap_qc_line.oh')
    def _compute_total_oh(self):
        for record in self:
            record.total_oh = sum(record.snap_qc_line.mapped('oh'))

    @api.depends('snap_qc_line.preventif')
    def _compute_total_preventif(self):
        for record in self:
            record.total_preventif = sum(record.snap_qc_line.mapped('preventif'))

    @api.depends('snap_qc_line.lain_lain')
    def _compute_total_lain_lain(self):
        for record in self:
            total_text = ""
            for line in record.snap_qc_line:
                if isinstance(line.lain_lain, str):
                    total_text += line.lain_lain + "\n"
            record.total_lain_lain = total_text.strip()

class SnapQcLine(models.Model):
    _name='snap.qc.line'
    _description='Hasil Snap'

    # Relasi balik ke model snap.qc (parent class)
    snap_qc_id = fields.Many2one('snap.qc', string='Snap QC', ondelete='cascade', index=True, copy=False)

    # Relasi ke model hr.employee
    operator = fields.Many2one('hr.employee', string='Responsible')

    # Relasi ke model data.mesin.produksi (datamesin.py)
    # mesin_produksi_id = fields.Many2many('data.mesin.produksi', string="Mesin Produksi")

    # Relasi ke model data.mesin.produksi (datamesin.py)
    nomor_mesin = fields.Many2one('data.mesin.produksi', string="Mesin")

    # Relasi ke model kode.kain (kodekain.py)
    kodekain = fields.Many2one('kode.kain',string="Kode Kain")

    # Relasi ke model blok.mesin (blok.py)
    blok_id = fields.Many2one('blok.mesin', string='Blok')

    # Relasi ke model line.mesin.produksi (line.py)
    line_id= fields.Many2one('line.mesin.produksi', string='Deret')

    tanggal_snap = fields.Date(string="Tanggal Snap", default=fields.Date.context_today)
    putus_pakan=fields.Boolean(string='Putus Pakan')
    putus_lusi = fields.Boolean(string="Putus Lusi") 
    ambrol = fields.Boolean(string="Ambrol") 
    dedel=fields.Boolean(string="Dedel")
    rantas=fields.Boolean(string="Rantas")
    keterangan = fields.Char(string="Lain Lain")
    preventif = fields.Boolean(string="Preventif")
    oh = fields.Boolean(string="Over Houle") 
    naik_beam = fields.Boolean(string="Naik Beam")
    hb = fields.Boolean(string="Habis Beam/Beam Baru")
    bendera_merah = fields.Boolean(string="Bendera Merah")
    lain_lain  =  fields.Char(string="Keterangan")
    
    shift = fields.Selection([
        ('1', 'Shift 1'),
        ('2', 'Shift 2'),
        ('3', 'Shift 3')
    ], string='Shift')
    
    putaran = fields.Selection([
            ('1', '1'),
            ('2', '2'),
            ('3', '3')
        ], string='Putaran')
    
    # Onchange = kodekain akan berubah mengikuti nomor mesin
    @api.onchange('nomor_mesin')
    def onchange_nomor_mesin(self):
         if self.nomor_mesin:
            self.kodekain = self.nomor_mesin.kodekain
