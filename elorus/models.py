from dataclasses import dataclass, field
from datetime import date as Date
from typing import List, Optional

from elorus.typings import AdType, CalculatorMode, DefaultCurrencyCode, DefaultLanguage


@dataclass
class Addresses:
    id: str
    address: str
    city: str
    state: str
    zip: str
    country: str
    branch_code: str
    ad_type: AdType

    def serialize(self):
        return {
            "id": self.id,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "country": self.country,
            "branch_code": self.branch_code,
            "ad_type": self.ad_type,
        }


@dataclass
class Email:
    email: str
    primary: Optional[bool] = False
    id: Optional[str] = None

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "primary": self.primary,
        }


@dataclass
class Phone:
    phone: str
    primary: Optional[bool] = False
    id: Optional[str] = None

    def serialize(self):
        return {
            "id": self.id,
            "phone": self.phone,
            "primary": self.primary,
        }


@dataclass
class TrackingCategory:
    trackingcategory: str
    option: str

    def serialize(self):
        return {
            "trackingcategory": self.trackingcategory,
            "option": self.option,
        }


@dataclass
class Contact:
    custom_id: str
    first_name: str
    last_name: str
    addresses: Optional[List[Addresses]]
    email: Optional[List[Email]]
    tracking_categories: Optional[List[TrackingCategory]]
    phones: list = field(default_factory=list)
    default_taxes: list = field(default_factory=list)
    client_type: int = 1
    active: Optional[bool] = True
    company: Optional[str] = ""
    profession: Optional[str] = ""
    vat_number: Optional[str] = ""
    is_client: Optional[bool] = False
    is_supplier: Optional[bool] = False
    default_currency_code: Optional[DefaultCurrencyCode] = "EUR"
    default_language: Optional[DefaultLanguage] = "en"
    default_theme: Optional[str] = None

    def serialize(self):
        return {
            "custom_id": self.custom_id,
            "active": self.active,
            "client_type": self.client_type,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "company": self.company,
            "profession": self.profession,
            "vat_number": self.vat_number,
            "is_client": self.is_client,
            "is_supplier": self.is_supplier,
            "default_taxes": self.default_taxes,
            "addresses": [address.serialize() for address in self.addresses],
            "email": [email.serialize() for email in self.email],
            "phones": [phone.serialize() for phone in self.phones],
            "tracking_categories": [
                tracking_category.serialize()
                for tracking_category in self.tracking_categories
            ],
            "default_currency_code": self.default_currency_code,
            "default_language": self.default_language,
            "default_theme": self.default_theme,
        }


@dataclass
class BillingAddress:
    address_line: str
    city: str
    state: str
    zip: str
    country: str

    def serialize(self):
        return {
            "address_line": self.address_line,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "country": self.country,
        }


@dataclass
class Item:
    product: str
    title: str
    description: str
    quantity: str
    unit_measure: int
    unit_value: str
    unit_discount: str
    unit_total: str
    taxes: list = field(default_factory=list)

    def serialize(self):
        return {
            "product": self.product,
            "title": self.title,
            "description": self.description,
            "quantity": self.quantity,
            "unit_measure": self.unit_measure,
            "unit_value": self.unit_value,
            "unit_discount": self.unit_discount,
            "unit_total": self.unit_total,
            "taxes": self.taxes,
        }


@dataclass
class Invoice:
    custom_id: str
    documenttype: int
    currency_code: Optional[DefaultCurrencyCode]
    draft: Optional[bool] = False
    sequence_id: Optional[str] = None
    number: Optional[str] = ""
    date: Date
    due_days = Optional[int] = 0
    client = int
    client_display_name: Optional[str] = ""
    client_profession: Optional[str] = ""
    client_vat_number: Optional[str] = ""
    billing_address: Optional[BillingAddress]
    shipping_address: Optional[BillingAddress]
    client_contact_person: Optional[str] = ""
    client_phone_number: Optional[str] = ""
    client_email: Optional[str] = ""
    exchange_rate: Optional[str] = ""
    calculator_mode: Optional[CalculatorMode] = "intial"
    items: List[Item]
    withholding_taxes: list = field(default_factory=list)
    template_id: Optional[str] = None
    public_notes: Optional[str] = ""
    trackingcategories = Optional[List[TrackingCategory]]

    def serialize(self):
        return {
            "custom_id": self.custom_id,
            "documenttype": self.documenttype,
            "currency_code": self.currency_code,
            "draft": self.draft,
            "sequence_id": self.sequence_id,
            "number": self.number,
            "date": self.date,
            "due_days": self.due_days,
            "client": self.client,
            "client_display_name": self.client_display_name,
            "client_profession": self.client_profession,
            "client_vat_number": self.client_vat_number,
            "billing_address": self.billing_address.serialize(),
            "shipping_address": self.shipping_address.serialize(),
            "client_contact_person": self.client_contact_person,
            "client_phone_number": self.client_phone_number,
            "client_email": self.client_email,
            "exchange_rate": self.exchange_rate,
            "calculator_mode": self.calculator_mode,
            "items": [item.serialize() for item in self.items],
            "withholding_taxes": self.withholding_taxes,
            "template_id": self.template_id,
            "public_notes": self.public_notes,
            "trackingcategories": [
                tracking_category.serialize()
                for tracking_category in self.trackingcategories
            ],
        }
