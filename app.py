import streamlit as st
import pandas as pd

st.set_page_config(page_title="Nayanam Dashboard", layout="wide")

st.title("📊 Nayanam Analytics Dashboard")

import os

# ===============================
# AUTO LOAD DATA (ROBUST VERSION)
# ===============================
file_path = "orders.xlsx"

if not os.path.exists(file_path):
    st.error("❌ orders.xlsx not found in deployed app")
    st.stop()

df = pd.read_excel(file_path)
df.columns = df.columns.str.strip()

st.success("✅ Data Loaded Successfully")

# ===============================
# CLEAN DATA
# ===============================
if "Grand Total (₹)" in df.columns:
    df = df.rename(columns={"Grand Total (₹)": "Total"})

df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

if "Delivery Boy" in df.columns:
    df["Delivery Boy"] = df["Delivery Boy"].fillna("Unknown")

# ===============================
# SIDEBAR FILTERS
# ===============================
st.sidebar.header("🔍 Filters")

# Payment Filter
if "Payment Type" in df.columns:
    payment_filter = st.sidebar.multiselect(
        "Payment Type",
        options=df["Payment Type"].dropna().unique()
    )
    if payment_filter:
        df = df[df["Payment Type"].isin(payment_filter)]

# Status Filter
if "Status" in df.columns:
    status_filter = st.sidebar.multiselect(
        "Order Status",
        options=df["Status"].dropna().unique()
    )
    if status_filter:
        df = df[df["Status"].isin(status_filter)]

# ===============================
# SUMMARY
# ===============================
st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹{df['Total'].sum():,.0f}")
col2.metric("🧾 Orders", len(df))
col3.metric("📊 Avg Order", f"₹{df['Total'].mean():.2f}")

# ===============================
# PAYMENT ANALYSIS
# ===============================
if "Payment Type" in df.columns:
    st.subheader("💳 Payment Split")
    pay = df.groupby("Payment Type")["Total"].sum()
    st.bar_chart(pay)

# ===============================
# DELIVERY ANALYSIS
# ===============================
if "Delivery Boy" in df.columns:
    st.subheader("🚴 Delivery Performance")

    delivery = (
        df.groupby("Delivery Boy")["Total"]
        .agg(["sum", "count"])
        .rename(columns={"sum": "Sales", "count": "Orders"})
        .sort_values(by="Sales", ascending=False)
    )

    st.dataframe(delivery)

# ===============================
# ORDER TYPE
# ===============================
if "Order Type" in df.columns:
    st.subheader("🍽️ Order Type")
    order_type = df["Order Type"].value_counts()
    st.bar_chart(order_type)

# ===============================
# STATUS
# ===============================
if "Status" in df.columns:
    st.subheader("📦 Order Status")
    status = df["Status"].value_counts()
    st.bar_chart(status)

# ===============================
# FINANCIALS
# ===============================
st.subheader("💸 Financials")

col4, col5, col6 = st.columns(3)

if "Total Discount (₹)" in df.columns:
    col4.metric("Discount", f"₹{df['Total Discount (₹)'].sum():,.0f}")

if "Total Tax (₹)" in df.columns:
    col5.metric("Tax", f"₹{df['Total Tax (₹)'].sum():,.0f}")

if "Delivery Charge (₹)" in df.columns and "Container Charge (₹)" in df.columns:
    charges = df["Delivery Charge (₹)"].sum() + df["Container Charge (₹)"].sum()
    col6.metric("Charges", f"₹{charges:,.0f}")

# ===============================
# QUICK QUERY
# ===============================
st.subheader("🤖 Quick Query")

query = st.text_input("Try: total / delivery / payment")

if query:
    q = query.lower()

    if "total" in q:
        st.success(f"₹{df['Total'].sum():,.0f}")

    elif "delivery" in q:
        st.dataframe(delivery)

    elif "payment" in q:
        st.write(pay)

    else:
        st.warning("Try: total / delivery / payment")

# ===============================
# EXPORT
# ===============================
if st.button("📤 Export Data"):
    df.to_excel("output.xlsx", index=False)
    st.success("Downloaded as output.xlsx")