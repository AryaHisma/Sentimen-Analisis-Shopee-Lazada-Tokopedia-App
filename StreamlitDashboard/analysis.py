# Import library streamlit
import streamlit as st 

import os
import shutil

# Import semua library yang kita butuhkan
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
from PIL import Image

from TextPreProcessing import text_analyzer_project
import nltk

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from memory_profiler import profile

import dask.dataframe as dd


@profile
def analysis():
    with st.container(height=360):
        @st.cache_data
        def display_image(image_path, use_column_width=True, channels="RGB"):
            """
            Menampilkan gambar di Streamlit.
            
            Parameters:
            - image_path (str): Path ke file gambar.
            - use_column_width (bool): Menentukan apakah gambar akan menggunakan lebar kolom penuh.
            - channels (str): Mode channel warna, bisa "RGB", "RGBA", dll.
            """
            image = Image.open(image_path)
            st.image(image, use_column_width=use_column_width, channels=channels)

        display_image("./assets/gambar/Untitled.png", use_column_width=True, channels="RGB")
        
        
    # Header datset
    st.header("Dataset")

    # Tab dataset
    tab_shopee, tab_lazada, tab_tokopedia = st.tabs(["Shopee", "Lazada", "Tokopedia"])

    with tab_shopee:
        
        @st.cache_data
        def display_data_shopee():
            df_raw_shopee = pd.read_csv("./assets/dataset/scrapped_data_shopee.csv")
            df_raw_shopee = df_raw_shopee[['content', 'at']]
            df_raw_shopee['at'] = pd.to_datetime(df_raw_shopee['at'], errors='coerce')
            df_raw_shopee['year'] = df_raw_shopee['at'].dt.year 
            df_raw_shopee = df_raw_shopee.where(pd.notnull(df_raw_shopee), None)           
            return df_raw_shopee
        
        st.dataframe(display_data_shopee(), use_container_width=True)
        
    with tab_lazada:
        
        @st.cache_data
        def display_data_lazada():
            df_raw_lazada = pd.read_csv("./assets/dataset/scrapped_data_lazada.csv")
            df_raw_lazada = df_raw_lazada[['content', 'at']]
            df_raw_lazada['at'] = pd.to_datetime(df_raw_lazada['at'], errors='coerce')
            df_raw_lazada['year'] = df_raw_lazada['at'].dt.year
            df_raw_lazada = df_raw_lazada.where(pd.notnull(df_raw_lazada), None)
            return df_raw_lazada
        
        st.dataframe(display_data_lazada(), use_container_width=True)
        
    with tab_tokopedia:
        
        @st.cache_data
        def display_data_tokped():
            df_raw_tokped = pd.read_csv("./assets/dataset/scrapped_data_tokped.csv")
            df_raw_tokped = df_raw_tokped[['content', 'at']]
            df_raw_tokped['at'] = pd.to_datetime(df_raw_tokped['at'], errors='coerce')
            df_raw_tokped['year'] = df_raw_tokped['at'].dt.year
            df_raw_tokped = df_raw_tokped.where(pd.notnull(df_raw_tokped), None)
            return df_raw_tokped
        
        st.dataframe(display_data_tokped(), use_container_width=True)
        

    # Header Text PreProcessing
    st.header("Text PreProcessing")
    st.markdown('''
                Text preprocessing adalah langkah awal dalam analisis teks dan pemrosesan bahasa alami (NLP) yang melibatkan pembersihan dan transformasi 
                data teks mentah menjadi format yang lebih bersih dan terstruktur. Tujuan utamanya adalah mempersiapkan data untuk analisis lebih lanjut, 
                seperti analisis sentimen, klasifikasi teks, atau pembuatan model bahasa
                ''')


    # SubHeader Text PreProcessing
    st.subheader("Lower text")
    st.markdown('''
                Mengubah semua huruf dalam teks menjadi huruf kecil untuk memastikan konsistensi, karena perbedaan huruf besar dan kecil tidak penting 
                dalam banyak aplikasi NLP. Contoh: Mengubah "Hello World" menjadi "hello world". Selain itu juga dilakukan transformasi unicode style dimana
                adanya penulisan kata yang tidak normal seperti "***contoh***" menjadi "contoh".
                ''')


         
    # Tab lowercase
    tab_lowercase_shopee, tab_lowercase_lazada, tab_lowercase_tokopedia = st.tabs(["Shopee", "Lazada", "Tokopedia"])

    with tab_lowercase_shopee:
        col_lowercase_shopee1, col_lowercase_shopee2 = st.columns([4, 1])
        
        with col_lowercase_shopee1:
            st.subheader("Dataset after lower case")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_lower_case_shopee():
                df_lowercase_shopee = pd.read_pickle("./assets/dataset/data_preprocess_shopee/df_text_clean_lower_shopee.pkl")
                df_lowercase_shopee = df_lowercase_shopee[['content', 'at']]
                df_lowercase_shopee['at'] = pd.to_datetime(df_lowercase_shopee['at'], errors='coerce')
                df_lowercase_shopee['year'] = df_lowercase_shopee['at'].dt.year
                df_lowercase_shopee = df_lowercase_shopee.where(pd.notnull(df_lowercase_shopee), None)
                return df_lowercase_shopee
            
            st.dataframe(get_dataset_after_lower_case_shopee(), use_container_width=True)
            
                                
        with col_lowercase_shopee2:
            st.subheader("Most frequent word after lower case")
            
            # Menentukan nilai n yang masuk akal
            n_unique_words_shopee = len(get_dataset_after_lower_case_shopee()['content'].str.split(expand=True).stack().unique())
            
            # most_frequent_words_text_clean_lower_shopee
            @st.cache_data
            def most_frequent_words_shopee_after_lowercase():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_lower_case_shopee(), col='content', n=n_unique_words_shopee)
            
            most_frequent_words_shopee_after_lowercase = most_frequent_words_shopee_after_lowercase()
            st.dataframe(most_frequent_words_shopee_after_lowercase, use_container_width=True, hide_index=True)
        
    with tab_lowercase_lazada:
        col_lowercase_lazada1, col_lowercase_lazada2 = st.columns([4, 1])
        
        with col_lowercase_lazada1:
            st.subheader("Dataset after lower case")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_lower_case_lazada():
                df_lowercase_lazada = pd.read_pickle("./assets/dataset/data_preprocess_lazada/df_text_clean_lower_lazada.pkl")
                df_lowercase_lazada = df_lowercase_lazada[['content', 'at']]
                df_lowercase_lazada['at'] = pd.to_datetime(df_lowercase_lazada['at'], errors='coerce')
                df_lowercase_lazada['year'] = df_lowercase_lazada['at'].dt.year
                df_lowercase_lazada = df_lowercase_lazada.where(pd.notnull(df_lowercase_lazada), None)
                return df_lowercase_lazada
            
            st.dataframe(get_dataset_after_lower_case_lazada(), use_container_width=True)
        
        with col_lowercase_lazada2:
            st.subheader("Most frequent word after lower case")
            
            # Menentukan nilai n yang masuk akal
            n_unique_words_lazada = len(get_dataset_after_lower_case_lazada()['content'].str.split(expand=True).stack().unique())
            
            # most_frequent_words_text_clean_lower_lazada
            @st.cache_data
            def most_frequent_words_lazada_after_lowercase():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_lower_case_lazada(), col='content', n=n_unique_words_shopee)
            
            most_frequent_words_lazada_after_lowercase = most_frequent_words_lazada_after_lowercase()
            st.dataframe(most_frequent_words_lazada_after_lowercase, use_container_width=True, hide_index=True)
        
    with tab_lowercase_tokopedia:
        col_lowercase_tokopedia1, col_lowercase_tokopedia2 = st.columns([4, 1])
        
        with col_lowercase_tokopedia1:
            st.subheader("Dataset after lower case")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_lower_case_tokped():
                df_lowercase_tokped = pd.read_pickle("./assets/dataset/data_preprocess_tokped/df_text_clean_lower_tokped.pkl")
                df_lowercase_tokped = df_lowercase_tokped[['content', 'at']]
                df_lowercase_tokped['at'] = pd.to_datetime(df_lowercase_tokped['at'], errors='coerce')
                df_lowercase_tokped['year'] = df_lowercase_tokped['at'].dt.year
                df_lowercase_tokped = df_lowercase_tokped.where(pd.notnull(df_lowercase_tokped), None)
                return df_lowercase_tokped
            
            st.dataframe(get_dataset_after_lower_case_tokped(), use_container_width=True)
            
        with col_lowercase_tokopedia2:
            st.subheader("Most frequent word after lower case")
            
            # Menentukan nilai n yang masuk akal
            n_unique_words_tokped = len(get_dataset_after_lower_case_tokped()['content'].str.split(expand=True).stack().unique())
            
            # most_frequent_words_text_clean_lower_lazada
            @st.cache_data
            def most_frequent_words_tokped_after_lowercase():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_lower_case_tokped(), col='content', n=n_unique_words_shopee)
            
            most_frequent_words_tokped_after_lowercase = most_frequent_words_tokped_after_lowercase()
            st.dataframe(most_frequent_words_tokped_after_lowercase, use_container_width=True, hide_index=True)
        
        
    # SubHeader Text PreProcessing
    st.subheader("Remove emoji")
    st.markdown('''
                Emoji mungkin tidak memberikan informasi yang berguna dalam beberapa jenis analisis teks.
                Menghapus emoji dapat membantu memastikan bahwa teks konsisten dan fokus pada konten yang relevan.
                ''')


    # Load dataset remove emoji
    # Tab remove emoji
    tab_removeemoji1, tab_removeemoji2, tab_removeemoji3 = st.tabs(["Shopee", "Lazada", "Tokopedia"])

    with tab_removeemoji1:
        col_removeemoji_shopee1, col_removeemoji_shopee2 = st.columns([4, 1])
        
        with col_removeemoji_shopee1:
            st.subheader("Dataset after remove emoji")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_removeemoji_shopee():
                df_removeemoji_shopee = pd.read_pickle("./assets/dataset/data_preprocess_shopee/df_text_clean_emoji_shopee.pkl")
                df_removeemoji_shopee = df_removeemoji_shopee[['content', 'at']]
                df_removeemoji_shopee['at'] = pd.to_datetime(df_removeemoji_shopee['at'], errors='coerce')
                df_removeemoji_shopee['year'] = df_removeemoji_shopee['at'].dt.year
                df_removeemoji_shopee = df_removeemoji_shopee.where(pd.notnull(df_removeemoji_shopee), None)
                return df_removeemoji_shopee
            
            st.dataframe(get_dataset_after_removeemoji_shopee(), use_container_width=True)
        
        with col_removeemoji_shopee2:
            st.subheader("Most frequent word after remove emoji")
            
            # Menentukan nilai n yang masuk akal
            n_unique_words_shopee = len(get_dataset_after_removeemoji_shopee()['content'].str.split(expand=True).stack().unique())
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_shopee_after_removeemoji():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_removeemoji_shopee(), col='content', n=n_unique_words_shopee)
            
            most_frequent_words_shopee_after_removeemoji = most_frequent_words_shopee_after_removeemoji()
            st.dataframe(most_frequent_words_shopee_after_removeemoji, use_container_width=True, hide_index=True)
            
        
    with tab_removeemoji2:
        col_removeemoji_lazada1, col_removeemoji_lazada2 = st.columns([4, 1])
        
        with col_removeemoji_lazada1:
            st.subheader("Dataset after remove emoji")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_removeemoji_lazada():
                df_removeemoji_lazada = pd.read_pickle("./assets/dataset/data_preprocess_lazada/df_text_clean_emoji_lazada.pkl")
                df_removeemoji_lazada = df_removeemoji_lazada[['content', 'at']]
                df_removeemoji_lazada['at'] = pd.to_datetime(df_removeemoji_lazada['at'], errors='coerce')
                df_removeemoji_lazada['year'] = df_removeemoji_lazada['at'].dt.year
                df_removeemoji_lazada = df_removeemoji_lazada.where(pd.notnull(df_removeemoji_lazada), None)
                return df_removeemoji_lazada
            
            st.dataframe(get_dataset_after_removeemoji_lazada(), use_container_width=True)
            
        with col_removeemoji_lazada2:
            st.subheader("Most frequent word after remove emoji")
        
            # Menentukan nilai n yang masuk akal
            n_unique_words_lazada = len(get_dataset_after_removeemoji_lazada()['content'].str.split(expand=True).stack().unique())
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_lazada_after_removeemoji():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_removeemoji_lazada(), col='content', n=n_unique_words_lazada)
            
            most_frequent_words_lazada_after_removeemoji = most_frequent_words_lazada_after_removeemoji()
            st.dataframe(most_frequent_words_lazada_after_removeemoji, use_container_width=True, hide_index=True)
            
        
    with tab_removeemoji3:
        col_removeemoji_tokped1, col_removeemoji_tokped2 = st.columns([4, 1])
        
        with col_removeemoji_tokped1:
            st.subheader("Dataset after remove emoji")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_removeemoji_tokped():
                df_removeemoji_tokped = pd.read_pickle("./assets/dataset/data_preprocess_tokped/df_text_clean_emoji_tokped.pkl")
                df_removeemoji_tokped = df_removeemoji_tokped[['content', 'at']]
                df_removeemoji_tokped['at'] = pd.to_datetime(df_removeemoji_tokped['at'], errors='coerce')
                df_removeemoji_tokped['year'] = df_removeemoji_tokped['at'].dt.year
                df_removeemoji_tokped = df_removeemoji_tokped.where(pd.notnull(df_removeemoji_tokped), None)
                return df_removeemoji_tokped
            
            st.dataframe(get_dataset_after_removeemoji_tokped(), use_container_width=True)
            
            
        with col_removeemoji_tokped2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_tokped = len(get_dataset_after_removeemoji_tokped()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after remove emoji
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after remove emoji")
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_tokped_after_removeemoji():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_removeemoji_tokped(), col='content', n=n_unique_words_tokped)
            
            most_frequent_words_tokped_after_removeemoji = most_frequent_words_tokped_after_removeemoji()
            st.dataframe(most_frequent_words_tokped_after_removeemoji, use_container_width=True, hide_index=True)
        
        
    # SubHeader Text PreProcessing
    st.subheader("Text Cleaning")
    st.markdown('''
                Menghapus tanda baca yang mungkin tidak memberikan informasi yang berguna dalam beberapa jenis analisis teks.
                Menghapus tanda baca dapat membantu memastikan bahwa teks konsisten dan fokus pada konten yang relevan.
                ''')

    
    # Load dataset text cleaning
    # Tab text cleaning
    tab_textclean1, tab_textclean2, tab_textclean3 = st.tabs(["Shopee", "Lazada", "Tokopedia"])

    with tab_textclean1:
        col_textclean_shopee1, col_textclean_shopee2 = st.columns([4, 1])
        
        with col_textclean_shopee1:
            st.subheader("Dataset after text cleaning")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_textclean_shopee():
                df_textcleaning_shopee = pd.read_pickle("./assets/dataset/data_preprocess_shopee/df_text_clean_shopee.pkl")
                df_textcleaning_shopee = df_textcleaning_shopee[['content', 'at']]
                df_textcleaning_shopee['at'] = pd.to_datetime(df_textcleaning_shopee['at'], errors='coerce')
                df_textcleaning_shopee['year'] = df_textcleaning_shopee['at'].dt.year
                df_textcleaning_shopee = df_textcleaning_shopee.where(pd.notnull(df_textcleaning_shopee), None)
                return df_textcleaning_shopee
            
            st.dataframe(get_dataset_after_textclean_shopee(), use_container_width=True)
            
        with col_textclean_shopee2:
            st.subheader("Most frequent word after text cleaning")
            
            # Menentukan nilai n yang masuk akal
            n_unique_words_shopee = len(get_dataset_after_textclean_shopee()['content'].str.split(expand=True).stack().unique())
        
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_shopee_after_textclean():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_textclean_shopee(), col='content', n=n_unique_words_shopee)
            
            most_frequent_words_shopee_after_textclean = most_frequent_words_shopee_after_textclean()
            st.dataframe(most_frequent_words_shopee_after_textclean, use_container_width=True)
            
    with tab_textclean2:
        col_textclean_lazada1, col_textclean_lazada2 = st.columns([4, 1])
        
        with col_textclean_lazada1:
            st.subheader("Dataset after text cleaning")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_textclean_lazada():
                df_textcleaning_lazada = pd.read_pickle("./assets/dataset/data_preprocess_lazada/df_text_clean_lazada.pkl")
                df_textcleaning_lazada = df_textcleaning_lazada[['content', 'at']]
                df_textcleaning_lazada['at'] = pd.to_datetime(df_textcleaning_lazada['at'], errors='coerce')
                df_textcleaning_lazada['year'] = df_textcleaning_lazada['at'].dt.year
                df_textcleaning_lazada = df_textcleaning_lazada.where(pd.notnull(df_textcleaning_lazada), None)
                return df_textcleaning_lazada
            
            st.dataframe(get_dataset_after_textclean_lazada(), use_container_width=True)
        
        with col_textclean_lazada2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_lazada = len(get_dataset_after_textclean_lazada()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after text cleaning
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after text cleaning")
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_lazada_after_textclean():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_textclean_lazada(), col='content', n=n_unique_words_lazada)
            
            most_frequent_words_lazada_after_textclean = most_frequent_words_lazada_after_textclean()
            st.dataframe(most_frequent_words_lazada_after_textclean, use_container_width=True)
        
    with tab_textclean3:
        col_textclean_tokped1, col_textclean_tokped2 = st.columns([4, 1])
        
        with col_textclean_tokped1:
            st.subheader("Dataset after text cleaning")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_textclean_tokped():
                df_textcleaning_tokped = pd.read_pickle("./assets/dataset/data_preprocess_tokped/df_text_clean_tokped.pkl")
                df_textcleaning_tokped = df_textcleaning_tokped[['content', 'at']]
                df_textcleaning_tokped['at'] = pd.to_datetime(df_textcleaning_tokped['at'], errors='coerce')
                df_textcleaning_tokped['year'] = df_textcleaning_tokped['at'].dt.year
                df_textcleaning_tokped = df_textcleaning_tokped.where(pd.notnull(df_textcleaning_tokped), None)
                return df_textcleaning_tokped
            
            st.dataframe(get_dataset_after_textclean_tokped(), use_container_width=True)
        
        
        with col_textclean_tokped2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_tokped = len(get_dataset_after_textclean_tokped()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after text cleaning
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after text cleaning")
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_tokped_after_textclean():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_textclean_tokped(), col='content', n=n_unique_words_tokped)
            
            most_frequent_words_tokped_after_textclean = most_frequent_words_tokped_after_textclean()
            st.dataframe(most_frequent_words_tokped_after_textclean, use_container_width=True)

    # SubHeader Text PreProcessing
    st.subheader("Slang Transformation") 
    st.markdown('''
               Mengubah kata kata slang (tidak baku) menjadi kata kata baku yang berguna untuk memberikan informasi dalam analisis teks.
               Mengubah kata kata slang (tidak baku) menjadi kata kata baku untuk mempermudah dalam analisis teks.
                ''')  
   
        
    # Load dataset slang
      
    # Tab remove emoji
    tab_slang11, tab_slang12, tab_slang13 = st.tabs(["Shopee", "Lazada", "Tokopedia"])

    with tab_slang11:
        col_slang_shopee1, col_slang_shopee2 = st.columns([4, 1])
        
        with col_slang_shopee1:
            st.subheader("Dataset after slang")
            st.write("")
            st.write("")
            
            
            @st.cache_data
            def get_dataset_after_slang_shopee():
                df_slang_shopee1 = pd.read_pickle("./assets/dataset/data_preprocess_shopee/df_text_slang1_shopee.pkl")
                df_slang_shopee1 = df_slang_shopee1[['content', 'at']]
                df_slang_shopee1['at'] = pd.to_datetime(df_slang_shopee1['at'], errors='coerce')
                df_slang_shopee1['year'] = df_slang_shopee1['at'].dt.year
                df_slang_shopee1 = df_slang_shopee1.where(pd.notnull(df_slang_shopee1), None)
                return df_slang_shopee1
            
            st.dataframe(get_dataset_after_slang_shopee(), use_container_width=True)
        
        
        with col_slang_shopee2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_shopee = len(get_dataset_after_slang_shopee()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after slang1
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after slang") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_shopee_slang():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_slang_shopee(), col='content', n=n_unique_words_shopee)
            
            most_frequent_words_shopee_slang = most_frequent_words_shopee_slang()
            st.dataframe(most_frequent_words_shopee_slang, use_container_width=True)
            
                               
    with tab_slang12:
        col_slang_lazada1, col_slang_lazada2 = st.columns([4, 1])
        
        with col_slang_lazada1:
            st.subheader("Dataset after slang")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_slang_lazada():
                df_slang_lazada1 = pd.read_pickle("./assets/dataset/data_preprocess_lazada/df_text_slang1_lazada.pkl")
                df_slang_lazada1 = df_slang_lazada1[['content', 'at']]
                df_slang_lazada1['at'] = pd.to_datetime(df_slang_lazada1['at'], errors='coerce')
                df_slang_lazada1['year'] = df_slang_lazada1['at'].dt.year
                df_slang_lazada1 = df_slang_lazada1.where(pd.notnull(df_slang_lazada1), None)
                return df_slang_lazada1
            
            st.dataframe(get_dataset_after_slang_lazada(), use_container_width=True)
            
        with col_slang_lazada2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_lazada = len(get_dataset_after_slang_lazada()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after slang1
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after slang") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_lazada_slang():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_slang_lazada(), col='content', n=n_unique_words_lazada)
            
            most_frequent_words_lazada_slang = most_frequent_words_lazada_slang()
            st.dataframe(most_frequent_words_lazada_slang, use_container_width=True)
        
    with tab_slang13:
        col_slang_tokped1, col_slang_tokped2 = st.columns([4, 1])
        
        with col_slang_tokped1:
            st.subheader("Dataset after slang")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_slang_tokped():
                df_slang_tokped1 = pd.read_pickle("./assets/dataset/data_preprocess_tokped/df_text_slang1_tokped.pkl")
                df_slang_tokped1 = df_slang_tokped1[['content', 'at']]
                df_slang_tokped1['at'] = pd.to_datetime(df_slang_tokped1['at'], errors='coerce')
                df_slang_tokped1['year'] = df_slang_tokped1['at'].dt.year
                df_slang_tokped1 = df_slang_tokped1.where(pd.notnull(df_slang_tokped1), None)
                return df_slang_tokped1
            
            st.dataframe(get_dataset_after_slang_tokped(), use_container_width=True)
            
        
        with col_slang_tokped2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_tokped = len(get_dataset_after_slang_tokped()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after slang1
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after slang") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_tokped_slang():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_slang_tokped(), col='content', n=n_unique_words_tokped)
            
            most_frequent_words_tokped_slang = most_frequent_words_tokped_slang()
            st.dataframe(most_frequent_words_tokped_slang, use_container_width=True)

    # SubHeader Stopword Removal
    st.subheader("Stemming")
    st.markdown('''
               Stemming adalah proses dalam pengolahan bahasa alami (Natural Language Processing atau NLP) yang digunakan untuk mengubah kata-kata 
               dalam bentuk yang bervariasi menjadi bentuk dasarnya atau akar katanya (stem). Tujuan utama dari stemming adalah untuk mengurangi variasi 
               kata yang berbeda namun memiliki arti yang sama, sehingga analisis data teks dapat dilakukan lebih efisien.
               Contoh sederhana dari stemming adalah sebagai berikut:
               Kata "berlari", "berlari-lari", dan "pelari" semuanya akan diubah menjadi akar kata "lari".
               Kata "makan", "memakan", "dimakan", dan "pemakan" akan diubah menjadi "makan".
                ''') 
    
    # Load dataset slang
    # Tab stopword
    tab_stem1, tab_stem2, tab_stem3 = st.tabs(["Shopee", "Lazada", "Tokopedia"])

    with tab_stem1:
        col_stem_shopee1, col_stem_shopee2 = st.columns([4, 1])
        
        with col_stem_shopee1:
            st.subheader("Dataset after stemming")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_stem_shopee():
                df_stem_shopee = pd.read_pickle("./assets/dataset/data_preprocess_shopee/df_text_stemming_shopee.pkl")
                df_stem_shopee = df_stem_shopee[['content', 'at']]
                df_stem_shopee['at'] = pd.to_datetime(df_stem_shopee['at'], errors='coerce')
                df_stem_shopee['year'] = df_stem_shopee['at'].dt.year
                df_stem_shopee = df_stem_shopee.where(pd.notnull(df_stem_shopee), None)
                return df_stem_shopee
            
            st.dataframe(get_dataset_after_stem_shopee(), use_container_width=True)
        
        with col_stem_shopee2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_shopee = len(get_dataset_after_stem_shopee()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after stopword removal
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after stemming") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_shopee_stem():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_stem_shopee(), col='content', n=n_unique_words_shopee)
            
            most_frequent_words_shopee_stem = most_frequent_words_shopee_stem()
            st.dataframe(most_frequent_words_shopee_stem, use_container_width=True)
        
    with tab_stem2:
        col_stem_lazada1, col_stem_lazada2 = st.columns([4, 1])
        
        with col_stem_lazada1:
            st.subheader("Dataset after stemming")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_stem_lazada():
                df_stem_lazada = pd.read_pickle("./assets/dataset/data_preprocess_lazada/df_text_stemming_lazada.pkl")
                df_stem_lazada = df_stem_lazada[['content', 'at']]
                df_stem_lazada['at'] = pd.to_datetime(df_stem_lazada['at'], errors='coerce')
                df_stem_lazada['year'] = df_stem_lazada['at'].dt.year
                df_stem_lazada = df_stem_lazada.where(pd.notnull(df_stem_lazada), None)
                return df_stem_lazada
            
            st.dataframe(get_dataset_after_stem_lazada(), use_container_width=True)
            
        with col_stem_lazada2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_lazada = len(get_dataset_after_stem_lazada()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after stopword removal
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after stemming") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_lazada_stem():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_stem_lazada(), col='content', n=n_unique_words_lazada)
            
            most_frequent_words_lazada_stem = most_frequent_words_lazada_stem()
            st.dataframe(most_frequent_words_lazada_stem, use_container_width=True)
        
    with tab_stem3:
        col_stem_tokped1, col_stem_tokped2 = st.columns([4, 1])
        
        with col_stem_tokped1:
            st.subheader("Dataset after stemming")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_stem_tokped():
                df_stem_tokped = pd.read_pickle("./assets/dataset/data_preprocess_tokped/df_text_stemming_tokped.pkl")
                df_stem_tokped = df_stem_tokped[['content', 'at']]
                df_stem_tokped['at'] = pd.to_datetime(df_stem_tokped['at'], errors='coerce')
                df_stem_tokped['year'] = df_stem_tokped['at'].dt.year
                df_stem_tokped = df_stem_tokped.where(pd.notnull(df_stem_tokped), None)
                return df_stem_tokped
            
            st.dataframe(get_dataset_after_stem_tokped(), use_container_width=True)
        
        with col_stem_tokped2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_tokped = len(get_dataset_after_stem_tokped()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after stopword removal
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after stemming") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_tokped_stem():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_stem_tokped(), col='content', n=n_unique_words_lazada)
            
            most_frequent_words_tokped_stem = most_frequent_words_tokped_stem()
            st.dataframe(most_frequent_words_tokped_stem, use_container_width=True)
    
    # SubHeader Stopword Removal
    st.subheader("Stopword Removal")
    st.markdown('''
               Menghapus kata-kata umum (seperti "yang", "yakni", "seperti") yang sering muncul tetapi tidak memberikan informasi penting.
                ''') 
    
    # Load dataset stopwords
    # Tab stopword
    tab_stopword1, tab_stopword2, tab_stopword3 = st.tabs(["Shopee", "Lazada", "Tokopedia"])

    with tab_stopword1:
        col_stopword_shopee1, col_stopword_shopee2 = st.columns([4, 1])
        
        with col_stopword_shopee1:
            st.subheader("Dataset after remove stopword")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_stopword_shopee():
                df_stopword_shopee = pd.read_pickle("./assets/dataset/data_preprocess_shopee/df_stopword_shopee.pkl")
                df_stopword_shopee = df_stopword_shopee[['content', 'at']]
                df_stopword_shopee['at'] = pd.to_datetime(df_stopword_shopee['at'], errors='coerce')
                df_stopword_shopee['year'] = df_stopword_shopee['at'].dt.year
                df_stopword_shopee = df_stopword_shopee.where(pd.notnull(df_stopword_shopee), None)
                return df_stopword_shopee
            
            st.dataframe(get_dataset_after_stopword_shopee(), use_container_width=True)
        
        with col_stopword_shopee2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_shopee = len(get_dataset_after_stopword_shopee()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after stopword removal
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after remove stopword") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_shopee_stopword():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_stopword_shopee(), col='content', n=n_unique_words_shopee)
            
            most_frequent_words_shopee_stopword = most_frequent_words_shopee_stopword()
            st.dataframe(most_frequent_words_shopee_stopword, use_container_width=True)
        
    with tab_stopword2:
        col_stopword_lazada1, col_stopword_lazada2 = st.columns([4, 1])
        
        with col_stopword_lazada1:
            st.subheader("Dataset after remove stopword")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_stopword_lazada():
                df_stopword_lazada = pd.read_pickle("./assets/dataset/data_preprocess_lazada/df_stopword_lazada.pkl")
                df_stopword_lazada = df_stopword_lazada[['content', 'at']]
                df_stopword_lazada['at'] = pd.to_datetime(df_stopword_lazada['at'], errors='coerce')
                df_stopword_lazada['year'] = df_stopword_lazada['at'].dt.year
                df_stopword_lazada = df_stopword_lazada.where(pd.notnull(df_stopword_lazada), None)
                return df_stopword_lazada
            
            st.dataframe(get_dataset_after_stopword_lazada(), use_container_width=True)
            
        with col_stopword_lazada2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_lazada = len(get_dataset_after_stopword_lazada()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after stopword removal
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after remove stopword") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_lazada_stopword():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_stopword_lazada(), col='content', n=n_unique_words_lazada)
            
            most_frequent_words_lazada_stopword = most_frequent_words_lazada_stopword()
            st.dataframe(most_frequent_words_lazada_stopword, use_container_width=True)
        
    with tab_stopword3:
        col_stopword_tokped1, col_stopword_tokped2 = st.columns([4, 1])
        
        with col_stopword_tokped1:
            st.subheader("Dataset after remove stopword")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            
            @st.cache_data
            def get_dataset_after_stopword_tokped():
                df_stopword_tokped = pd.read_pickle("./assets/dataset/data_preprocess_tokped/df_stopword_tokped.pkl")
                df_stopword_tokped = df_stopword_tokped[['content', 'at']]
                df_stopword_tokped['at'] = pd.to_datetime(df_stopword_tokped['at'], errors='coerce')
                df_stopword_tokped['year'] = df_stopword_tokped['at'].dt.year
                df_stopword_tokped = df_stopword_tokped.where(pd.notnull(df_stopword_tokped), None)
                return df_stopword_tokped
            
            st.dataframe(get_dataset_after_stopword_tokped(), use_container_width=True)
        
        with col_stopword_tokped2:
            # Menentukan nilai n yang masuk akal
            n_unique_words_tokped = len(get_dataset_after_stopword_tokped()['content'].str.split(expand=True).stack().unique())
            
            # Most frequent word after stopword removal
            # SubHeader Text PreProcessing
            st.subheader("Most frequent word after remove stopword") 
            
            # Mengambil kata-kata yang paling sering muncul
            @st.cache_data
            def most_frequent_words_tokped_stopword():
                return  text_analyzer_project.most_frequent_words(get_dataset_after_stopword_tokped(), col='content', n=n_unique_words_lazada)
            
            most_frequent_words_tokped_stopword = most_frequent_words_tokped_stopword()
            st.dataframe(most_frequent_words_tokped_stopword, use_container_width=True)
    
    
    # Load data grafik
    
    @st.cache_data
    def data_grafik_shopee():
        df_clean_shopee1 = pd.read_pickle("./assets/dataset/data_preprocess_shopee/df_stopword_shopee.pkl")
        df_clean_shopee1['at'] = pd.to_datetime(df_clean_shopee1['at'], errors='coerce')
        df_clean_shopee1['year'] = df_clean_shopee1['at'].dt.year
        df_clean_shopee1 = df_clean_shopee1.where(pd.notnull(df_clean_shopee1), None)
        df_clean_shopee1 = df_clean_shopee1[['content', 'at', 'year']]
        return df_clean_shopee1
    
    @st.cache_data
    def data_grafik_lazada():
        df_clean_lazada1 = pd.read_pickle("./assets/dataset/data_preprocess_lazada/df_stopword_lazada.pkl")
        df_clean_lazada1['at'] = pd.to_datetime(df_clean_lazada1['at'], errors='coerce')
        df_clean_lazada1['year'] = df_clean_lazada1['at'].dt.year
        df_clean_lazada1 = df_clean_lazada1.where(pd.notnull(df_clean_lazada1), None)
        df_clean_lazada1 = df_clean_lazada1[['content', 'at', 'year']]
        return df_clean_lazada1
    
    @st.cache_data
    def data_grafik_tokped():
        df_clean_tokped1 = pd.read_pickle("./assets/dataset/data_preprocess_tokped/df_stopword_tokped.pkl")
        df_clean_tokped1['at'] = pd.to_datetime(df_clean_tokped1['at'], errors='coerce')
        df_clean_tokped1['year'] = df_clean_tokped1['at'].dt.year
        df_clean_tokped1 = df_clean_tokped1.where(pd.notnull(df_clean_tokped1), None)
        df_clean_tokped1 = df_clean_tokped1[['content', 'at', 'year']]
        return df_clean_tokped1
    
    
    # SubHeader Distribusi frekuensi
    st.subheader("Distribusi frekuensi")
    st.markdown('''
               Memvisualisasikan distribusi frekuensi dari kata, yaitu : distribusi frekuensi jumlah huruf, distribusi frekuensi jumlah kata per teks dan 
               distribusi frekuensi panjang kata rata rata.
               
               Distribusi frekuensi jumlah huruf adalah penghitungan seberapa sering sebuah teks memiliki jumlah huruf tertentu. 
               Misalnya, jika Anda memiliki kumpulan teks, distribusi ini akan menunjukkan seberapa banyak teks yang memiliki, 
               misalnya, 5 huruf, 10 huruf, dan seterusnya. Distribusi ini memberikan gambaran tentang seberapa panjang atau pendek karakteristik 
               teks dalam hal jumlah huruf.
               
               Distribusi frekuensi jumlah kata per teks adalah penghitungan seberapa sering jumlah kata tertentu muncul dalam sebuah teks. 
               Sebagai contoh, jika Anda menganalisis sekumpulan ulasan produk, distribusi ini akan menunjukkan berapa banyak ulasan yang terdiri 
               dari, misalnya, 5 kata, 10 kata, dan seterusnya. Hal ini membantu memahami apakah teks cenderung terdiri dari sedikit kata (pendek) 
               atau banyak kata (panjang).
               
               Distribusi frekuensi panjang kata rata-rata adalah penghitungan yang menunjukkan seberapa sering kata-kata dalam teks memiliki 
               panjang tertentu jika dihitung rata-rata. Misalnya, jika sebuah teks terdiri dari 10 kata dengan jumlah total huruf sebanyak 50, 
               maka panjang kata rata-ratanya adalah 5 huruf per kata. Distribusi ini menunjukkan seberapa sering kata-kata dalam teks cenderung 
               memiliki panjang tertentu, memberikan wawasan tentang kompleksitas atau kesederhanaan kata yang digunakan dalam teks tersebut.

                ''')
    
    # Tab stopword
    tab_distribusi_shopee, tab_distribusi_lazada, tab_distribusi_tokped = st.tabs(["Shopee", "Lazada", "Tokopedia"])
    
    with tab_distribusi_shopee:
        col_freq_of_char_shopee1, col_freq_of_char_shopee2, col_freq_of_char_shopee3 = st.columns(3)
        
        with col_freq_of_char_shopee1:
            # Panggil fungsi untuk menghasilkan plot
                fig = text_analyzer_project.plot_letter_frequency_distribution(data_grafik_shopee(), 'content', bins=100)
                
                # Tampilkan plot di Streamlit
                st.plotly_chart(fig)
            
            
        with col_freq_of_char_shopee2:
            # Panggil fungsi untuk menghasilkan plot
                fig = text_analyzer_project.freq_of_words_plotly_analisis(data_grafik_shopee(), 'content')
                
                # Tampilkan plot di Streamlit
                st.plotly_chart(fig)
            
            
        with col_freq_of_char_shopee3:
            plt_freq_meanlength_word_shopee = text_analyzer_project.freq_meanlength_word(data_grafik_shopee(), col='content')
            st.plotly_chart(plt_freq_meanlength_word_shopee)
            
    
    
    with tab_distribusi_lazada:
        col_freq_of_char_lazada1, col_freq_of_char_lazada2, col_freq_of_char_lazada3 = st.columns(3)
        
        with col_freq_of_char_lazada1:
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.plot_letter_frequency_distribution(data_grafik_lazada(), 'content', bins=100)
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
            
            
        with col_freq_of_char_lazada2:
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.freq_of_words_plotly_analisis(data_grafik_lazada(), 'content')
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
            
            
        with col_freq_of_char_lazada3:
            plt_freq_meanlength_word_lazada = text_analyzer_project.freq_meanlength_word(data_grafik_lazada(), col='content')
            st.plotly_chart(plt_freq_meanlength_word_lazada)
    
    
    with tab_distribusi_tokped:
        col_freq_of_char_tokped1, col_freq_of_char_tokped2, col_freq_of_char_tokped3 = st.columns(3)
        
        with col_freq_of_char_tokped1:
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.plot_letter_frequency_distribution(data_grafik_tokped(), 'content', bins=100)
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
            
            
        with col_freq_of_char_tokped2:
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.freq_of_words_plotly_analisis(data_grafik_tokped(), 'content')
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
            
            
        with col_freq_of_char_tokped3:
            plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(data_grafik_tokped(), col='content')
            st.plotly_chart(plt_freq_meanlength_word_tokped)
    
    
    # SubHeader N-gram & Wordcloud
    st.subheader("N-gram & Wordcloud")
    st.markdown('''
               N-gram adalah sebuah teknik dalam pengolahan bahasa alami (NLP) yang digunakan untuk menganalisis dan memodelkan urutan kata atau token dalam teks. 
               Istilah "n-gram" mengacu pada urutan kata atau token yang memiliki panjang tertentu, di mana "n" adalah jumlah kata atau token dalam urutan tersebut.
               
               
               Wordcloud adalah visualisasi yang sering digunakan untuk menampilkan frekuensi atau pentingnya kata dalam kumpulan teks dengan cara yang 
               intuitif dan menarik. Dalam wordcloud, kata-kata yang lebih sering muncul dalam teks akan ditampilkan dengan ukuran yang lebih besar, 
               sementara kata-kata yang kurang sering muncul akan ditampilkan dengan ukuran yang lebih kecil.
                ''')
    
    # Tab Ngram dan wordcloud
    tab_ngramword_shopee, tab_ngramword_lazada, tab_ngramword_tokped = st.tabs(["Shopee", "Lazada", "Tokopedia"])
    
    with tab_ngramword_shopee:
        tab_ngramword_shopee1, tab_ngramword_shopee2, tab_ngramword_shopee3 = st.columns(3)
        # Ganti nilai None atau NaN dengan string kosong
        # df_clean_tokped['content'] = stopword_shopee()['content'].fillna('')

        
        with tab_ngramword_shopee1:
            with st.container(height=400, border=True):
                st.write('N-gram (4 kata) --> Mengambil 4 kata per unit yang sering muncul')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_4gram = text_analyzer_project.top_ngram(data_grafik_shopee(), col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_4gram = pd.DataFrame(result_df_top_4gram, columns=['N-gram (4 kata)', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_4gram)

        with tab_ngramword_shopee2:
            with st.container(height=400, border=True):
                st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_2gram = text_analyzer_project.combine_top_ngram(data_grafik_shopee(), col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_2gram_df = pd.DataFrame(result_df_top_2gram, columns=['N-gram 4 kata menjadi 2 kata', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_2gram_df)
        
        with tab_ngramword_shopee3:
            with st.container(height=400, border=True):
                st.write('Wordcloud N-gram (4 kata)')
                
                @st.cache_data
                def generate_wordcloud_shopee(df):
                    return text_analyzer_project.generate_wordcloud(df, col='N-gram (4 kata)')
                
                plt_generate_wordcloud_shopee = generate_wordcloud_shopee(result_df_top_4gram)
                
                st.pyplot(plt_generate_wordcloud_shopee)
            
    
    
    with tab_ngramword_lazada:
        tab_ngramword_lazada1, tab_ngramword_lazada2, tab_ngramword_lazada3 = st.columns(3)
        # Ganti nilai None atau NaN dengan string kosong
        # df_clean_tokped['content'] = stopword_shopee()['content'].fillna('')

        
        with tab_ngramword_lazada1:
            with st.container(height=400, border=True):
                st.write('N-gram (4 kata) --> Mengambil 4 kata per unit yang sering muncul')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_4gram = text_analyzer_project.top_ngram(data_grafik_lazada(), col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_4gram = pd.DataFrame(result_df_top_4gram, columns=['N-gram (4 kata)', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_4gram)

        with tab_ngramword_lazada2:
            with st.container(height=400, border=True):
                st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_2gram = text_analyzer_project.combine_top_ngram(data_grafik_lazada(), col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_2gram_df = pd.DataFrame(result_df_top_2gram, columns=['N-gram 4 kata menjadi 2 kata', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_2gram_df)
        
        with tab_ngramword_lazada3:
            with st.container(height=400, border=True):
                st.write('Wordcloud N-gram (4 kata)')
                
                @st.cache_data
                def generate_wordcloud_lazada(df):
                    return text_analyzer_project.generate_wordcloud(df, col='N-gram (4 kata)')
                
                plt_generate_wordcloud_lazada = generate_wordcloud_lazada(result_df_top_4gram)
                
                st.pyplot(plt_generate_wordcloud_lazada)
    
    
    with tab_ngramword_tokped:
        tab_ngramword_tokped1, tab_ngramword_tokped2, tab_ngramword_tokped3 = st.columns(3)
        # Ganti nilai None atau NaN dengan string kosong
        # df_clean_tokped['content'] = stopword_shopee()['content'].fillna('')

        
        with tab_ngramword_tokped1:
            with st.container(height=400, border=True):
                st.write('N-gram (4 kata) --> Mengambil 4 kata per unit yang sering muncul')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_4gram = text_analyzer_project.top_ngram(data_grafik_tokped(), col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_4gram = pd.DataFrame(result_df_top_4gram, columns=['N-gram (4 kata)', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_4gram)

        with tab_ngramword_tokped2:
            with st.container(height=400, border=True):
                st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_2gram = text_analyzer_project.combine_top_ngram(data_grafik_tokped(), col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_2gram_df = pd.DataFrame(result_df_top_2gram, columns=['N-gram 4 kata menjadi 2 kata', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_2gram_df)
        
        with tab_ngramword_tokped3:
            with st.container(height=400, border=True):
                st.write('Wordcloud N-gram (4 kata)')
                
                @st.cache_data
                def generate_wordcloud_tokped(df):
                    return text_analyzer_project.generate_wordcloud(df, col='N-gram (4 kata)')
                
                plt_generate_wordcloud_tokped = generate_wordcloud_tokped(result_df_top_4gram)
                
                st.pyplot(plt_generate_wordcloud_tokped)

    
    # SubHeader Most Influential, Most Important Connection, Best Connector
    st.subheader("Most Influential (Paling Berpengaruh), Most Important Connection (Koneksi Paling Penting) & Best Connector (Penghubung Terbaik)")
    st.markdown('''
               Most Influential (Paling Berpengaruh): merujuk pada node (simpul) yang memiliki pengaruh terbesar dalam jaringan. 
               Node ini mungkin memiliki banyak koneksi (hubungan) dengan node lain atau berada pada posisi strategis yang memungkinkan mereka 
               untuk memengaruhi banyak bagian dari jaringan.
                    
               Most Important Connection (Koneksi Paling Penting): merujuk pada hubungan atau jalur yang paling penting dalam jaringan. 
               Koneksi ini mungkin kritis untuk komunikasi atau aliran informasi dalam jaringan.
               
               Best Connector (Penghubung Terbaik): merujuk pada node yang berfungsi sebagai penghubung utama dalam jaringan, menghubungkan 
               berbagai bagian jaringan yang mungkin tidak terhubung langsung tanpa kehadiran node tersebut.     
                         
                ''')
    
    # Tab Most Influential, Most Important Connection, Best Connector
    tab_most_shopee, tab_most_lazada, tab_most_tokped = st.tabs(["Shopee", "Lazada", "Tokopedia"])
    
    with tab_most_shopee:
        col_most_shopee1, col_most_shopee2, col_most_shopee3 = st.columns(3)
        
        # Inisiasi ngram
        result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(data_grafik_shopee(), col='content', n=4, most_common=50)

        # Inisiasi graph
        G = nx.Graph()

        for items, count in result_combine_top_4gram:
            G.add_edge(items[0], items[1], weight=count)

        with col_most_shopee1:
            with st.container(height=350, border=True):
                st.write('Most Influential (Paling Berpengaruh) N-gram 4 kata menjadi 2 kata')
                
                # Most Influential
                most_influential = nx.degree_centrality(G)
                
                # Convert to DataFrame
                df_most_influential = pd.DataFrame(
                    sorted(most_influential.items(), key=lambda x: x[1], reverse=True), 
                    columns=['N-gram 4 kata menjadi 2 kata', 'Degree Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_most_influential, use_container_width=True)

        with col_most_shopee2:
            with st.container(height=350, border=True):
                st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                
                # Most Important Connection
                most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                
                # Convert to DataFrame
                df_most_important = pd.DataFrame(
                    sorted(most_important.items(), key=lambda x: x[1], reverse=True),
                    columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_most_important, use_container_width=True)
                
        with col_most_shopee3:
            with st.container(height=350, border=True):
                st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                
                # Best Connector
                best_connector = nx.betweenness_centrality(G)
                
                # Convert to DataFrame
                df_best_connector = pd.DataFrame(
                    sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
                    columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_best_connector, use_container_width=True)
    
    
    
    with tab_most_lazada:
        col_most_lazada1, col_most_lazada2, col_most_lazada3 = st.columns(3)
        
        # Inisiasi ngram
        result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(data_grafik_lazada(), col='content', n=4, most_common=50)

        # Inisiasi graph
        G = nx.Graph()

        for items, count in result_combine_top_4gram:
            G.add_edge(items[0], items[1], weight=count)

        with col_most_lazada1:
            with st.container(height=350, border=True):
                st.write('Most Influential (Paling Berpengaruh) N-gram 4 kata menjadi 2 kata')
                
                # Most Influential
                most_influential = nx.degree_centrality(G)
                
                # Convert to DataFrame
                df_most_influential = pd.DataFrame(
                    sorted(most_influential.items(), key=lambda x: x[1], reverse=True), 
                    columns=['N-gram 4 kata menjadi 2 kata', 'Degree Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_most_influential, use_container_width=True)

        with col_most_lazada2:
            with st.container(height=350, border=True):
                st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                
                # Most Important Connection
                most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                
                # Convert to DataFrame
                df_most_important = pd.DataFrame(
                    sorted(most_important.items(), key=lambda x: x[1], reverse=True),
                    columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_most_important, use_container_width=True)
                
        with col_most_lazada3:
            with st.container(height=350, border=True):
                st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                
                # Best Connector
                best_connector = nx.betweenness_centrality(G)
                
                # Convert to DataFrame
                df_best_connector = pd.DataFrame(
                    sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
                    columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_best_connector, use_container_width=True)
    
    
    
    with tab_most_tokped:
        col_most_tokped1, col_most_tokped2, col_most_tokped3 = st.columns(3)
        
        # Inisiasi ngram
        result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(data_grafik_tokped(), col='content', n=4, most_common=50)

        # Inisiasi graph
        G = nx.Graph()

        for items, count in result_combine_top_4gram:
            G.add_edge(items[0], items[1], weight=count)

        with col_most_tokped1:
            with st.container(height=350, border=True):
                st.write('Most Influential (Paling Berpengaruh) N-gram 4 kata menjadi 2 kata')
                
                # Most Influential
                most_influential = nx.degree_centrality(G)
                
                # Convert to DataFrame
                df_most_influential = pd.DataFrame(
                    sorted(most_influential.items(), key=lambda x: x[1], reverse=True), 
                    columns=['N-gram 4 kata menjadi 2 kata', 'Degree Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_most_influential, use_container_width=True)

        with col_most_tokped2:
            with st.container(height=350, border=True):
                st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                
                # Most Important Connection
                most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                
                # Convert to DataFrame
                df_most_important = pd.DataFrame(
                    sorted(most_important.items(), key=lambda x: x[1], reverse=True),
                    columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_most_important, use_container_width=True)
                
        with col_most_tokped3:
            with st.container(height=350, border=True):
                st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                
                # Best Connector
                best_connector = nx.betweenness_centrality(G)
                
                # Convert to DataFrame
                df_best_connector = pd.DataFrame(
                    sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
                    columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
                )
                
                # Display DataFrame
                st.dataframe(df_best_connector, use_container_width=True)
    
    
    # SubHeader Network Analisis
    st.subheader("Network Analisis")
    st.markdown('''
               Analisis jaringan (network analysis) adalah pendekatan untuk mempelajari hubungan dan struktur antara entitas yang saling terhubung dalam bentuk 
               grafik atau jaringan. Ini melibatkan pemodelan dan analisis berbagai jenis hubungan dalam sistem kompleks, mulai dari jejaring sosial hingga 
               sistem biologis dan teknologi.      
                ''')
    
    # Tab Ngram dan wordcloud
    tab_network_shopee, tab_network_lazada, tab_network_tokped = st.tabs(["Shopee", "Lazada", "Tokopedia"])
    
    
    with tab_network_shopee:
        st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
        st.markdown('''
                    **Note:** 
                    
                    **Most Common** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                    most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)

                    ''')
        
        # @st.cache_data
        def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata (df, most_common):
            # Tampilkan DataFrame dengan pengaturan tampilan khusus
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram(data_grafik_shopee(), col='content', n=4, most_common=most_common)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

            # Inisiasi layout
            pos = nx.spring_layout(G, k=0.9)

            # Degree centrality
            degree_centrality = nx.degree_centrality(G)
            node_size = [v * 1000 for v in degree_centrality.values()]
            node_color = [v for v in degree_centrality.values()]

            # Plot
            fig, ax = plt.subplots(figsize=(16, 11.8))
            nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

            # Tambahkan judul dan colorbar
            plt.title('Network Analysis of Review', fontsize=16)
            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
            cbar.set_label('Degree Centrality')

            return fig
        
        
        col_mostcommon1, col_mostcommon2 = st.columns(2)
        
        with col_mostcommon1:
            # Buat input untuk parameter most_common di Streamlit
            most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_10')
            
        with col_mostcommon2:
            pass
            # # Buat input untuk parameter most_common di Streamlit
            # most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=10, step=10, key='most_common_input_10')

        # Panggil fungsi dengan parameter most_common yang diberikan
        fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata(data_grafik_shopee(), most_common=most_common_input)

        # Tampilkan plot di Streamlit
        st.pyplot(fig)
    
    
    with tab_network_lazada:
        st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
        st.markdown('''
                    **Note:** 
                    
                    **Most Common** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                    most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                    ''')
        
        # @st.cache_data
        def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata (df, most_common):
            # Tampilkan DataFrame dengan pengaturan tampilan khusus
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram(data_grafik_lazada(), col='content', n=4, most_common=most_common)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

            # Inisiasi layout
            pos = nx.spring_layout(G, k=0.9)

            # Degree centrality
            degree_centrality = nx.degree_centrality(G)
            node_size = [v * 1000 for v in degree_centrality.values()]
            node_color = [v for v in degree_centrality.values()]

            # Plot
            fig, ax = plt.subplots(figsize=(16, 11.8))
            nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
            nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, ax=ax)
            nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

            # Tambahkan judul dan colorbar
            plt.title('Network Analysis of Review', fontsize=16)
            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
            cbar.set_label('Degree Centrality')

            return fig
        
        
        col_mostcommon1, col_mostcommon2 = st.columns(2)
        
        with col_mostcommon1:
            # Buat input untuk parameter most_common di Streamlit
            most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_11')
            
        with col_mostcommon2:
            pass
            # # Buat input untuk parameter most_common di Streamlit
            # most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=10, step=10, key='most_common_input_10')

        # Panggil fungsi dengan parameter most_common yang diberikan
        fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata(data_grafik_lazada(), most_common=most_common_input)

        # Tampilkan plot di Streamlit
        st.pyplot(fig)
    
    
    with tab_network_tokped:
        st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
        st.markdown('''
                    **Note:** 
                    
                    **Most Common** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                    most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                    ''')
        
        # @st.cache_data
        def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata(df, most_common):
            # Tampilkan DataFrame dengan pengaturan tampilan khusus
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram(data_grafik_tokped(), col='content', n=4, most_common=most_common)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

            # Inisiasi layout
            pos = nx.spring_layout(G, k=0.9)

            # Degree centrality
            degree_centrality = nx.degree_centrality(G)
            node_size = [v * 1000 for v in degree_centrality.values()]
            node_color = [v for v in degree_centrality.values()]

            # Plot menggunakan Plotly
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]
                edge_x.append(x0)
                edge_x.append(x1)
                edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                edge_y.append(None)

            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                mode='lines')

            node_x = []
            node_y = []
            for node in G.nodes():
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers+text',
                text=[f'{node} ({degree_centrality[node]:.2f})' for node in G.nodes()],
                textposition="top center",
                marker=dict(
                    size=node_size,
                    color=node_color,
                    colorscale='Blues',
                    line=dict(width=2, color='black')
                ),
                hoverinfo='text'
            )

            fig = go.Figure(data=[edge_trace, node_trace],
                            layout=go.Layout(
                                title='<br>Network Analysis of Review',
                                titlefont_size=16,
                                showlegend=False,
                                hovermode='closest',
                                margin=dict(b=0, l=0, r=0, t=50),
                                annotations=[dict(
                                    text="Degree Centrality",
                                    showarrow=False,
                                    xref="paper", yref="paper",
                                    x=0.005, y=-0.002)],
                                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                paper_bgcolor='white',  # Ganti background menjadi putih
                                plot_bgcolor='white'    # Ganti plot background menjadi putih
                            )
                        )

            return fig
        
        
        col_mostcommon1, col_mostcommon2 = st.columns(2)
        
        with col_mostcommon1:
            # Buat input untuk parameter most_common di Streamlit
            most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_12')
            
        with col_mostcommon2:
            pass
            # # Buat input untuk parameter most_common di Streamlit
            # most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=10, step=10, key='most_common_input_10')

        # Panggil fungsi dengan parameter most_common yang diberikan
        fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata(data_grafik_tokped(), most_common=most_common_input)

        # Tampilkan plot di Streamlit
        st.plotly_chart(fig)
        
        
        







