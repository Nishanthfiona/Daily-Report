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

    # Bar chart for Leads Given over time with trendline
    leads_chart = px.bar(df, x='Date', y='Lead Generated', title="Leads Given Over Time", color='Lead Generated')
    leads_chart.update_traces(marker=dict(color='lightgreen', line=dict(color='green', width=2)))
    
    # Add trendline to the chart
    leads_chart.add_scatter(x=df['Date'], y=df['Leads Trendline'], mode='lines', name='Leads Trendline', 
                            line=dict(color='green', width=3))

    # Bar chart for Sales over time with trendline
    sales_chart = px.bar(df, x='Date', y='Sales', title="Sales Over Time", color='Sales')
    sales_chart.update_traces(marker=dict(color='lightgreen', line=dict(color='green', width=2)))

    # Add trendline to the chart
    sales_chart.add_scatter(x=df['Date'], y=df['Sales Trendline'], mode='lines', name='Sales Trendline', 
                            line=dict(color='green', width=3))

    # Styling the layout
    leads_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Lead Generated",
        template="plotly_dark",
        title_x=0.5,
        showlegend=True
    )

    sales_chart.update_layout(
        xaxis_title="Date",
        yaxis_title="Sales",
        template="plotly_dark",
        title_x=0.5,
        showlegend=True
    )

    # Display both charts
    st.plotly_chart(leads_chart)
    st.plotly_chart(sales_chart)

else:
    st.write("Please upload an Excel file to see the charts.")
