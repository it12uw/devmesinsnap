from odoo import http
from odoo.http import request

class MesinProduksiController(http.Controller):
    @http.route('/your/endpoint', type='json', auth='user')
    def load_mesin_produksi(self, line_id, blok_id):
        # Lakukan pengambilan data mesin produksi berdasarkan line_id dan blok_id
        mesin_produksi_records = request.env['data.mesin.produksi'].search([
            ('line_id', '=', line_id),
            ('blok_id', '=', blok_id),
        ])

        # Proses data sesuai kebutuhan
        mesin_produksi_data = []

        for mesin_produksi in mesin_produksi_records:
            mesin_produksi_data.append({
                'id': mesin_produksi.id,
                'name': mesin_produksi.name,
                # Tambahkan field lain sesuai kebutuhan
            })

        return mesin_produksi_data
