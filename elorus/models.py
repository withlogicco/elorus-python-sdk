from dataclasses import dataclass, field
from typing import List, Optional

from elorus.typings import AdType, DefaultCurrencyCode, DefaultLanguage


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