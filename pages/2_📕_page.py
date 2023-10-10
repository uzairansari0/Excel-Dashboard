import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard Page 1",
                   page_icon=":bar_chart:",
                   layout="wide")

@st.experimental_memo
def get_data_from_excel():
    df = pd.read_csv("SampleSuperstore.csv", skip_blank_lines=True, na_values=["NA", "N/A"])
    df.dropna()

    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M").dt.hour
    return df
df = get_data_from_excel()

# st.dataframe(df)

# ----sidebar----

st.sidebar.header("Please Filter Here:")
State = st.sidebar.multiselect(
        "Select the State:",
        options=df["State"].unique(),
        default=df["State"].unique()[0]
    )


ship_mode = st.sidebar.multiselect(
    "Select the Ship Mode Type:",
    options=df["ship_mode"].unique(),
    default=df["ship_mode"].unique(),
)

Segment = st.sidebar.multiselect(
    "Select the Segment Type:",
    options=df["Segment"].unique(),
    default=df["Segment"].unique(),
)

df_selection = df.query(
    "State == @State & ship_mode == @ship_mode & Segment == @Segment"
)

# st.dataframe(df_selection)


# ---- MAINPAGE ----
st.title(":bar_chart: Sales Dashboard Page 1")
st.markdown("##")

# ---- TOP KPI'S ----

total_sales = int(df_selection["Total"].sum())

average_rating = round(df_selection["Rating"].mean(), 1)
try:
  star_rating = ":star:" * int(round(average_rating, 0))

  average_sale_by_transition = round(df_selection["Total"].mean(), 2)

  left_column, middle_column, right_column = st.columns(3)
  with left_column:
      st.subheader("Total Sales:")
      st.subheader(f"US $ {total_sales:,}")

  with middle_column:
      st.subheader("Average Rating:")
      st.subheader(f"{average_rating} {star_rating}")

  with right_column:
      st.subheader("Average Sales Per Transaction:")
      st.subheader(f"US $ {average_sale_by_transition}")

  st.markdown("---")

  # SALES BY PRODUCT LINE [BAR CHART]

  sales_by_product_line = (
      df_selection.groupby(by=["Category"]).sum(numeric_only=True)[["Total"]].sort_values(by="Total")
  )
  fig_product_sales = px.bar(
      sales_by_product_line,
      x="Total",
      y=sales_by_product_line.index,
      orientation="h",
      title="<b>Sales by Category  Line</b>",
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
      df_selection.groupby(by=["Category"]).sum(numeric_only=True)[["Quantity"]]
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

  # ---- TOP SELLING PRODUCTS [DONUT CHART] ----

  top_selling_regions = (
      df_selection.groupby(by=["Region"]).sum(numeric_only=True)[["Quantity"]]
      .sort_values(by="Quantity", ascending=False)
  )

  fig_top_regions = go.Figure(
      go.Pie(
          labels=top_selling_regions.index,
          values=top_selling_regions["Quantity"],
          # hole=0.5
      )
  )

  fig_top_regions.update_traces(
      textposition="inside",
      textinfo="percent+label",
      marker=dict(colors=px.colors.qualitative.Alphabet)
  )

  fig_top_regions.update_layout(
      title="<b>Top Selling Regions</b>",
      template="plotly_white"
  )

  left_column, right_column = st.columns(2)
  left_column.plotly_chart(fig_hourly_sales, use_container_with=True)
  right_column.plotly_chart(fig_product_sales, use_container_with=True)

  left_column, right_column = st.columns(2)
  left_column.plotly_chart(fig_top_products, use_container_width=True)
  right_column.plotly_chart(fig_top_regions, use_container_width=True)
except ValueError:
    st.subheader(':point_left: Please Filter:')
  
# --- HIDE STREAMLIT STYLE ---

hide_st_style = """
                <style>
                #MainMenu{visibility:hidden;}
                footer{visibility:hidden;}
                header{visibility:hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html = True)


