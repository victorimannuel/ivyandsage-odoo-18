from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _set_delivery_date(self, date):
        self.commitment_date = date