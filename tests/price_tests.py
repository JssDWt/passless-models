from decimal import Decimal
from unittest import TestCase
from passless_models import Price

class PriceTests(TestCase):
    def test_tax_assertion_valid(self):
        Price(
            withoutTax=Decimal('1.0'),
            withTax=Decimal('1.21'),
            tax=Decimal('0.21')
        )
    
    def test_tax_assertion_off(self):
        with self.assertRaises(AssertionError, msg="tax does not add up."):
            Price(
                withoutTax=Decimal('0.99'),
                withTax=Decimal('1.21'),
                tax=Decimal('0.21')
            )