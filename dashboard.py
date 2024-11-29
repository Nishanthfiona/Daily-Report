import streamlit as st
import pandas as pd
import plotly.express as px

# Uploading the file via Streamlit uploader
st.title("Leads and Sales Analytics Dashboard")

# File upload widget for Excel file
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Load the data from both sheets
    df_leads = pd.read_excel(uploaded_file, sheet_name='Sheet1')
    df_sales = pd.read_excel(uploaded_file, sheet_name='Sheet2')

    # Merge the two dataframes on 'Date' and 'Counselors' to combine the leads and sales data
    df = pd.merge(df_leads, df_sales, on=['Date', 'Counselors'], how='inner')

    # Ensure the Date column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Line chart for Leads Given over time
    leads_chart = px.line(df, x='Date', y='Lead Generated', title="Leads Given Over Time")
    leads_chart.update_traces(mode='markers+lines', name='Leads Given')

    # Line chart for Sales over time
    sales_chart = px.line(df, x='Date', y='Sales', title="Sales Over Time")
    sales_chart.update_traces(mode='markers+lines', name='Sales')

    # Display both charts
    st.plotly_chart(leads_chart)
    st.plotly_chart(sales_chart)

    # Optional: You can add more metrics below later for KPI calculation

else:
    st.write("Please upload an Excel file to see the charts.")
