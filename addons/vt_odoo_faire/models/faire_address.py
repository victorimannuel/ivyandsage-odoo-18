from odoo import api, fields, models, _


class FaireAddress(models.Model):
    _name = "faire.address"
    _description = "Faire Address"
    
    faire_address_id = fields.Char(string='Faire Address ID')
    name = fields.Char(string='Name')
    address1 = fields.Datetime(string='Address1')
    address2 = fields.Datetime(string='Address2')
    postal_code = fields.Char(string='Postal Code')
    city = fields.Char(string='City')
    state = fields.Char(string='State')
    state_code = fields.Char(string='State Code')
    phone_number = fields.Char(string='Phone Number')
    country = fields.Char(string='Country')
    country_code = fields.Char(string='Country Code')
    company_name = fields.Char(string='Company Name')
    address_type = fields.Char(string='Address Type')