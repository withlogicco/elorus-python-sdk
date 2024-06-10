from dataclasses import asdict
from typing import Optional

import httpx

from elorus.auth import ElorusAuthentication
from elorus.exceptions import (
    AuthenticationError,
    AuthorizationError,
    BadRequestError,
    Error,
    ThrottlingError,
)
from elorus.models import Contact, EmailBody, Invoice


class Client:
    def __init__(
        self,
        api_key: str,
        elorus_organization_id: str,
        is_demo: bool = False,
        base_url: Optional[str] = "https://api.elorus.com",
        api_version: Optional[str] = "v1.1",
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.elorus_organization_id = elorus_organization_id
        self.is_demo = is_demo
        self.api_version = api_version

        self.contacts = Contacts(self)
        self.invoices = Invoices(self)

    def _get_auth(self):
        return ElorusAuthentication(
            token=self.api_key,
            elorus_organization_id=self.elorus_organization_id,
            is_demo=self.is_demo,
        )

    def handle_file_download(self, response):
        content_disposition = response.headers.get("Content-Disposition", "")
        if "filename=" not in content_disposition:
            raise ValueError("No filename found in Content-Disposition header")
        filename_kv = content_disposition.split("filename=")
        if len(filename_kv) < 2:
            raise ValueError("Invalid Content-Disposition header format")
        filename = filename_kv[1]
        return filename, response.content

    def _handle_response(self, response: httpx.Response):
        if response.headers.get("Content-Type", "").lower() == "application/pdf":
            return self.handle_file_download(response)

        if response.status_code == 204:
            return response.text

        message = response.json()

        if response.status_code == 401:
            raise AuthenticationError(
                message=message,
                response=response,
            )

        if response.status_code == 403:
            raise AuthorizationError(
                message=message,
                response=response,
            )

        if response.status_code == 429:
            raise ThrottlingError(
                message=message,
                response=response,
            )

        if response.status_code == 400:
            raise BadRequestError(
                message=message,
                response=response,
            )

        if response.status_code >= 500:
            raise Error(
                message=message,
                response=response,
            )

        try:
            response.raise_for_status()
            return message
        except:
            error = f"{response.text}"
            content_type = response.headers.get("Content-Type", "").lower()
            if content_type == "application/json":
                resp = response.json()
                error_message_keys = ("message", "msg", "detail")
                error_message = next(
                    (resp[key] for key in error_message_keys if key in resp), None
                )
                if error_message:
                    error = f"Message: {error_message} , Error details: {resp.get('errors')}, {resp.get('data')}"
                    raise Error(error, response)

            raise Error(error, response)

    def _handle_request(
        self, method: str, path: str, payload: Optional[dict] = None, **kwargs
    ) -> httpx.Response:
        auth = self._get_auth()
        url = f"{self.base_url}/{self.api_version}/{path}"
        with httpx.Client(auth=auth) as client:
            response = client.request(method, url, json=payload, **kwargs)
            return self._handle_response(response)


class SubClient(Client):
    client: Client

    def __init__(self, client: Client):
        self.client = client


class Contacts(SubClient):

    def list(self, **params):
        return self.client._handle_request("GET", "contacts/", params=params)

    def create(self, contact: Contact):
        payload = asdict(contact)
        return self.client._handle_request("POST", "contacts/", payload=payload)

    def get(self, contact_id: str):
        return self.client._handle_request("GET", f"contacts/{contact_id}/")

    def update(self, contact_id: str, contact: Contact):
        payload = asdict(contact)
        return self.client._handle_request(
            "PUT", f"contacts/{contact_id}/", payload=payload
        )

    def delete(self, contact_id: str):
        return self.client._handle_request("DELETE", f"contacts/{contact_id}/")


class Invoices(SubClient):

    def list(self, **params):
        return self.client._handle_request("GET", "invoices/", params=params)

    def create(self, invoice: Invoice):
        payload = invoice.clean_dict()
        return self.client._handle_request("POST", "invoices/", payload=payload)

    def get(self, invoice_id: str):
        return self.client._handle_request("GET", f"invoices/{invoice_id}/")

    def update(self, invoice_id: str, invoice: Invoice):
        payload = invoice.clean_dict()
        return self.client._handle_request(
            "PUT", f"invoices/{invoice_id}/", payload=payload
        )

    def partial_update(self, invoice_id: str, invoice: Invoice):
        payload = invoice.clean_dict()
        return self.client._handle_request(
            "PATCH", f"invoices/{invoice_id}/", payload=payload
        )

    def delete(self, invoice_id: str):
        return self.client._handle_request("DELETE", f"invoices/{invoice_id}/")

    def post_email(self, invoice_id: str, email_body: EmailBody):
        payload = email_body.clean_dict()
        return self.client._handle_request(
            "POST", f"invoices/{invoice_id}/email/", payload=payload
        )

    def get_email(self, invoice_id: str):
        return self.client._handle_request("GET", f"invoices/{invoice_id}/email/")

    def get_pdf(self, invoice_id: str):
        return self.client._handle_request("GET", f"invoices/{invoice_id}/pdf/")

    def mark_void(self, invoice_id: str, is_void: bool = True):
        payload = {"is_void": is_void}
        return self.client._handle_request(
            "POST", f"invoices/{invoice_id}/void/", payload=payload
        )
