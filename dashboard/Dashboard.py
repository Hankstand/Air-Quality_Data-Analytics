import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.colors as PC
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Air Quality Dashboard",
    page_icon="🌍",
    layout="wide"
)

air_quality_data = pd.read_csv('merge_data.csv')
air_quality_data['datetime'] = pd.to_datetime(air_quality_data['datetime'])

pollutant_metrics = list(air_quality_data.columns[:6])
weather_metrics = list(air_quality_data.columns[6:10]) + [air_quality_data.columns[11]]
category_ranges = ['Excellent', 'Good', 'Slightly Polluted', 'Lightly Polluted', 'Moderately Polluted', 'Heavily Polluted']

st.title('Air Quality Trends in Beijing (2013-2017) across 12 Stations')

with st.sidebar:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image("Logo.png", width=100)
    with col3:
        st.write(' ')
    st.header('Filters')

station_options = ['Overall Station'] + list(air_quality_data['station'].unique())
selected_stations = st.sidebar.multiselect('Select Stations', station_options)

category_options = ['Overall Category'] + list(air_quality_data['Category'].unique())
selected_category = st.sidebar.selectbox('Select Category', category_options, index=0)

min_date = pd.to_datetime('2013-03-01').date()
max_date = pd.to_datetime('2017-02-28').date()

