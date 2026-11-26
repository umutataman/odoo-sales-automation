# Test Plan: Odoo 18 Sales, Quote-to-Cash

## 1. Scope

**Under test:** quotation → sales order → invoice → payment (Odoo 18, Sales and Invoicing, demo data). This is the flow that turns a deal into money, so a bug here costs money.

**Out of scope:** inventory, email, PDF layout, multi-currency, performance, security.

## 2. Requirements

| ID | Requirement | Test cases |
|---|---|---|
| BR-01 | Totals are correct: quantity × price, plus 15% tax. | TC-01, TC-03 |
| BR-02 | A confirmed order can be invoiced and paid. | TC-01, TC-05 |
| BR-03 | Payment status matches the payment: full gives *Paid*. | TC-01, TC-04 |
| BR-04 | Every quotation has a customer. | TC-02 |

## 3. Strategy

- **Risk-based:** the money path (TC-01) and bad-data blocking (TC-02) will be automated first.
- **API + UI:** test data is created through the API, the flow runs in the UI, and the result is checked through the API.
- **Own data per test:** a unique customer and product per test, so tests run in parallel.
- **Page Object Model:** tests call business actions (new quotation, confirm, invoice, pay) and only check results. Locators prefer Odoo's roles and labels (the Customer combobox, the status bar), then stable field names.
- **Reliable:** no sleeps, only auto-waiting checks. Trace and screenshot are kept on failure.
- **Environments:** the same tests run on local, test or stage. Settings come from a `.env.<environment>` file, chosen with `TEST_ENV`. Passwords for shared environments come from CI secrets, never from code.
- **CI:** every push and nightly. Manual cases run before each release.

## 4. Test cases

**TC-01 · Quotation to paid invoice · P1 · BR-01 to BR-03 · Selected for automation**

| Step | Expected result |
|---|---|
| 1. New quotation: test customer, test product ($100, 15% tax), quantity 3 | Untaxed $300.00, Tax $45.00, Total $345.00 |
| 2. Click **Confirm** | Status *Sales Order* |
| 3. **Create Invoice** → **Create Draft** → **Confirm** | Status *Posted* |
| 4. **Pay** → **Create Payment** | *Paid* ribbon |
| 5. Check the invoice through the API | Payment state *paid*, total 345 |

**TC-02 · Quotation needs a customer · P2 · BR-04 · Selected for automation**

| Step | Expected result |
|---|---|
| 1. New quotation with the test product, no customer | — |
| 2. Click **Save** | "Invalid fields: Customer"; Customer field marked invalid |
| 3. Check through the API | No order with the test product exists |

**Manual cases (automate later)**

| ID | Case | Expected result |
|---|---|---|
| TC-03 | Tax rounding: 3 × $33.33 | Tax $15.00, Total $114.99 |
| TC-04 | Partial payment: pay $100 of $230 | *Partial*, $130.00 left |
| TC-05 | Confirm an order with no lines | Should be blocked. **Fails:** see DEF-001 |

## 5. Defect: DEF-001

**A sales order can be confirmed with no order lines** · Medium · found by TC-05

- **Steps:** New quotation, select a customer, add no lines, click **Confirm**.
- **Expected:** blocked with a message.
- **Actual:** confirmed with a $0.00 total, and **Create Invoice** is still offered.
- **Next:** the product owner decides: fix it, or change the requirement.
