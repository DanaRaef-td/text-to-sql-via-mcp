ACCOUNT_SCHEMA = """
Tables in the iScore Teradata Vantage database:

dim_customer(customer_id, national_id, first_name, last_name, date_of_birth, address, employer, file_since_date)
dim_tradeline(tradeline_id, customer_id, lender_id, account_type_id, open_date, close_date, credit_limit_or_loan_amount, outstanding_balance, status, available_credit)
dim_lender(lender_id, lender_name, lender_type, is_bureau_member)
dim_account_type(account_type_id, account_type_name, credit_category)
dim_date(date_key, full_date, day_of_week, day_of_month, month_num, month_name, quarter, year, is_weekend, is_score_update_day)
fact_credit_score(score_id, customer_id, date_key, score_value)
fact_score_factors(score_id, factor_name, weight_pct, factor_score_contribution, impact)
fact_payment_history(tradeline_id, date_key, payment_status, amount_due, amount_paid)
fact_inquiries(inquiry_id, customer_id, lender_id, date_key, inquiry_type)
fact_self_inquiries(self_inquiry_id, customer_id, date_key, channel, purpose)
fact_disputes(dispute_id, customer_id, tradeline_id, reason_code, filed_date, dispute_channel, status, resolution_date, resolution_notes)
fact_legal_actions(legal_action_id, customer_id, tradeline_id, plaintiff_lender_id, case_number, court_name, filing_date, case_status, judgment_amount, judgment_date)
fact_collections(collection_id, account_id, customer_id, collection_agency_name, original_creditor_lender_id, amount_owed, date_placed, status)
"""

ACCOUNT_SQL_PROMPT = """\
You generate Teradata SQL for a read-only question answering program.

Return exactly one SELECT query and no Markdown or explanation.
Use only this schema:
{schema}

Never use SELECT *.
Never use LIMIT you can use Qualify row_number() over (order by ...) instead.
Do not modify data or database objects.
Limit detailed row results to a reasonable amount.
Question: {question}
SQL:
"""

ACCOUNT_ANSWER_PROMPT = """\
Answer the user's question using only the database results below.
If the results do not answer it, say that the data is insufficient.
Do not invent facts.

Question: {question}
Database results: {rows}
"""