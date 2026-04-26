import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

bike_df = pd.read_csv("dashboard/main_data.csv")

st.title("Dashboard Analisis Data Bike Sharing")

#Filter Tahun
col_spacer, col_filter = st.columns([4, 1]) 
with col_filter:
    year_filter = st.selectbox(
        "", 
        options=[2011, 2012], 
        index=1,
        label_visibility="collapsed" 
    )
filtered_df = bike_df[bike_df['yr_hour'] == (0 if year_filter == 2011 else 1)]

#Score Card
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = filtered_df['cnt_hour'].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    avg_casual = int(filtered_df['casual_hour'].mean())
    st.metric("Rata-rata Casual / Jam", value=f"{avg_casual}")
with col3:
    avg_registered = int(filtered_df['registered_hour'].mean())
    st.metric("Rata-rata Registered / Jam", value=f"{avg_registered}")
st.divider()

#Visualisasi 1
st.subheader("1. Segmentasi Pengguna: Hari Kerja vs Hari Libur")
view_q1 = st.radio("Pilih Tampilan Data:", ["Perbandingan", "Fokus Casual", "Fokus Registered"], horizontal=True, key="q1_radio")

segment_data = filtered_df.groupby('workingday_hour')[['casual_hour', 'registered_hour']].mean().reset_index()

if view_q1 == "Perbandingan":
    df_melted_q1 = segment_data.melt(id_vars='workingday_hour', var_name='Tipe Pengguna', value_name='Rata-rata Sewa')
    fig1 = px.bar(
        df_melted_q1, x='workingday_hour', y='Rata-rata Sewa', color='Tipe Pengguna',
        barmode='group', color_discrete_map={'casual_hour': '#FFA500', 'registered_hour': '#1F77B4'},
        labels={'workingday_hour': 'Hari Kerja', 'Rata-rata Sewa': 'Jumlah Sewa'}
    )
    st.plotly_chart(fig1, use_container_width=True)
elif view_q1 == "Fokus Casual":
    fig1 = px.bar(segment_data, x='workingday_hour', y='casual_hour', color_discrete_sequence=['#FFA500'], title="Rata-rata Sewa Casual")
    st.plotly_chart(fig1, use_container_width=True)
else:
    fig1 = px.bar(segment_data, x='workingday_hour', y='registered_hour', color_discrete_sequence=['#1F77B4'], title="Rata-rata Sewa Registered")
    st.plotly_chart(fig1, use_container_width=True)

#Visualisasi 2
st.subheader("2. Dampak Cuaca terhadap Penyewaan")
weather_impact = filtered_df.groupby('weathersit_hour')['cnt_hour'].mean().reset_index()
weather_order = ['Cerah', 'Berkabut', 'Hujan Ringan']
weather_impact = weather_impact[weather_impact['weathersit_hour'].isin(weather_order)]

fig2 = px.bar(
    weather_impact, x='weathersit_hour', y='cnt_hour', 
    color='weathersit_hour', category_orders={"weathersit_hour": weather_order},
    color_discrete_sequence=px.colors.sequential.Tealgrn,
    labels={'cnt_hour': 'Rata-rata Sewa', 'weathersit_hour': 'Kondisi Cuaca'}
)
st.plotly_chart(fig2, use_container_width=True)

#Visualisasi 3
st.subheader("3. Pola Waktu Sewa Hari Kerja")
if 'time_category' in filtered_df.columns:
    view_q3 = st.radio("Pilih Tipe Pengguna:", ["Casual", "Registered"], horizontal=True, key="q3_radio")
    
    working_pattern = filtered_df[filtered_df['workingday_hour'] == 'Ya'].groupby('time_category')[['casual_hour', 'registered_hour']].mean()
    working_pattern = working_pattern.reindex(['Pagi', 'Siang', 'Sore', 'Malam']).reset_index()
    
    if view_q3 == "Casual":
        fig3 = px.bar(
            working_pattern, x='time_category', y='casual_hour',
            color_discrete_sequence=['#FFA500'],
            labels={'casual_hour': 'Rata-rata Sewa', 'time_category': 'Waktu'},
            title="Pola Harian Pengguna Casual (Hari Kerja)"
        )
    else:
        fig3 = px.bar(
            working_pattern, x='time_category', y='registered_hour',
            color_discrete_sequence=['#1F77B4'],
            labels={'registered_hour': 'Rata-rata Sewa', 'time_category': 'Waktu'},
            title="Pola Harian Pengguna Registered (Hari Kerja)"
        )
    st.plotly_chart(fig3, use_container_width=True)
else:
    st.error("Kolom 'time_category' tidak ditemukan!")

#WM
st.divider()
st.caption('Copyright (c) Happy Ending Forever - Dicoding Data Analysis Project 2026')