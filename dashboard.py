{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "50742e12-a5b8-4b5c-a48c-eb554f746014",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2024-11-29 17:07:19.495 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\Users\\GWG1\\anaconda3\\Lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "import streamlit as st\n",
    "import pandas as pd\n",
    "import plotly.express as px\n",
    "from datetime import datetime, timedelta\n",
    "\n",
    "# Title of the App\n",
    "st.title(\"Sales and Leads Dashboard\")\n",
    "\n",
    "# File Uploader\n",
    "uploaded_file = st.file_uploader(\"Upload Excel File\", type=[\"xlsx\"])\n",
    "if uploaded_file:\n",
    "    # Load Excel Sheets\n",
    "    leads_data = pd.read_excel(uploaded_file, sheet_name=0)  # First sheet\n",
    "    sales_data = pd.read_excel(uploaded_file, sheet_name=1)  # Second sheet\n",
    "\n",
    "    # Sidebar Date Filters\n",
    "    st.sidebar.header(\"Filter by Date\")\n",
    "    start_date = st.sidebar.date_input(\"Start Date\", datetime.now().replace(day=1))\n",
    "    end_date = st.sidebar.date_input(\"End Date\", datetime.now())\n",
    "    \n",
    "    # Filter Data\n",
    "    leads_data = leads_data[(leads_data['Date'] >= pd.to_datetime(start_date)) & \n",
    "                            (leads_data['Date'] <= pd.to_datetime(end_date))]\n",
    "    sales_data = sales_data[(sales_data['Date'] >= pd.to_datetime(start_date)) & \n",
    "                            (sales_data['Date'] <= pd.to_datetime(end_date))]\n",
    "\n",
    "    # 1. Leads vs Date Chart\n",
    "    st.subheader(\"Leads Given Trend\")\n",
    "    leads_chart = px.line(leads_data, x='Date', y='Leads Given', title=\"Leads Given Over Time\")\n",
    "    st.plotly_chart(leads_chart)\n",
    "\n",
    "    # 2. Sales vs Date Chart\n",

    "    st.subheader(\"Sales Trend\")\n",
    "    sales_chart = px.line(sales_data, x='Date', y='Sales', title=\"Sales Over Time\")\n",
    "    st.plotly_chart(sales_chart)\n",
    "\n",
    "    # Current Month Metrics\n",
    "    st.header(\"Current Month Metrics\")\n",
    "    today = datetime.now()\n",
    "    current_month_data = sales_data[sales_data['Date'].dt.month == today.month]\n",
    "\n",
    "    # Sum of Sales\n",
    "    total_sales = current_month_data['Sales'].sum()\n",
    "    st.metric(\"Total Sales (Current Month)\", total_sales)\n",
    "\n",
    "    # Working Days Logic\n",
    "    first_day_of_month = today.replace(day=1)\n",
    "    days_in_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - first_day_of_month\n",
    "    total_days = days_in_month.days\n",
    "    weekdays = [(first_day_of_month + timedelta(days=i)).weekday() for i in range(total_days)]\n",
    "    working_days = sum(1 for d in weekdays if (d < 5 and d % 2 == 0) or (d < 6 and d % 2 == 1))\n",
    "    st.metric(\"Total Working Days (Current Month)\", working_days)\n",
    "\n",
    "    # Manual Holiday Input\n",
    "    holidays = st.number_input(\"Additional Holidays\", value=0, step=1)\n",
    "    worked_days = working_days - holidays\n",
    "    st.metric(\"Worked Days (Current Month)\", worked_days)\n",
    "\n",
    "    # Target Sales\n",
    "    target_sales = st.number_input(\"Sales Target for the Month\", value=0, step=1)\n",
    "    st.metric(\"Sales Target\", target_sales)\n",
    "\n",
    "    # Daily Average to Meet Target\n",
    "    daily_avg_required = target_sales / working_days\n",
    "    st.metric(\"Required Daily Average to Meet Target\", round(daily_avg_required, 2))\n",
    "\n",
    "    # Current Month Average Sales\n",
    "    avg_sales_per_day = total_sales / worked_days if worked_days else 0\n",
    "    st.metric(\"Current Month Sales Average\", round(avg_sales_per_day, 2))\n",
    "\n",
    "    # Where We Should Be\n",
    "    sales_should_be = daily_avg_required * worked_days\n",
    "    st.metric(\"Expected Sales (As of Today)\", round(sales_should_be, 2))\n",
    "\n",
    "    # Deficit\n",
    "    deficit = sales_should_be - total_sales\n",
    "    st.metric(\"Deficit\", round(deficit, 2))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "715e9218-eb80-4f64-abed-10d530afe2d8",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
