from httpx import Auth


class ElorusAuthentication(Auth):
    def __init__(self, token: str, elorus_organization_id: str, is_demo: bool = False):
        self.token = token
        self.elorus_organization_id = elorus_organization_id
        self.is_demo = is_demo

    def auth_flow(self, request):
        request.headers["Authorization"] = f"Token {self.token}"
        request.headers["X-Elorus-Organization"] = self.elorus_organization_id
        if self.is_demo:
            request.headers["X-Elorus-Demo"] = "true"
        yield request
