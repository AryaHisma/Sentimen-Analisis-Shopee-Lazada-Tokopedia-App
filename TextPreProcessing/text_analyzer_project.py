# from praprocessing_data import Preprocessor as pp
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import nltk
import seaborn as sns
import numpy as np 
from nltk.util import ngrams
from collections import Counter
from wordcloud import WordCloud
import networkx as nx
import plotly.express as px
import plotly.graph_objects as go
from sklearn.feature_extraction.text import CountVectorizer
import scipy.stats as stats
import plotly.graph_objects as go
from scipy.stats import gaussian_kde
import plotly.figure_factory as ff
import streamlit as st
import re

# nltk.download('punkt')

sns.set(style='whitegrid')


'''
Distribusi Frekuensi jumlah huruf pada suatu data
Distribusi Frekuensi jumlah kata pada suatu data
Distribusi Frekuensi panjang kata rata-rata pada suatu data
Distribusi Frekuensi kata yang sering keluar
Distribusi N-gram
Network Analysis
'''

# def freq_of_char(df, col):
#     """
#     Menampilkan histogram distribusi frekuensi jumlah karakter per teks dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk jumlah karakter.
#     """
#     plt.figure(1, figsize=(10, 6))

#     bins_range = np.arange(0, 250, 10)
#     chars = df[col].str.len()

#     sns.histplot(chars, bins=bins_range, kde=True, color='skyblue')
#     plt.title('Distribusi Frekuensi Jumlah Karakter per Teks', fontsize=16)
#     plt.xlabel('Jumlah Karakter', fontsize=14)
#     plt.ylabel('Frekuensi', fontsize=14)
#     plt.axvline(chars.mean(), color='red', linestyle='dashed', linewidth=1)
#     plt.text(chars.mean() + 5, plt.ylim()[1] * 0.9, f'Mean: {chars.mean():.2f}', color='red')
#     plt.show()

def freq_of_char(df, col):
    """
    Menampilkan histogram distribusi frekuensi jumlah karakter per teks dalam kolom yang ditentukan.
    
    Parameters:
    - df: DataFrame yang berisi teks.
    - col: Nama kolom yang akan dianalisis untuk jumlah karakter.
    
    Returns:
    - fig: Objek figure Matplotlib.
    - ax: Objek axes Matplotlib.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Rentang bins untuk histogram
    bins_range = np.arange(0, 250, 10)
    chars = df[col].str.len()
    
    # Membuat histogram dengan KDE
    sns.histplot(chars, bins=bins_range, kde=True, color='skyblue', ax=ax)
    ax.set_title('Distribusi Frekuensi Jumlah Karakter per Teks', fontsize=16)
    ax.set_xlabel('Jumlah Karakter', fontsize=14)
    ax.set_ylabel('Frekuensi', fontsize=14)
    
    # Menambahkan garis putus-putus untuk rata-rata
    mean_char = chars.mean()
    ax.axvline(mean_char, color='red', linestyle='dashed', linewidth=1)
    ax.text(mean_char + 5, ax.get_ylim()[1] * 0.9, f'Mean: {mean_char:.2f}', color='red')
    
    return fig, ax

# def freq_of_char(df, col):
#     """
#     Menampilkan histogram distribusi frekuensi jumlah karakter per teks dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk jumlah karakter.
    
#     Returns:
#     - fig: Matplotlib figure object untuk digunakan di Streamlit.
#     """
#     # Membuat objek figure dan axis
#     fig, ax = plt.subplots(figsize=(10, 6))

#     # Menentukan rentang bins
#     bins_range = np.arange(0, 250, 10)
#     # Menghitung jumlah karakter dalam setiap teks
#     chars = df[col].str.len()

#     # Membuat histogram menggunakan Seaborn
#     sns.histplot(chars, bins=bins_range, kde=True, color='skyblue', ax=ax)

#     # Menambahkan judul dan label
#     ax.set_title('Distribusi Frekuensi Jumlah Karakter per Teks', fontsize=16)
#     ax.set_xlabel('Jumlah Karakter', fontsize=14)
#     ax.set_ylabel('Frekuensi', fontsize=14)

#     # Menambahkan garis vertikal untuk nilai rata-rata
#     mean_value = chars.mean()
#     ax.axvline(mean_value, color='red', linestyle='dashed', linewidth=1)
#     ax.text(mean_value + 5, ax.get_ylim()[1] * 0.9, f'Mean: {mean_value:.2f}', color='red')

#     # Menambahkan label untuk nilai maksimum frekuensi
#     n, bins, patches = ax.hist(chars, bins=bins_range, color='skyblue', edgecolor='black')
#     max_freq = n.max()
#     max_freq_bin = bins[n.argmax()]
#     ax.text(max_freq_bin + 5, max_freq, f'Max Freq: {max_freq}', color='blue', verticalalignment='bottom')

#     plt.tight_layout()
#     # Mengembalikan objek figure
#     return fig

# def freq_of_char(df, col):
#     """
#     Menampilkan histogram distribusi frekuensi jumlah karakter per teks dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk jumlah karakter.
    
#     Returns:
#     - fig: Matplotlib figure object untuk digunakan di Streamlit.
#     """
#     # Mengatasi None atau NaN dengan menggantinya menjadi string kosong
#     df[col] = df[col].fillna('')

#     # Membuat objek figure dan axis
#     fig, ax = plt.subplots(figsize=(10, 8))

#     # Menentukan rentang bins
#     bins_range = np.arange(0, 250, 10)
#     # Menghitung jumlah karakter dalam setiap teks
#     chars = df[col].str.len()

#     # Membuat histogram menggunakan Seaborn
#     sns.histplot(chars, bins=bins_range, kde=True, color='skyblue', ax=ax)

#     # Menambahkan judul dan label
#     ax.set_title('Distribusi Frekuensi Jumlah Karakter per Teks', fontsize=16)
#     ax.set_xlabel('Jumlah Karakter', fontsize=14)
#     ax.set_ylabel('Frekuensi', fontsize=14)

#     # Menambahkan garis vertikal untuk nilai rata-rata
#     mean_value = chars.mean()
#     ax.axvline(mean_value, color='red', linestyle='dashed', linewidth=1)
#     ax.text(mean_value + 5, ax.get_ylim()[1] * 0.9, f'Mean: {mean_value:.2f}', color='red')

#     # Menambahkan label untuk nilai maksimum frekuensi
#     n, bins, patches = ax.hist(chars, bins=bins_range, color='skyblue', edgecolor='black')
#     max_freq = n.max()
#     max_freq_bin = bins[n.argmax()]
#     ax.text(max_freq_bin + 5, max_freq, f'Max Freq: {max_freq}', color='blue', verticalalignment='bottom')

#     plt.tight_layout()
#     # Mengembalikan objek figure
#     return fig

# def freq_of_char(df, col):
#     """
#     Menampilkan histogram distribusi frekuensi jumlah karakter per teks dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk jumlah karakter.
    
#     Returns:
#     - fig: Matplotlib figure object untuk digunakan di Streamlit.
#     """
#     # Mengatasi None atau NaN dengan menggantinya menjadi string kosong
#     df[col] = df[col].fillna('')

