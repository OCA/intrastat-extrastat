from odoo.exceptions import ValidationError
from odoo.tests import tagged

from .common import IntrastatCommon


@tagged("post_install", "-at_install")
class TestIntrastatBase(IntrastatCommon):
    """Tests for this module"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                mail_create_nolog=True,
                mail_create_nosubscribe=True,
                mail_notrack=True,
                no_reset_password=True,
                tracking_disable=True,
            )
        )
        cls.fp_b2c = cls.fp_obj.create(
            {
                "name": "Test",
                "vat_required": False,
                "intrastat": "b2c",
            }
        )
        cls.fp_b2b = cls.fp_obj.create(
            {
                "name": "Test",
                "vat_required": True,
                "intrastat": "b2b",
            }
        )
        cls.journal_sale = cls.env["account.journal"].search(
            [("company_id", "=", cls.demo_company.id), ("type", "=", "sale")], limit=1
        )

    def test_company(self):
        # add 'Demo user' to intrastat_remind_user_ids
        self.demo_company.write(
            {"intrastat_remind_user_ids": [(6, False, [self.demo_user.id])]}
        )
        # then check if intrastat_email_list contains the email of the user
        self.assertEqual(self.demo_company.intrastat_email_list, self.demo_user.email)

    def test_no_email(self):
        self.demo_user.email = False
        with self.assertRaises(ValidationError):
            self.demo_company.write(
                {"intrastat_remind_user_ids": [(6, False, [self.demo_user.id])]}
            )

    def test_accessory(self):
        with self.assertRaises(ValidationError):
            self.shipping_cost.type = "consu"

    def test_fiscal_position(self):
        with self.assertRaises(ValidationError):
            self.env["account.fiscal.position"].create(
                {
                    "name": "TestB2B",
                    "vat_required": False,
                    "intrastat": "b2b",
                }
            )
        with self.assertRaises(ValidationError):
            self.env["account.fiscal.position"].create(
                {
                    "name": "TestB2C",
                    "vat_required": True,
                    "intrastat": "b2c",
                }
            )

    def test_account_move_fp_intrastat(self):
        invoice = self.env["account.move"].create(
            {
                "name": "Test",
                "move_type": "out_invoice",
                "invoice_date": "2021-01-01",
                "invoice_date_due": "2021-01-01",
                "partner_id": self.demo_company.partner_id.id,
                "fiscal_position_id": self.fp_b2b.id,
                "journal_id": self.journal_sale.id,
            }
        )
        self.assertEqual(invoice.intrastat_fiscal_position, "b2b")
        invoice.intrastat_fiscal_position = "b2c"
        self.assertEqual(invoice.intrastat_fiscal_position, "b2c")
        # Check that duplicating the invoice does not copy the intrastat value
        invoice_2 = invoice.copy()
        self.assertEqual(invoice.fiscal_position_id, invoice_2.fiscal_position_id)
        self.assertEqual(invoice_2.intrastat_fiscal_position, "b2b")

    def test_out_invoice_refund_fp_intrastat(self):
        partner = self.demo_company.partner_id
        invoice = self.env["account.move"].create(
            {
                "name": "Test",
                "move_type": "out_invoice",
                "invoice_date": "2021-01-01",
                "invoice_date_due": "2021-01-01",
                "partner_id": partner.id,
                "fiscal_position_id": self.fp_b2b.id,
                "journal_id": self.journal_sale.id,
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "name": "Test",
                            "quantity": 1,
                            "price_unit": 100,
                            "account_id": partner.property_account_receivable_id.id,
                        },
                    )
                ],
            }
        )
        invoice.intrastat_fiscal_position = "b2c"
        invoice.action_post()
        self.assertEqual(invoice.intrastat_fiscal_position, "b2c")
        move_reversal = (
            self.env["account.move.reversal"]
            .with_context(active_model="account.move", active_ids=invoice.ids)
            .create(
                {
                    "date": "2021-01-01",
                    "reason": "no reason",
                    "refund_method": "refund",
                    "journal_id": invoice.journal_id.id,
                }
            )
        )
        reversal = move_reversal.reverse_moves()
        reverse_move = self.env["account.move"].browse(reversal["res_id"])

        self.assertEqual(
            reverse_move.intrastat_fiscal_position,
            "b2b",
        )
