import uuid

import pytest
from xmlrpc.client import ServerProxy

from config import URL, DB, USER, PASSWORD

@pytest.fixture(scope="session")
def base_url():
    return URL

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    api = playwright.request.new_context(base_url=URL)
    api.post("/web/session/authenticate", data={"params": {"db": DB, "login": USER, "password": PASSWORD}})

    return {**browser_context_args, "storage_state": api.storage_state()}

@pytest.fixture(scope="session")
def odoo():
    uid = ServerProxy(f"{URL}/xmlrpc/2/common").authenticate(DB, USER, PASSWORD, {})
    models = ServerProxy(f"{URL}/xmlrpc/2/object")

    def call(model, method, *args):
        return models.execute_kw(DB, uid, PASSWORD, model, method, list(args))
    return call

@pytest.fixture
def customer(odoo):
    name = f"QA Customer {uuid.uuid4().hex[:6]}"
    odoo("res.partner", "create", {"name": name})
    return name


@pytest.fixture
def product(odoo):
    name = f"QA Product {uuid.uuid4().hex[:6]}"
    tax = odoo("account.tax", "search", [["type_tax_use", "=", "sale"],["amount", "=", 15]])
    odoo("product.product", "create", {"name": name, "list_price": 100, "taxes_id": tax, "invoice_policy": "order"})
    return name