#     # Membuat objek figure dan axis
#     fig, ax = plt.subplots(figsize=(10, 8))

#     # Menentukan rentang bins
#     bins_range = np.arange(0, 250, 10)
#     # Menghitung jumlah karakter dalam setiap teks
#     chars = df[col].str.len()

#     # Membuat histogram menggunakan Seaborn
#     sns.histplot(chars, bins=bins_range, kde=True, color='skyblue', ax=ax)

#     # Menambahkan judul dan label
#     ax.set_title('Distribusi Frekuensi Jumlah Karakter per Teks', fontsize=16)
#     ax.set_xlabel('Jumlah Karakter', fontsize=14)
#     ax.set_ylabel('Frekuensi', fontsize=14)

#     # Menambahkan garis vertikal untuk nilai rata-rata
#     mean_value = chars.mean()
#     ax.axvline(mean_value, color='red', linestyle='dashed', linewidth=1)
#     ax.text(mean_value + 5, ax.get_ylim()[1] * 0.9, f'Mean: {mean_value:.2f}', color='red')

#     # Menambahkan label untuk nilai maksimum frekuensi
#     max_freq = chars.value_counts().max()
#     max_freq_bin = chars.value_counts().idxmax()
#     ax.text(max_freq_bin + 5, max_freq, f'Max Freq: {max_freq}', color='blue', verticalalignment='bottom')

#     plt.tight_layout()
#     # Mengembalikan objek figure
#     return fig

# def freq_of_char_plotly(df, col):
#     """
#     Menampilkan histogram interaktif distribusi frekuensi jumlah karakter per teks dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk jumlah karakter.
    
#     Returns:
#     - fig: Plotly figure object untuk digunakan di Streamlit.
#     """
#     # Mengatasi None atau NaN dengan menggantinya menjadi string kosong
#     df[col] = df[col].fillna('')

#     # Menghitung jumlah karakter dalam setiap teks
#     df['char_count'] = df[col].str.len()

#     # Membuat histogram interaktif menggunakan Plotly
#     fig = px.histogram(df, x='char_count', nbins=25, title='Distribusi Frekuensi Jumlah Karakter per Teks',
#                        labels={'char_count': 'Jumlah Karakter'},
#                        template='plotly_white')

#     # Menambahkan garis vertikal untuk nilai rata-rata
#     mean_value = df['char_count'].mean()
#     fig.add_vline(x=mean_value, line_dash="dash", line_color="red",
#                   annotation_text=f'Mean: {mean_value:.2f}', annotation_position="top right")

#     # Menambahkan label untuk nilai maksimum frekuensi
#     max_freq = df['char_count'].value_counts().max()
#     max_freq_bin = df['char_count'].value_counts().idxmax()
#     fig.add_annotation(x=max_freq_bin, y=max_freq, text=f'Max Freq: {max_freq}', 
#                        showarrow=True, arrowhead=2, ax=20, ay=-40, bgcolor="blue", opacity=0.7, font=dict(color="white"))

#     # Update layout for better visuals
#     fig.update_layout(
#         xaxis_title='Jumlah Karakter',
#         yaxis_title='Frekuensi',
#         bargap=0.1
#     )

#     return fig

# def plot_letter_frequency_distribution(df, column, bins):
#     """
#     Menampilkan distribusi frekuensi jumlah huruf pada kolom tertentu menggunakan Altair.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - column: Nama kolom yang akan dianalisis.
#     - bins: Jumlah bin untuk histogram.
    
#     Returns:
#     - chart: Objek Altair chart yang dapat digunakan di Streamlit.
#     """
#     # Menghitung jumlah huruf untuk setiap entri teks di kolom yang ditentukan
#     df['length'] = df[column].apply(lambda x: len(str(x)))
    
#     # Membuat DataFrame untuk histogram
#     freq_df = df['length'].value_counts().reset_index()
#     freq_df.columns = ['length', 'frequency']
    
#     # Mendapatkan rentang sumbu x dan y
#     x_max = freq_df['length'].max()
#     y_max = freq_df['frequency'].max()
    
#     # Menentukan garis rata-rata
#     mean_length = df['length'].mean()
    
#     # Membuat histogram
#     histogram = alt.Chart(freq_df).mark_bar().encode(
#         x=alt.X('length:O', title='Jumlah Huruf', bin=alt.Bin(maxbins=bins)),
#         y=alt.Y('frequency:Q', title='Frekuensi', scale=alt.Scale(domain=[0, y_max])),
#         tooltip=['length', 'frequency']
#     )
    
#     # Membuat garis rata-rata
#     mean_line = alt.Chart(pd.DataFrame({'mean_length': [mean_length]})).mark_rule(color='red', strokeDash=[4, 4]).encode(
#         x=alt.X('mean_length:Q', title='Rata-Rata Jumlah Huruf')
#     )
    
#     # Menggabungkan histogram dan garis rata-rata
#     final_chart = alt.layer(
#         histogram,
#         mean_line
#     ).properties(
#         title={
#             'text': 'Distribusi Frekuensi Jumlah Huruf',
#             'fontSize': 16,
#             'font': 'Arial',
#             'anchor': 'middle',
#             'color': 'black'
#         },
#         width=600,
#         height=400
#     ).configure_view(
#         stroke='none'  # Menghapus garis batas di sekitar chart
#     ).configure_axis(
#         grid=False,  # Menghilangkan grid
#         tickColor='black',  # Warna sumbu x dan y
#         titleColor='black'  # Warna label sumbu x dan y
#     ).configure_title(
#         fontSize=16,
#         font='Arial',
#         anchor='middle',
#         color='black'
#     )
    
#     return final_chart

