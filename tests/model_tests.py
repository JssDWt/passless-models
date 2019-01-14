from unittest import TestCase
from passless_models import Receipt
from datetime import datetime
from dateutil.tz import tzoffset
from decimal import Decimal

class ReceiptTests(TestCase):
    def test_receipt_deserialization(self):
        receipt_json = """{
            "time": "2018-11-26T13:43:00+01:00",
            "currency": "EUR",
            "subTotal": {
                "withoutTax": 39,
                "withTax": 39,
                "tax": 0
            },
            "totalDiscount": {
                "withoutTax": 0,
                "withTax": 0,
                "tax": 0
            },
            "totalPrice": {
                "withoutTax": 39,
                "withTax": 39,
                "tax": 0
            },
            "totalFee": {
                "withoutTax": 0,
                "withTax": 0,
                "tax": 0
            },
            "totalPaid": 39,
            "items": [
                {
                    "name": "SCL3711 NFC reader/writer",
                    "quantity": 1.00,
                    "unit": "pc",
                    "unitPrice": {
                        "withoutTax": 39,
                        "withTax": 39,
                        "tax": 0
                    },
                    "subTotal": {
                        "withoutTax": 39,
                        "withTax": 39,
                        "tax": 0
                    },
                    "totalDiscount": {
                        "withoutTax": 0,
                        "withTax": 0,
                        "tax": 0
                    },
                    "totalPrice": {
                        "withoutTax": 39,
                        "withTax": 39,
                        "tax": 0
                    },
                    "taxClass": {
                        "name": "Zero rate",
                        "fraction": 0
                    },
                    "shortDescription": "Compact and capable usb rfid reader/writer",
                    "description": "With its functional solid mechanical design that has no removable parts that you may loose, SCL3711 is perfect for mobile uses. Also, it supports NFC peer-to-peer protocol.",
                    "brand": "Identive",
                    "discounts": []
                }
            ],
            "payments": [
                {
                    "method": "card",
                    "amount": 39,
                    "meta": {
                        "type": "Maestro",
                        "cardNumber": "1234 5678 1234 5678",
                        "expiration": "2023-10-28T00:00:00Z"
                    }
                }
            ],
            "vendor": {
                "name": "NFC store",
                "address": "Techniekweg 42, 1234AA, Utrecht",
                "phone": "030-42424242",
                "vatNumber": "NL424242424B42",
                "kvkNumber": "42424242",
                "email": "info@nfcstore.com",
                "web": "https://www.nfcstore.io/",
                "meta": {}
            },
            "vendorReference": "20181126-000316",
            "fees": [],
            "loyalties": []
            }"""

        instance = Receipt.from_json(receipt_json)
        self.assertEqual(instance.time, datetime(2018,11,26,13,43,00,0,tzinfo=tzoffset("UTC+1",60*60)))
        self.assertEqual(instance.currency, "EUR")
        self.assertEqual(instance.subTotal.withoutTax, 39)
        self.assertEqual(instance.subTotal.withTax, 39)
        self.assertEqual(instance.subTotal.tax, 0)
        self.assertEqual(instance.totalDiscount.withoutTax, 0)
        self.assertEqual(instance.totalDiscount.withTax, 0)
        self.assertEqual(instance.totalDiscount.tax, 0)
        self.assertEqual(instance.totalPrice.withoutTax, 39)
        self.assertEqual(instance.totalPrice.withTax, 39)
        self.assertEqual(instance.totalPrice.tax, 0)
        self.assertEqual(instance.totalFee.withoutTax, 0)
        self.assertEqual(instance.totalFee.withTax, 0)
        self.assertEqual(instance.totalFee.tax, 0)
        self.assertEqual(instance.totalPaid, 39)
        self.assertEqual(len(instance.items), 1)
        item = instance.items[0]
        self.assertEqual(item.name, "SCL3711 NFC reader/writer")
        self.assertEqual(item.quantity, 1)
        self.assertEqual(item.unit, "pc")
        self.assertEqual(item.unitPrice.withoutTax, 39)
        self.assertEqual(item.unitPrice.withTax, 39)
        self.assertEqual(item.unitPrice.tax, 0)
        self.assertEqual(item.subTotal.withoutTax, 39)
        self.assertEqual(item.subTotal.withTax, 39)
        self.assertEqual(item.subTotal.tax, 0)
        self.assertEqual(item.totalDiscount.withoutTax, 0)
        self.assertEqual(item.totalDiscount.withTax, 0)
        self.assertEqual(item.totalDiscount.tax, 0)
        self.assertEqual(item.totalPrice.withoutTax, 39)
        self.assertEqual(item.totalPrice.withTax, 39)
        self.assertEqual(item.totalPrice.tax, 0)
        self.assertEqual(item.taxClass.name, "Zero rate")
        self.assertEqual(item.taxClass.fraction, 0)
        self.assertEqual(item.shortDescription, "Compact and capable usb rfid reader/writer")
        self.assertEqual(item.description, "With its functional solid mechanical design that has no removable parts that you may loose, SCL3711 is perfect for mobile uses. Also, it supports NFC peer-to-peer protocol.")
        self.assertEqual(item.brand, "Identive")
        self.assertIsInstance(item.discounts, list)
        self.assertEqual(len(item.discounts), 0)
        self.assertEqual(len(instance.payments), 1)
        payment = instance.payments[0]
        self.assertEqual(payment.method, "card")
        self.assertEqual(payment.amount, 39)
        self.assertEqual(payment.meta['type'], "Maestro")
        self.assertEqual(payment.meta['cardNumber'], "1234 5678 1234 5678")
        self.assertEqual(payment.meta['expiration'], "2023-10-28T00:00:00Z")
        self.assertEqual(instance.vendor.name, "NFC store")
        self.assertEqual(instance.vendor.address, "Techniekweg 42, 1234AA, Utrecht")
        self.assertEqual(instance.vendor.phone, "030-42424242")
        self.assertEqual(instance.vendor.vatNumber, "NL424242424B42")
        self.assertEqual(instance.vendor.kvkNumber, "42424242")
        self.assertEqual(instance.vendor.email, "info@nfcstore.com")
        self.assertEqual(instance.vendor.web, "https://www.nfcstore.io/")
        self.assertIsInstance(instance.vendor.meta, dict)
        self.assertEqual(instance.vendorReference, "20181126-000316")
        self.assertIsInstance(instance.fees, list)
        self.assertEqual(len(instance.fees), 0)
        self.assertIsInstance(instance.loyalties, list)
        self.assertEqual(len(instance.loyalties), 0)
        