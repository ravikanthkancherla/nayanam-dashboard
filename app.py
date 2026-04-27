import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Nayanam Dashboard", layout="wide")

st.title("📊 Nayanam Analytics Dashboard")

# ===============================
# LOAD CSV (STABLE VERSION)
# ===============================
file_path = "orders.csv"

if not os.path.exists(file_path):
    st.error("❌ orders.csv not found in repo")
    st.stop()

df = pd.read_csv(file_path)
df.columns = df.columns.str.strip()

# ===============================
# CLEAN DATA
# ===============================
if "Grand Total (₹)" in df.columns:
    df = df.rename(columns={"Grand Total (₹)": "Total"})

df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

if "Delivery Boy" in df.columns:
    df["Delivery Boy"] = df["Delivery Boy"].fillna("Unknown")

# ===============================
# SUMMARY
# ===============================
st.subheader("📊 Summary")

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹{df['Total'].sum():,.0f}")
col2.metric("🧾 Orders", len(df))
col3.metric("📊 Avg Order", f"₹{df['Total'].mean():.2f}")

# ===============================
# PAYMENT
# ===============================
if "Payment Type" in df.columns:
    st.subheader("💳 Payment Split")
    pay = df.groupby("Payment Type")["Total"].sum()
    st.bar_chart(pay)

# ===============================
# DELIVERY
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
# STATUS
# ===============================
if "Status" in df.columns:
    st.subheader("📦 Order Status")
    st.bar_chart(df["Status"].value_counts())

# ===============================
# EXPORT
# ===============================
if st.button("📤 Export Data"):
    df.to_csv("output.csv", index=False)
    st.success("Downloaded as output.csv")