def plot_letter_frequency_distribution(df, column, bins):
    """
    Menampilkan distribusi frekuensi jumlah huruf pada kolom tertentu menggunakan Plotly,
    termasuk garis KDE (Kernel Density Estimation).
    
    Parameters:
    - df: DataFrame yang berisi teks.
    - column: Nama kolom yang akan dianalisis.
    - bins: Jumlah bin untuk histogram.
    
    Returns:
    - fig: Objek Plotly figure yang dapat digunakan di Streamlit.
    """
    # Menghitung jumlah huruf untuk setiap entri teks di kolom yang ditentukan
    df['length'] = df[column].apply(lambda x: len(str(x)))
    
    # Menghitung frekuensi jumlah huruf
    counts, edges = np.histogram(df['length'], bins=bins)
    
    # Menghitung midpoints untuk setiap bin
    bin_centers = (edges[:-1] + edges[1:]) / 2
    
    # Menghitung KDE
    kde = gaussian_kde(df['length'])
    kde_x = np.linspace(df['length'].min(), df['length'].max(), 1000)
    kde_y = kde.pdf(kde_x)
    kde_y = kde_y * (edges[1] - edges[0]) * len(df['length']) / kde_y.sum()  # Normalisasi KDE
    
    # Membuat histogram
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=bin_centers,
        y=counts,
        width=(edges[1] - edges[0]) * 0.8,  # Menambahkan jarak antar bin
        marker_color='skyblue',
        showlegend=False  # Menghilangkan legend
    ))
    
    # Menambahkan garis KDE
    fig.add_trace(go.Scatter(
        x=kde_x,
        y=kde_y,
        mode='lines',
        line=dict(color='green', width=2),
        showlegend=False  # Menghilangkan legend
    ))
    
    # Menghitung rata-rata jumlah huruf
    mean_length = df['length'].mean()
    
    # Menambahkan garis rata-rata
    fig.add_shape(
        type='line',
        x0=mean_length, x1=mean_length,
        y0=0, y1=max(counts),
        line=dict(color='red', dash='dash', width=2),
        name='Rata-Rata'
    )
    
    # Menambahkan label pada garis rata-rata
    fig.add_annotation(
        x=mean_length,
        y=max(counts), #a * 0.9,
        text=f'Rata-Rata: {mean_length:.2f}',
        showarrow=True,
        arrowhead=2,
        font=dict(color='red', size=12)
    )
    
    # Mengatur layout
    fig.update_layout(
        title={
            'text': 'Distribusi Frekuensi Jumlah Huruf',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': 'black'}
        },
        xaxis_title='Jumlah Huruf',
        yaxis_title='Frekuensi',
        xaxis=dict(
            range=[0, max(df['length']) + 100],  # Interval sumbu x dimulai dari 0
            dtick=200,  # Interval sumbu x
            title_font=dict(size=14, color='black'),
            tickfont=dict(size=12, color='black'),
            showline=True,  # Menampilkan garis sumbu x
            linecolor='black'  # Warna garis sumbu x
        ),
        yaxis=dict(
            range=[0, max(counts) + 100],  # Interval sumbu y dimulai dari 0
            dtick=500,  # Interval sumbu y
            title_font=dict(size=14, color='black'),
            tickfont=dict(size=12, color='black'),
            showline=True,  # Menampilkan garis sumbu y
            linecolor='black'  # Warna garis sumbu y
        ),
        plot_bgcolor='white',  # Background putih
        paper_bgcolor='white',  # Background plotly putih
        margin=dict(l=40, r=40, t=60, b=40),  # Margin
        bargap=0.2  # Jarak antar bar histogram
    )
    
    return fig

# def freq_of_words(df, col):
#     """
#     Menampilkan histogram distribusi frekuensi jumlah kata per teks dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk jumlah kata.
#     """
#     plt.figure(2, figsize=(10, 6))

#     bins_range = np.arange(0, 50)
#     words = df[col].str.split().map(len)

#     sns.histplot(words, bins=bins_range, kde=True, color='salmon')
#     plt.title('Distribusi Frekuensi Jumlah Kata per Teks', fontsize=16)
#     plt.xlabel('Jumlah Kata', fontsize=14)
#     plt.ylabel('Frekuensi', fontsize=14)
#     plt.axvline(words.mean(), color='blue', linestyle='dashed', linewidth=1)
#     plt.text(words.mean() + 1, plt.ylim()[1] * 0.9, f'Mean: {words.mean():.2f}', color='blue')
#     plt.show()

# def freq_of_words(df, col):
#     """
#     Menampilkan histogram distribusi frekuensi jumlah kata per teks dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk jumlah kata.
    
#     Returns:
#     - fig: Matplotlib figure object untuk digunakan di Streamlit.
#     """
#     # Membuat objek figure dan axis
#     fig, ax = plt.subplots(figsize=(10, 8))

#     # Menentukan rentang bins
#     bins_range = np.arange(0, 50)
#     # Menghitung jumlah kata dalam setiap teks
#     words = df[col].str.split().map(len)

#     # Membuat histogram menggunakan Seaborn
#     sns.histplot(words, bins=bins_range, kde=True, color='salmon', ax=ax)

#     # Menambahkan judul dan label
#     ax.set_title('Distribusi Frekuensi Jumlah Kata per Teks', fontsize=16)
#     ax.set_xlabel('Jumlah Kata', fontsize=14)
#     ax.set_ylabel('Frekuensi', fontsize=14)

#     # Menambahkan garis vertikal untuk nilai rata-rata
#     mean_value = words.mean()
#     ax.axvline(mean_value, color='blue', linestyle='dashed', linewidth=1)
#     ax.text(mean_value + 1, ax.get_ylim()[1] * 0.9, f'Mean: {mean_value:.2f}', color='blue')

#     # Menambahkan label untuk nilai maksimum frekuensi
#     n, bins, patches = ax.hist(words, bins=bins_range, color='salmon', edgecolor='black')
#     max_freq = n.max()
#     max_freq_bin = bins[n.argmax()]
#     ax.text(max_freq_bin + 1, max_freq, f'Max Freq: {max_freq}', color='green', verticalalignment='bottom')

#     plt.tight_layout()
#     # Mengembalikan objek figure
#     return fig


def freq_of_words_plotly(df, col):
    """
    Menampilkan histogram distribusi frekuensi jumlah kata per teks dalam kolom yang ditentukan.
    
    Parameters:
    - df: DataFrame yang berisi teks.
    - col: Nama kolom yang akan dianalisis untuk jumlah kata.
    
    Returns:
    - fig: Plotly figure object untuk digunakan di Streamlit.
    """
    # Menghitung jumlah kata dalam setiap teks
    words = df[col].str.split().apply(len)
    
    # Menentukan rentang bins
    bins_range = np.arange(0, 50, 1)

    # Hitung histogram
    hist_values, bin_edges = np.histogram(words, bins=bins_range, density=False)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Hitung KDE
    kde = gaussian_kde(words, bw_method=0.3)  # Bandwidth method dapat disesuaikan
    kde_x = np.linspace(0, 50, 1000)
    kde_y = kde.pdf(kde_x)
    
    # Menyesuaikan KDE dengan skala histogram
    kde_y = kde_y * hist_values.max() * (bin_edges[1] - bin_edges[0]) / kde_y.max()

    # Membuat histogram dan KDE menggunakan Plotly
    fig = go.Figure()

    # Tambahkan histogram
    fig.add_trace(go.Bar(
        x=bin_centers,
        y=hist_values,
        marker_color='skyblue',
        name='Frekuensi',
        opacity=0.7
    ))

    # Tambahkan KDE
    fig.add_trace(go.Scatter(
        x=kde_x,
        y=kde_y,
        mode='lines',
        line=dict(color='green', width=2),
        name='KDE'
    ))

    # Mengatur layout
    fig.update_layout(
        title={'text': 'Distribusi Frekuensi Jumlah Kata per Teks', 'x': 0.2, 'font': {'color': 'black', 'size': 15}},
        xaxis_title='Jumlah Kata',
        yaxis_title='Frekuensi',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            gridcolor='lightgrey',
            tick0=0,
            dtick=10,  # Interval setiap 10
            range=[0, 50],  # Batas maksimum sumbu x
            title_font=dict(color='black'),
            tickfont=dict(color='black'),
            zeroline=True,  # Menampilkan garis sumbu x
            zerolinecolor='black',  # Warna garis sumbu x
            zerolinewidth=2  # Ketebalan garis sumbu x
        ),
        yaxis=dict(
            gridcolor='lightgrey',
            tick0=0,
            dtick=500,  # Interval setiap 500
            range=[0, max(hist_values) + 500],  # Batas maksimum sumbu y   
            title_font=dict(color='black'),
            tickfont=dict(color='black'),
            zeroline=True,  # Menampilkan garis sumbu y
            zerolinecolor='black',  # Warna garis sumbu y
            zerolinewidth=2  # Ketebalan garis sumbu y
        ),
        font=dict(color='black'),  # Mengatur warna teks pada keseluruhan plot
        showlegend=False  # Menghilangkan legend
    )
    
    # Menambahkan garis vertikal untuk nilai rata-rata
    mean_value = words.mean()
    fig.add_shape(type='line',
                  x0=mean_value, y0=0, x1=mean_value, y1=max(hist_values) + 500,
                  line=dict(color='red', dash='dash', width=2))
    fig.add_annotation(x=mean_value, y=max(hist_values) - 500,
                       text=f'Rata-rata: {mean_value:.2f}',
                       showarrow=True,
                       arrowhead=1,
                       ax=30,
                       ay=-40,
                       font=dict(color='red', size=12))

    return fig
    

