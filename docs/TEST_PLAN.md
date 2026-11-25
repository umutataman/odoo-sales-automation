# Test Plan: Odoo 18 Sales, Quote-to-Cash

## 1. Scope

**Process under test:** quotation → sales order → invoice → payment in Odoo 18 (Sales and Invoicing, demo data).

This is the flow that turns a deal into money. A defect here means wrong totals, missed invoices or unrecorded payments.

- **In scope:** quotation validation, price and tax totals, order confirmation, invoicing, payment status.
- **Out of scope:** inventory, email, PDF layout, multi-currency, performance, security.
- **Next scope:** credit notes, down payments, pricelists, user-role permissions.

## 2. Requirements and traceability

| ID | Requirement | Test cases | Automate first |
|---|---|---|---|
| BR-01 | Totals are correct: quantity × price, minus discount, plus tax. | TC-01, TC-03, TC-04 | TC-01 |
| BR-02 | A confirmed quotation becomes a sales order that can be invoiced. | TC-01, TC-08 | TC-01 |
| BR-03 | An order is invoiced once, for the ordered quantity. | TC-01, TC-06 | TC-01 |
| BR-04 | Payment status matches payments: full gives *Paid*, partial gives *Partial*. | TC-01, TC-05 | TC-01 |
| BR-05 | Every quotation has a customer. | TC-02 | TC-02 |
| BR-06 | A confirmed order cannot be deleted. | TC-07 | No |

## 3. Strategy

- **Risk-based priority:** P1 is money and the main flow, P2 is validation, P3 is edge cases.
- **API + UI:** test data is created through the API, the behaviour runs through the UI, and the result is checked again through the API.
- **Own data per test:** each test creates a unique customer and a $100 product with 15% tax, so tests run in parallel and in any order.
- **Page Object Model:** selectors live only in page classes.
- **No sleeps:** only Playwright's auto-waiting assertions.
- **Failure evidence:** trace, screenshot and HTML report.
- **Tool:** Playwright for Python with pytest. It auto-waits, has a trace viewer, and Python is my strongest language.

## 4. Test cycles

| When | What runs |
|---|---|
| Every push and pull request | Automated tests, in parallel |
| Nightly | Automated tests |
| Each release | Automated tests plus the manual cases |

## 5. Test cases

### TC-01 · Quotation to paid invoice · P1 · BR-01 to BR-04 · Automate first

| Step | Action | Expected result |
|---|---|---|
| 1 | Open a new quotation | The form opens |
| 2 | Select the test customer | Customer is set |
| 3 | Add the test product, quantity 3 | One order line |
| 4 | Check totals | Untaxed $300.00, Tax $45.00, Total $345.00 |
| 5 | Click **Confirm** | Status is *Sales Order* |
| 6 | **Create Invoice** → **Create Draft** | A draft invoice opens |
| 7 | Click **Confirm** on the invoice | Status is *Posted* |
| 8 | **Pay** → **Create Payment** | *Paid* ribbon |
| 9 | Check through the API | Order is `sale` and `invoiced`; invoice is `paid`, total 345, nothing left to pay |

### TC-02 · Quotation needs a customer · P2 · BR-05 · Automate first

| Step | Action | Expected result |
|---|---|---|
| 1 | Open a new quotation | The form opens |
| 2 | Add the test product, leave the customer empty | One order line |
| 3 | Click **Save** | The save is blocked |
| 4 | Check the error | "Invalid fields: Customer" message; Customer field marked invalid |
| 5 | Check through the API | No sales order with the test product exists |

### Manual cases (automation candidates later)

| ID | Title | Pri | Expected result |
|---|---|---|---|
| TC-03 | 10% line discount, qty 1 | P1 | Total $103.50 |
| TC-04 | Tax rounding: 3 × $33.33 | P1 | Tax $15.00, Total $114.99 |
| TC-05 | Partial payment: pay $100 of $230 | P1 | *Partial*, $130.00 left |
| TC-06 | Return to a fully invoiced order | P1 | **Create Invoice** is gone |
| TC-07 | Delete a confirmed order | P2 | Blocked with an error |
| TC-08 | Confirm with no order lines | P2 | **Fails:** the order is confirmed. See DEF-001 |

## 6. Why TC-01 and TC-02 are automated first

- **TC-01** covers the whole money path and four of six requirements in one test. If it fails, the business cannot bill. It is the smoke test for every change.
- **TC-02** is the negative side: bad data must be stopped at the door.
- **Next:** TC-03 and TC-04 become one parametrized test.

## 7. Defect report

**DEF-001 · A sales order can be confirmed with no order lines** · Medium / P2 · found by TC-08

1. Sales → New quotation, select a customer, add no lines.
2. Click **Confirm**.

- **Expected:** blocked, for example "Add at least one product line".
- **Actual:** the order is confirmed with a $0.00 total, and **Create Invoice** is still offered.
- **Impact:** empty orders count in sales reports.
- **Note:** this is standard Odoo behaviour, so the product owner decides: fix it, or update the requirement.

## 8. Exit criteria

All P1 cases pass, every failure has a defect with evidence, and no P1 defect is open.
