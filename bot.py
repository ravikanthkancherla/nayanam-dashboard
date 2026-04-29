import pandas as pd
from datetime import datetime, timedelta

FILE = "nayanam_data.xlsx"

def fmt(x):
    try:
        return f"₹{x:,.0f}"
    except:
        return x

def load_data():
    df = pd.read_excel(FILE)

    df["Created"] = pd.to_datetime(df.get("Created"), errors="coerce")
    df["Total"] = pd.to_numeric(df.get("Total"), errors="coerce")

    if "Sub Order Type" not in df.columns:
        df["Sub Order Type"] = df.get("Order Type", "Dine-In")

    df["Delivery Boy"] = df.get("Delivery Boy", "Unknown")

    return df

def apply_date_filter(df, mode):

    if mode == "today":
        return df[df["Created"].dt.date == datetime.today().date()]

    if mode == "yesterday":
        return df[df["Created"].dt.date == (datetime.today() - timedelta(days=1)).date()]

    try:
        d = datetime.strptime(mode, "%d-%m-%Y").date()
        return df[df["Created"].dt.date == d]
    except:
        pass

    try:
        m = datetime.strptime(mode, "%m-%Y")
        return df[
            (df["Created"].dt.month == m.month) &
            (df["Created"].dt.year == m.year)
        ]
    except:
        pass

    return df

def sales_location(df, outlet, date_mode):

    df = df[df["Outlet"] == outlet]
    df = apply_date_filter(df, date_mode)

    if df.empty:
        return "❌ No data"

    total = df["Total"].sum()
    orders = len(df)
    aov = total / orders if orders else 0

    split = df.groupby("Sub Order Type")["Total"].sum()
    pct = (split / total * 100).round(1)

    text = f"📊 {outlet} SALES ({date_mode.upper()})\n\n"
    text += f"💰 {fmt(total)} | 📦 {orders} | AOV {fmt(aov)}\n\n"

    for k in split.index:
        text += f"{k} → {fmt(split[k])} ({pct[k]}%)\n"

    return text

def staff_location(df, outlet, date_mode):

    df = df[df["Outlet"] == outlet]
    df = apply_date_filter(df, date_mode)

    if df.empty:
        return "❌ No data"

    df["WorkDate"] = df["Created"].dt.date
    days = df.groupby("Delivery Boy")["WorkDate"].nunique()

    temp = df.groupby("Delivery Boy").agg(
        Sales=("Total", "sum"),
        Orders=("Total", "count")
    )

    temp["AOV"] = temp["Sales"] / temp["Orders"]
    temp["Days"] = days

    max_sales = temp["Sales"].max()
    max_orders = temp["Orders"].max()

    temp["Score"] = (
        (temp["Sales"] / max_sales * 50) +
        (temp["Orders"] / max_orders * 30) +
        (temp["Days"] / temp["Days"].max() * 20)
    ).round(0)

    def tag(score):
        if score >= 80:
            return "⭐ Star"
        elif score >= 60:
            return "👍 Good"
        else:
            return "⚠️ Improve"

    temp["Tag"] = temp["Score"].apply(tag)

    sorted_df = temp.sort_values("Score", ascending=False)

    text = f"👨‍💼 {outlet} CAPTAIN ({date_mode.upper()})\n\n"

    for i, r in sorted_df.iterrows():
        text += f"{i} → {fmt(r['Sales'])} | {int(r['Orders'])} | {int(r['Days'])}d | {r['Tag']}\n"

    return text