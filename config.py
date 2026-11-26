import os

from dotenv import load_dotenv

TEST_ENV = os.getenv("TEST_ENV", "local")

load_dotenv(f".env.{TEST_ENV}")

URL = os.getenv("ODOO_URL")
DB = os.getenv("ODOO_DB")
USER = os.getenv("ODOO_USER")
PASSWORD = os.getenv("ODOO_PASSWORD")