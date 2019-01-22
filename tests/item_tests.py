from decimal import Decimal
from unittest import TestCase
from passless_models import Item, Price, TaxClass

class ItemTests(TestCase):
    def test_tax_assertion_rounding_flexibility(self):
        price=Price(
            withoutTax=Decimal('0.99'),
            withTax=Decimal('1.20'),
            tax=Decimal('0.21')
        )
        Item(
            name="Thing",
            quantity=1,
            unit="pc",
            unitPrice=price,
            subtotal=price,
            totalDiscount=Price(0,0,0),
            totalPrice=price,
            taxClass=TaxClass(
                "Full rate",
                fraction=Decimal('0.21')
            )
        )

    def test_tax_assertion_raises(self):
        price=Price(
            withoutTax=Decimal('2'),
            withTax=Decimal('2.21'),
            tax=Decimal('0.21')
        )

        with self.assertRaises(AssertionError, msg="Tax price not equal to tax rate"):
            Item(
                name="Thing",
                quantity=1,
                unit="pc",
                unitPrice=price,
                subtotal=price,
                totalDiscount=Price(0,0,0),
                totalPrice=price,
                taxClass=TaxClass(
                    "Full rate",
                    fraction=Decimal('0.21')
                )
            )