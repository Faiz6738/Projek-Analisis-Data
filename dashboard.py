# import library
from multiprocessing import Value
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import streamlit as st

# import dataset
bike_df = pd.read_csv('hour_data_fix.csv')

# format tipe data ke format datetime dan reset index
bike_df.reset_index(inplace=True)
bike_df['datetime'] = pd.to_datetime(bike_df['datetime'])

# membuat komponen filter
min_date = bike_df['datetime'].min()
max_date = bike_df['datetime'].max()

# Memberikan judul dashboard
st.title('Dashboard Bike Sharing Dataset')

#Memberikan tab
tab1, tab2, tab3 = st.tabs(["Total Sewa", "Pengaruh Cuaca dan Musim", "Analisis Lanjutan"])
 
with tab1:
    #Memberikan total sewa rental
    total = bike_df.total.sum()
    st.metric("Total Sewa", value=total)

    #Memberikan subheader Total Sewa Pertahun
    st.subheader('Total Sewa Tahunan')

    #Memberikan bar chart
    sns.set_style('whitegrid')
    sns.set_context('talk')
    fig, ax = plt.subplots(figsize=(15, 6))
    date_colors = {"2011": "#90E0EF", "2012": "#0077B6"}
    sns.barplot(data=bike_df.groupby(by=bike_df["datetime"].dt.year.astype(str)).agg({
                'total': 'sum'
                }).reset_index(),
                x='datetime',
                y='total',
                palette=date_colors,
                ax=ax
                )

    ax.set_xlabel('Tahun')

    # Menambahkan angka di atas bar
    for container in ax.containers:
        ax.bar_label(container, fontsize=12)
    
    st.pyplot(fig)

    #Memberikan subheader Presentase Total Sewa Pertahun
    st.subheader('Presentase Total Sewa Tahunan')
    #Memberikan pie chart
    fig, ax = plt.subplots(figsize=(12, 12))
    plt.pie(
    data=bike_df.groupby(by=bike_df["datetime"].dt.year).agg({
        'total': 'sum'
        }).reset_index(),
        x='total',
        labels='datetime',
        colors = ("#90E0EF", "#0077B6"),
        wedgeprops={'width': 0.65},
        textprops={'color':"black"},
        autopct='%1.1f%%'
    )
    plt.show()

    st.pyplot(fig)
 
with tab2:
    #Memberikan subheader 
    st.subheader('Total Sewa Berdasarkan Cuaca')

    # Plot bar
    fig, ax = plt.subplots(figsize=(25, 15))

    colors_a = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(data=bike_df.groupby(by="weather").agg({
                "total": "sum"
                }).sort_values(by="total", ascending=False).reset_index(),
                x='weather',
                y='total',
                palette=colors_a,
                ax=ax)

    # Set judul dan label sumbu
    ax.set_xlabel('Cuaca', fontsize=25)

    # Menambahkan angka di atas bar
    for container in ax.containers:
        ax.bar_label(container, fontsize=25)
    
    # Menambahkan legend untuk menjelaskan makna dari setiap angka di sumbu x
    legend_labels = {
        "1": "Cera, Sedikit Berawan, Berawan sebagian",
        "2": "Kabut + Berawan, Kabut + Awan pecah, Kabut + Sedikit awan, Kabut",
        "3": "Salju Ringan, Hujan Ringan + Badai Petir + Awan Tersebar, Hujan Ringan + Awan Tersebar",
        "4": "Hujan Lebat + Palet Es + Badai Petir + Kabut, Salju + Kabut"
    }
    legend_elements = [plt.Line2D([0], [0], marker='o', color='w', label=label, markerfacecolor=color, markersize=10) 
                    for label, color in zip(legend_labels.values(), colors_a)]
    ax.legend(handles=legend_elements, labels=legend_labels.values(), loc='upper right', fontsize=20)
    st.pyplot(fig)
    

    #Memberikan subheader 
    st.subheader('Total Sewa Berdasarkan Musim')

    # Plot bar
    fig, ax = plt.subplots(figsize=(25, 15))

    colors_a = ["#D3D3D3", "#D3D3D3", "#72BCD4", "#D3D3D3"]

    sns.barplot(data=bike_df.groupby(by="season").agg({
                "total": "sum"
                }).sort_values(by="total", ascending=False).reset_index(),
                x='season',
                y='total',
                palette=colors_a,
                ax=ax)

    # Set judul dan label sumbu
    ax.set_xlabel('Musim', fontsize=25)

    #Menambahkan angka di atas bar
    for container in ax.containers:
        ax.bar_label(container, fontsize=30)

    # Ganti nama di bawah bar plot
    ax.set_xticklabels(['Semi', 'Panas', 'Gugur', 'Dingin'], fontsize=30)

    st.pyplot(fig)


with tab3:
    # membuat distribusi temperature, kelembapan udara, dan kecepatan angin
    st.subheader('Distribusi Temperatur, Kelembapan Udara, & Kecepatan Angin')

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5)) 

    # distribusi temperatur 
    sns.histplot(data=np.log(bike_df['temp']),
            kde=True,
            ax=ax[0])

    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Temperatur", loc="center", fontsize=12)
    ax[0].tick_params(axis ='y', labelsize=10)
    ax[0].tick_params(axis ='x', labelsize=10)

    # distribusi kelembapan udara
    sns.histplot(data=np.log(bike_df['hum']),
            kde=True,
            ax=ax[1])

    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("Kelembapan Udara", loc="center", fontsize=12)
    ax[1].tick_params(axis ='y', labelsize=10)
    ax[1].tick_params(axis ='x', labelsize=10)
    st.pyplot(fig)


    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5)) 
    # distribusi kec. angin
    sns.histplot(data=np.log(bike_df['windspeed']),
            kde=True,
            ax=ax[0])

    ax[0].set_ylabel(None)
    ax[0].set_xlabel(None)
    ax[0].set_title("Kecepatan Angin", loc="center", fontsize=12)
    ax[0].tick_params(axis ='y', labelsize=10)
    ax[0].tick_params(axis ='x', labelsize=10)

    #distribusi variabel total
    sns.histplot(data=np.log(bike_df['total']),
            kde=True,
            ax=ax[1])

    ax[1].set_ylabel(None)
    ax[1].set_xlabel(None)
    ax[1].set_title("Distribusi Total Sewa", loc="center", fontsize=12)
    ax[1].tick_params(axis ='y', labelsize=10)
    ax[1].tick_params(axis ='x', labelsize=10)

    st.pyplot(fig)

    # Nilai Korelasi
    st.subheader('Korelasi Spearman dari Total Sewa vs Temperatur, Kelembapan Udara, & Kecepatan Udara')

    fig, ax = plt.subplots(figsize=(20,20))

    corr = bike_df[['temp',
            'hum', 
            'windspeed', 
            'total']].corr(method='spearman')
    
    sns.heatmap(data=corr,
                annot=True, cmap='Blues',
                annot_kws={'size': 30})
    ax.tick_params(axis='x', labelsize=30)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

st.caption('Copyright (c) Nur Faiz Ramadhan 2023')