def freq_of_words_plotly_analisis(df, col):
    """
    Menampilkan histogram distribusi frekuensi jumlah kata per teks dalam kolom yang ditentukan.
    
    Parameters:
    - df: DataFrame yang berisi teks.
    - col: Nama kolom yang akan dianalisis untuk jumlah kata.
    
    Returns:
    - fig: Plotly figure object untuk digunakan di Streamlit.
    """
    # Mengganti nilai NaN dengan string kosong, atau memeriksa apakah elemen adalah string
    df[col] = df[col].fillna('')  # Mengganti NaN dengan string kosong
    words = df[col].apply(lambda x: len(str(x).split()))  # Menghitung jumlah kata hanya untuk string
    
    # Menentukan rentang bins
    bins_range = np.arange(0, 50, 1)

    # Hitung histogram
    hist_values, bin_edges = np.histogram(words, bins=bins_range, density=False)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Hitung KDE
    kde = gaussian_kde(words, bw_method=0.3)  # Bandwidth method dapat disesuaikan
    kde_x = np.linspace(0, 50, 1000)
    kde_y = kde.pdf(kde_x)
    
    # Menyesuaikan KDE dengan skala histogram
    kde_y = kde_y * hist_values.max() * (bin_edges[1] - bin_edges[0]) / kde_y.max()

    # Membuat histogram dan KDE menggunakan Plotly
    fig = go.Figure()

    # Tambahkan histogram
    fig.add_trace(go.Bar(
        x=bin_centers,
        y=hist_values,
        marker_color='skyblue',
        name='Frekuensi',
        opacity=0.7
    ))

    # Tambahkan KDE
    fig.add_trace(go.Scatter(
        x=kde_x,
        y=kde_y,
        mode='lines',
        line=dict(color='green', width=2),
        name='KDE'
    ))

    # Mengatur layout
    fig.update_layout(
        title={'text': 'Distribusi Frekuensi Jumlah Kata per Teks', 'x': 0.2, 'font': {'color': 'black', 'size': 15}},
        xaxis_title='Jumlah Kata',
        yaxis_title='Frekuensi',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            gridcolor='lightgrey',
            tick0=0,
            dtick=10,  # Interval setiap 10
            range=[0, 50],  # Batas maksimum sumbu x
            title_font=dict(color='black'),
            tickfont=dict(color='black'),
            zeroline=True,  # Menampilkan garis sumbu x
            zerolinecolor='black',  # Warna garis sumbu x
            zerolinewidth=2  # Ketebalan garis sumbu x
        ),
        yaxis=dict(
            gridcolor='lightgrey',
            tick0=0,
            dtick=500,  # Interval setiap 500
            range=[0, max(hist_values) + 500],  # Batas maksimum sumbu y   
            title_font=dict(color='black'),
            tickfont=dict(color='black'),
            zeroline=True,  # Menampilkan garis sumbu y
            zerolinecolor='black',  # Warna garis sumbu y
            zerolinewidth=2  # Ketebalan garis sumbu y
        ),
        font=dict(color='black'),  # Mengatur warna teks pada keseluruhan plot
        showlegend=False  # Menghilangkan legend
    )
    
    # Menambahkan garis vertikal untuk nilai rata-rata
    mean_value = words.mean()
    fig.add_shape(type='line',
                  x0=mean_value, y0=0, x1=mean_value, y1=max(hist_values) + 500,
                  line=dict(color='red', dash='dash', width=2))
    fig.add_annotation(x=mean_value, y=max(hist_values) - 500,
                       text=f'Rata-rata: {mean_value:.2f}',
                       showarrow=True,
                       arrowhead=1,
                       ax=30,
                       ay=-40,
                       font=dict(color='red', size=12))

    return fig


# def freq_meanlength_word(df, col):
#     """
#     Menampilkan histogram distribusi frekuensi panjang kata rata-rata dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk panjang kata rata-rata.
#     """
#     plt.figure(3, figsize=(10, 6))
    
#     # Hitung panjang rata-rata setiap kata dalam teks
#     words = df[col].str.split().apply(lambda x: [len(i) for i in x]).map(np.mean)

#     sns.histplot(words, kde=True, color='salmon')
#     plt.title('Distribusi Frekuensi Panjang Kata Rata-Rata', fontsize=16)
#     plt.xlabel('Panjang Rata-Rata Kata', fontsize=14)
#     plt.ylabel('Frekuensi', fontsize=14)
#     plt.axvline(words.mean(), color='blue', linestyle='dashed', linewidth=1)
#     plt.text(words.mean() + 0.1, plt.ylim()[1] * 0.9, f'Mean: {words.mean():.2f}', color='blue')
#     plt.show()


# def freq_meanlength_word(df, col):
#     """
#     Menampilkan histogram distribusi frekuensi panjang kata rata-rata dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk panjang kata rata-rata.
    
#     Returns:
#     - fig: Matplotlib figure object untuk digunakan di Streamlit.
#     """
#     # Membuat objek figure dan axis
#     fig, ax = plt.subplots(figsize=(10, 8))
    
#     # Hitung panjang rata-rata setiap kata dalam teks
#     words = df[col].str.split().apply(lambda x: [len(i) for i in x]).map(np.mean)

#     # Membuat histogram menggunakan Seaborn
#     sns.histplot(words, kde=True, color='salmon', ax=ax)

#     # Menambahkan judul dan label
#     ax.set_title('Distribusi Frekuensi Panjang Kata Rata-Rata', fontsize=16)
#     ax.set_xlabel('Panjang Rata-Rata Kata', fontsize=14)
#     ax.set_ylabel('Frekuensi', fontsize=14)

