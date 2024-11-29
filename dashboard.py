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

    # Clean up column names to ensure no extra spaces or issues
    df_leads.columns = df_leads.columns.str.strip()
    df_sales.columns = df_sales.columns.str.strip()

    # Merge the two dataframes on 'Date' and 'Counselors' to combine the leads and sales data
    df = pd.merge(df_leads, df_sales, on=['Date', 'Counselors'], how='inner')

    # Ensure the Date column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])

    # Sidebar filters for Date Range and Counselors
    st.sidebar.header('Filters')
    
    # Date Range Filter
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    selected_date_range = st.sidebar.date_input("Select Date Range", [min_date, max_date])

    # Filter the Data based on selected date range
    df_filtered = df[(df['Date'] >= pd.to_datetime(selected_date_range[0])) & 
                     (df['Date'] <= pd.to_datetime(selected_date_range[1]))]

    # Counselor Dropdown filter
    selected_counselors = st.sidebar.multiselect(
        "Select Counselors", 
        options=df_filtered['Counselors'].unique(), 
        default=df_filtered['Counselors'].unique()
    )
    
    # Filter by selected counselors
    df_filtered = df_filtered[df_filtered['Counselors'].isin(selected_counselors)]

    # Ensure the correct columns are referenced
    if 'Lead Generated' in df_filtered.columns and 'Sales' in df_filtered.columns:
        # Line chart for Leads Given over time with Trendline
        leads_chart = px.line(df_filtered, x='Date', y='Lead Generated', title="Leads Given Over Time",
                              trendline="ols", trendline_color_override="red")  # Adding trendline (Ordinary Least Squares)
        leads_chart.update_traces(mode='markers+lines', name='Leads Given')

        # Line chart for Sales over time with Trendline
        sales_chart = px.line(df_filtered, x='Date', y='Sales', title="Sales Over Time",
                              trendline="ols", trendline_color_override="blue")  # Adding trendline (Ordinary Least Squares)
        sales_chart.update_traces(mode='markers+lines', name='Sales')

        # Display both charts (making them wider)
        st.plotly_chart(leads_chart, use_container_width=True)
        st.plotly_chart(sales_chart, use_container_width=True)
    else:
        st.error("The required columns ('Lead Generated' or 'Sales') are missing from the data.")
else:
    st.write("Please upload an Excel file to see the charts.")
