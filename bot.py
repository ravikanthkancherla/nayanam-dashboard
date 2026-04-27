import pandas as pd
from datetime import datetime, timedelta

# =========================
# DISPLAY SETTINGS
# =========================
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 2000)
pd.set_option('display.expand_frame_repr', False)

print("🚀 Nayanam Analytics Engine (Clean Version)")

# =========================
# LOAD DATA
# =========================
try:
    df = pd.read_excel("orders.xlsx")
    df.columns = df.columns.str.strip()
except:
    print("❌ orders.xlsx not found")
    exit()

# =========================
# CLEAN DATA
# =========================
if "Grand Total (₹)" in df.columns:
    df = df.rename(columns={"Grand Total (₹)": "Total"})
else:
    print("❌ Grand Total column missing")
    exit()

df["Total"] = pd.to_numeric(df["Total"], errors="coerce")

if "Created" in df.columns:
    df["Created"] = pd.to_datetime(df["Created"], errors="coerce", dayfirst=True)

df["Delivery Boy"] = df.get("Delivery Boy", "Unknown").fillna("Unknown")

# =========================
# FILTER MODULE
# =========================
def apply_filters(data, query):
    if "today" in query:
        return data[data["Created"].dt.date == datetime.now().date()]

    elif "yesterday" in query:
        y = (datetime.now() - timedelta(days=1)).date()
        return data[data["Created"].dt.date == y]

    return data


# =========================
# ANALYTICS MODULES
# =========================

def summary(data):
    return f"""
📊 SUMMARY
💰 Sales: ₹{data['Total'].sum():,.0f}
🧾 Orders: {len(data)}
📊 Avg Order: ₹{data['Total'].mean():.2f}
"""


def delivery_analysis(data):
    result = data.groupby("Delivery Boy")["Total"].agg(["sum", "count"])
    result.columns = ["Sales", "Orders"]
    return "\n🚴 Delivery Performance:\n" + result.sort_values(by="Sales", ascending=False).to_string()


def payment_analysis(data):
    if "Payment Type" not in data.columns:
        return "No payment data"
    return "\n💳 Payment Split:\n" + data.groupby("Payment Type")["Total"].sum().to_string()


def status_analysis(data):
    return "\n📦 Status:\n" + data["Status"].value_counts().to_string()


def order_type_analysis(data):
    return "\n🍽️ Order Type:\n" + data["Order Type"].value_counts().to_string()


def financials(data):
    return f"""
💸 Discount: ₹{data['Total Discount (₹)'].sum():,.0f}
🧾 Tax: ₹{data['Total Tax (₹)'].sum():,.0f}
📦 Charges: ₹{data['Delivery Charge (₹)'].sum() + data['Container Charge (₹)'].sum():,.0f}
"""


def hourly_sales(data):
    if "Created" not in data.columns:
        return "No time data"
    data["Hour"] = data["Created"].dt.hour
    return "\n⏰ Hourly Sales:\n" + data.groupby("Hour")["Total"].sum().to_string()


def customer_search(data, query):
    name = query.replace("customer", "").strip()
    return data[data["Customer Name"].str.contains(name, case=False, na=False)].to_string(index=False)


def phone_search(data, query):
    num = query.replace("phone", "").strip()
    return data[data["Customer Phone"].astype(str).str.contains(num)].to_string(index=False)


def order_search(data, query):
    num = query.replace("order", "").strip()
    return data[data["Order No."].astype(str).str.contains(num)].to_string(index=False)


# =========================
# MAIN QUERY ENGINE
# =========================
def get_summary(query):
    query = query.lower().strip()

    data = apply_filters(df, query)

    if "summary" in query or "total" in query:
        return summary(data)

    elif "delivery" in query:
        return delivery_analysis(data)

    elif "payment" in query:
        return payment_analysis(data)

    elif "status" in query:
        return status_analysis(data)

    elif "order type" in query:
        return order_type_analysis(data)

    elif "financial" in query or "tax" in query or "discount" in query:
        return financials(data)

    elif "hour" in query:
        return hourly_sales(data)

    elif "customer" in query:
        return customer_search(data, query)

    elif "phone" in query:
        return phone_search(data, query)

    elif "order " in query:
        return order_search(data, query)

    elif "show" in query:
        return data.head(50).to_string(index=False)

    elif "columns" in query:
        return "\n".join(data.columns)

    elif "export" in query:
        data.to_excel("output.xlsx", index=False)
        return "✅ Exported as output.xlsx"

    else:
        return """
Try:
summary / total
delivery / delivery today
payment
status
order type
financial
hour
customer ravi
phone 9876
order 123
show
export
"""


# =========================
# LOOP
# =========================
print("\n✅ Ready 🚀 (type 'exit')")

while True:
    q = input("\nAsk: ")
    if q.lower() == "exit":
        break

    print("\n" + "-"*80)
    print(get_summary(q))
    print("-"*80)