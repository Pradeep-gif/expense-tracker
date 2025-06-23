import streamlit as st
import pandas as pd
import datetime
import os

st.title("💸 Expense Tracker")
st.write("Track your daily expenses easily.")

# CSV file path
csv_file = "data/expenses.csv"

# ------------------ INPUT FORM ------------------ #
with st.form("expense_form"):
    date = st.date_input("Date", datetime.date.today())
    category = st.selectbox("Category", ["Food", "Travel", "Bills", "Other"])
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.5)
    note = st.text_input("Note")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_data = pd.DataFrame([[date, category, amount, note]],
                                columns=["Date", "Category", "Amount", "Note"])
        
        # Create folder if not exists
        os.makedirs("data", exist_ok=True)

        # Save to CSV
        if os.path.exists(csv_file):
            new_data.to_csv(csv_file, mode='a', header=False, index=False)
        else:
            new_data.to_csv(csv_file, index=False)
        
        st.success("✅ Expense added successfully!")

# ------------------ SHOW TABLE ------------------ #
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    st.subheader("📋 Your Expenses")
    st.dataframe(df)
