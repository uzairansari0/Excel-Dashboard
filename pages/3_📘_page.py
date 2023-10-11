import pandas as pd
import plotly.express as px
import streamlit as st
import datetime
from datetime import time
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Dashboard Page 4",
                   page_icon=":bar_chart:",
                   layout="wide")


@st.experimental_memo
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine='openpyxl',
        sheet_name='Sales',
        skiprows=3,
        usecols='B:R',
        nrows=1000
    )

    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
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

dates = st.sidebar.date_input(
    "Please select the Date",
    datetime.date(2021, 1, 1),
)

# slider_date = st.sidebar.slider(
#     "Select Dates",
#     # value=(time(10, 30), time(12, 45))
# )


df_selection = df.query(
    "City == @city & Customer_type == @customer_type & Gender == @gender & Date == @dates "
)

# st.dataframe(df_selection)


# ---- MAINPAGE ----
st.title(":date: Sales Dashboard 'Calender' Page")
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
    df_selection.groupby(by=["Product line"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
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

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_with=True)
right_column.plotly_chart(fig_product_sales, use_container_with=True)

# --- HIDE STREAMLIT STYLE ---

hide_st_style = """
                <style>
                #MainMenu{visibility:hidden;}
                footer{visibility:hidden;}
                header{visibility:hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)