start_date = st.sidebar.date_input('Start Date', min(air_quality_data['datetime']).date(), min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input('End Date', max(air_quality_data['datetime']).date(), min_value=min_date, max_value=max_date)

start_hour = st.sidebar.slider('Start Hour', 0, 23, 0)
end_hour = st.sidebar.slider('End Hour', 0, 23, 23)

if 'Overall Station' in selected_stations:
    selected_stations.remove('Overall Station')

air_quality_data['Date'] = air_quality_data['datetime'].dt.date
air_quality_data['Hour'] = air_quality_data['datetime'].dt.hour

station_condition = air_quality_data['station'].isin(selected_stations) if selected_stations else True
category_condition = (air_quality_data['Category'] == selected_category) if selected_category != 'Overall Category' else True
date_filter = (air_quality_data['Date'] >= start_date) & (air_quality_data['Date'] <= end_date)
hour_filter = (air_quality_data['Hour'] >= start_hour) & (air_quality_data['Hour'] <= end_hour)

filtered_data = air_quality_data[station_condition & category_condition & date_filter & hour_filter]

selected_stations_string = ', '.join(selected_stations) if selected_stations else 'All Stations'
st.write(f"**Key Metrics for {selected_stations_string} - {selected_category}**")

order_category = filtered_data.groupby('Category')['datetime'].nunique().reindex(category_ranges)

column_list = st.columns(3)
for index, (category, count) in enumerate(order_category.items()):
    formatted_count = "{:,}".format(count) 
    column = column_list[index % 3]  
    column.metric(category, f"{formatted_count} Days")  

category_counts = air_quality_data['Category'].value_counts().reindex(category_ranges, fill_value=0).reset_index()
category_counts.columns = ['Category', 'Count']

colors = ['#abd162', '#f6d460', '#fb9a52', '#f5676b', '#a37cb9', '#a07682'] 

fig = px.pie(category_counts, values='Count', names='Category', title='Percentage Distribution of Air Quality Categories', height=600, width=800, hole=0.5, color_discrete_sequence=colors)
fig.update_traces(sort=False)
st.plotly_chart(fig, use_container_width=True)  

col1, col2 = st.columns(2)
with col1:
    selected_parameter = st.selectbox('Choose Air Pollutant Metric', pollutant_metrics)
with col2:
    frequency_options = ['Hourly', 'Daily', 'Weekly', 'Monthly', 'Yearly']
    selected_frequency = st.selectbox('Choose Time Frequency', frequency_options)

frequency_mapping = {'Hourly': 'H', 'Daily': 'D', 'Weekly': 'W', 'Monthly': 'M', 'Yearly': 'Y'}

filtered_data_resampled = filtered_data.groupby(['station',
                                                 pd.Grouper(key='datetime',
                                                            freq=frequency_mapping[selected_frequency])])[selected_parameter].mean().reset_index()

fig = px.line(filtered_data_resampled, x='datetime', y=selected_parameter, color='station',
              title=f'{selected_parameter} {selected_frequency} Levels by Station Over Time')

st.plotly_chart(fig, use_container_width=True)

col1 = st.columns(1)[0]
with col1:
    selected_parameter = st.selectbox('Select Air Pollutant Parameter', pollutant_metrics, key='param_select')

average_pollutant = filtered_data.groupby('station')[selected_parameter].mean()
best_worst_stations = pd.concat([average_pollutant.nsmallest(5), average_pollutant.nlargest(5)]).index.tolist()
filtered_data_best_worst = filtered_data[filtered_data['station'].isin(best_worst_stations)]

fig = make_subplots(rows=1, cols=2, subplot_titles=("5 Best Stations", "5 Worst Stations"))

for i, station_type in enumerate(['Best Stations', 'Worst Stations']):
    station_air_quality_data = filtered_data_best_worst[filtered_data_best_worst['station'].isin(best_worst_stations[i*5:(i+1)*5])]
    station_air_quality_data_resampled = station_air_quality_data.groupby(['station',
                                                   pd.Grouper(key='datetime')])[selected_parameter].mean().reset_index()
    station_air_quality_data_avg = station_air_quality_data_resampled.groupby('station')[selected_parameter].mean().reset_index()  # Calculate average
    fig.add_trace(go.Bar(x=station_air_quality_data_avg['station'], y=station_air_quality_data_avg[selected_parameter], 
                         name=station_type, marker_color='green' if station_type == 'Best Stations' else 'red'), row=1, col=i+1)

fig.update_layout(height=600, width=800, title_text=f'Average {selected_parameter} Levels by Station Over Time')
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
parameters = pollutant_metrics + weather_metrics
with col1:
    selected_parameter1 = st.selectbox('Choose Parameter 1', parameters)
with col2:
    selected_parameter2 = st.selectbox('Choose Parameter 2', parameters)

fig_scatter = px.scatter(filtered_data, x=selected_parameter1, y=selected_parameter2,
                         color='station', title=f'{selected_parameter1} vs. {selected_parameter2} Correlation')
st.plotly_chart(fig_scatter, use_container_width=True)

pivot_air_quality_data = filtered_data.pivot_table(index='station', columns='Category', values='PM2.5', aggfunc='count', fill_value=0)
pivot_air_quality_data.sort_index(ascending=False, inplace=True)

fig = px.bar(pivot_air_quality_data, x=category_ranges, y=pivot_air_quality_data.index, title='Air Quality by Station',
             labels={'station': 'Station', 'value': 'Count', 'variable': 'Category'},
             color_discrete_sequence=colors)
fig.update_layout(barmode='stack', height=600, width=800)

st.plotly_chart(fig, use_container_width=True)


category_order_mapping = {category: i for i, category in enumerate(category_ranges)}
grouped_air_quality_data = air_quality_data.groupby(['wd', 'Category']).size().reset_index(name='count')
grouped_air_quality_data['Category_Order'] = grouped_air_quality_data['Category'].map(category_order_mapping)
grouped_air_quality_data.sort_values(by=['Category_Order', 'wd'], inplace=True)
color_scale = PC.sequential.Greens

fig = go.Figure()

for i, category in enumerate(category_ranges):
    category_air_quality_data = grouped_air_quality_data[grouped_air_quality_data['Category'] == category]
    color = color_scale[i] 
    fig.add_trace(go.Barpolar(r=category_air_quality_data['count'], theta=category_air_quality_data['wd'], name=category, text=category_air_quality_data['count'], hoverinfo='text', marker=dict(color=color)))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, max(grouped_air_quality_data['count'])])
    ), title="Air Quality Variations by Wind Direction", height=600, width=800
)
st.plotly_chart(fig, use_container_width=True)
