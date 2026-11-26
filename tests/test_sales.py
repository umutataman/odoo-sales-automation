from playwright.sync_api import expect
import pytest

from pages.sales_page import SalesPage

@pytest.mark.smoke
def test_quotation_to_paid_invoice(page, customer, product, odoo):
    # Step 1: Create a new quotation with 3 units of the product for the customer
    sales = SalesPage(page)
    sales.new_quotation(product, 3, customer)
    expect(sales.totals).to_contain_text("$ 300.00")
    expect(sales.totals).to_contain_text("$ 45.00")
    expect(sales.totals).to_contain_text("$ 345.00")


    # Step 2-4: Confirm the quotation, create and post the invoice, and register the payment
    sales.confirm()
    expect(sales.status).to_contain_text("Sales Order")
    sales.create_and_post_invoice()
    expect(sales.status).to_contain_text("Posted")
    sales.register_payment()
    expect(sales.paid_ribbon).to_contain_text("Paid")

    # Step 5: DB verification of the screen
    [invoice] = odoo("account.move", "search_read", [["invoice_line_ids.product_id.name", "=", product]],
                     ["payment_state", "amount_total"])
    assert (invoice["payment_state"], invoice["amount_total"]) == ("paid", 345)

@pytest.mark.negative
def test_quotation_requires_customer(page, product, odoo):
    sales = SalesPage(page)
    # Step 1-2: Create a new quotation with 1 unit of the product without a customer
    sales.new_quotation(product, 1)
    sales.save()

    expect(sales.notification).to_contain_text("Invalid fields: Customer")
    expect(sales.customer_field).to_contain_class("o_field_invalid")

    # Step 3: assert is not created in DB
    assert odoo("sale.order", "search_count", [["order_line.product_id.name", "=", product]]) == 0