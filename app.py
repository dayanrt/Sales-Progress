import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config(page_title="Breakeven", page_icon=":bar_chart:", 
layout="wide")
df = pd.read_excel(io='FS odometro 2024.xlsx', 
engine='openpyxl', 
sheet_name='Export',
skiprows=0,
usecols='A:P',
nrows=233,)
#df['Year'] = df['Invoice date'].dt.year
#df['Month'] = df['Invoice date'].dt.month_name()
st.sidebar.header("Please Filter Here")
#FY = st.sidebar.multiselect("Select the FY:", options=df["FY"].unique(), default=df["FY"].unique())
Quarter = st.sidebar.multiselect("Select the Quarter:", options=df["Quarter"].unique(), default=df["Quarter"].unique())
BU = st.sidebar.multiselect("Select the BU:", options=df["BU"].unique(), default=df["BU"].unique())
#Year = st.sidebar.multiselect("Select the Year:", options=df["Year"].unique(), default=df["Year"].unique())
#Month = st.sidebar.multiselect("Select the Month:", options=df["Month"].unique(), default=df["Month"].unique())
df_selection = df.query("Quarter == @Quarter & BU == @BU")
st.dataframe(df_selection)
st.title("CT MX 2024-2025 Dashboard")
st.markdown("##")
total_sales1 = int(df_selection["Total amount GBP"].sum())
SLA = -200000
Intercompany = -168000
left_column, middle_column, right_column = st.columns(3)
with left_column: 
  st.subheader("Total sales:")
  st.subheader(f"GBP {total_sales1:,}")
with middle_column:
  st.subheader("SLA:")
  st.subheader(f":red[GBP {SLA:,}]")
with right_column:
  st.subheader("Intercompany:")
  st.subheader(f":red[GBP {Intercompany:,}]")
st.markdown("---")
#sales_by_Workorder = (df_selection.groupby(by=["Workorder"]).sum()[["Total amount GBP"]].sort_values(by="Total amount GBP"))
#fig_product_income = px.bar(sales_by_Workorder, x="Total amount GBP", y=sales_by_Workorder.index,orientation="h",title="<b>Sales by Workorder</b>",color_discrete_sequence=["#0083B8"] * len(sales_by_Workorder),template="plotly_white")
#fig_product_income.update_layout(plot_bgcolor="rgba(0,0,0,0)", font=dict(color="black"), yaxis=dict(showgrid=True, gridcolor='#cecdcd'), xaxis=dict(showgrid=True, gridcolor='#cecdcd'),height=900)  
#sales_by_account = (df_selection.groupby(by=["Account"]).sum()[["Total amount GBP"]].sort_values(by="Total amount GBP"))
fig1 = go.Figure(go.Indicator(domain = {'x': [0, 1], 'y': [0, 1]}, value = int(df_selection["Total amount GBP"].sum()), mode = "gauge+number+delta", title = {'text': "Sales target; Breakeven: 0"}, delta = {'reference': 0, "prefix": "0.0;"}, gauge = {'axis': {'range': [-500000, 500000]},'steps' : [{'range': [-500000, 0], 'color': "tomato"},{'range': [0, 100000], 'color': "orange"}],'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 150000}}))
st.plotly_chart(fig1, use_container_width=True)
st.markdown("---")
fig_account_income = px.pie(df_selection, values = "Total amount GBP2", names = "Account Group", hole =0.5)
fig_account_income.update_traces(text = df_selection["Account Group"], textposition= "outside")
fig_account_income.update_layout(legend = dict(orientation="h", yanchor="top", y=0, xanchor="left", x=0.33))
fig_account_income1 = px.pie(df_selection, values = "Total amount GBP2", names = "Service Types", hole =0.5)
fig_account_income1.update_traces(text = df_selection["Service Types"], textposition= "inside")
left_column, right_column = st.columns(2)
with left_column:
  left_column.plotly_chart(fig_account_income, use_container_width=True)
with right_column:
  right_column.plotly_chart(fig_account_income1, use_container_width=True)
st.markdown("---")