#     # Menambahkan garis vertikal untuk nilai rata-rata
#     mean_value = words.mean()
#     ax.axvline(mean_value, color='blue', linestyle='dashed', linewidth=1)
#     ax.text(mean_value + 0.1, ax.get_ylim()[1] * 0.9, f'Mean: {mean_value:.2f}', color='blue')

#     # Menambahkan label untuk nilai maksimum frekuensi
#     n, bins, patches = ax.hist(words, bins=30, color='salmon', edgecolor='black')
#     max_freq = n.max()
#     max_freq_bin = bins[n.argmax()]
#     ax.text(max_freq_bin + 0.1, max_freq, f'Max Freq: {max_freq}', color='green', verticalalignment='bottom')

#     plt.tight_layout()
#     # Mengembalikan objek figure
#     return fig


def freq_meanlength_word(df, col):
    """
    Menampilkan histogram distribusi frekuensi panjang kata rata-rata dalam kolom yang ditentukan.
    
    Parameters:
    - df: DataFrame yang berisi teks.
    - col: Nama kolom yang akan dianalisis untuk panjang kata rata-rata.
    
    Returns:
    - fig: Plotly figure object untuk digunakan di Streamlit.
    """
    # Menghitung panjang rata-rata setiap kata dalam teks
    words_mean_length = df[col].str.split().apply(lambda x: np.mean([len(word) for word in x if len(word) > 0]))

    # Menghilangkan nilai NaN yang mungkin muncul dari teks kosong
    words_mean_length = words_mean_length.dropna()

    # Membuat histogram
    hist_values, bin_edges = np.histogram(words_mean_length, bins=50)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

    # Membuat KDE
    kde = gaussian_kde(words_mean_length, bw_method=0.3)
    kde_x = np.linspace(0, words_mean_length.max(), 1000)
    kde_y = kde.evaluate(kde_x)  # Menggunakan evaluate untuk mendapatkan nilai KDE

    # Menyesuaikan KDE dengan skala histogram tanpa normalisasi
    kde_y = kde_y * (hist_values.max() * (bin_edges[1] - bin_edges[0]))

    # Membuat figure Plotly
    fig = go.Figure()

    # Menambahkan histogram ke figure
    fig.add_trace(go.Bar(
        x=bin_centers,
        y=hist_values,
        marker_color='skyblue',
        name='Frekuensi',
        opacity=0.7
    ))

    # Menambahkan KDE ke figure
    fig.add_trace(go.Scatter(
        x=kde_x,
        y=kde_y,
        mode='lines',
        line=dict(color='green', width=2),
        name='KDE'
    ))

    # Mengatur layout
    fig.update_layout(
        title={'text': 'Distribusi Frekuensi Panjang Kata Rata-Rata', 'x': 0.1, 'font': {'color': 'black', 'size': 16}},
        xaxis_title='Panjang Rata-Rata Kata',
        yaxis_title='Frekuensi',
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            gridcolor='lightgrey',
            tick0=0,
            dtick=10,  # Interval sumbu x setiap 10
            range=[0, max(words_mean_length + 10)],  # Batas maksimum sumbu x
            title_font=dict(color='black'),
            tickfont=dict(color='black'),
            zeroline=True,  # Menampilkan garis sumbu x
            zerolinecolor='black',  # Warna garis sumbu x
            zerolinewidth=2  # Ketebalan garis sumbu x
        ),
        yaxis=dict(
            gridcolor='lightgrey',
            tick0=0,
            dtick=2000,  # Interval sumbu y setiap 500
            range=[0, hist_values.max() + 500],  # Batas maksimum sumbu y
            title_font=dict(color='black'),
            tickfont=dict(color='black'),
            zeroline=True,  # Menampilkan garis sumbu y
            zerolinecolor='black',  # Warna garis sumbu y
            zerolinewidth=2,  # Ketebalan garis sumbu y
            tickformat=',d'  # Format angka pada sumbu y sebagai angka lengkap
        ),
        font=dict(color='black'),  # Mengatur warna teks pada keseluruhan plot
        showlegend=False  # Menghilangkan legend
    )

    # Menambahkan garis vertikal untuk nilai rata-rata
    mean_value = words_mean_length.mean()
    fig.add_shape(type='line',
                  x0=mean_value, y0=0, x1=mean_value, y1=hist_values.max(),
                  line=dict(color='red', dash='dash', width=2))
    fig.add_annotation(x=mean_value, y=hist_values.max(),
                       text=f'Rata-rata: {mean_value:.2f}',
                       showarrow=True,
                       arrowhead=1,
                       ax=30,
                       ay=-30,
                       font=dict(color='red', size=12))

    return fig

    
# def generate_wordcloud(df, col):
#     """
#     Menampilkan WordCloud dari teks dalam kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame yang berisi teks.
#     - col: Nama kolom yang akan dianalisis untuk WordCloud.
#     """
#     # Gabungkan semua teks menjadi satu string
#     text = ' '.join(df[col])

#     # Inisialisasi WordCloud
#     wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

#     # Tampilkan WordCloud
#     plt.figure(figsize=(10, 5))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.axis('off')
#     plt.title('WordCloud untuk Kolom {}'.format(col), fontsize=16)
#     plt.show()


def generate_wordcloud(df, col):
    """
    Menampilkan WordCloud dari teks dalam kolom yang ditentukan.
    
    Parameters:
    - df: DataFrame yang berisi teks.
    - col: Nama kolom yang akan dianalisis untuk WordCloud.
    
    Returns:
    - fig: Matplotlib figure object untuk digunakan di Streamlit.
    """
    # Gabungkan semua teks menjadi satu string
    text = ' '.join(df[col].astype(str))

    # Inisialisasi WordCloud
    wordcloud = WordCloud(width=800, height=550, background_color='white').generate(text)

    # Membuat objek figure dan axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Tampilkan WordCloud
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('WordCloud untuk Kolom {}'.format(col), fontsize=16)

    # Mengembalikan objek figure
    return fig

def generate_wordcloud_text(text):
    """
    Menampilkan WordCloud dari teks yang diberikan.
    
    Parameters:
    - text: Teks yang akan dianalisis untuk WordCloud.
    
    Returns:
    - fig: Matplotlib figure object untuk digunakan di Streamlit.
    """
    # Inisialisasi WordCloud
    wordcloud = WordCloud(width=800, height=550, background_color='white').generate(text)

    # Membuat objek figure dan axis
    fig, ax = plt.subplots(figsize=(10, 10))

    # Tampilkan WordCloud
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('WordCloud', fontsize=16)

    # Mengembalikan objek figure
    return fig


def generate_wordcloud_text_app(text):
    """
    Menampilkan WordCloud dari teks yang diberikan.
    
    Parameters:
    - text: Teks yang akan dianalisis untuk WordCloud.
    
    Returns:
    - fig: Matplotlib figure object untuk digunakan di Streamlit.
    """
    # Inisialisasi WordCloud
    wordcloud = WordCloud(width=300, height=115, background_color='white').generate(text)

    # Membuat objek figure dan axis
    fig, ax = plt.subplots(figsize=(20, 20))

    # Tampilkan WordCloud
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('WordCloud', fontsize=16)

    # Mengembalikan objek figure
    return fig


