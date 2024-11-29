import streamlit as st
import pandas as pd
import plotly.express as px
from scipy import stats

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

    # Optional: Smoothing using rolling averages
    df['Lead Generated Smooth'] = df['Lead Generated'].rolling(window=7).mean()
    df['Sales Smooth'] = df['Sales'].rolling(window=7).mean()

    # Adding trendlines manually
    slope_leads, intercept_leads, _, _, _ = stats.linregress(df['Date'].map(pd.Timestamp.toordinal), df['Lead Generated'])
    df['Leads Trendline'] = slope_leads * df['Date'].map(pd.Timestamp.toordinal) + intercept_leads

    slope_sales, intercept_sales, _, _, _ = stats.linregress(df['Date'].map(pd.Timestamp.toordinal), df['Sales'])
    df['Sales Trendline'] = slope_sales * df['Date'].map(pd.Timestamp.toordinal) + intercept_sales

    # Extract year, month, and day for drilldown
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Create hierarchical data using Plotly date hierarchy
    leads_chart = px.line(df, 
                          x='Date', 
                          y=['Lead Generated', 'Leads Trendline'], 
                          title="Leads Given Over Time",
                          labels={'Lead Generated': 'Leads Given'},
                          line_shape='linear',
                          markers=True)

    sales_chart = px.line(df, 
                          x='Date', 
                          y=['Sales', 'Sales Trendline'], 
                          title="Sales Over Time",
                          labels={'Sales': 'Sales'},
                          line_shape='linear',
                          markers=True)

    # Add date hierarchy to the x-axis for both charts (Year > Month > Day)
    leads_chart.update_layout(
        xaxis=dict(
            tickformat="%b %d, %Y",
            rangeslider_visible=True,
            type="category",  # Ensure that Plotly can handle this as categorical
            tickmode='array',
            tickvals=df['Date'].dt.date.unique()
        ),
        showlegend=True,
        template="plotly_dark",
        title_x=0.5
    )

    sales_chart.update_layout(
        xaxis=dict(
            tickformat="%b %d, %Y",
            rangeslider_visible=True,
            type="category",  # Ensure that Plotly can handle this as categorical
            tickmode='array',
            tickvals=df['Date'].dt.date.unique()
        ),
        showlegend=True,
        template="plotly_dark",
        title_x=0.5
    )

    # Display both charts
    st.plotly_chart(leads_chart)
    st.plotly_chart(sales_chart)

else:
    st.write("Please upload an Excel file to see the charts.")
