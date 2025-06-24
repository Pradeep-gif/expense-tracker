import streamlit as st
import csv
import os
import json
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Set page config
st.set_page_config(page_title="Expense Tracker", layout="centered")

# CSV file path
csv_file = "data/expenses.csv"

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_dict = json.loads(st.secrets["GOOGLE_SHEETS_CREDS"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open("ExpenseTrackerData").sheet1

# App title
st.title("💰 Expense Tracker")

# Form for expense entry
with st.form("expense_form"):
    date = st.date_input("Date")
    category = st.selectbox("Category", ["Food", "Transport", "Entertainment", "Utilities", "Other"])
    amount = st.number_input("Amount", min_value=0.01, step=0.01)
    description = st.text_input("Description")

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        # Save to CSV
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        with open(csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, category, amount, description])

        # Save to Google Sheet
        sheet.append_row([str(date), category, amount, description])

        st.success("✅ Expense added!")

# Display saved expenses
if os.path.exists(csv_file):
    st.subheader("📊 Expense History")
    with open(csv_file, "r") as f:
