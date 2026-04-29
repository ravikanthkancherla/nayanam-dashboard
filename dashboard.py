import pandas as pd
import gradio as gr
import plotly.express as px

FILE = "nayanam_data.xlsx"

# ===============================
# FORMAT
# ===============================
def fmt(x):
    return f"₹{x:,.2f}"

# ===============================
# LOAD DATA
# ===============================
def load_data():
    xls = pd.ExcelFile(FILE)
    df_list = []

    for sheet in xls.sheet_names:
        temp = pd.read_excel(FILE, sheet_name=sheet)

        sales_col = [c for c in temp.columns if "total" in str(c).lower() or "amount" in str(c).lower()]
        if not sales_col:
            continue

        temp["Total"] = pd.to_numeric(temp[sales_col[0]], errors="coerce")

        sub_col = [c for c in temp.columns if "sub order" in str(c).lower()]
        temp["Sub Order Type"] = temp[sub_col[0]] if sub_col else "Unknown"

        order_col = [c for c in temp.columns if "order type" in str(c).lower()]
        temp["Order Type"] = temp[order_col[0]] if order_col else "Unknown"

        temp["Delivery Boy"] = temp.get("Delivery Boy","Unknown")
        temp["Outlet"] = sheet

        df_list.append(temp)

    return pd.concat(df_list, ignore_index=True)

# ===============================
# DASHBOARD LOGIC
# ===============================
def dashboard(outlet):

    df = load_data()

    df_filtered = df.copy()
    if outlet != "All":
        df_filtered = df[df["Outlet"] == outlet]

    # KPIs
    sales = df_filtered["Total"].sum()
    orders = len(df_filtered)
    aov = sales / orders if orders else 0

    # COMPARISON KPIs (ALL)
    total_sales = df["Total"].sum()
    total_orders = len(df)
    total_aov = total_sales / total_orders if total_orders else 0

    # ===============================
    # CHARTS
    # ===============================

    # Outlet Sales
    outlet_chart = df.groupby("Outlet")["Total"].sum().reset_index()
    fig_outlet = px.bar(outlet_chart, x="Outlet", y="Total", title="Sales by Outlet")

    # Sub Order Pie
    sub_chart = df_filtered.groupby("Sub Order Type")["Total"].sum().reset_index()
    fig_sub = px.pie(sub_chart, names="Sub Order Type", values="Total", title="Channel Mix")

    # Order Type Count
    order_chart = df_filtered.groupby("Order Type")["Total"].count().reset_index()
    fig_order = px.bar(order_chart, x="Order Type", y="Total", title="Order Count")

    # ===============================
    # STAFF TABLE
    # ===============================
    staff = df_filtered.groupby("Delivery Boy")["Total"].sum().sort_values(ascending=False).head(10)
    staff_df = staff.reset_index()
    staff_df.columns = ["Staff","Sales"]
    staff_df["Sales"] = staff_df["Sales"].apply(fmt)

    # ===============================
    # TEXT OUTPUTS
    # ===============================
    kpi_selected = f"""
Selected Outlet:
Sales: {fmt(sales)}
Orders: {orders}
AOV: {fmt(aov)}
"""

    kpi_all = f"""
All Outlets:
Sales: {fmt(total_sales)}
Orders: {total_orders}
AOV: {fmt(total_aov)}
"""

    return kpi_selected, kpi_all, fig_outlet, fig_sub, fig_order, staff_df

# ===============================
# UI
# ===============================
df_init = load_data()
outlets = ["All"] + list(df_init["Outlet"].dropna().unique())

with gr.Blocks() as app:

    gr.Markdown("# 📊 Nayanam Investor Dashboard")

    outlet = gr.Dropdown(outlets, label="Select Outlet", value="All")
    btn = gr.Button("Load Dashboard")

    gr.Markdown("## KPI Summary")
    kpi_selected = gr.Textbox(label="Selected Outlet KPI")
    kpi_all = gr.Textbox(label="All Outlet KPI")

    gr.Markdown("## 📊 Charts")
    chart1 = gr.Plot()
    chart2 = gr.Plot()
    chart3 = gr.Plot()

    gr.Markdown("## 👨‍💼 Top Staff")
    staff = gr.Dataframe()

    btn.click(
        dashboard,
        inputs=outlet,
        outputs=[kpi_selected, kpi_all, chart1, chart2, chart3, staff]
    )

app.launch()