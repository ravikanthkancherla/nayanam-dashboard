import pandas as pd
import gradio as gr
import plotly.express as px
from datetime import datetime, timedelta

# ===============================
# PASSWORD
# ===============================
PASSWORD = "nayanam123"

# ===============================
# LOAD DATA
# ===============================
df = pd.read_csv("orders.csv")
df.columns = df.columns.str.strip()

if "Grand Total (₹)" in df.columns:
    df = df.rename(columns={"Grand Total (₹)": "Total"})

df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

if "Delivery Boy" in df.columns:
    df["Delivery Boy"] = df["Delivery Boy"].fillna("Unknown")

# Date column
if "Created" in df.columns:
    df["Created"] = pd.to_datetime(df["Created"], errors="coerce", dayfirst=True)

# ===============================
# FILTER FUNCTION
# ===============================
def apply_date_filter(data, date_filter):

    if "Created" not in data.columns:
        return data

    today = datetime.now().date()

    if date_filter == "Today":
        return data[data["Created"].dt.date == today]

    elif date_filter == "Yesterday":
        y = today - timedelta(days=1)
        return data[data["Created"].dt.date == y]

    elif date_filter == "This Month":
        return data[data["Created"].dt.month == today.month]

    return data

# ===============================
# DASHBOARD FUNCTION
# ===============================
def dashboard(pwd, date_filter, payment_filter, delivery_filter):

    # Login check
    if pwd != PASSWORD:
        return "❌ Wrong Password", "", "", None, None, None

    data = df.copy()

    # Apply date filter
    data = apply_date_filter(data, date_filter)

    # Apply filters
    if payment_filter:
        data = data[data["Payment Type"].isin(payment_filter)]

    if delivery_filter:
        data = data[data["Delivery Boy"].isin(delivery_filter)]

    # KPIs
    total_sales = f"₹{data['Total'].sum():,.0f}"
    total_orders = len(data)
    avg_order = f"₹{data['Total'].mean():.2f}"

    # Payment Chart
    if "Payment Type" in data.columns:
        pay = data.groupby("Payment Type")["Total"].sum().reset_index()
        fig_payment = px.bar(pay, x="Payment Type", y="Total", title="Payment Split")
    else:
        fig_payment = None

    # Delivery Chart
    delivery = (
        data.groupby("Delivery Boy")["Total"]
        .sum()
        .reset_index()
        .sort_values(by="Total", ascending=False)
    )

    fig_delivery = px.bar(delivery, x="Delivery Boy", y="Total", title="Delivery Performance")

    return total_sales, total_orders, avg_order, fig_payment, fig_delivery, data.head(50)

# ===============================
# FILTER OPTIONS
# ===============================
payment_options = df["Payment Type"].dropna().unique().tolist() if "Payment Type" in df.columns else []
delivery_options = df["Delivery Boy"].dropna().unique().tolist() if "Delivery Boy" in df.columns else []

# ===============================
# UI
# ===============================
with gr.Blocks(title="Nayanam Dashboard") as app:

    gr.Markdown("# 📊 Nayanam Investor Dashboard")

    pwd = gr.Textbox(label="🔐 Enter Password", type="password")

    date_filter = gr.Dropdown(
        ["All", "Today", "Yesterday", "This Month"],
        value="All",
        label="📅 Date Filter"
    )

    with gr.Row():
        payment_filter = gr.Dropdown(payment_options, multiselect=True, label="Payment Type")
        delivery_filter = gr.Dropdown(delivery_options, multiselect=True, label="Delivery Boy")

    run_btn = gr.Button("🚀 Load Dashboard")

    with gr.Row():
        total_sales = gr.Textbox(label="💰 Total Sales")
        total_orders = gr.Textbox(label="🧾 Orders")
        avg_order = gr.Textbox(label="📊 Avg Order")

    payment_chart = gr.Plot()
    delivery_chart = gr.Plot()

    table = gr.Dataframe()

    run_btn.click(
        dashboard,
        inputs=[pwd, date_filter, payment_filter, delivery_filter],
        outputs=[total_sales, total_orders, avg_order, payment_chart, delivery_chart, table]
    )

# ===============================
# RUN
# ===============================
app.launch(share=True)