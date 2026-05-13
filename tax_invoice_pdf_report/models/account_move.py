from odoo import models, api, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_dispatch_no(self, invoice_id):
        dispatch = invoice_id.invoice_line_ids.sale_line_ids.order_id.picking_ids.filtered(
            lambda x: x.y_dispatch_doc_no).mapped('y_dispatch_doc_no')
        return ','.join(dispatch) if dispatch else ''

    def get_dispatch_through(self, invoice_id):
        carrier = invoice_id.invoice_line_ids.sale_line_ids.order_id.picking_ids.filtered(
            lambda x: x.y_transporter).mapped('y_transporter')
        return ','.join(carrier.mapped('name')) if carrier else ''
    
    def get_lutbond_number(self, invoice_id):
        lut_bond = invoice_id.invoice_line_ids.sale_line_ids.order_id.filtered(
            lambda x: x.y_lut_bond_no).mapped('y_lut_bond_no')
        return ','.join(lut_bond) if lut_bond else ''

    def get_vehicle_number(self, invoice_id):
        vehicle = invoice_id.invoice_line_ids.sale_line_ids.order_id.picking_ids.filtered(
            lambda x: x.y_ext_vehicle_no).mapped('y_ext_vehicle_no')
        return ','.join(vehicle) if vehicle else ''

    def get_po_number(self, invoice_id):
        po_ids = invoice_id.invoice_line_ids.sale_line_ids.order_id.filtered(lambda x: x.y_po_no)
        return ','.join(po_ids.mapped('y_po_no')) if po_ids else ''

    def get_po_date(self, invoice_id):
        po_ids = invoice_id.invoice_line_ids.sale_line_ids.order_id.filtered(lambda x: x.y_po_date)
        return ','.join(str(po_date) for po_date in po_ids.mapped('y_po_date')) if po_ids else ''
    
    def tax_calculation(self):
        allowed_groups, all_taxes = {'SGST', 'CGST', 'IGST','CESS'}, {"taxes": []}
        for line in self.invoice_line_ids:
            hsn, tax_vals = line.l10n_in_hsn_code, line._get_tax_line_group_values()
            for tax in line.tax_ids.filtered(lambda t: t.tax_group_id.name in ('GST', 'IGST')):
                existing = next((t for t in all_taxes["taxes"] if t["parent_tax"] == tax.name and t["hsn_code"] == hsn), None)
                if not existing:
                    existing = {
                        "parent_tax": tax.name, "parent_tax_group": tax.tax_group_id.name,
                        "parent_tax_amount": 0, "child_taxes": {}, "hsn_code": hsn,
                        "price_subtotal": line.price_subtotal
                    }
                    all_taxes["taxes"].append(existing)
                existing["parent_tax_amount"] += round(line.price_subtotal, 2)
                for group in allowed_groups:
                    amount, rate = tax_vals.get(group), tax_vals.get(f"{group}_RATE", 0)
                    if amount:
                        existing["child_taxes"].setdefault(group, {
                            "tax_id": group, "name": f"{rate}% {group}", "rate": float(rate),
                            "amount": 0, "tax_group": group, "hsn_code": hsn
                        })["amount"] += round(amount, 2)
        for tax in all_taxes["taxes"]:
            tax["child_taxes"] = list(tax["child_taxes"].values())
        return all_taxes