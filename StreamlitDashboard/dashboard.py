# Import library
import streamlit as st
from PIL import Image
import pandas as pd
from TextPreProcessing import text_analyzer_project
import os
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px

def dashboard():
    # Menambahkan CSS untuk mempercantik radio button
    st.markdown(
        """
        <style>
        /* Gaya untuk container radio button */
        div[role="radiogroup"] {
            display: flex;
            justify-content: left;
            gap: 20px;
        }
        /* Gaya untuk setiap label radio button */
        div[role="radiogroup"] > label {
            background-color: #0000ff;
            border-radius: 20px;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        /* Gaya untuk label saat hover */
        div[role="radiogroup"] > label:hover {
            background-color: #ffcccb;
        }
        /* Gaya untuk label yang terpilih */
        div[role="radiogroup"] > label[aria-checked="true"] {
            background-color: #f46b6b;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True
    )


    # Menggunakan radio button sebagai tab
    selected_language = st.radio(
        "Pilih Bahasa / Select Language", 
        ["Bahasa Indonesia", "English"], 
        horizontal=True
    )

    # Menampilkan konten berdasarkan pilihan bahasa
    if selected_language == "Bahasa Indonesia":
        # Menampilkan gambar di atas dashboard
        def display_image(image_path, use_column_width=True):
            image = Image.open(image_path)
            st.image(image, use_column_width=use_column_width)

        # Tampilan gambar header
        display_image("./assets/gambar/dashboard title.png", use_column_width=True)
        
        # Load dataset
        df_clean_shopee = pd.read_parquet("./assets/dataset/data_preprocess_shopee/df_stopword_shopee.parquet")
        df_clean_lazada = pd.read_parquet("./assets/dataset/data_preprocess_lazada/df_stopword_lazada.parquet")
        df_clean_tokped = pd.read_parquet("./assets/dataset/data_preprocess_tokped/df_stopword_tokped.parquet")

        # Konversi kolom 'at' menjadi datetime
        df_clean_shopee['at'] = pd.to_datetime(df_clean_shopee['at'], errors='coerce')
        df_clean_lazada['at'] = pd.to_datetime(df_clean_lazada['at'], errors='coerce')
        df_clean_tokped['at'] = pd.to_datetime(df_clean_tokped['at'], errors='coerce')
        
        # Menambah kolom untuk tahun
        df_clean_shopee['year'] = df_clean_shopee['at'].dt.year
        df_clean_lazada['year'] = df_clean_lazada['at'].dt.year
        df_clean_tokped['year'] = df_clean_tokped['at'].dt.year
        
        
        df_clean_shopee['marketplace'] = 'Shopee'
        df_clean_lazada['marketplace'] = 'Lazada'
        df_clean_tokped['marketplace'] = 'Tokopedia'

        combined_df = pd.concat([df_clean_shopee[['year', 'marketplace']],
                                df_clean_lazada[['year', 'marketplace']],
                                df_clean_tokped[['year', 'marketplace']]])
        
        
        st.markdown(''' 
                    Berikut ini adalah dashboard sentiment analisis marketplace online dengan fokus aplikasi shopee, lazada dan tokopedia.
                    Dataset yang ditampilkan adalah dataset yang sudah dipreprocessing (lower case, remove emoji, text cleaning, slang tranformation dan 
                    remove stopwords) dapat dilihat pada bagian preprocessing data. Pembaca juga dapat melihat exploratory data analisis pada bagian 
                    exploratory data analisis.
                    Dataset ini terdiri dari beberapa kolom, yaitu : content : berisi review pelanggan pengguna aplikasi yang sudah dipreprocessing, 
                    at : tanggal dan waktu review pelanggan pengguna, year : tahun review pelanggan pengguna.
                    
                                
                                ''')
        
        
        # Misalnya, kita punya df_clean_shopee, df_clean_lazada, df_clean_tokped
        stats_shopee = text_analyzer_project.calculate_text_statistics(df_clean_shopee, 'content')
        stats_lazada = text_analyzer_project.calculate_text_statistics(df_clean_lazada, 'content')
        stats_tokped = text_analyzer_project.calculate_text_statistics(df_clean_tokped, 'content')
        
        
        with st.container(height=185, border=True):
                # Menampilkan hasil untuk setiap marketplace
                # st.write(f"#### Statistik Deskriptif")
            
                cols2 = st.columns([1, 1, 1])

                with cols2[0]:
                    st.write(text_analyzer_project.display_statistics(stats_shopee, "Shopee"), unsafe_allow_html=True)

                with cols2[1]:
                    st.write(text_analyzer_project.display_statistics(stats_lazada, "Lazada"), unsafe_allow_html=True)

                with cols2[2]:
                    st.write(text_analyzer_project.display_statistics(stats_tokped, "Tokopedia"), unsafe_allow_html=True)
        

        # Mengatur kolom untuk menampilkan card secara horizontal
        row_1 = st.columns(2)
        
        with row_1[0]:
            with st.container(height=480, border=True):
                # Membuat plot
                fig = px.histogram(combined_df, 
                                x='year', 
                                color='marketplace', 
                                barmode='group', 
                                labels={'year':'Year', 'marketplace':'Marketplace'},
                                title='Perbandingan Jumlah Ulasan Berdasarkan Tahun')

                # Menyesuaikan tampilan
                fig.update_layout(
                    xaxis_title='Tahun', 
                    yaxis_title='Jumlah Ulasan', 
                    title_x=0.2, 
                    template='plotly_white',
                    plot_bgcolor='white',  # Background plot menjadi putih
                    paper_bgcolor='white',  # Background seluruh area menjadi putih
                    xaxis=dict(
                        title_font=dict(size=14, color='black'),
                        tickfont=dict(size=12, color='black')
                    ),
                    yaxis=dict(
                        title_font=dict(size=14, color='black'),
                        tickfont=dict(size=12, color='black')
                    ),
                    title=dict(
                        font=dict(size=16, color='black')
                    ),
                    legend=dict(
                        title_font=dict(size=12, color='black'),  # Mengubah warna teks judul legend menjadi hitam
                        font=dict(size=12, color='black')       # Mengubah warna teks label legend menjadi hitam
                        # bordercolor='black',                      # Mengatur warna border legend (opsional)
                        # borderwidth=1                            # Mengatur lebar border legend (opsional)
                    )
                )

                # Menampilkan plot di Streamlit
                st.plotly_chart(fig)   
                
        with row_1[1]:
            with st.container(height=480, border=True):
                # Asumsikan df_clean_shopee, df_clean_lazada, df_clean_tokped sudah ada
                n = 2  # Misal kita menggunakan bigram
                most_common = 5  # Mengambil 20 n-gram paling umum

                # Menghitung n-gram untuk setiap dataset
                df_ngram_shopee = text_analyzer_project.combine_top_ngram_df(df_clean_shopee, col='content', n=n, most_common=most_common)
                df_ngram_lazada = text_analyzer_project.combine_top_ngram_df(df_clean_lazada, col='content', n=n, most_common=most_common)
                df_ngram_tokped = text_analyzer_project.combine_top_ngram_df(df_clean_tokped, col='content', n=n, most_common=most_common)

                # Menambahkan kolom marketplace
                df_ngram_shopee['marketplace'] = 'Shopee'
                df_ngram_lazada['marketplace'] = 'Lazada'
                df_ngram_tokped['marketplace'] = 'Tokopedia'

                # Menggabungkan semua DataFrame
                combined_ngram_df = pd.concat([df_ngram_shopee, df_ngram_lazada, df_ngram_tokped])
                
                
                combined_ngram_df = combined_ngram_df.sort_values(by=['ngram', 'frequency'], ascending=[True, False])

                
                # Membuat bar chart
                fig = px.bar(combined_ngram_df, 
                            x='ngram', 
                            y='frequency', 
                            color='marketplace', 
                            labels={'ngram': 'N-gram', 'frequency': 'Frequency'},
                            title='Top 5 N-grams Yang Sering Muncul Diketiga Marketplace')

                # Menyesuaikan tampilan
                fig.update_layout(
                    xaxis_title='N-gram', 
                    yaxis_title='Frequency', 
                    title_x=0.2, 
                    template='plotly_white',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis=dict(
                        title_font=dict(size=14, color='black'),
                        tickfont=dict(size=12, color='black'),
                        categoryorder='total descending'  # Mengurutkan sumbu x berdasarkan frekuensi total
                    ),
                    yaxis=dict(
                        title_font=dict(size=14, color='black'),
                        tickfont=dict(size=12, color='black')
                    ),
                    title=dict(
                        font=dict(size=16, color='black')
                    ),
                    legend=dict(
                        title_font=dict(size=12, color='black'),
                        font=dict(size=12, color='black')
                    )
                )

                # Menampilkan plot di Streamlit
                st.plotly_chart(fig)
        
        
        # row0 = st.columns(2)
        
        
        # with row0[0]:
        #     # Asumsikan df_clean_shopee, df_clean_lazada, df_clean_tokped sudah ada
        #     n = 2  # Misal kita menggunakan bigram
        #     most_common = 5  # Mengambil 20 n-gram paling umum

        #     # Menghitung n-gram untuk setiap dataset
        #     df_ngram_shopee = text_analyzer_project.combine_top_ngram_df(df_clean_shopee, col='content', n=n, most_common=most_common)
        #     df_ngram_lazada = text_analyzer_project.combine_top_ngram_df(df_clean_lazada, col='content', n=n, most_common=most_common)
        #     df_ngram_tokped = text_analyzer_project.combine_top_ngram_df(df_clean_tokped, col='content', n=n, most_common=most_common)

        #     # Menambahkan kolom marketplace
        #     df_ngram_shopee['marketplace'] = 'Shopee'
        #     df_ngram_lazada['marketplace'] = 'Lazada'
        #     df_ngram_tokped['marketplace'] = 'Tokopedia'

        #     # Menggabungkan semua DataFrame
        #     combined_ngram_df = pd.concat([df_ngram_shopee, df_ngram_lazada, df_ngram_tokped])
            
            
        #     combined_ngram_df = combined_ngram_df.sort_values(by=['ngram', 'frequency'], ascending=[True, False])

            
        #     with st.container(height=480, border=True):
        #         # Membuat bar chart
        #         fig = px.bar(combined_ngram_df, 
        #                     x='ngram', 
        #                     y='frequency', 
        #                     color='marketplace', 
        #                     labels={'ngram': 'N-gram', 'frequency': 'Frequency'},
        #                     title='Top 5 N-grams Yang Sering Muncul Diketiga Marketplace')

        #         # Menyesuaikan tampilan
        #         fig.update_layout(
        #             xaxis_title='N-gram', 
        #             yaxis_title='Frequency', 
        #             title_x=0.2, 
        #             template='plotly_white',
        #             plot_bgcolor='white',
        #             paper_bgcolor='white',
        #             xaxis=dict(
        #                 title_font=dict(size=14, color='black'),
        #                 tickfont=dict(size=12, color='black'),
        #                 categoryorder='total descending'  # Mengurutkan sumbu x berdasarkan frekuensi total
        #             ),
        #             yaxis=dict(
        #                 title_font=dict(size=14, color='black'),
        #                 tickfont=dict(size=12, color='black')
        #             ),
        #             title=dict(
        #                 font=dict(size=16, color='black')
        #             ),
        #             legend=dict(
        #                 title_font=dict(size=12, color='black'),
        #                 font=dict(size=12, color='black')
        #             )
        #         )

        #         # Menampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row0[1]:
        #     # Asumsikan df_clean_shopee, df_clean_lazada, df_clean_tokped sudah ada
        #     n = 2  # Misal kita menggunakan bigram
        #     most_common = 5  # Mengambil 20 n-gram paling umum

        #     # Menghitung n-gram untuk setiap dataset
        #     df_ngram_shopee = text_analyzer_project.combine_top_ngram_df(df_clean_shopee, col='content', n=n, most_common=most_common)
        #     df_ngram_lazada = text_analyzer_project.combine_top_ngram_df(df_clean_lazada, col='content', n=n, most_common=most_common)
        #     df_ngram_tokped = text_analyzer_project.combine_top_ngram_df(df_clean_tokped, col='content', n=n, most_common=most_common)

        #     # Menambahkan kolom marketplace
        #     df_ngram_shopee['marketplace'] = 'Shopee'
        #     df_ngram_lazada['marketplace'] = 'Lazada'
        #     df_ngram_tokped['marketplace'] = 'Tokopedia'

        #     # Menggabungkan semua DataFrame
        #     combined_ngram_df = pd.concat([df_ngram_shopee, df_ngram_lazada, df_ngram_tokped])
            
            
        #     combined_ngram_df = combined_ngram_df.sort_values(by=['ngram', 'frequency'], ascending=[True, False])

            
        #     combined_ngram_df_sorted = combined_ngram_df.sort_values(by=['marketplace', 'frequency'], ascending=[True, False])
            
        #     # Menggunakan Streamlit container
        #     with st.container(height=480, border=True):
        #         # Membuat bar chart
        #         fig = px.bar(combined_ngram_df_sorted, 
        #                     x='ngram', 
        #                     y='frequency', 
        #                     color='marketplace', 
        #                     facet_col='marketplace',
        #                     labels={'ngram': 'N-gram', 'frequency': 'Frequency'},
        #                     title='Top N-grams Berdasarkan Marketplace')

        #         # Menyesuaikan tampilan
        #         fig.update_layout(
        #             xaxis_title='N-gram', 
        #             yaxis_title='Frequency', 
        #             title_x=0.2, 
        #             template='plotly_white',
        #             plot_bgcolor='white',
        #             paper_bgcolor='white',
        #             xaxis=dict(
        #                 title_font=dict(size=14, color='black'),
        #                 tickfont=dict(size=12, color='black'),
        #                 categoryorder='total descending',  # Mengurutkan sumbu x berdasarkan frekuensi total
        #                 tickmode='array',  # Mode tick untuk memastikan kategori ditampilkan sesuai urutan
        #             ),
        #             yaxis=dict(
        #                 title_font=dict(size=14, color='black'),
        #                 tickfont=dict(size=12, color='black'),
        #                 tickmode='array',  # Mode tick untuk memastikan angka ditampilkan sesuai urutan
        #             ),
        #             title=dict(
        #                 font=dict(size=16, color='black')
        #             ),
        #             legend=dict(
        #                 title_font=dict(size=12, color='black'),
        #                 font=dict(size=12, color='black')
        #             )
        #         )

        #         # Menampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        def display_summary(platform, positive, negative, neutral=None):
            """
            Fungsi untuk menampilkan ringkasan analisis teks dalam bentuk card di Streamlit dengan tampilan lebih ringkas.
            """
            st.markdown(f"""
            <div style="background-color: #ffffff; padding: 10px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0px 3px 6px rgba(0,0,0,0.1);">
                <h4 style="color: #333333; margin-bottom: 8px;">{platform}</h4>
                <h5 style="color: #008000; margin-bottom: 4px;">Sentimen Positif</h5>
                <p style="color: #000000; font-size: 14px; margin-bottom: 8px;">{positive}</p>
                <h5 style="color: #FF0000; margin-bottom: 4px;">Sentimen Negatif</h5>
                <p style="color: #000000; font-size: 14px; margin-bottom: 8px;">{negative}</p>
                {'<h5 style="color: #000080; margin-bottom: 4px;">Sentimen Netral</h5><p style="color: #000000; font-size: 14px; margin-bottom: 8px;">' + neutral + '</p>' if neutral else ''}
            </div>
            """, unsafe_allow_html=True)

        col_nar = st.columns(3)
        
        with col_nar[0]:
            with st.container(height=380, border=True):
                # Layout Streamlit# Shopee
                positive_shopee = "Kata 'Belanja Shopee' sering dikaitkan dengan 'gratis ongkir', pengguna merasa terbantu dalam memenuhi kebutuhan."
                negative_shopee = "Kata 'Barang tidak' sering kali terkait dengan barang yang tidak sesuai pesanan, deskripsi, atau gambar. 'Biaya layanan' dan 'biaya penanganan' juga menimbulkan sentimen negatif, walau tidak sering dibahas."
                display_summary("Shopee", positive_shopee, negative_shopee)
                

        with col_nar[1]:
            with st.container(height=380, border=True):
                # Lazada
                positive_lazada = "Kata 'Belanja Lazada' dikaitkan dengan kemudahan, harga murah, dan pengiriman cepat."
                negative_lazada = "Kata 'Barang tidak' dan 'gratis ongkir' kadang menerima ulasan negatif terkait ketidaksesuaian barang dan batasan minimal belanja untuk voucher."
                display_summary("Lazada", positive_lazada, negative_lazada)
                st.write("")
                st.write("")

        
        with col_nar[2]:
            with st.container(height=380, border=True):
                # Tokopedia
                positive_tokopedia = "Kata 'Terimakasih Tokopedia' sering dikaitkan dengan 'Skill Academy' dan 'sangat membantu', dengan ulasan positif mengenai kemudahan dan manfaat dari pelatihan yang disediakan."
                neutral_tokopedia = "Kata 'Skill Academy' terkait dengan pelatihan prakerja mendapat ulasan netral."
                display_summary("Tokopedia", positive_tokopedia, "", neutral_tokopedia)
        
        

        
        
        
        # Filter berdasarkan tahun
        # years = sorted(df_clean_shopee['year'].dropna().unique())  # Mengambil tahun unik
        # selected_years = st.multiselect('Pilih Tahun Untuk Melihat Tahun Tertentu yang diinginkan (Bisa Multiple Input):', years, key='year_selection_1')

        # if selected_years:
        #     df_clean_shopee = df_clean_shopee[df_clean_shopee['year'].isin(selected_years)]
        #     df_clean_lazada = df_clean_lazada[df_clean_lazada['year'].isin(selected_years)]
        #     df_clean_tokped = df_clean_tokped[df_clean_tokped['year'].isin(selected_years)]
        #     st.write(f"Data untuk tahun {', '.join(map(str, selected_years))}")
        
        # # Layout 3 kolom untuk masing-masing platform
        # row1 = st.columns(3)
        
        # with row1[0]:
        #     st.title("Shopee")
                
        #     with st.container(height=400, border=True):
        #         st.markdown('''
        #                     Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di Shopee adalah "belanja shopee', 
        #                     "gratis ongkir",  "barang tidak", "shopee pay", "perbaikan mohon", "biaya layanan", 
        #                     dan "biaya penanganan".
                            
        #                     - Sentimen Positif: "Belanja Shopee" sering dikaitkan dengan "gratis ongkir", pengguna merasa terbantu dalam memenuhi kebutuhan.
                            
        #                     - Sentimen Negatif: "Barang tidak" sering kali terkait dengan barang yang tidak sesuai pesanan, deskripsi, atau gambar. "Biaya layanan" 
        #                     dan "biaya penanganan" juga menimbulkan sentimen negatif, walau tidak sering dibahas.
        #                     ''')
            
            
            
            # with st.container(height=400, border=True):
            #     st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            #     result_df_top_4gram_shopee = text_analyzer_project.combine_top_ngram(df_clean_shopee, col='content', n=4)
            #     result_df_top_4gram_shopee = pd.DataFrame(result_df_top_4gram_shopee, columns=['N-gram (4 kata)', 'Frekuensi'])
            #     st.dataframe(result_df_top_4gram_shopee, use_container_width=True)
                
                
                
            # with st.container(height=380, border=True):
            #     st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
                
            #     @st.cache_data(persist=True)
            #     def generate_wordcloud_shopee(df):
            #         return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
                
            #     plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_shopee)
            #     st.pyplot(plt_generate_wordcloud_shopee)

        # with row1[1]:
        #     st.title("Lazada")
            
            
        #     with st.container(height=400, border=True):
        #         st.markdown('''
        #                     Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di lazada adalah "belanja lazada", 
        #                     "tidak sesuai",  "barang tidak", "gratis ongkir", "pengiriman cepat".

        #                     Kata "belanja lazada" : identik dengan sentimen positif bagi shopee. Pengguna sangat senang, sangat puas berbelanja dilazada.
        #                     beberapa komentar positif lainnya belanja dilazada tidak ribet, harga murah dan tidak kecewa. Kata "belanja lazada" juga 
        #                     sering dikaitkan dengan kata "gratis ongkir", "barang tidak", dan "pengiriman cepat.
                            
        #                     Kata "belanja lazada" yang dikaitkkan dengan "gratis ongkir" menerima ulasan negatif dari pengguna lazada, yaitu perihal minimal
        #                     belanja dan tidak tersedianya voucher gratis ongkir.
                            
        #                     Kata "belanja lazada" yang dikaitkan dengan "barang tidak" menerima ulasan negatif dari pengguna, yaitu : barang yang diterima 
        #                     pengguna tidak sesuai gambar, tidak sesuai deskripsi dan pesanan.
                            
        #                     Kata "belanja lazada" yang dikaitkan dengan "pengiriman cepat" mendapat ulasan positif dari pengguna dimana kurir yang mengantarkan
        #                     barang ramah. 
                            
        #                     ''')
            
            # with st.container(height=400, border=True):
            #     st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            #     result_df_top_4gram_lazada = text_analyzer_project.combine_top_ngram(df_clean_lazada, col='content', n=4)
            #     result_df_top_4gram_lazada = pd.DataFrame(result_df_top_4gram_lazada, columns=['N-gram (4 kata)', 'Frekuensi'])
            #     st.dataframe(result_df_top_4gram_lazada, use_container_width=True)
                
                
            # with st.container(height=380, border=True):
            #     st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
                
            #     @st.cache_data(persist=True)
            #     def generate_wordcloud_shopee(df):
            #         return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
                
            #     plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_lazada)
            #     st.pyplot(plt_generate_wordcloud_shopee)

        # with row1[2]:
        #     st.title("Tokopedia")
            
        #     with st.container(height=400, border=True):
        #         st.markdown('''
        #                     Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di tokopedia adalah "terimakasih tokopedia", 
        #                     "sangat menbantu",  "skill academy", "pelatihan prakerja".

        #                     Kata "terimakasih tokopedia" mendapatkan ulasan positif dari penggunanya berupa komentar sangat bagus dan mudah dipahami.
        #                     Kata "terimakasih tokopedia" terkait langsung dengan kata "skill academy" dan kata "sangat membantu" yang mendapatkan ulasan positif
        #                     dari para penggunanya. 
                            
        #                     Kata "terimakasih tokopedia" yang berkaitan dengan kata "skill academy" mendapatkan ulasan netral seperti membeli pelatihan 
        #                     by ruang guru, kartu prakerja dan pelatihan prakerja.
                            
        #                     Kata "terimakasih tokopedia" yang berkaitan dengan kata "sangat membantu" mendapatkan ulasan positif seperti sangat membantu 
        #                     mengikuti pelatihan dan menyelesaikan pelatihan. 
        #                     ''')
                
            # with st.container(height=400, border=True):
            #     st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            #     result_df_top_4gram_tokped = text_analyzer_project.combine_top_ngram(df_clean_tokped, col='content', n=4)
            #     result_df_top_4gram_tokped = pd.DataFrame(result_df_top_4gram_tokped, columns=['N-gram (4 kata)', 'Frekuensi'])
            #     st.dataframe(result_df_top_4gram_tokped, use_container_width=True)
                
                
                
            # with st.container(height=380, border=True):
            #     st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
                
            #     @st.cache_data(persist=True)
            #     def generate_wordcloud_shopee(df):
            #         return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
                
            #     plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_tokped)
            #     st.pyplot(plt_generate_wordcloud_shopee)

        # with st.container(height=80, border=True):
        #     st.markdown('''
        #         Most Influential (Paling Berpengaruh):merujuk pada node (simpul) yang memiliki pengaruh terbesar dalam jaringan. 
        #         Node ini mungkin memiliki banyak koneksi (hubungan) dengan node lain atau berada pada posisi strategis yang memungkinkan mereka 
        #         untuk memengaruhi banyak bagian dari jaringan.
        #         ''')

        row2 = st.columns(3)
        
        with row2[0]:
            # Inisiasi ngram
                result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

                # Inisiasi graph
                G = nx.Graph()

                for items, count in result_combine_top_4gram:
                    G.add_edge(items[0], items[1], weight=count)

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
                    
                    
                    
        with row2[1]:
            # Inisiasi ngram
                result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

                # Inisiasi graph
                G = nx.Graph()

                for items, count in result_combine_top_4gram:
                    G.add_edge(items[0], items[1], weight=count)

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
                    
                    
                    
        with row2[2]:
            # Inisiasi ngram
                result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

                # Inisiasi graph
                G = nx.Graph()

                for items, count in result_combine_top_4gram:
                    G.add_edge(items[0], items[1], weight=count)

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
        
        
        
        # with st.container(height=80, border=True):
        #             st.markdown('''
        #                 Most Important Connection (Koneksi Paling Penting): merujuk pada hubungan atau jalur yang paling penting dalam jaringan. 
        #                 Koneksi ini mungkin kritis untuk komunikasi atau aliran informasi dalam jaringan.
        #                 ''')
        
        
        # row3 = st.columns(3)
        
        # with row3[0]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                    
        #             # Most Important Connection
        #             most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                    
        #             # Convert to DataFrame
        #             df_most_important = pd.DataFrame(
        #                 sorted(most_important.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_most_important, use_container_width=True)
                    
                    
                    
        # with row3[1]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                    
        #             # Most Important Connection
        #             most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                    
        #             # Convert to DataFrame
        #             df_most_important = pd.DataFrame(
        #                 sorted(most_important.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_most_important, use_container_width=True)
                    
                    
                    
        # with row3[2]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                    
        #             # Most Important Connection
        #             most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                    
        #             # Convert to DataFrame
        #             df_most_important = pd.DataFrame(
        #                 sorted(most_important.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_most_important, use_container_width=True)
        
        
        # # Hitung Betweenness Centrality untuk ketiga dataset
        # df_best_connector_shopee = text_analyzer_project.compute_betweenness_centrality(df_clean_shopee, col='content', n=4, most_common=5, marketplace_name='Shopee')
        # df_best_connector_lazada = text_analyzer_project.compute_betweenness_centrality(df_clean_lazada, col='content', n=4, most_common=5, marketplace_name='Lazada')
        # df_best_connector_tokped = text_analyzer_project.compute_betweenness_centrality(df_clean_tokped, col='content', n=4, most_common=5, marketplace_name='Tokopedia')

        # # Gabungkan data dari ketiga marketplace
        # combined_df_best_connector = pd.concat([df_best_connector_shopee, df_best_connector_lazada, df_best_connector_tokped])

        # # Plot bar chart
        # with st.container(height=480, border=True):
        #     fig = px.bar(combined_df_best_connector,
        #                 x='N-gram', 
        #                 y='Betweenness Centrality', 
        #                 color='Marketplace', 
        #                 title='Best Connector N-gram 4 Kata Menjadi 2 Kata (Comparative)',
        #                 barmode='group',
        #                 labels={'N-gram': 'N-gram 4 Kata', 'Betweenness Centrality': 'Betweenness Centrality'},
        #                 height=400)
            
        #     # Mengatur tampilan chart
        #     fig.update_layout(
        #         xaxis_title='N-gram 4 Kata', 
        #         yaxis_title='Betweenness Centrality',
        #         title_x=0.5,
        #         template='plotly_white',
        #         plot_bgcolor='white',
        #         paper_bgcolor='white',
        #         xaxis=dict(
        #             title_font=dict(size=14, color='black'),
        #             tickfont=dict(size=12, color='black'),
        #             categoryorder='total descending'
        #         ),
        #         yaxis=dict(
        #             title_font=dict(size=14, color='black'),
        #             tickfont=dict(size=12, color='black')
        #         ),
        #         title=dict(
        #             font=dict(size=16, color='black')
        #         ),
        #         legend=dict(
        #             title_font=dict(size=12, color='black'),
        #             font=dict(size=12, color='black')
        #         )
        #     )
            
        #     # Menampilkan plot di Streamlit
        #     st.plotly_chart(fig)
        
        
        
        # with st.container(height=80, border=True):
        #             st.markdown('''
        #                 Best Connector (Penghubung Terbaik): merujuk pada node yang berfungsi sebagai penghubung utama dalam jaringan, menghubungkan 
        #                 berbagai bagian jaringan yang mungkin tidak terhubung langsung tanpa kehadiran node tersebut.
        #                 ''')
        
        
        # row4 = st.columns(3)
        
        # with row4[0]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                    
        #             # Best Connector
        #             best_connector = nx.betweenness_centrality(G)
                    
        #             # Convert to DataFrame
        #             df_best_connector = pd.DataFrame(
        #                 sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_best_connector, use_container_width=True)
                    
                    
                    
        # with row4[1]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                    
        #             # Best Connector
        #             best_connector = nx.betweenness_centrality(G)
                    
        #             # Convert to DataFrame
        #             df_best_connector = pd.DataFrame(
        #                 sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_best_connector, use_container_width=True)
                    
                    
                    
        # with row4[2]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                    
        #             # Best Connector
        #             best_connector = nx.betweenness_centrality(G)
                    
        #             # Convert to DataFrame
        #             df_best_connector = pd.DataFrame(
        #                 sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_best_connector, use_container_width=True)
        
        
        with st.container(height=300, border=True):
                    st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
                    st.markdown('''
                                **Noted :**
                                
                                **"Most Common"** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                                most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                                
                                **"Center Node atau Node Pusat"** adalah titik fokus atau simpul utama dalam sebuah graf yang menjadi pusat perhatian atau 
                                referensi dalam analisis.                                                                  
                                **"Pilih parameter center node berdasarkan kata yang ada di Most influencial**"" (Center node yang diinput default)
                                
                                **"Depth atau Kedalaman"** dalam konteks graf menunjukkan seberapa jauh Anda ingin mengeksplorasi 
                                dari node pusat. Ini mengacu pada jumlah lapisan atau tingkat kedekatan yang ingin Anda pertimbangkan dalam analisis.
                                ''')
        
        
        row5 = st.columns(3)
        
        with row5[0]:
            with st.container(height=800, border=True):
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df, most_common, center_node, depth):
                        result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

                        G = nx.Graph()
                        for items, count in result_combine_top_4gram:
                            G.add_edge(items[0], items[1], weight=count)

                        def get_subgraph(G, center_node, depth):
                            nodes = set([center_node])
                            for _ in range(depth):
                                neighbors = set()
                                for node in nodes:
                                    neighbors.update(G.neighbors(node))
                                nodes.update(neighbors)
                            return G.subgraph(nodes)

                        if center_node in G.nodes():
                            subgraph = get_subgraph(G, center_node, depth)
                            pos = nx.spring_layout(subgraph, k=0.5)

                            degree_centrality = nx.degree_centrality(subgraph)
                            node_size = [v * 1000 for v in degree_centrality.values()]
                            node_color = [v for v in degree_centrality.values()]

                            fig, ax = plt.subplots(figsize=(20, 30))
                            nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                            nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                            nx.draw_networkx_labels(subgraph, pos, font_size=25, ax=ax)

                            plt.title('Network Analysis of Review', fontsize=25)
                            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                            cbar.set_label('Degree Centrality')

                            return fig
                        else:
                            st.info('''
                            **"Pilih parameter center node berdasarkan kata yang ada di Most influencial**"" (Center node yang diinput default)
                            ''')
                            return None

                col_mostcommon11, col_mostcommon21, col_mostcommon31 = st.columns(3)

                with col_mostcommon11:
                    most_common_input2 = st.number_input('Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_1')

                with col_mostcommon21:
                    center_node = st.text_input("Center Node:", value='belanja shopee', key='center_node_input_1')

                with col_mostcommon31:
                    depth = st.number_input('Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_2')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_shopee, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
        
        
        with row5[1]:
            with st.container(height=800, border=True):
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df, most_common, center_node, depth):
                        result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

                        G = nx.Graph()
                        for items, count in result_combine_top_4gram:
                            G.add_edge(items[0], items[1], weight=count)

                        def get_subgraph(G, center_node, depth):
                            nodes = set([center_node])
                            for _ in range(depth):
                                neighbors = set()
                                for node in nodes:
                                    neighbors.update(G.neighbors(node))
                                nodes.update(neighbors)
                            return G.subgraph(nodes)

                        if center_node in G.nodes():
                            subgraph = get_subgraph(G, center_node, depth)
                            pos = nx.spring_layout(subgraph, k=0.5)

                            degree_centrality = nx.degree_centrality(subgraph)
                            node_size = [v * 1000 for v in degree_centrality.values()]
                            node_color = [v for v in degree_centrality.values()]

                            fig, ax = plt.subplots(figsize=(20, 30))
                            nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                            nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                            nx.draw_networkx_labels(subgraph, pos, font_size=25, ax=ax)

                            plt.title('Network Analysis of Review', fontsize=25)
                            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                            cbar.set_label('Degree Centrality')

                            return fig
                        else:
                            st.info('''
                            **"Pilih parameter center node berdasarkan kata yang ada di Most influencial, Most importance 
                                connection dan Best connector**"" (Center node yang diinput default)
                            ''')
                            return None

                col_mostcommon11, col_mostcommon21, col_mostcommon31 = st.columns(3)

                with col_mostcommon11:
                    most_common_input2 = st.number_input('Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_3')

                with col_mostcommon21:
                    center_node = st.text_input("Center Node:", value='belanja lazada', key='center_node_input_2')

                with col_mostcommon31:
                    depth = st.number_input('Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_4')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_lazada, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
        
        
        with row5[2]:
            with st.container(height=800, border=True):
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df, most_common, center_node, depth):
                        result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

                        G = nx.Graph()
                        for items, count in result_combine_top_4gram:
                            G.add_edge(items[0], items[1], weight=count)

                        def get_subgraph(G, center_node, depth):
                            nodes = set([center_node])
                            for _ in range(depth):
                                neighbors = set()
                                for node in nodes:
                                    neighbors.update(G.neighbors(node))
                                nodes.update(neighbors)
                            return G.subgraph(nodes)

                        if center_node in G.nodes():
                            subgraph = get_subgraph(G, center_node, depth)
                            pos = nx.spring_layout(subgraph, k=0.5)

                            degree_centrality = nx.degree_centrality(subgraph)
                            node_size = [v * 1000 for v in degree_centrality.values()]
                            node_color = [v for v in degree_centrality.values()]

                            fig, ax = plt.subplots(figsize=(20, 30))
                            nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                            nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                            nx.draw_networkx_labels(subgraph, pos, font_size=25, ax=ax)

                            plt.title('Network Analysis of Review', fontsize=25)
                            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                            cbar.set_label('Degree Centrality')

                            return fig
                        else:
                            st.info('''
                            **"Pilih parameter center node berdasarkan kata yang ada di Most influencial, Most importance 
                                connection dan Best connector**"" (Center node yang diinput default)
                            ''')
                            return None

                col_mostcommon11, col_mostcommon21, col_mostcommon31 = st.columns(3)

                with col_mostcommon11:
                    most_common_input2 = st.number_input('Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_5')

                with col_mostcommon21:
                    center_node = st.text_input("Center Node:", value='terimakasih tokopedia', key='center_node_input_3')

                with col_mostcommon31:
                    depth = st.number_input('Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_6')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_tokped, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
        
        
        # with st.container(height=80, border=True):
        #     st.markdown('''
        #                 Distribusi frekuensi jumlah huruf adalah penghitungan seberapa sering sebuah teks memiliki jumlah huruf tertentu. 
        #                 Misalnya, jika Anda memiliki kumpulan teks, distribusi ini akan menunjukkan seberapa banyak teks yang memiliki, 
        #                 misalnya, 5 huruf, 10 huruf, dan seterusnya. Distribusi ini memberikan gambaran tentang seberapa panjang atau pendek karakteristik 
        #                 teks dalam hal jumlah huruf.
        #                     ''')
        
        
        # row6 = st.columns(3)
        
        # with row6[0]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_shopee, 'content', bins=100)
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row6[1]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_lazada, 'content', bins=100)
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row6[2]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_tokped, 'content', bins=100)
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with st.container(height=100, border=True):
        #     st.markdown('''
        #                 Distribusi frekuensi jumlah kata per teks adalah penghitungan seberapa sering jumlah kata tertentu muncul dalam sebuah teks. 
        #                 Sebagai contoh, jika Anda menganalisis sekumpulan ulasan produk, distribusi ini akan menunjukkan berapa banyak ulasan yang terdiri 
        #                 dari, misalnya, 5 kata, 10 kata, dan seterusnya. Hal ini membantu memahami apakah teks cenderung terdiri dari sedikit kata (pendek) 
        #                 atau banyak kata (panjang).
        #                     ''')
        
        
        # row6 = st.columns(3)
        
        # with row6[0]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.freq_of_words_plotly(df_clean_shopee, 'content')
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row6[1]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.freq_of_words_plotly(df_clean_lazada, 'content')
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row6[2]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.freq_of_words_plotly(df_clean_tokped, 'content')
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with st.container(height=100, border=True):
        #     st.markdown('''
        #                 Distribusi frekuensi panjang kata rata-rata adalah penghitungan yang menunjukkan seberapa sering kata-kata dalam teks memiliki 
        #                 panjang tertentu jika dihitung rata-rata. Misalnya, jika sebuah teks terdiri dari 10 kata dengan jumlah total huruf sebanyak 50, 
        #                 maka panjang kata rata-ratanya adalah 5 huruf per kata. Distribusi ini menunjukkan seberapa sering kata-kata dalam teks cenderung 
        #                 memiliki panjang tertentu, memberikan wawasan tentang kompleksitas atau kesederhanaan kata yang digunakan dalam teks tersebut.
        #                     ''')
        
        
        # row6 = st.columns(3)
        
        # with row6[0]:
        #     with st.container(height=480, border=True):
        #         plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_shopee, col='content')
        #         st.plotly_chart(plt_freq_meanlength_word_tokped)
        
        
        # with row6[1]:
        #     with st.container(height=480, border=True):
        #         plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_lazada, col='content')
        #         st.plotly_chart(plt_freq_meanlength_word_tokped)
        
        
        # with row6[2]:
        #     with st.container(height=480, border=True):
        #         plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_tokped, col='content')
        #         st.plotly_chart(plt_freq_meanlength_word_tokped)
    
    
    else :
        # Menampilkan gambar di atas dashboard
        def display_image(image_path, use_column_width=True):
            image = Image.open(image_path)
            st.image(image, use_column_width=use_column_width)

        # Tampilan gambar header
        display_image("./assets/gambar/dashboard title.png", use_column_width=True)
        
        # Load dataset
        df_clean_shopee = pd.read_parquet("./assets/dataset/data_preprocess_shopee/df_stopword_shopee.parquet")
        df_clean_lazada = pd.read_parquet("./assets/dataset/data_preprocess_lazada/df_stopword_lazada.parquet")
        df_clean_tokped = pd.read_parquet("./assets/dataset/data_preprocess_tokped/df_stopword_tokped.parquet")

        # Konversi kolom 'at' menjadi datetime
        df_clean_shopee['at'] = pd.to_datetime(df_clean_shopee['at'], errors='coerce')
        df_clean_lazada['at'] = pd.to_datetime(df_clean_lazada['at'], errors='coerce')
        df_clean_tokped['at'] = pd.to_datetime(df_clean_tokped['at'], errors='coerce')
        
        # Menambah kolom untuk tahun
        df_clean_shopee['year'] = df_clean_shopee['at'].dt.year
        df_clean_lazada['year'] = df_clean_lazada['at'].dt.year
        df_clean_tokped['year'] = df_clean_tokped['at'].dt.year
        
        
        df_clean_shopee['marketplace'] = 'Shopee'
        df_clean_lazada['marketplace'] = 'Lazada'
        df_clean_tokped['marketplace'] = 'Tokopedia'

        combined_df = pd.concat([df_clean_shopee[['year', 'marketplace']],
                                df_clean_lazada[['year', 'marketplace']],
                                df_clean_tokped[['year', 'marketplace']]])
        
        
        st.markdown(''' 
                    Berikut ini adalah dashboard sentiment analisis marketplace online dengan fokus aplikasi shopee, lazada dan tokopedia.
                    Dataset yang ditampilkan adalah dataset yang sudah dipreprocessing (lower case, remove emoji, text cleaning, slang tranformation dan 
                    remove stopwords) dapat dilihat pada bagian preprocessing data. Pembaca juga dapat melihat exploratory data analisis pada bagian 
                    exploratory data analisis.
                    Dataset ini terdiri dari beberapa kolom, yaitu : content : berisi review pelanggan pengguna aplikasi yang sudah dipreprocessing, 
                    at : tanggal dan waktu review pelanggan pengguna, year : tahun review pelanggan pengguna.
                    
                                
                                ''')
        
        
        # Misalnya, kita punya df_clean_shopee, df_clean_lazada, df_clean_tokped
        stats_shopee = text_analyzer_project.calculate_text_statistics(df_clean_shopee, 'content')
        stats_lazada = text_analyzer_project.calculate_text_statistics(df_clean_lazada, 'content')
        stats_tokped = text_analyzer_project.calculate_text_statistics(df_clean_tokped, 'content')
        
        
        with st.container(height=185, border=True):
                # Menampilkan hasil untuk setiap marketplace
                # st.write(f"#### Statistik Deskriptif")
            
                cols2 = st.columns([1, 1, 1])

                with cols2[0]:
                    st.write(text_analyzer_project.display_statistics(stats_shopee, "Shopee"), unsafe_allow_html=True)

                with cols2[1]:
                    st.write(text_analyzer_project.display_statistics(stats_lazada, "Lazada"), unsafe_allow_html=True)

                with cols2[2]:
                    st.write(text_analyzer_project.display_statistics(stats_tokped, "Tokopedia"), unsafe_allow_html=True)
        

        # Mengatur kolom untuk menampilkan card secara horizontal
        row_1 = st.columns(2)
        
        with row_1[0]:
            with st.container(height=480, border=True):
                # Membuat plot
                fig = px.histogram(combined_df, 
                                x='year', 
                                color='marketplace', 
                                barmode='group', 
                                labels={'year':'Year', 'marketplace':'Marketplace'},
                                title='Perbandingan Jumlah Ulasan Berdasarkan Tahun')

                # Menyesuaikan tampilan
                fig.update_layout(
                    xaxis_title='Tahun', 
                    yaxis_title='Jumlah Ulasan', 
                    title_x=0.2, 
                    template='plotly_white',
                    plot_bgcolor='white',  # Background plot menjadi putih
                    paper_bgcolor='white',  # Background seluruh area menjadi putih
                    xaxis=dict(
                        title_font=dict(size=14, color='black'),
                        tickfont=dict(size=12, color='black')
                    ),
                    yaxis=dict(
                        title_font=dict(size=14, color='black'),
                        tickfont=dict(size=12, color='black')
                    ),
                    title=dict(
                        font=dict(size=16, color='black')
                    ),
                    legend=dict(
                        title_font=dict(size=12, color='black'),  # Mengubah warna teks judul legend menjadi hitam
                        font=dict(size=12, color='black')       # Mengubah warna teks label legend menjadi hitam
                        # bordercolor='black',                      # Mengatur warna border legend (opsional)
                        # borderwidth=1                            # Mengatur lebar border legend (opsional)
                    )
                )

                # Menampilkan plot di Streamlit
                st.plotly_chart(fig)   
                
        with row_1[1]:
            with st.container(height=480, border=True):
                # Asumsikan df_clean_shopee, df_clean_lazada, df_clean_tokped sudah ada
                n = 2  # Misal kita menggunakan bigram
                most_common = 5  # Mengambil 20 n-gram paling umum

                # Menghitung n-gram untuk setiap dataset
                df_ngram_shopee = text_analyzer_project.combine_top_ngram_df(df_clean_shopee, col='content', n=n, most_common=most_common)
                df_ngram_lazada = text_analyzer_project.combine_top_ngram_df(df_clean_lazada, col='content', n=n, most_common=most_common)
                df_ngram_tokped = text_analyzer_project.combine_top_ngram_df(df_clean_tokped, col='content', n=n, most_common=most_common)

                # Menambahkan kolom marketplace
                df_ngram_shopee['marketplace'] = 'Shopee'
                df_ngram_lazada['marketplace'] = 'Lazada'
                df_ngram_tokped['marketplace'] = 'Tokopedia'

                # Menggabungkan semua DataFrame
                combined_ngram_df = pd.concat([df_ngram_shopee, df_ngram_lazada, df_ngram_tokped])
                
                
                combined_ngram_df = combined_ngram_df.sort_values(by=['ngram', 'frequency'], ascending=[True, False])

                
                # Membuat bar chart
                fig = px.bar(combined_ngram_df, 
                            x='ngram', 
                            y='frequency', 
                            color='marketplace', 
                            labels={'ngram': 'N-gram', 'frequency': 'Frequency'},
                            title='Top 5 N-grams Yang Sering Muncul Diketiga Marketplace')

                # Menyesuaikan tampilan
                fig.update_layout(
                    xaxis_title='N-gram', 
                    yaxis_title='Frequency', 
                    title_x=0.2, 
                    template='plotly_white',
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    xaxis=dict(
                        title_font=dict(size=14, color='black'),
                        tickfont=dict(size=12, color='black'),
                        categoryorder='total descending'  # Mengurutkan sumbu x berdasarkan frekuensi total
                    ),
                    yaxis=dict(
                        title_font=dict(size=14, color='black'),
                        tickfont=dict(size=12, color='black')
                    ),
                    title=dict(
                        font=dict(size=16, color='black')
                    ),
                    legend=dict(
                        title_font=dict(size=12, color='black'),
                        font=dict(size=12, color='black')
                    )
                )

                # Menampilkan plot di Streamlit
                st.plotly_chart(fig)
        
        
        # row0 = st.columns(2)
        
        
        # with row0[0]:
        #     # Asumsikan df_clean_shopee, df_clean_lazada, df_clean_tokped sudah ada
        #     n = 2  # Misal kita menggunakan bigram
        #     most_common = 5  # Mengambil 20 n-gram paling umum

        #     # Menghitung n-gram untuk setiap dataset
        #     df_ngram_shopee = text_analyzer_project.combine_top_ngram_df(df_clean_shopee, col='content', n=n, most_common=most_common)
        #     df_ngram_lazada = text_analyzer_project.combine_top_ngram_df(df_clean_lazada, col='content', n=n, most_common=most_common)
        #     df_ngram_tokped = text_analyzer_project.combine_top_ngram_df(df_clean_tokped, col='content', n=n, most_common=most_common)

        #     # Menambahkan kolom marketplace
        #     df_ngram_shopee['marketplace'] = 'Shopee'
        #     df_ngram_lazada['marketplace'] = 'Lazada'
        #     df_ngram_tokped['marketplace'] = 'Tokopedia'

        #     # Menggabungkan semua DataFrame
        #     combined_ngram_df = pd.concat([df_ngram_shopee, df_ngram_lazada, df_ngram_tokped])
            
            
        #     combined_ngram_df = combined_ngram_df.sort_values(by=['ngram', 'frequency'], ascending=[True, False])

            
        #     with st.container(height=480, border=True):
        #         # Membuat bar chart
        #         fig = px.bar(combined_ngram_df, 
        #                     x='ngram', 
        #                     y='frequency', 
        #                     color='marketplace', 
        #                     labels={'ngram': 'N-gram', 'frequency': 'Frequency'},
        #                     title='Top 5 N-grams Yang Sering Muncul Diketiga Marketplace')

        #         # Menyesuaikan tampilan
        #         fig.update_layout(
        #             xaxis_title='N-gram', 
        #             yaxis_title='Frequency', 
        #             title_x=0.2, 
        #             template='plotly_white',
        #             plot_bgcolor='white',
        #             paper_bgcolor='white',
        #             xaxis=dict(
        #                 title_font=dict(size=14, color='black'),
        #                 tickfont=dict(size=12, color='black'),
        #                 categoryorder='total descending'  # Mengurutkan sumbu x berdasarkan frekuensi total
        #             ),
        #             yaxis=dict(
        #                 title_font=dict(size=14, color='black'),
        #                 tickfont=dict(size=12, color='black')
        #             ),
        #             title=dict(
        #                 font=dict(size=16, color='black')
        #             ),
        #             legend=dict(
        #                 title_font=dict(size=12, color='black'),
        #                 font=dict(size=12, color='black')
        #             )
        #         )

        #         # Menampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row0[1]:
        #     # Asumsikan df_clean_shopee, df_clean_lazada, df_clean_tokped sudah ada
        #     n = 2  # Misal kita menggunakan bigram
        #     most_common = 5  # Mengambil 20 n-gram paling umum

        #     # Menghitung n-gram untuk setiap dataset
        #     df_ngram_shopee = text_analyzer_project.combine_top_ngram_df(df_clean_shopee, col='content', n=n, most_common=most_common)
        #     df_ngram_lazada = text_analyzer_project.combine_top_ngram_df(df_clean_lazada, col='content', n=n, most_common=most_common)
        #     df_ngram_tokped = text_analyzer_project.combine_top_ngram_df(df_clean_tokped, col='content', n=n, most_common=most_common)

        #     # Menambahkan kolom marketplace
        #     df_ngram_shopee['marketplace'] = 'Shopee'
        #     df_ngram_lazada['marketplace'] = 'Lazada'
        #     df_ngram_tokped['marketplace'] = 'Tokopedia'

        #     # Menggabungkan semua DataFrame
        #     combined_ngram_df = pd.concat([df_ngram_shopee, df_ngram_lazada, df_ngram_tokped])
            
            
        #     combined_ngram_df = combined_ngram_df.sort_values(by=['ngram', 'frequency'], ascending=[True, False])

            
        #     combined_ngram_df_sorted = combined_ngram_df.sort_values(by=['marketplace', 'frequency'], ascending=[True, False])
            
        #     # Menggunakan Streamlit container
        #     with st.container(height=480, border=True):
        #         # Membuat bar chart
        #         fig = px.bar(combined_ngram_df_sorted, 
        #                     x='ngram', 
        #                     y='frequency', 
        #                     color='marketplace', 
        #                     facet_col='marketplace',
        #                     labels={'ngram': 'N-gram', 'frequency': 'Frequency'},
        #                     title='Top N-grams Berdasarkan Marketplace')

        #         # Menyesuaikan tampilan
        #         fig.update_layout(
        #             xaxis_title='N-gram', 
        #             yaxis_title='Frequency', 
        #             title_x=0.2, 
        #             template='plotly_white',
        #             plot_bgcolor='white',
        #             paper_bgcolor='white',
        #             xaxis=dict(
        #                 title_font=dict(size=14, color='black'),
        #                 tickfont=dict(size=12, color='black'),
        #                 categoryorder='total descending',  # Mengurutkan sumbu x berdasarkan frekuensi total
        #                 tickmode='array',  # Mode tick untuk memastikan kategori ditampilkan sesuai urutan
        #             ),
        #             yaxis=dict(
        #                 title_font=dict(size=14, color='black'),
        #                 tickfont=dict(size=12, color='black'),
        #                 tickmode='array',  # Mode tick untuk memastikan angka ditampilkan sesuai urutan
        #             ),
        #             title=dict(
        #                 font=dict(size=16, color='black')
        #             ),
        #             legend=dict(
        #                 title_font=dict(size=12, color='black'),
        #                 font=dict(size=12, color='black')
        #             )
        #         )

        #         # Menampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        def display_summary(platform, positive, negative, neutral=None):
            """
            Fungsi untuk menampilkan ringkasan analisis teks dalam bentuk card di Streamlit dengan tampilan lebih ringkas.
            """
            st.markdown(f"""
            <div style="background-color: #ffffff; padding: 10px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0px 3px 6px rgba(0,0,0,0.1);">
                <h4 style="color: #333333; margin-bottom: 8px;">{platform}</h4>
                <h5 style="color: #008000; margin-bottom: 4px;">Sentimen Positif</h5>
                <p style="color: #000000; font-size: 14px; margin-bottom: 8px;">{positive}</p>
                <h5 style="color: #FF0000; margin-bottom: 4px;">Sentimen Negatif</h5>
                <p style="color: #000000; font-size: 14px; margin-bottom: 8px;">{negative}</p>
                {'<h5 style="color: #000080; margin-bottom: 4px;">Sentimen Netral</h5><p style="color: #000000; font-size: 14px; margin-bottom: 8px;">' + neutral + '</p>' if neutral else ''}
            </div>
            """, unsafe_allow_html=True)

        col_nar = st.columns(3)
        
        with col_nar[0]:
            with st.container(height=380, border=True):
                # Layout Streamlit# Shopee
                positive_shopee = "Kata 'Belanja Shopee' sering dikaitkan dengan 'gratis ongkir', pengguna merasa terbantu dalam memenuhi kebutuhan."
                negative_shopee = "Kata 'Barang tidak' sering kali terkait dengan barang yang tidak sesuai pesanan, deskripsi, atau gambar. 'Biaya layanan' dan 'biaya penanganan' juga menimbulkan sentimen negatif, walau tidak sering dibahas."
                display_summary("Shopee", positive_shopee, negative_shopee)
                

        with col_nar[1]:
            with st.container(height=380, border=True):
                # Lazada
                positive_lazada = "Kata 'Belanja Lazada' dikaitkan dengan kemudahan, harga murah, dan pengiriman cepat."
                negative_lazada = "Kata 'Barang tidak' dan 'gratis ongkir' kadang menerima ulasan negatif terkait ketidaksesuaian barang dan batasan minimal belanja untuk voucher."
                display_summary("Lazada", positive_lazada, negative_lazada)
                st.write("")
                st.write("")

        
        with col_nar[2]:
            with st.container(height=380, border=True):
                # Tokopedia
                positive_tokopedia = "Kata 'Terimakasih Tokopedia' sering dikaitkan dengan 'Skill Academy' dan 'sangat membantu', dengan ulasan positif mengenai kemudahan dan manfaat dari pelatihan yang disediakan."
                neutral_tokopedia = "Kata 'Skill Academy' terkait dengan pelatihan prakerja mendapat ulasan netral."
                display_summary("Tokopedia", positive_tokopedia, "", neutral_tokopedia)
        
        

        
        
        
        # Filter berdasarkan tahun
        # years = sorted(df_clean_shopee['year'].dropna().unique())  # Mengambil tahun unik
        # selected_years = st.multiselect('Pilih Tahun Untuk Melihat Tahun Tertentu yang diinginkan (Bisa Multiple Input):', years, key='year_selection_1')

        # if selected_years:
        #     df_clean_shopee = df_clean_shopee[df_clean_shopee['year'].isin(selected_years)]
        #     df_clean_lazada = df_clean_lazada[df_clean_lazada['year'].isin(selected_years)]
        #     df_clean_tokped = df_clean_tokped[df_clean_tokped['year'].isin(selected_years)]
        #     st.write(f"Data untuk tahun {', '.join(map(str, selected_years))}")
        
        # # Layout 3 kolom untuk masing-masing platform
        # row1 = st.columns(3)
        
        # with row1[0]:
        #     st.title("Shopee")
                
        #     with st.container(height=400, border=True):
        #         st.markdown('''
        #                     Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di Shopee adalah "belanja shopee', 
        #                     "gratis ongkir",  "barang tidak", "shopee pay", "perbaikan mohon", "biaya layanan", 
        #                     dan "biaya penanganan".
                            
        #                     - Sentimen Positif: "Belanja Shopee" sering dikaitkan dengan "gratis ongkir", pengguna merasa terbantu dalam memenuhi kebutuhan.
                            
        #                     - Sentimen Negatif: "Barang tidak" sering kali terkait dengan barang yang tidak sesuai pesanan, deskripsi, atau gambar. "Biaya layanan" 
        #                     dan "biaya penanganan" juga menimbulkan sentimen negatif, walau tidak sering dibahas.
        #                     ''')
            
            
            
            # with st.container(height=400, border=True):
            #     st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            #     result_df_top_4gram_shopee = text_analyzer_project.combine_top_ngram(df_clean_shopee, col='content', n=4)
            #     result_df_top_4gram_shopee = pd.DataFrame(result_df_top_4gram_shopee, columns=['N-gram (4 kata)', 'Frekuensi'])
            #     st.dataframe(result_df_top_4gram_shopee, use_container_width=True)
                
                
                
            # with st.container(height=380, border=True):
            #     st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
                
            #     @st.cache_data(persist=True)
            #     def generate_wordcloud_shopee(df):
            #         return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
                
            #     plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_shopee)
            #     st.pyplot(plt_generate_wordcloud_shopee)

        # with row1[1]:
        #     st.title("Lazada")
            
            
        #     with st.container(height=400, border=True):
        #         st.markdown('''
        #                     Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di lazada adalah "belanja lazada", 
        #                     "tidak sesuai",  "barang tidak", "gratis ongkir", "pengiriman cepat".

        #                     Kata "belanja lazada" : identik dengan sentimen positif bagi shopee. Pengguna sangat senang, sangat puas berbelanja dilazada.
        #                     beberapa komentar positif lainnya belanja dilazada tidak ribet, harga murah dan tidak kecewa. Kata "belanja lazada" juga 
        #                     sering dikaitkan dengan kata "gratis ongkir", "barang tidak", dan "pengiriman cepat.
                            
        #                     Kata "belanja lazada" yang dikaitkkan dengan "gratis ongkir" menerima ulasan negatif dari pengguna lazada, yaitu perihal minimal
        #                     belanja dan tidak tersedianya voucher gratis ongkir.
                            
        #                     Kata "belanja lazada" yang dikaitkan dengan "barang tidak" menerima ulasan negatif dari pengguna, yaitu : barang yang diterima 
        #                     pengguna tidak sesuai gambar, tidak sesuai deskripsi dan pesanan.
                            
        #                     Kata "belanja lazada" yang dikaitkan dengan "pengiriman cepat" mendapat ulasan positif dari pengguna dimana kurir yang mengantarkan
        #                     barang ramah. 
                            
        #                     ''')
            
            # with st.container(height=400, border=True):
            #     st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            #     result_df_top_4gram_lazada = text_analyzer_project.combine_top_ngram(df_clean_lazada, col='content', n=4)
            #     result_df_top_4gram_lazada = pd.DataFrame(result_df_top_4gram_lazada, columns=['N-gram (4 kata)', 'Frekuensi'])
            #     st.dataframe(result_df_top_4gram_lazada, use_container_width=True)
                
                
            # with st.container(height=380, border=True):
            #     st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
                
            #     @st.cache_data(persist=True)
            #     def generate_wordcloud_shopee(df):
            #         return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
                
            #     plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_lazada)
            #     st.pyplot(plt_generate_wordcloud_shopee)

        # with row1[2]:
        #     st.title("Tokopedia")
            
        #     with st.container(height=400, border=True):
        #         st.markdown('''
        #                     Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di tokopedia adalah "terimakasih tokopedia", 
        #                     "sangat menbantu",  "skill academy", "pelatihan prakerja".

        #                     Kata "terimakasih tokopedia" mendapatkan ulasan positif dari penggunanya berupa komentar sangat bagus dan mudah dipahami.
        #                     Kata "terimakasih tokopedia" terkait langsung dengan kata "skill academy" dan kata "sangat membantu" yang mendapatkan ulasan positif
        #                     dari para penggunanya. 
                            
        #                     Kata "terimakasih tokopedia" yang berkaitan dengan kata "skill academy" mendapatkan ulasan netral seperti membeli pelatihan 
        #                     by ruang guru, kartu prakerja dan pelatihan prakerja.
                            
        #                     Kata "terimakasih tokopedia" yang berkaitan dengan kata "sangat membantu" mendapatkan ulasan positif seperti sangat membantu 
        #                     mengikuti pelatihan dan menyelesaikan pelatihan. 
        #                     ''')
                
            # with st.container(height=400, border=True):
            #     st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            #     result_df_top_4gram_tokped = text_analyzer_project.combine_top_ngram(df_clean_tokped, col='content', n=4)
            #     result_df_top_4gram_tokped = pd.DataFrame(result_df_top_4gram_tokped, columns=['N-gram (4 kata)', 'Frekuensi'])
            #     st.dataframe(result_df_top_4gram_tokped, use_container_width=True)
                
                
                
            # with st.container(height=380, border=True):
            #     st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
                
            #     @st.cache_data(persist=True)
            #     def generate_wordcloud_shopee(df):
            #         return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
                
            #     plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_tokped)
            #     st.pyplot(plt_generate_wordcloud_shopee)

        # with st.container(height=80, border=True):
        #     st.markdown('''
        #         Most Influential (Paling Berpengaruh):merujuk pada node (simpul) yang memiliki pengaruh terbesar dalam jaringan. 
        #         Node ini mungkin memiliki banyak koneksi (hubungan) dengan node lain atau berada pada posisi strategis yang memungkinkan mereka 
        #         untuk memengaruhi banyak bagian dari jaringan.
        #         ''')

        row2 = st.columns(3)
        
        with row2[0]:
            # Inisiasi ngram
                result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

                # Inisiasi graph
                G = nx.Graph()

                for items, count in result_combine_top_4gram:
                    G.add_edge(items[0], items[1], weight=count)

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
                    
                    
                    
        with row2[1]:
            # Inisiasi ngram
                result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

                # Inisiasi graph
                G = nx.Graph()

                for items, count in result_combine_top_4gram:
                    G.add_edge(items[0], items[1], weight=count)

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
                    
                    
                    
        with row2[2]:
            # Inisiasi ngram
                result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

                # Inisiasi graph
                G = nx.Graph()

                for items, count in result_combine_top_4gram:
                    G.add_edge(items[0], items[1], weight=count)

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
        
        
        
        # with st.container(height=80, border=True):
        #             st.markdown('''
        #                 Most Important Connection (Koneksi Paling Penting): merujuk pada hubungan atau jalur yang paling penting dalam jaringan. 
        #                 Koneksi ini mungkin kritis untuk komunikasi atau aliran informasi dalam jaringan.
        #                 ''')
        
        
        # row3 = st.columns(3)
        
        # with row3[0]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                    
        #             # Most Important Connection
        #             most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                    
        #             # Convert to DataFrame
        #             df_most_important = pd.DataFrame(
        #                 sorted(most_important.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_most_important, use_container_width=True)
                    
                    
                    
        # with row3[1]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                    
        #             # Most Important Connection
        #             most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                    
        #             # Convert to DataFrame
        #             df_most_important = pd.DataFrame(
        #                 sorted(most_important.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_most_important, use_container_width=True)
                    
                    
                    
        # with row3[2]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Most Important Connection (Koneksi Paling Penting) N-gram 4 kata menjadi 2 kata')
                    
        #             # Most Important Connection
        #             most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                    
        #             # Convert to DataFrame
        #             df_most_important = pd.DataFrame(
        #                 sorted(most_important.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Eigenvector Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_most_important, use_container_width=True)
        
        
        # # Hitung Betweenness Centrality untuk ketiga dataset
        # df_best_connector_shopee = text_analyzer_project.compute_betweenness_centrality(df_clean_shopee, col='content', n=4, most_common=5, marketplace_name='Shopee')
        # df_best_connector_lazada = text_analyzer_project.compute_betweenness_centrality(df_clean_lazada, col='content', n=4, most_common=5, marketplace_name='Lazada')
        # df_best_connector_tokped = text_analyzer_project.compute_betweenness_centrality(df_clean_tokped, col='content', n=4, most_common=5, marketplace_name='Tokopedia')

        # # Gabungkan data dari ketiga marketplace
        # combined_df_best_connector = pd.concat([df_best_connector_shopee, df_best_connector_lazada, df_best_connector_tokped])

        # # Plot bar chart
        # with st.container(height=480, border=True):
        #     fig = px.bar(combined_df_best_connector,
        #                 x='N-gram', 
        #                 y='Betweenness Centrality', 
        #                 color='Marketplace', 
        #                 title='Best Connector N-gram 4 Kata Menjadi 2 Kata (Comparative)',
        #                 barmode='group',
        #                 labels={'N-gram': 'N-gram 4 Kata', 'Betweenness Centrality': 'Betweenness Centrality'},
        #                 height=400)
            
        #     # Mengatur tampilan chart
        #     fig.update_layout(
        #         xaxis_title='N-gram 4 Kata', 
        #         yaxis_title='Betweenness Centrality',
        #         title_x=0.5,
        #         template='plotly_white',
        #         plot_bgcolor='white',
        #         paper_bgcolor='white',
        #         xaxis=dict(
        #             title_font=dict(size=14, color='black'),
        #             tickfont=dict(size=12, color='black'),
        #             categoryorder='total descending'
        #         ),
        #         yaxis=dict(
        #             title_font=dict(size=14, color='black'),
        #             tickfont=dict(size=12, color='black')
        #         ),
        #         title=dict(
        #             font=dict(size=16, color='black')
        #         ),
        #         legend=dict(
        #             title_font=dict(size=12, color='black'),
        #             font=dict(size=12, color='black')
        #         )
        #     )
            
        #     # Menampilkan plot di Streamlit
        #     st.plotly_chart(fig)
        
        
        
        # with st.container(height=80, border=True):
        #             st.markdown('''
        #                 Best Connector (Penghubung Terbaik): merujuk pada node yang berfungsi sebagai penghubung utama dalam jaringan, menghubungkan 
        #                 berbagai bagian jaringan yang mungkin tidak terhubung langsung tanpa kehadiran node tersebut.
        #                 ''')
        
        
        # row4 = st.columns(3)
        
        # with row4[0]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                    
        #             # Best Connector
        #             best_connector = nx.betweenness_centrality(G)
                    
        #             # Convert to DataFrame
        #             df_best_connector = pd.DataFrame(
        #                 sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_best_connector, use_container_width=True)
                    
                    
                    
        # with row4[1]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                    
        #             # Best Connector
        #             best_connector = nx.betweenness_centrality(G)
                    
        #             # Convert to DataFrame
        #             df_best_connector = pd.DataFrame(
        #                 sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_best_connector, use_container_width=True)
                    
                    
                    
        # with row4[2]:
        #     # Inisiasi ngram
        #         result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

        #         # Inisiasi graph
        #         G = nx.Graph()

        #         for items, count in result_combine_top_4gram:
        #             G.add_edge(items[0], items[1], weight=count)

        #         with st.container(height=350, border=True):
        #             st.write('Best Connector (Penghubung Terbaik) N-gram 4 kata menjadi 2 kata')
                    
        #             # Best Connector
        #             best_connector = nx.betweenness_centrality(G)
                    
        #             # Convert to DataFrame
        #             df_best_connector = pd.DataFrame(
        #                 sorted(best_connector.items(), key=lambda x: x[1], reverse=True),
        #                 columns=['N-gram 4 kata menjadi 2 kata', 'Betweenness Centrality']
        #             )
                    
        #             # Display DataFrame
        #             st.dataframe(df_best_connector, use_container_width=True)
        
        
        with st.container(height=300, border=True):
                    st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
                    st.markdown('''
                                **Noted :**
                                
                                **"Most Common"** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                                most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                                
                                **"Center Node atau Node Pusat"** adalah titik fokus atau simpul utama dalam sebuah graf yang menjadi pusat perhatian atau 
                                referensi dalam analisis.                                                                  
                                **"Pilih parameter center node berdasarkan kata yang ada di Most influencial**"" (Center node yang diinput default)
                                
                                **"Depth atau Kedalaman"** dalam konteks graf menunjukkan seberapa jauh Anda ingin mengeksplorasi 
                                dari node pusat. Ini mengacu pada jumlah lapisan atau tingkat kedekatan yang ingin Anda pertimbangkan dalam analisis.
                                ''')
        
        
        row5 = st.columns(3)
        
        with row5[0]:
            with st.container(height=800, border=True):
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df, most_common, center_node, depth):
                        result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

                        G = nx.Graph()
                        for items, count in result_combine_top_4gram:
                            G.add_edge(items[0], items[1], weight=count)

                        def get_subgraph(G, center_node, depth):
                            nodes = set([center_node])
                            for _ in range(depth):
                                neighbors = set()
                                for node in nodes:
                                    neighbors.update(G.neighbors(node))
                                nodes.update(neighbors)
                            return G.subgraph(nodes)

                        if center_node in G.nodes():
                            subgraph = get_subgraph(G, center_node, depth)
                            pos = nx.spring_layout(subgraph, k=0.5)

                            degree_centrality = nx.degree_centrality(subgraph)
                            node_size = [v * 1000 for v in degree_centrality.values()]
                            node_color = [v for v in degree_centrality.values()]

                            fig, ax = plt.subplots(figsize=(20, 30))
                            nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                            nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                            nx.draw_networkx_labels(subgraph, pos, font_size=25, ax=ax)

                            plt.title('Network Analysis of Review', fontsize=25)
                            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                            cbar.set_label('Degree Centrality')

                            return fig
                        else:
                            st.info('''
                            **"Pilih parameter center node berdasarkan kata yang ada di Most influencial**"" (Center node yang diinput default)
                            ''')
                            return None

                col_mostcommon11, col_mostcommon21, col_mostcommon31 = st.columns(3)

                with col_mostcommon11:
                    most_common_input2 = st.number_input('Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_1')

                with col_mostcommon21:
                    center_node = st.text_input("Center Node:", value='belanja shopee', key='center_node_input_1')

                with col_mostcommon31:
                    depth = st.number_input('Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_2')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_shopee, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
        
        
        with row5[1]:
            with st.container(height=800, border=True):
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df, most_common, center_node, depth):
                        result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

                        G = nx.Graph()
                        for items, count in result_combine_top_4gram:
                            G.add_edge(items[0], items[1], weight=count)

                        def get_subgraph(G, center_node, depth):
                            nodes = set([center_node])
                            for _ in range(depth):
                                neighbors = set()
                                for node in nodes:
                                    neighbors.update(G.neighbors(node))
                                nodes.update(neighbors)
                            return G.subgraph(nodes)

                        if center_node in G.nodes():
                            subgraph = get_subgraph(G, center_node, depth)
                            pos = nx.spring_layout(subgraph, k=0.5)

                            degree_centrality = nx.degree_centrality(subgraph)
                            node_size = [v * 1000 for v in degree_centrality.values()]
                            node_color = [v for v in degree_centrality.values()]

                            fig, ax = plt.subplots(figsize=(20, 30))
                            nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                            nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                            nx.draw_networkx_labels(subgraph, pos, font_size=25, ax=ax)

                            plt.title('Network Analysis of Review', fontsize=25)
                            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                            cbar.set_label('Degree Centrality')

                            return fig
                        else:
                            st.info('''
                            **"Pilih parameter center node berdasarkan kata yang ada di Most influencial, Most importance 
                                connection dan Best connector**"" (Center node yang diinput default)
                            ''')
                            return None

                col_mostcommon11, col_mostcommon21, col_mostcommon31 = st.columns(3)

                with col_mostcommon11:
                    most_common_input2 = st.number_input('Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_3')

                with col_mostcommon21:
                    center_node = st.text_input("Center Node:", value='belanja lazada', key='center_node_input_2')

                with col_mostcommon31:
                    depth = st.number_input('Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_4')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_lazada, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
        
        
        with row5[2]:
            with st.container(height=800, border=True):
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df, most_common, center_node, depth):
                        result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

                        G = nx.Graph()
                        for items, count in result_combine_top_4gram:
                            G.add_edge(items[0], items[1], weight=count)

                        def get_subgraph(G, center_node, depth):
                            nodes = set([center_node])
                            for _ in range(depth):
                                neighbors = set()
                                for node in nodes:
                                    neighbors.update(G.neighbors(node))
                                nodes.update(neighbors)
                            return G.subgraph(nodes)

                        if center_node in G.nodes():
                            subgraph = get_subgraph(G, center_node, depth)
                            pos = nx.spring_layout(subgraph, k=0.5)

                            degree_centrality = nx.degree_centrality(subgraph)
                            node_size = [v * 1000 for v in degree_centrality.values()]
                            node_color = [v for v in degree_centrality.values()]

                            fig, ax = plt.subplots(figsize=(20, 30))
                            nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                            nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                            nx.draw_networkx_labels(subgraph, pos, font_size=25, ax=ax)

                            plt.title('Network Analysis of Review', fontsize=25)
                            cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                            cbar.set_label('Degree Centrality')

                            return fig
                        else:
                            st.info('''
                            **"Pilih parameter center node berdasarkan kata yang ada di Most influencial, Most importance 
                                connection dan Best connector**"" (Center node yang diinput default)
                            ''')
                            return None

                col_mostcommon11, col_mostcommon21, col_mostcommon31 = st.columns(3)

                with col_mostcommon11:
                    most_common_input2 = st.number_input('Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_5')

                with col_mostcommon21:
                    center_node = st.text_input("Center Node:", value='terimakasih tokopedia', key='center_node_input_3')

                with col_mostcommon31:
                    depth = st.number_input('Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_6')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_tokped, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
        
        
        # with st.container(height=80, border=True):
        #     st.markdown('''
        #                 Distribusi frekuensi jumlah huruf adalah penghitungan seberapa sering sebuah teks memiliki jumlah huruf tertentu. 
        #                 Misalnya, jika Anda memiliki kumpulan teks, distribusi ini akan menunjukkan seberapa banyak teks yang memiliki, 
        #                 misalnya, 5 huruf, 10 huruf, dan seterusnya. Distribusi ini memberikan gambaran tentang seberapa panjang atau pendek karakteristik 
        #                 teks dalam hal jumlah huruf.
        #                     ''')
        
        
        # row6 = st.columns(3)
        
        # with row6[0]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_shopee, 'content', bins=100)
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row6[1]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_lazada, 'content', bins=100)
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row6[2]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_tokped, 'content', bins=100)
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with st.container(height=100, border=True):
        #     st.markdown('''
        #                 Distribusi frekuensi jumlah kata per teks adalah penghitungan seberapa sering jumlah kata tertentu muncul dalam sebuah teks. 
        #                 Sebagai contoh, jika Anda menganalisis sekumpulan ulasan produk, distribusi ini akan menunjukkan berapa banyak ulasan yang terdiri 
        #                 dari, misalnya, 5 kata, 10 kata, dan seterusnya. Hal ini membantu memahami apakah teks cenderung terdiri dari sedikit kata (pendek) 
        #                 atau banyak kata (panjang).
        #                     ''')
        
        
        # row6 = st.columns(3)
        
        # with row6[0]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.freq_of_words_plotly(df_clean_shopee, 'content')
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row6[1]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.freq_of_words_plotly(df_clean_lazada, 'content')
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with row6[2]:
        #     with st.container(height=480, border=True):
        #         # Panggil fungsi untuk menghasilkan plot
        #         fig = text_analyzer_project.freq_of_words_plotly(df_clean_tokped, 'content')
                
        #         # Tampilkan plot di Streamlit
        #         st.plotly_chart(fig)
        
        
        # with st.container(height=100, border=True):
        #     st.markdown('''
        #                 Distribusi frekuensi panjang kata rata-rata adalah penghitungan yang menunjukkan seberapa sering kata-kata dalam teks memiliki 
        #                 panjang tertentu jika dihitung rata-rata. Misalnya, jika sebuah teks terdiri dari 10 kata dengan jumlah total huruf sebanyak 50, 
        #                 maka panjang kata rata-ratanya adalah 5 huruf per kata. Distribusi ini menunjukkan seberapa sering kata-kata dalam teks cenderung 
        #                 memiliki panjang tertentu, memberikan wawasan tentang kompleksitas atau kesederhanaan kata yang digunakan dalam teks tersebut.
        #                     ''')
        
        
        # row6 = st.columns(3)
        
        # with row6[0]:
        #     with st.container(height=480, border=True):
        #         plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_shopee, col='content')
        #         st.plotly_chart(plt_freq_meanlength_word_tokped)
        
        
        # with row6[1]:
        #     with st.container(height=480, border=True):
        #         plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_lazada, col='content')
        #         st.plotly_chart(plt_freq_meanlength_word_tokped)
        
        
        # with row6[2]:
        #     with st.container(height=480, border=True):
        #         plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_tokped, col='content')
        #         st.plotly_chart(plt_freq_meanlength_word_tokped)
    
    
    