def most_frequent_words(df, col, n=10):
    """
    Menghitung kata-kata yang paling sering muncul dalam kolom tertentu dan mengembalikannya sebagai DataFrame.
    
    Parameters:
    df (pd.DataFrame): DataFrame yang berisi teks.
    column (str): Nama kolom yang akan dianalisis.
    n (int): Jumlah kata yang paling sering muncul untuk dikembalikan.
    
    Returns:
    pd.DataFrame: DataFrame yang berisi kata dan frekuensinya.
    """
    # Tokenisasi setiap teks menjadi daftar kata
    df['tokens'] = df[col].apply(lambda x: str(x).split())
    
    # Flatten list of lists into a single list of words
    all_words = [word for tokens in df['tokens'] for word in tokens]

    # Hitung frekuensi kemunculan setiap kata
    freq = nltk.probability.FreqDist(all_words)
    
    # Dapatkan kata yang paling sering muncul sesuai parameter n
    most_frequents = freq.most_common(n)
    
    # Buat DataFrame dari daftar kata yang paling sering
    df_most_frequent = pd.DataFrame(most_frequents, columns=['word', 'frequency'])
    
    return df_most_frequent

def most_frequent_words_text(text, n=10):
    """
    Menghitung kata-kata yang paling sering muncul dalam teks dan mengembalikannya sebagai DataFrame.
    
    Parameters:
    text (str): Teks yang akan dianalisis.
    n (int): Jumlah kata yang paling sering muncul untuk dikembalikan.
    
    Returns:
    pd.DataFrame: DataFrame yang berisi kata dan frekuensinya.
    """
    # Tokenisasi teks menjadi daftar kata
    tokens = text.split()
    
    # Hitung frekuensi kemunculan setiap kata
    freq = nltk.probability.FreqDist(tokens)
    
    # Dapatkan kata yang paling sering muncul sesuai parameter n
    most_frequents = freq.most_common(n)
    
    # Buat DataFrame dari daftar kata yang paling sering
    df_most_frequent = pd.DataFrame(most_frequents, columns=['word', 'frequency'])
    
    return df_most_frequent


def generate_ngrams_text(text, n, most_common=10):
    """
    Membuat n-gram dari teks dan mengembalikannya sebagai DataFrame yang berisi n-gram dan frekuensinya.
    
    Parameters:
    text (str): Teks yang akan dianalisis.
    n (int): Jumlah kata dalam n-gram (misalnya 2 untuk bigram, 3 untuk trigram).
    most_common (int): Jumlah n-gram yang paling sering muncul untuk dikembalikan.
    
    Returns:
    pd.DataFrame: DataFrame yang berisi n-gram dan frekuensinya.
    """
    # Tokenisasi teks menjadi kata-kata
    tokens = nltk.word_tokenize(text)
    
    # Membuat n-gram
    ngrams = list(nltk.ngrams(tokens, n))
    
    # Menghitung frekuensi n-gram
    ngram_freq = Counter(ngrams)
    
    # Mendapatkan n-gram yang paling sering muncul
    most_frequent_ngrams = ngram_freq.most_common(most_common)
    
    # Mengonversi hasil ke dalam DataFrame
    df_most_frequent = pd.DataFrame(most_frequent_ngrams, columns=[f'{n}-gram', 'Frequency'])
    
    return df_most_frequent


def df_top_ngram(df, col, n):   # , most_common=50
    """
    Menghitung n-gram yang paling sering muncul dalam kolom yang ditentukan dan mengembalikannya sebagai DataFrame.
    
    Parameters:
    - df: DataFrame dengan kolom teks yang sudah dibersihkan.
    - col: Nama kolom yang berisi teks untuk dianalisis.
    - n: Integer, ukuran dari n-gram.
    - most_common: Integer, jumlah n-gram yang paling sering muncul untuk dikembalikan.
    
    Returns:
    - DataFrame dengan kolom 'n_gram' dan 'frequency'.
    """

    # Gabungkan teks dari kolom yang ditentukan menjadi satu string
    texts = ' '.join(df[col])
    
    # Buat n-gram dari teks yang digabungkan
    ngram = ngrams(texts.split(), n)
    
    # Hitung frekuensi kemunculan setiap n-gram
    counts = Counter(ngram)
    
    # Dapatkan n-gram yang paling umum
    top_ngram = counts.most_common()  #most_common
    
    # Buat DataFrame dari hasil
    df_top_ngram = pd.DataFrame(top_ngram, columns=['n_gram', 'frequency'])
    
    return df_top_ngram

# def generate_ngrams_text(df, column, n):
#     # Menggabungkan seluruh teks dalam kolom yang dituju
#     text_data = df[column].str.cat(sep=' ')
    
#     # Membuat n-gram menggunakan CountVectorizer
#     vectorizer = CountVectorizer(ngram_range=(n, n))
#     ngram_matrix = vectorizer.fit_transform([text_data])
    
#     # Menghitung frekuensi setiap n-gram
#     ngram_counts = ngram_matrix.toarray().flatten()
#     ngrams = vectorizer.get_feature_names_out()
    
#     # Menggabungkan n-gram dengan frekuensinya ke dalam dataframe
#     ngram_df = pd.DataFrame({'N-gram': ngrams, 'Frequency': ngram_counts})
    
#     # Mengurutkan dataframe berdasarkan frekuensi
#     ngram_df = ngram_df.sort_values(by='Frequency', ascending=False).reset_index(drop=True)
    
#     return ngram_df

def top_ngram(df, col, n):   #, most_common=50
    """
    Menghitung n-gram yang paling sering muncul dalam kolom yang ditentukan dan mengembalikannya sebagai DataFrame.
    
    Parameters:
    - df: DataFrame dengan kolom teks yang sudah dibersihkan.
    - col: Nama kolom yang berisi teks untuk dianalisis.
    - n: Integer, ukuran dari n-gram.
    - most_common: Integer, jumlah n-gram yang paling sering muncul untuk dikembalikan.
    
    Returns:
    - DataFrame dengan kolom 'n_gram' dan 'frequency'.
    """

    # Gabungkan teks dari kolom yang ditentukan menjadi satu string
    texts = ' '.join(df[col])
    
    # Buat n-gram dari teks yang digabungkan
    ngram = ngrams(texts.split(), n)
    
    # Hitung frekuensi kemunculan setiap n-gram
    counts = Counter(ngram)
    
    # Dapatkan n-gram yang paling umum
    top_ngram = counts.most_common()    #most_common
    
    return top_ngram

def top_ngram_text(text, n):
    """
    Menghitung n-gram yang paling sering muncul dalam teks yang diberikan dan mengembalikannya sebagai DataFrame.
    
    Parameters:
    - text: String yang berisi teks untuk dianalisis.
    - n: Integer, ukuran dari n-gram.
    
    Returns:
    - DataFrame dengan kolom 'n_gram' dan 'frequency'.
    """
    # Buat n-gram dari teks yang diberikan
    ngram = ngrams(text.split(), n)
    
    # Hitung frekuensi kemunculan setiap n-gram
    counts = Counter(ngram)
    
    # Ubah hasil ke dalam DataFrame
    ngram_df = pd.DataFrame(counts.items(), columns=['n_gram', 'frequency'])
    
    # Urutkan berdasarkan frekuensi dari yang paling sering muncul
    ngram_df = ngram_df.sort_values(by='frequency', ascending=False).reset_index(drop=True)
    
    return ngram_df

