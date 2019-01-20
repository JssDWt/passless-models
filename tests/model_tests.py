from unittest import TestCase
from passless_models import Receipt
from datetime import datetime
from dateutil.tz import tzoffset
from decimal import Decimal
import json

TEST_RECEIPT = """{
    "time": "2018-11-26T13:43:00+01:00",
    "currency": "EUR",
    "subtotal": {
        "withoutTax": 100,
        "withTax": 121.0,
        "tax": 21.0
    },
    "totalDiscount": {
        "withoutTax": 0,
        "withTax": 0,
        "tax": 0
    },
    "totalPrice": {
        "withoutTax": 100,
        "withTax": 121.0,
        "tax": 21.0
    },
    "totalFee": {
        "withoutTax": 0,
        "withTax": 0,
        "tax": 0
    },
    "totalPaid": 121,
    "items": [
        {
            "name": "SCL3711 NFC reader/writer",
            "quantity": 1.00,
            "unit": "pc",
            "unitPrice": {
                "withoutTax": 100,
                "withTax": 121.0,
                "tax": 21.0
            },
            "subtotal": {
                "withoutTax": 100,
                "withTax": 121.0,
                "tax": 21.0
            },
            "totalDiscount": {
                "withoutTax": 0,
                "withTax": 0,
                "tax": 0
            },
            "totalPrice": {
                "withoutTax": 100,
                "withTax": 121.0,
                "tax": 21.0
            },
            "taxClass": {
                "name": "Full rate",
                "fraction": 0.21
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
            "amount": 121,
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
        "logo": null,
        "meta": {}
    },
    "vendorReference": "20181126-000316",
    "fees": [],
    "loyalties": []
    }"""
class ReceiptTests(TestCase):
    def test_receipt_deserialization(self):
        instance = Receipt.from_json(TEST_RECEIPT)
        self.assertEqual(instance.time, datetime(2018,11,26,13,43,00,0,tzinfo=tzoffset("UTC+1",60*60)))
        self.assertEqual(instance.currency, "EUR")
        self.assertEqual(float(instance.subtotal.withoutTax), 100)
        self.assertEqual(float(instance.subtotal.withTax), 121)
        self.assertEqual(float(instance.subtotal.tax), 21)
        self.assertEqual(float(instance.totalDiscount.withoutTax), 0)
        self.assertEqual(float(instance.totalDiscount.withTax), 0)
        self.assertEqual(float(instance.totalDiscount.tax), 0)
        self.assertEqual(float(instance.totalPrice.withoutTax), 100)
        self.assertEqual(float(instance.totalPrice.withTax), 121)
        self.assertEqual(float(instance.totalPrice.tax), 21)
        self.assertEqual(float(instance.totalFee.withoutTax), 0)
        self.assertEqual(float(instance.totalFee.withTax), 0)
        self.assertEqual(float(instance.totalFee.tax), 0)
        self.assertEqual(float(instance.totalPaid), 121)
        self.assertEqual(len(instance.items), 1)
        item = instance.items[0]
        self.assertEqual(item.name, "SCL3711 NFC reader/writer")
        self.assertEqual(float(item.quantity), 1)
        self.assertEqual(item.unit, "pc")
        self.assertEqual(float(item.unitPrice.withoutTax), 100)
        self.assertEqual(float(item.unitPrice.withTax), 121)
        self.assertEqual(float(item.unitPrice.tax), 21)
        self.assertEqual(float(item.subtotal.withoutTax), 100)
        self.assertEqual(float(item.subtotal.withTax), 121)
        self.assertEqual(float(item.subtotal.tax), 21)
        self.assertEqual(float(item.totalDiscount.withoutTax), 0)
        self.assertEqual(float(item.totalDiscount.withTax), 0)
        self.assertEqual(float(item.totalDiscount.tax), 0)
        self.assertEqual(float(item.totalPrice.withoutTax), 100)
        self.assertEqual(float(item.totalPrice.withTax), 121)
        self.assertEqual(float(item.totalPrice.tax), 21)
        self.assertEqual(item.taxClass.name, "Full rate")
        self.assertAlmostEqual(float(item.taxClass.fraction), 0.21)
        self.assertEqual(item.shortDescription, "Compact and capable usb rfid reader/writer")
        self.assertEqual(item.description, "With its functional solid mechanical design that has no removable parts that you may loose, SCL3711 is perfect for mobile uses. Also, it supports NFC peer-to-peer protocol.")
        self.assertEqual(item.brand, "Identive")
        self.assertIsInstance(item.discounts, list)
        self.assertEqual(len(item.discounts), 0)
        self.assertEqual(len(instance.payments), 1)
        payment = instance.payments[0]
        self.assertEqual(payment.method, "card")
        self.assertEqual(float(payment.amount), 121)
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
    
    def test_round_trip(self):
        loaded = json.loads(TEST_RECEIPT)
        expected = json.dumps(loaded, sort_keys=True)
        receipt = Receipt.from_json(TEST_RECEIPT)
        actual = receipt.to_json()
        self.assertEqual(expected, actual)
