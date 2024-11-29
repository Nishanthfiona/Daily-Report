import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# Title of the App
st.title("Sales and Leads Dashboard")

# File Uploader
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    # Load Excel Sheets
    leads_data = pd.read_excel(uploaded_file, sheet_name=0)  # First sheet
    sales_data = pd.read_excel(uploaded_file, sheet_name=1)  # Second sheet

    # Sidebar Date Filters
    st.sidebar.header("Filter by Date")
    start_date = st.sidebar.date_input("Start Date", datetime.now().replace(day=1))
    end_date = st.sidebar.date_input("End Date", datetime.now())

    # Filter Data
    leads_data = leads_data[(leads_data['Date'] >= pd.to_datetime(start_date)) & 
                             (leads_data['Date'] <= pd.to_datetime(end_date))]
    sales_data = sales_data[(sales_data['Date'] >= pd.to_datetime(start_date)) & 
                             (sales_data['Date'] <= pd.to_datetime(end_date))]

    # 1. Leads vs Date Chart
    st.subheader("Leads Given Trend")
    leads_chart = px.line(leads_data, x='Date', y='Leads Given', title="Leads Given Over Time")
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
    daily_avg_required = target_sales / working_days if working_days else 0
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

else:
    st.warning("Please upload an Excel file.")