def top_ngram_text_most(text, n):
    """
    Menghitung n-gram yang paling sering muncul dalam teks yang diberikan dan mengembalikannya sebagai list of tuples.
    
    Parameters:
    - text: String yang berisi teks untuk dianalisis.
    - n: Integer, ukuran dari n-gram.
    
    Returns:
    - List of tuples dengan format ([word1, word2, ...], frequency).
    """
    # Buat n-gram dari teks yang diberikan
    ngram = ngrams(text.split(), n)
    
    # Hitung frekuensi kemunculan setiap n-gram
    counts = Counter(ngram)
    
    # Ubah hasil ke dalam list of tuples
    result = [((list(ngram)), count) for ngram, count in counts.items()]
    
    # Urutkan berdasarkan frekuensi dari yang paling sering muncul
    result = sorted(result, key=lambda x: x[1], reverse=True)
    
    return result

def combine_top_ngram(df, col, n, most_common=10):
    """
    Menghitung n-gram yang paling sering muncul dalam kolom yang ditentukan dan mengembalikannya sebagai DataFrame.
    
    Parameters:
    - df: DataFrame dengan kolom teks yang sudah dibersihkan.
    - col: Nama kolom yang berisi teks untuk dianalisis.
    - n: Integer, ukuran dari n-gram.
    - most_common: Integer, jumlah n-gram yang paling sering muncul untuk dikembalikan.
    
    Returns:
    - List of tuples dengan n-gram yang digabungkan dan frekuensinya.
    """

    # Gabungkan teks dari kolom yang ditentukan menjadi satu string
    texts = ' '.join(df[col])
    
    # Buat n-gram dari teks yang digabungkan
    ngram = ngrams(texts.split(), n)
    
    # Hitung frekuensi kemunculan setiap n-gram
    counts = Counter(ngram)
    
    # Dapatkan n-gram yang paling umum
    top_ngram = counts.most_common(most_common)
    
    # Gabungkan kata-kata dalam setiap n-gram menjadi dua pasangan kata
    combined_ngrams = [((' '.join(ngram[:2]), ' '.join(ngram[2:])), freq) for ngram, freq in top_ngram]
    
    return combined_ngrams

def combine_top_ngram_most_common(df, col, n, most_common=50):
    """
    Menghitung n-gram yang paling sering muncul dalam kolom yang ditentukan dan mengembalikannya sebagai DataFrame.
    
    Parameters:
    - df: DataFrame dengan kolom teks yang sudah dibersihkan.
    - col: Nama kolom yang berisi teks untuk dianalisis.
    - n: Integer, ukuran dari n-gram.
    - most_common: Integer, jumlah n-gram yang paling sering muncul untuk dikembalikan.
    
    Returns:
    - List of tuples dengan n-gram yang digabungkan dan frekuensinya.
    """

    # Gabungkan teks dari kolom yang ditentukan menjadi satu string
    texts = ' '.join(df[col])
    
    # Buat n-gram dari teks yang digabungkan
    ngram = ngrams(texts.split(), n)
    
    # Hitung frekuensi kemunculan setiap n-gram
    counts = Counter(ngram)
    
    # Dapatkan n-gram yang paling umum
    top_ngram = counts.most_common(most_common)
    
    # Gabungkan kata-kata dalam setiap n-gram menjadi dua pasangan kata
    combined_ngrams = [((' '.join(ngram[:2]), ' '.join(ngram[2:])), freq) for ngram, freq in top_ngram]
    
    return combined_ngrams


# def combine_top_ngram_most_common_text(text, n, most_common=50):
#     """
#     Menghitung n-gram yang paling sering muncul dari teks yang diberikan dan mengembalikannya sebagai list of tuples.
    
#     Parameters:
#     - text: String yang berisi teks untuk dianalisis.
#     - n: Integer, ukuran dari n-gram.
#     - most_common: Integer, jumlah n-gram yang paling sering muncul untuk dikembalikan.
    
#     Returns:
#     - List of tuples dengan n-gram yang digabungkan dan frekuensinya.
#     """
#     # Menghapus spasi berlebih dan spasi di awal/akhir teks
#     text = re.sub(r'\s+', ' ', text).strip()

#     # Buat n-gram dari teks yang diberikan
#     ngram = ngrams(text.split(), n)
    
#     # Hitung frekuensi kemunculan setiap n-gram
#     counts = Counter(ngram)
    
#     # Dapatkan n-gram yang paling umum
#     top_ngram = counts.most_common(most_common)
    
#     # # Gabungkan kata-kata dalam setiap n-gram menjadi dua pasangan kata
#     # combined_ngrams = [((' '.join(ngram[:2]), ' '.join(ngram[2:])), freq) for ngram, freq in top_ngram]
    
#     return top_ngram


def combine_df_top_ngram(df, col, n):
    """
    Menghitung n-gram yang paling sering muncul dalam kolom yang ditentukan dan mengembalikannya sebagai DataFrame.
    
    Parameters:
    - df: DataFrame dengan kolom teks yang sudah dibersihkan.
    - col: Nama kolom yang berisi teks untuk dianalisis.
    - n: Integer, ukuran dari n-gram.
    - most_common: Integer, jumlah n-gram yang paling sering muncul untuk dikembalikan.
    
    Returns:
    - pd.DataFrame dengan n-gram yang digabungkan dan frekuensinya.
    """
    # Gabungkan teks dari kolom yang ditentukan menjadi satu string
    texts = ' '.join(df[col].fillna(''))

    # Buat n-gram dari teks yang digabungkan
    ngram = ngrams(texts.split(), n)

    # Hitung frekuensi kemunculan setiap n-gram
    counts = Counter(ngram)

    # Dapatkan n-gram yang paling umum
    top_ngram = counts.most_common()

    # Gabungkan kata-kata dalam setiap n-gram menjadi string
    combined_ngrams = [(' '.join(ngram), freq) for ngram, freq in top_ngram]

    # Konversi ke DataFrame
    df_top_ngrams = pd.DataFrame(combined_ngrams, columns=['ngram', 'frequency'])

    return df_top_ngrams


def transform_ngrams_to_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mengubah n-gram dalam DataFrame menjadi tuple dengan pasangan kata.

    Parameters:
    - df: DataFrame yang memiliki kolom 'n_gram' dan 'frequency'.

    Returns:
    - DataFrame dengan n-gram dalam format tuple dengan pasangan kata.
    """
    if 'n_gram' not in df.columns:
        raise ValueError("DataFrame harus memiliki kolom 'n_gram'.")
    if 'frequency' not in df.columns:
        raise ValueError("DataFrame harus memiliki kolom 'frequency'.")
    
    def format_n_gram(ngram_tuple):
        # Gabungkan kata-kata berpasangan menjadi tuple
        paired_words = tuple(' '.join(ngram_tuple[i:i+2]) for i in range(0, len(ngram_tuple), 2))
        return paired_words

    # Terapkan fungsi pada kolom 'n_gram'
    df['n_gram'] = df['n_gram'].apply(format_n_gram)
    return df




# def plot_ngram_network(df, col, n, most_common=50):
#     """
#     Menampilkan jaringan n-gram dari kolom yang ditentukan.
    
