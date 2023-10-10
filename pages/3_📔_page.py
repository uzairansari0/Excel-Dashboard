import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
import datetime
from datetime import datetime


st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")


@st.experimental_memo
def get_data_from_excel():
    df= pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000
    )

    df["hour"] = df["Time"].dt.hour
    return df


df = get_data_from_excel()
# st.dataframe(df)

# ----sidebar----

st.sidebar.header("Please Filter Here:")

city = st.sidebar.multiselect(
    "Select the city:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

gender = st.sidebar.multiselect(
    "Select the Gender Type:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

# Get the min and max dates from the date column
min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

# Define the default date range for the slider
default_range = (min_date, max_date)

# Create a slider widget for selecting date range
date_range = st.sidebar.slider(
    "Select a date range:",
    min_value=min_date,
    max_value=max_date,
    value=default_range,
    step=pd.to_timedelta(1, unit='d')
)

# Filter the data based on the selected date range
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])
filtered_data = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]



df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender "
)

# st.dataframe(df_selection)


# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard Page 2")
st.markdown("##")

# ---- TOP KPI'S ----

total_sales = int(df_selection["Total"].sum())
average_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transation = round(df_selection["Total"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")

with middle_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"US $ {average_sale_by_transation}")

st.markdown("---")

# SALES BY PRODUCT LINE [BAR CHART]

sales_by_product_line = (
    df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=['#0083B8'] * len(sales_by_product_line),
    template="plotly_white"
)

fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# SALES BY HOUR [BAR CHART]

sales_by_hour = df_selection.groupby(by=["hour"]).sum(numeric_only=True)[["Total"]]
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by Hour</b>",
    color_discrete_sequence=['#0083B8'] * len(sales_by_hour),
    template="plotly_white"
)

fig_hourly_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(tickmode="linear"),
    yaxis=(dict(showgrid=False))
)

# ---- TOP SELLING PRODUCTS [DONUT CHART] ----

top_selling_products = (
    df_selection.groupby(by=["Product line"]).sum()[["Quantity"]]
    .sort_values(by="Quantity", ascending=False)
)

fig_top_products = go.Figure(
    go.Pie(
        labels=top_selling_products.index,
        values=top_selling_products["Quantity"],
        hole=0.5
    )
)

fig_top_products.update_traces(
    textposition="inside",
    textinfo="percent+label",
    marker=dict(colors=px.colors.qualitative.Alphabet)
)

fig_top_products.update_layout(
    title="<b>Top Selling Products</b>",
    template="plotly_white"
)



left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_with=True)
right_column.plotly_chart(fig_product_sales, use_container_with=True)
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_top_products, use_container_width=True)

right_column.plotly_chart(fig_top_products, use_container_width=True)


# --- HIDE STREAMLIT STYLE ---

hide_st_style = """
                <style>
                #MainMenu{visibility:hidden;}
                footer{visibility:hidden;}
                header{visibility:hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
