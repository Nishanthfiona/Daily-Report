import pandas as pd
import plotly.express as px
import streamlit as st
from openpyxl import load_workbook

# Load and process Excel file
def reload_excel_file(file_path):
    wb = load_workbook(file_path)
    sheet = wb.active
    df = pd.DataFrame(sheet.values)
    df.columns = df.iloc[0]  # Use first row as header
    df = df.drop(0)  # Drop first row
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # Drop rows with invalid dates
    return df

# Load your data
file_path = 'your_excel_file.xlsx'  # Update with your file path
leads_data = reload_excel_file(file_path)

# Display KPIs
st.metric("Total Sales for Current Month", total_sales_current_month)
st.metric("Working Days this Month", working_days_current_month)

# Date filter widget
start_date = st.date_input("Start Date", pd.to_datetime('2024-01-01'))
end_date = st.date_input("End Date", pd.to_datetime('2024-12-31'))

# Filter data based on date range
filtered_data = leads_data[(leads_data['Date'] >= start_date) & (leads_data['Date'] <= end_date)]

# Plot the filtered data
leads_chart = px.line(filtered_data, x='Date', y='Leads Given', title="Leads Given Over Time")
st.plotly_chart(leads_chart)

    # 2. Sales vs Date Chart
    st.subheader("Sales Trend")
    sales_chart = px.line(sales_data, x='Date', y='Sales', title="Sales Over Time")
    st.plotly_chart(sales_chart)

    # Current Month Metrics
    st.header("Current Month Metrics")
    today = datetime.now()
    current_month_data = sales_data[sales_data['Date'].dt.month == today.month]

    # Sum of Sales
    total_sales = current_month_data['Sales'].sum()
    st.metric("Total Sales (Current Month)", total_sales)

    # Working Days Logic
    first_day_of_month = today.replace(day=1)
    days_in_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - first_day_of_month
    total_days = days_in_month.days
    weekdays = [(first_day_of_month + timedelta(days=i)).weekday() for i in range(total_days)]
    working_days = sum(1 for d in weekdays if (d < 5 and d % 2 == 0) or (d < 6 and d % 2 == 1))
    st.metric("Total Working Days (Current Month)", working_days)

    # Manual Holiday Input
    holidays = st.number_input("Additional Holidays", value=0, step=1)
    worked_days = working_days - holidays
    st.metric("Worked Days (Current Month)", worked_days)

    # Target Sales
    target_sales = st.number_input("Sales Target for the Month", value=0, step=1)
    st.metric("Sales Target", target_sales)

    # Daily Average to Meet Target
    daily_avg_required = target_sales / working_days
    st.metric("Required Daily Average to Meet Target", round(daily_avg_required, 2))

    # Current Month Average Sales
    avg_sales_per_day = total_sales / worked_days if worked_days else 0
    st.metric("Current Month Sales Average", round(avg_sales_per_day, 2))

    # Where We Should Be
    sales_should_be = daily_avg_required * worked_days
    st.metric("Expected Sales (As of Today)", round(sales_should_be, 2))

    # Deficit
    deficit = sales_should_be - total_sales
    st.metric("Deficit", round(deficit, 2))
