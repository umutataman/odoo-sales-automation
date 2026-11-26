from playwright.sync_api import Page, Locator


class SalesPage:
    def __init__(self, page: Page):
        self.page = page
        self.customer = page.get_by_role("combobox", name="Customer")
        self.order_line = page.locator(".o_selected_row")
        self.totals = page.locator("[name='tax_totals']")
        self.status = page.get_by_role("radio", checked=True)
        self.paid_ribbon = page.locator(".o_widget_web_ribbon")
        self.notification = page.locator(".o_notification")
        self.customer_field = page.locator("div[name='partner_id']")


    def click(self, name: str):
        '''Buttons by their exact visible label that user sees on the page.'''
        self.page.get_by_role("button", name=name, exact=True).click()

    def pick(self, field: Locator, value: str):
        field.fill(value)
        self.page.get_by_role("option", name=value, exact=True).click()

    def new_quotation(self, product:str, quantity:int, customer:str = None):
        self.page.goto("/odoo/sales/new")
        if customer:
            self.pick(self.customer, customer)
        self.click("Add a product")
        self.pick(self.order_line.get_by_placeholder("Search a product"), product)
        self.order_line.locator("[name=product_uom_qty] input").fill(str(quantity))
        self.order_line.locator("[name=price_unit] input").click()

    def confirm(self):
        self.click("Confirm")

    def create_and_post_invoice(self):
        self.click("Create Invoice")
        self.click("Create Draft")
        self.click("Confirm")

    def register_payment(self):
        self.click("Pay")
        self.click("Create Payment")

    def save(self):
        self.click("Save manually")