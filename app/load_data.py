from pathlib import Path
import os

import pandas as pd
from dotenv import load_dotenv
from teradataml import copy_to_sql, create_context

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env", override=True)

WORKBOOK = Path("data/iscore_synthetic_data.xlsx")
TABLES = [
    "dim_date",
    "dim_customer",
    "dim_lender",
    "dim_account_type",
    "fact_credit_score",
    "fact_score_factors",
    "fact_payment_history",
    "fact_inquiries",
    "fact_self_inquiries",
    "fact_disputes",
    "fact_legal_actions",
    "fact_collections",
]

def main():
    print("Connecting to Vantage...")
    create_context(
        host=os.environ["TD_HOST"],
        username=os.environ["TD_USER"],
        password=os.environ["TD_PASSWORD"],
    )
    print("Connected to Vantage Successfully...")

    print(f"Loading data from {WORKBOOK}...")
    for table_name in TABLES:
        rows = pd.read_excel(WORKBOOK, sheet_name=table_name)

        copy_to_sql(
            df=rows,
            table_name=table_name,
            if_exists="replace",
            index=False,
        )

        print(f"Loaded {table_name}: {len(rows)} rows")

if __name__ == "__main__":
    main()