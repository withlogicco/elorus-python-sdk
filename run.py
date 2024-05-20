from elorus.client import Client

client = Client(
    api_key="dab7b293fcb8b17ca2c1a36d855bfa684c35b03e",
    elorus_organization_id="301341342796613934",
    is_demo=True,
)

contacts = client.contacts.list()
print(contacts)
