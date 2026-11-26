# Odoo Sales Automation

UI tests for the Odoo 18 Quote-to-Cash flow: quotation → sales order → invoice → payment.

Built with Playwright, Python, pytest and the Page Object Model. CI runs on GitHub Actions.

- **Video walkthrough:** https://youtu.be/r2_qj2jpmfM
- **Test plan:** [docs/TEST_PLAN.md](docs/TEST_PLAN.md)

## Tests

- **TC-01:** quotation to paid invoice
- **TC-02:** a quotation cannot be saved without a customer

## Run locally

Start the Odoo test environment (Docker):

```bash
./scripts/setup_odoo.sh
```

Install and run:

```bash
uv sync
uv run playwright install chromium
uv run pytest -n auto
```

Settings come from `.env.<environment>`, chosen with `TEST_ENV` (default: `local`).
