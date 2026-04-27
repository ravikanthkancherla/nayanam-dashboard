import streamlit as st
import pandas as pd

st.title("📊 Nayanam Analytics Dashboard")

uploaded_file = st.file_uploader("Upload Order Report", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
# --- CLEAN ---
df.columns = df.columns.str.strip()

if "Grand Total (₹)" in df.columns:
    df = df.rename(columns={"Grand Total (₹)": "Total"})

# --- DATE FIX ---
if "Created" in df.columns:
    df["Created"] = pd.to_datetime(df["Created"], errors="coerce", dayfirst=True)
st.sidebar.header("🔍 Filters")

# Date filter
if "Created" in df.columns:
    min_date = df["Created"].min()
    max_date = df["Created"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        [min_date, max_date]
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df["Created"].dt.date >= start_date) & (df["Created"].dt.date <= end_date)]

# Payment filter
if "Payment Type" in df.columns:
    payment_filter = st.sidebar.multiselect(
        "Payment Type",
        options=df["Payment Type"].dropna().unique()
    )
    if payment_filter:
        df = df[df["Payment Type"].isin(payment_filter)]

# Status filter
if "Status" in df.columns:
    status_filter = st.sidebar.multiselect(
        "Order Status",
        options=df["Status"].dropna().unique()
    )
    if status_filter:
        df = df[df["Status"].isin(status_filter)]
item_file = st.file_uploader("Upload Item Report (Optional)", type=["xlsx"])
if item_file:
    items = pd.read_excel(item_file)
    items.columns = items.columns.str.strip()

    items = items.rename(columns={
        "Quantity": "Qty",
        "Total Amount": "Total"
    })

    st.subheader("🍽️ Item Analysis")

    top_items = items.groupby("Item Name")["Qty"].sum().sort_values(ascending=False).head(5)
    st.write("Top Items")
    st.bar_chart(top_items)

    low_items = items.groupby("Item Name")["Qty"].sum().sort_values().head(5)
    st.write("Low Items")
    st.bar_chart(low_items)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"₹{df['Total'].sum():,.0f}")
col2.metric("🧾 Orders", len(df))
col3.metric("📊 Avg Order", f"₹{df['Total'].mean():.2f}")

if "Created" in df.columns:
    st.subheader("📈 Sales Trend")

    trend = df.groupby(df["Created"].dt.date)["Total"].sum()
    st.line_chart(trend)
if "Order Type" in df.columns:
    st.subheader("🍽️ Order Type Split")
    order_type = df["Order Type"].value_counts()
    st.bar_chart(order_type)

    df.columns = df.columns.str.strip()

    if "Grand Total (₹)" in df.columns:
        df = df.rename(columns={"Grand Total (₹)": "Total"})

    # Summary
    st.subheader("📊 Summary")
    total_sales = df["Total"].sum()
    total_orders = len(df)
    avg_order = df["Total"].mean()

    st.metric("Total Sales", f"₹{total_sales:,.0f}")
    st.metric("Total Orders", total_orders)
    st.metric("Avg Order Value", f"₹{avg_order:.2f}")

    # Payment Split
    if "Payment Type" in df.columns:
        st.subheader("💳 Payment Split")
        pay = df.groupby("Payment Type")["Total"].sum()
        st.bar_chart(pay)

    # Ask Question
    st.subheader("🤖 Ask a Question")
    query = st.text_input("Ask anything (e.g., total, payment, status, delivery boy)")

if query:
    query = query.lower()

    if "total" in query:
        st.success(f"Total Sales: ₹{total_sales:,.0f}")

    elif "orders" in query:
        st.success(f"Total Orders: {total_orders}")

    elif "average" in query:
        st.success(f"Average Order Value: ₹{avg_order:.2f}")

    elif "payment" in query:
        if "Payment Type" in df.columns:
            pay = df.groupby("Payment Type")["Total"].sum()
            st.write(pay)

    elif "status" in query:
        if "Status" in df.columns:
            st.write(df["Status"].value_counts())

    elif "delivery" in query:
        if "Delivery Boy" in df.columns:
            st.write(df["Delivery Boy"].value_counts())

    elif "order type" in query:
        if "Order Type" in df.columns:
            st.write(df["Order Type"].value_counts())

    elif "discount" in query:
        if "Total Discount (₹)" in df.columns:
            st.write(f"Total Discount: ₹{df['Total Discount (₹)'].sum():,.0f}")

    elif "show data" in query:
        st.dataframe(df)

    else:
        st.warning("Try: total / orders / payment / status / delivery / order type / discount / show data")

import urllib.parse

st.subheader("📤 Send Report to WhatsApp")

# Generate message
message = f"""
📊 NAYANAM DAILY REPORT

💰 Total Sales: ₹{df['Total'].sum():,.0f}
🧾 Orders: {len(df)}
📊 Avg Order: ₹{df['Total'].mean():.2f}
"""

# Payment split
if "Payment Type" in df.columns:
    pay = df.groupby("Payment Type")["Total"].sum()
    message += "\n💳 Payment Split:\n" + pay.to_string()

# Encode message
encoded_message = urllib.parse.quote(message)

# 👉 Replace number
phone_number = "91XXXXXXXXXX"

whatsapp_url = f"https://wa.me/{phone_number}?text={encoded_message}"

st.link_button("📲 Send to WhatsApp", whatsapp_url)