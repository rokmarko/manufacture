# Copyright 2022 Tecnativa - Víctor Martínez
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    product_id = fields.Many2one(
        'product.product', 'Product',
        domain="[('bom_ids', '!=', False), ('bom_ids.active', '=', True), ('bom_ids.type', 'in', ['normal', 'subcontract']), ('type', 'in', ['product', 'consu']), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        readonly=True, required=True, check_company=True,
        states={'draft': [('readonly', False)]})


    # Overwrite the field domain for adding subcontracting BoMs with the check
    bom_id = fields.Many2one(
        domain="""[
        '&',
            '|',
                ('company_id', '=', False),
                ('company_id', '=', company_id),
            '&',
                '|',
                    ('product_id','=',product_id),
                    '&',
                        ('product_tmpl_id.product_variant_ids','=',product_id),
                        ('product_id','=',False),
        '|',
            ('type', '=', 'normal'),
            '&', ('type', '=', 'subcontract'), ('allow_in_regular_production', '=', True)
        ]""",
    )
