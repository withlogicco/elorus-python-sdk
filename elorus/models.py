from dataclasses import asdict, dataclass, field
from datetime import date as Date
from typing import List, Optional

from elorus.typings import AdType, CalculatorMode, DefaultCurrencyCode, DefaultLanguage


@dataclass
class BaseDataClass:
    def clean_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None and v != ""}


@dataclass
class Addresses(BaseDataClass):
    id: str
    address: str
    city: str
    state: str
    zip: str
    country: str
    branch_code: str
    ad_type: AdType


@dataclass
class Email(BaseDataClass):
    email: str
    primary: Optional[bool] = False
    id: Optional[str] = None


@dataclass
class Phone(BaseDataClass):
    phone: str
    primary: Optional[bool] = False
    id: Optional[str] = None


@dataclass
class TrackingCategory(BaseDataClass):
    trackingcategory: str
    option: str


@dataclass
class Contact(BaseDataClass):
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


@dataclass
class BillingAddress(BaseDataClass):
    address_line: str
    city: str
    state: str
    zip: str
    country: str


@dataclass
class Item(BaseDataClass):
    product: str
    description: str
    quantity: str
    unit_measure: int
    unit_value: str
    unit_discount: str
    unit_total: str
    mydata_classification_category: str
    mydata_classification_type: str
    taxes: list = field(default_factory=list)
    title: Optional[str] = ""

    def clean_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None and v != ""}


@dataclass
class Invoice(BaseDataClass):
    custom_id: str
    documenttype: int
    currency_code: Optional[DefaultCurrencyCode]
    date: Date
    client: int
    due_days: Optional[int]
    billing_address: Optional[BillingAddress]
    shipping_address: Optional[BillingAddress]
    items: List[Item]
    trackingcategories: Optional[List[TrackingCategory]]
    client_display_name: Optional[str] = field(default="")
    draft: Optional[bool] = False
    sequence_id: Optional[str] = None
    number: Optional[str] = ""
    client_profession: Optional[str] = ""
    client_vat_number: Optional[str] = ""
    client_contact_person: Optional[str] = ""
    client_phone_number: Optional[str] = ""
    exchange_rate: Optional[str] = "1.0"
    client_email: Optional[str] = ""
    calculator_mode: Optional[CalculatorMode] = "initial"
    withholding_taxes: list = field(default_factory=list)
    template_id: Optional[str] = None
    public_notes: Optional[str] = ""


@dataclass
class EmailBody(BaseDataClass):
    to: str
    subject: str
    message: str
    store_to: Optional[bool] = False
    cc: Optional[str] = ""
    bcc: Optional[str] = ""
    attach_pdf: Optional[bool] = False
    sender_name: Optional[str] = ""
    attachments: list = field(default_factory=list)
