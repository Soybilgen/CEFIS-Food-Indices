import streamlit as st
import pandas as pd
import plotly.express as px

# Change page margins
st.set_page_config(layout="wide", page_title="CEFIS Food Price Index", page_icon=":food:")

# Load the data
subindices = pd.read_csv('daily_detailed_subindices.csv')
subprices = pd.read_csv('daily_detailed_subprices.csv')
main_index = pd.read_csv('daily_mainindices.csv')

# Convert the 'date' column to datetime format
subindices['date'] = pd.to_datetime(subindices['date'])
subprices['date'] = pd.to_datetime(subprices['date'])
main_index['date'] = pd.to_datetime(main_index['date'])

last_day = main_index["date"][main_index.__len__()-1]

date_range_previous_month = pd.date_range(start=(last_day - pd.DateOffset(months=1) - pd.DateOffset(days=last_day.day-1)), end=(last_day - pd.DateOffset(months=1)), freq='D')
date_range_previous_year = pd.date_range(start=(last_day - pd.DateOffset(years=1) - pd.DateOffset(days=last_day.day-1)), end=(last_day - pd.DateOffset(years=1)), freq='D')
date_range_current_month = pd.date_range(start=(last_day - pd.DateOffset(days=last_day.day-1)), end=(last_day), freq='D')

price_index_previous_month = main_index.loc[main_index['date'].isin(date_range_previous_month), "CEFIS Food Index"].mean()
price_index_current_month = main_index.loc[main_index['date'].isin(date_range_current_month), "CEFIS Food Index"].mean()
mom_growth = round((price_index_current_month/price_index_previous_month-1)*100,2)

price_index_previous_year = main_index.loc[main_index['date'].isin(date_range_previous_year), "CEFIS Food Index"].mean()
price_index_current_month = main_index.loc[main_index['date'].isin(date_range_current_month), "CEFIS Food Index"].mean()
yoy_growth = round((price_index_current_month/price_index_previous_year-1)*100,2)

# Sidebar
st.sidebar.header('Select Indices')

# Select items
selected_item1 = st.sidebar.selectbox('Choose the subindex for the upper figure', options=subindices.columns[1:])
selected_type1 = st.sidebar.selectbox('Choose the upper figure type', ['Price Index', 'Price Level'])
selected_item2 = st.sidebar.selectbox('Choose the competing index for the lower figure', options=main_index.columns[2:])

st.sidebar.markdown("For visualization purposes, the competing index is reindexed to 2020M01=100.")
st.sidebar.markdown("<a href='https://data.tuik.gov.tr/Kategori/GetKategori?p=Enflasyon-ve-Fiyat-106'>Turkstat food index</a> refers to Turkish Statistical Institute's price index for food and non-alcoholic beverages.", unsafe_allow_html=True)
st.sidebar.markdown("<a href='https://bilgibankasi.ito.org.tr/tr/istatistik-verileri/istanbul-ucretler-gecinme/gruplar-itibariyle-degisim?year=95'>ITO food index</a> refers to Istanbul Chamber of Commerce's wage earners index for food expenditure.", unsafe_allow_html=True)
st.sidebar.markdown("""
  #### The final update is {temp}  
""".format(temp=str(last_day.strftime("%d %B %Y"))))

# Main
st.title('CEFIS Daily Food Price Indices')

st.markdown("The <a href='https://cefis.bilgi.edu.tr/'>CEFIS</a> Food Price Indices are a result of an extensive data collection process, where we gather daily food price data from five major online retail chains in Turkey. This process, which has been ongoing since July 2018, allows us to extract a vast amount of price data each day. \
            We follow the procedure established by the Turkish Statistical Institute (TurkStat), classifying the prices into one of the 131 food and non-alcoholic beverages subcategory provided by TurkStat. \
            For each subcategory, we take the geometric average of all prices in that subcategory each day. After obtaining geometric prices, we index all subcategories using the base period January 2020 = 100. \
            In cases where we were unable to collect data, we use linear interpolation to estimate the values of missing observations. After forming 131 daily food subindices, we multiply the subindex weights used by TurkStat by our daily subindex values to obtain our daily main food index.\
            For more information on our methodology, please see our <a href='https://link.springer.com/article/10.1007/s41549-023-00084-2'>methodology paper</a>.", unsafe_allow_html=True)

st.markdown("In this dashboard, we display the subindices that are used to create our main food index in the upper figure. You can choose any subindex or its associated price level using the left menu. \
             We also display the main food index and the competing index in the lower figure. You can also choose the competing index using the left menu.")

st.markdown(""" **:red[ The {date} month-on-month CEFIS food inflation is {MoM}%. ]**
            """.format(date=str(last_day.strftime("%B %Y")), MoM=mom_growth))

st.markdown(""" **:red[ The {date} year-on-year CEFIS food inflation is {YoY}%. ]**
            """.format(date=str(last_day.strftime("%B %Y")), YoY=yoy_growth))

# Main
st.header(f'Daily Time Series of {selected_item1}')
if selected_type1 == 'Price Index':
    # Time series plot
    fig1 = px.line(subindices[["date", selected_item1]], y=selected_item1, x="date", 
                # title=f'Daily Time Series of {selected_item1}', 
                template="seaborn", render_mode='webg1',
                labels={
                        "date": "Date",
                        selected_item1 : "Index Value, 2020M01=100"
                    },
                    width=800, height=600)
    fig1.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True,)
else:
        # Time series plot
    fig1 = px.line(subprices[["date", selected_item1]], y=selected_item1, x="date", 
                # title=f'Daily Time Series of {selected_item1}', 
                template="seaborn", render_mode='webg1',
                labels={
                        "date": "Date",
                        selected_item1 : "Price Level"
                    },
                    width=800, height=600)
    fig1.update_xaxes(rangeslider_visible=True)
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True,)

# Main
st.header(f'Daily Time Series of {main_index.columns[1]} and {selected_item2}')

# Time series plot
fig2_data = main_index[["date", main_index.columns[1], selected_item2]]
fig2 = px.line(fig2_data, y=fig2_data.columns[1:], x="date", 
              # title=f'Daily Time Series of {main_index.columns[1]} and {selected_item2}', 
              template="seaborn", render_mode='webg1',
              labels={
                     "date": "Date",
                     "value" : "Index Value, 2020M01=100"
                 },
                 width=800, height=600)
fig2.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01,
    title=None, 
))
fig2.update_xaxes(rangeslider_visible=True)
fig2.update_traces(line=dict(color='red'), selector=dict(name=fig2_data.columns[2]))
st.plotly_chart(fig2, use_container_width=True)

# Raw data
if selected_type1 == 'Price Index':
    raw_data = pd.concat([subindices[["date", selected_item1]], main_index[[main_index.columns[1], selected_item2]]], axis=1)
else:
    raw_data = pd.concat([subprices[["date", selected_item1]], main_index[[main_index.columns[1], selected_item2]]], axis=1)
# convert datetime to date
raw_data['date'] = raw_data['date'].dt.date
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(raw_data)