#     Parameters:
#     - df: DataFrame dengan kolom teks yang sudah dibersihkan.
#     - col: Nama kolom yang berisi teks untuk dianalisis.
#     - n: Integer, ukuran dari n-gram.
#     - most_common: Integer, jumlah n-gram yang paling sering muncul untuk dikembalikan.
#     """
#     # Hitung n-gram menggunakan fungsi yang sudah ada
#     df_ngram = n_grams(df, col, n, most_common)
    
#     # Buat graf kosong
#     G = nx.Graph()
    
#     # Tambahkan node dan edge ke graf
#     for ngram, freq in zip(df_ngram['n_gram'], df_ngram['frequency']):
#         # Node n-gram
#         G.add_node(' '.join(ngram), size=freq)
#         # Tambahkan edge antara n-gram yang bertetangga
#         for i in range(len(ngram) - 1):
#             edge = (ngram[i], ngram[i + 1])
#             if G.has_edge(*edge):
#                 G[edge[0]][edge[1]]['weight'] += freq
#             else:
#                 G.add_edge(*edge, weight=freq)
    
#     # Visualisasi graf
#     plt.figure(figsize=(12, 12))
    
#     # Posisi node dengan layout Fruchterman-Reingold
#     pos = nx.spring_layout(G, k=0.5, iterations=50)
    
#     # Ukuran node berdasarkan frekuensi
#     sizes = [G.nodes[node]['size'] * 100 for node in G]
    
#     # Gambarkan graf
#     nx.draw(G, pos, with_labels=True, node_size=sizes, node_color='skyblue', edge_color='gray', 
#             font_size=12, font_weight='bold', width=[G[u][v]['weight'] / 10 for u, v in G.edges()])
    
#     plt.title('Jaringan N-Gram', fontsize=16)
#     plt.show()


# def  freq_of_char(df):
#     plt.figure(1, figsize=(10,6))

#     bins_range = np.arange(0, 250, 10)
#     chars = df['clean'].str.len()

#     sns.histplot(chars, bins=bins_range, kde=True, color='skyblue')
#     plt.title('Distribusi Frekuensi Jumlah Karakter per Tweet', fontsize=16)
#     plt.xlabel('Jumlah Karakter', fontsize=14)
#     plt.ylabel('Frekuensi', fontsize=14)
#     plt.axvline(chars.mean(), color='red', linestyle='dashed', linewidth=1)
#     plt.text(chars.mean() + 5, 50, f'Mean: {chars.mean():.2f}', color='red')
#     plt.show()

# def freq_of_words(df):
#     plt.figure(2, figsize=(10,6))

#     bins_range = np.arange(0, 50)
#     words = df['clean'].str.split().map(lambda x: len(x))

#     sns.histplot(words, bins=bins_range, kde=True, color='salmon')
#     plt.title('Distribusi Frekuensi Jumlah Kata per Tweet', fontsize=16)
#     plt.xlabel('Jumlah Kata', fontsize=14)
#     plt.ylabel('Frekuensi', fontsize=14)
#     plt.axvline(words.mean(), color='blue', linestyle='dashed', linewidth=1)
#     plt.text(words.mean() + 1, 50, f'Mean: {words.mean():.2f}', color='blue')
#     plt.show()


# def freq_meanlength_word(df):
#     plt.figure(3, figsize=(10,6))
#     words = df['tweet'].str.split().apply(lambda x : [len(i) for i in x]).map(lambda x: np.mean(x))

#     sns.histplot(words, kde=True, color='salmon')
#     plt.title('Distribusi Frekuensi panjang kata rata-rata', fontsize=16)
#     plt.xlabel('Jumlah Kata', fontsize=14)
#     plt.ylabel('Frekuensi', fontsize=14)
#     plt.axvline(words.mean(), color='blue', linestyle='dashed', linewidth=1)
#     plt.text(words.mean() + 1, 50, f'Mean: {words.mean():.2f}', color='blue')
#     plt.show()

# Load data

# pp = pp()

# def clean_file(x:str, pp=pp):
#     result = pp.lowercase(x)
#     result = pp.remove_stopwords(result)
#     result = pp.text_cleaning(result)
#     # result = pp.lemmatizing(result)

#     return result 

# df['clean'] = df['tweet'].apply(lambda x: clean_file(x))

# def most_frequent_words(df):
#     """
#     [[aku, suka bola], [aku, makan, bakso]] --> [aku, suka, bola, aku, suka, bakso]
#     """

#     df['tokens'] = df['text_cleaned'].apply(lambda x : str(x).split())
#     tweets = [word for tweet in df['tokens'] for word in tweet]

#     freq = nltk.probability.FreqDist(tweets)
#     print(freq)
#     most_frequents = freq.most_common(100)
#     print(f"20 Kata yang sering muncul:{most_frequents}")

# def n_grams(df, n, common=50):
#     """
#     [[aku, suka bola], [aku, makan, bakso]] --> [aku, suka, bola, aku, suka, bakso] --> "aku suka bola aku suka bakso"
#     """

#     texts = ' '.join(df['clean'])
#     ngram = ngrams(texts.split(), n)
#     counts = Counter(ngram)
#     top_ngram = counts.most_common(common)

#     return top_ngram


# def n_grams(df, n, common=50):
#     """
#     Menghitung n-gram yang paling sering muncul dalam kolom 'clean' dan mengembalikannya sebagai DataFrame.
    
#     Parameters:
#     - df: DataFrame dengan kolom 'clean' yang sudah dibersihkan.
#     - n: Integer, ukuran dari n-gram.
#     - common: Integer, jumlah n-gram yang paling sering muncul untuk dikembalikan.
    
#     Returns:
#     - DataFrame dengan kolom 'n_gram' dan 'frequency'.
#     """

#     # Gabungkan teks menjadi satu string
#     texts = ' '.join(df['clean'])
    
#     # Buat n-gram dari teks yang digabungkan
#     ngram = ngrams(texts.split(), n)
    
#     # Hitung frekuensi kemunculan setiap n-gram
#     counts = Counter(ngram)
    
#     # Dapatkan n-gram yang paling umum
#     top_ngram = counts.most_common(common)
    
#     # Buat DataFrame dari hasil
#     df_top_ngram = pd.DataFrame(top_ngram, columns=['n_gram', 'frequency'])
    
#     return df_top_ngram

    
    




if __name__ == "__main__":
    pass
    # freq_of_char(df['clean'])
    # freq_of_words(df['clean'])
    # freq_meanlength_word(df['clean'])

    # most_frequent_words(df)

    # plt.show()
