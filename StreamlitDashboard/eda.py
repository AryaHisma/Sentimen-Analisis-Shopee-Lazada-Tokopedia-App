# Import library
import streamlit as st
from PIL import Image

import os
import shutil
import pandas as pd


from TextPreProcessing import text_analyzer_project

import networkx as nx
import matplotlib.pyplot as plt



def eda():
    with st.container(height=310):
        @st.cache_data(persist=True)
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

        display_image("./assets/gambar/EDA.png", use_column_width=True, channels="RGB")
    
    # Load dataset
    col_shopee, col_lazada, col_tokped = st.columns(3)
    
    # Load data
    df_clean_shopee = pd.read_parquet("./assets/dataset/data_preprocess_shopee/df_stopword_shopee.parquet")
    df_clean_lazada = pd.read_parquet("./assets/dataset/data_preprocess_lazada/df_stopword_lazada.parquet")
    df_clean_tokped = pd.read_parquet("./assets/dataset/data_preprocess_tokped/df_stopword_tokped.parquet")

    
    # Konversi kolom 'at' menjadi datetime
    df_clean_shopee['at'] = pd.to_datetime(df_clean_shopee['at'], errors='coerce')
    df_clean_lazada['at'] = pd.to_datetime(df_clean_lazada['at'], errors='coerce')
    df_clean_tokped['at'] = pd.to_datetime(df_clean_tokped['at'], errors='coerce')
    
    # Menambah kolom untuk tahun, bulan, dan tanggal
    df_clean_shopee['year'] = df_clean_shopee['at'].dt.year

    df_clean_lazada['year'] = df_clean_lazada['at'].dt.year

    df_clean_tokped['year'] = df_clean_tokped['at'].dt.year

    # Mengganti NaN dengan None
    df_clean_shopee = df_clean_shopee.where(pd.notnull(df_clean_shopee), None)
    df_clean_lazada = df_clean_lazada.where(pd.notnull(df_clean_lazada), None)
    df_clean_tokped = df_clean_tokped.where(pd.notnull(df_clean_tokped), None)

    # Konversi kolom datetime ke string
    # df_clean_shopee['at'] = df_clean_shopee['at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # df_clean_lazada['at'] = df_clean_lazada['at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # df_clean_tokped['at'] = df_clean_tokped['at'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # Subset kolom di dataset
    df_clean_shopee = df_clean_shopee[['content', 'at', 'year']]
    df_clean_lazada = df_clean_lazada[['content', 'at', 'year']]
    df_clean_tokped = df_clean_tokped[['content', 'at', 'year']]
    
    
    
    # Tab dataset
    tab_shopee, tab_lazada, tab_tokopedia = st.tabs(["Shopee", "Lazada", "Tokopedia"])

    with tab_shopee:
        # Pastikan kolom yang berisi tahun ada dalam DataFrame
        if 'year' in df_clean_shopee.columns:
            # Menampilkan filter tahun
            years = df_clean_shopee['year'].unique()  # Ambil tahun unik dari kolom
            selected_years = st.multiselect('Pilih Tahun:', sorted(years), key='year_selection_1')

            # Menampilkan data yang difilter berdasarkan tahun yang dipilih
            if selected_years:
                filtered_df = df_clean_shopee[df_clean_shopee['year'].isin(selected_years)]
                st.write(f"Data untuk tahun {', '.join(map(str, selected_years))}")
                # Subset kolom di dataset
                df_clean_shopee = filtered_df[['content', 'at', 'year']]
            else:
                st.write("Pilih tahun untuk memfilter data berdasarkan tahun")
        else:
            st.error("Kolom 'year' tidak ditemukan dalam DataFrame.")
            
        
        
        # Create rows with 3 columns each
        row1 = st.columns([4, 1])
        row2 = st.columns(3)
        row3 = st.columns(3)
        row4 = st.columns(3)
        row5 = st.columns(2)
        row6 = st.columns(3)
        row7 = st.columns(3)

        # Adding unique content with borders to each column
        with row1[0]:
            with st.container(height=450, border=True):
                st.write('Dataset')
                st.dataframe(df_clean_shopee, use_container_width=True, hide_index=True)

        with row1[1]:
            with st.container(height=450, border=True):
                st.write('Kata kata yang sering muncul')
                n_unique_words_shopee = len(df_clean_shopee['content'].str.split(expand=True).stack().unique())
                most_frequent_words__stopword_shopee = text_analyzer_project.most_frequent_words(df_clean_shopee, col='content', n=n_unique_words_shopee)
                st.dataframe(most_frequent_words__stopword_shopee, use_container_width=True, hide_index=True)
                
        
        # Tampilkan DataFrame dengan pengaturan tampilan khusus
        st.write(" ")
        
        # Ganti nilai None atau NaN dengan string kosong
        df_clean_shopee['content'] = df_clean_shopee['content'].fillna('')

        
        with row2[0]:
            with st.container(height=400, border=True):
                st.write('N-gram (4 kata) --> Mengambil 4 kata per unit yang sering muncul')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_4gram = text_analyzer_project.top_ngram(df_clean_shopee, col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_4gram = pd.DataFrame(result_df_top_4gram, columns=['N-gram (4 kata)', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_4gram)

        with row2[1]:
            with st.container(height=400, border=True):
                st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_2gram = text_analyzer_project.combine_top_ngram(df_clean_shopee, col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_2gram_df = pd.DataFrame(result_df_top_2gram, columns=['N-gram 4 kata menjadi 2 kata', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_2gram_df)
        
        with row2[2]:
            with st.container(height=400, border=True):
                st.write('Wordcloud N-gram (4 kata)')
                
                @st.cache_data(persist=True)
                def generate_wordcloud_shopee(df):
                    return text_analyzer_project.generate_wordcloud(df, col='content')
                
                plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_shopee)
                
                st.pyplot(plt_generate_wordcloud_shopee)
                
        
        st.write(" ")
        
        with row3[0]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Most Influential (Paling Berpengaruh):merujuk pada node (simpul) yang memiliki pengaruh terbesar dalam jaringan. 
                    Node ini mungkin memiliki banyak koneksi (hubungan) dengan node lain atau berada pada posisi strategis yang memungkinkan mereka 
                    untuk memengaruhi banyak bagian dari jaringan.
                    ''')
                
        with row3[1]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Most Important Connection (Koneksi Paling Penting): merujuk pada hubungan atau jalur yang paling penting dalam jaringan. 
                    Koneksi ini mungkin kritis untuk komunikasi atau aliran informasi dalam jaringan.
                    ''')
                
        with row3[2]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Best Connector (Penghubung Terbaik): merujuk pada node yang berfungsi sebagai penghubung utama dalam jaringan, menghubungkan 
                    berbagai bagian jaringan yang mungkin tidak terhubung langsung tanpa kehadiran node tersebut.
                    ''')
        
        st.write(" ")
        
        # Inisiasi ngram
        result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

        # Inisiasi graph
        G = nx.Graph()

        for items, count in result_combine_top_4gram:
            G.add_edge(items[0], items[1], weight=count)

        with row4[0]:
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

        with row4[1]:
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
                
        with row4[2]:
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

        st.write(" ")
        
        with row5[0]:
            with st.container(height=850, border=True):
                st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
                st.markdown('''
                            Noted : 
                            **"Most Common"** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                            most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                            ''')
                
                # @st.cache_data(persist=True)
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata (df, most_common):
                    # Tampilkan DataFrame dengan pengaturan tampilan khusus
                    result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

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
                    fig, ax = plt.subplots(figsize=(16, 13))
                    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, ax=ax)
                    nx.draw_networkx_labels(G, pos, font_size=14, ax=ax)

                    # Tambahkan judul dan colorbar
                    plt.title('Network Analysis of Review', fontsize=16)
                    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                    cbar.set_label('Degree Centrality')

                    return fig
                
                
                col_mostcommon1, col_mostcommon2 = st.columns(2)
                
                with col_mostcommon1:
                    # Buat input untuk parameter most_common di Streamlit
                    most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_1')
                    
                with col_mostcommon2:
                    pass
                    # # Buat input untuk parameter most_common di Streamlit
                    # most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=10, step=10, key='most_common_input_2')

                # Panggil fungsi dengan parameter most_common yang diberikan
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata(df_clean_shopee, most_common=most_common_input)

                # Tampilkan plot di Streamlit
                st.pyplot(fig)

        with row5[1]:
            with st.container(height=850, border=True):
                st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata dengan parameter')
                st.markdown('''
                            **"Center Node atau Node Pusat"** adalah titik fokus atau simpul utama dalam sebuah graf yang menjadi pusat perhatian atau 
                            referensi dalam analisis. 
                            
                            
                            
                            **"Depth atau Kedalaman"** dalam konteks graf menunjukkan seberapa jauh Anda ingin mengeksplorasi 
                            dari node pusat. Ini mengacu pada jumlah lapisan atau tingkat kedekatan yang ingin Anda pertimbangkan dalam analisis.
                            ''')
                
                
                
                
                # @st.cache_data(persist=True)
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

                        fig, ax = plt.subplots(figsize=(15, 10.7))
                        nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                        nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                        nx.draw_networkx_labels(subgraph, pos, font_size=14, ax=ax)

                        plt.title('Network Analysis of Review', fontsize=16)
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
                    most_common_input2 = st.number_input('Input Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_3')

                with col_mostcommon21:
                    center_node = st.text_input("Masukkan parameter center node:", value='belanja shopee', key='center_node_input_1')

                with col_mostcommon31:
                    depth = st.number_input('Input Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_4')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_shopee, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
                    
                    
        st.write(" ")
        
        with row6[0]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi jumlah huruf adalah penghitungan seberapa sering sebuah teks memiliki jumlah huruf tertentu. 
                    Misalnya, jika Anda memiliki kumpulan teks, distribusi ini akan menunjukkan seberapa banyak teks yang memiliki, 
                    misalnya, 5 huruf, 10 huruf, dan seterusnya. Distribusi ini memberikan gambaran tentang seberapa panjang atau pendek karakteristik 
                    teks dalam hal jumlah huruf.
                    ''')
                
        with row6[1]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi jumlah kata per teks adalah penghitungan seberapa sering jumlah kata tertentu muncul dalam sebuah teks. 
                    Sebagai contoh, jika Anda menganalisis sekumpulan ulasan produk, distribusi ini akan menunjukkan berapa banyak ulasan yang terdiri 
                    dari, misalnya, 5 kata, 10 kata, dan seterusnya. Hal ini membantu memahami apakah teks cenderung terdiri dari sedikit kata (pendek) 
                    atau banyak kata (panjang).
                    ''')
                
        with row6[2]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi panjang kata rata-rata adalah penghitungan yang menunjukkan seberapa sering kata-kata dalam teks memiliki 
                    panjang tertentu jika dihitung rata-rata. Misalnya, jika sebuah teks terdiri dari 10 kata dengan jumlah total huruf sebanyak 50, 
                    maka panjang kata rata-ratanya adalah 5 huruf per kata. Distribusi ini menunjukkan seberapa sering kata-kata dalam teks cenderung 
                    memiliki panjang tertentu, memberikan wawasan tentang kompleksitas atau kesederhanaan kata yang digunakan dalam teks tersebut.
                    ''')
                    
                      
        st.write(" ")
        
        with row7[0]:
            with st.container(height=480, border=True):
                # Panggil fungsi untuk menghasilkan plot
                fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_shopee, 'content', bins=100)
                
                # Tampilkan plot di Streamlit
                st.plotly_chart(fig)
    

        with row7[1]:
            with st.container(height=480, border=True):
                # Panggil fungsi untuk menghasilkan plot
                fig = text_analyzer_project.freq_of_words_plotly(df_clean_shopee, 'content')
                
                # Tampilkan plot di Streamlit
                st.plotly_chart(fig)
                
                
        with row7[2]:
            with st.container(height=480, border=True):
                plt_freq_meanlength_word_shopee = text_analyzer_project.freq_meanlength_word(df_clean_shopee, col='content')
                st.plotly_chart(plt_freq_meanlength_word_shopee)
                
    with tab_lazada:
        # Pastikan kolom yang berisi tahun ada dalam DataFrame
        if 'year' in df_clean_lazada.columns:
            # Menampilkan filter tahun
            years = df_clean_lazada['year'].unique()  # Ambil tahun unik dari kolom
            selected_years = st.multiselect('Pilih Tahun:', sorted(years), key='year_selection_2')

            # Menampilkan data yang difilter berdasarkan tahun yang dipilih
            if selected_years:
                filtered_df = df_clean_lazada[df_clean_lazada['year'].isin(selected_years)]
                st.write(f"Data untuk tahun {', '.join(map(str, selected_years))}")
                # Subset kolom di dataset
                df_clean_lazada = filtered_df[['content', 'at', 'year']]
            else:
                st.write("Pilih tahun untuk memfilter data berdasarkan tahun")
        else:
            st.error("Kolom 'year' tidak ditemukan dalam DataFrame.")
            
        
        
        # Create rows with 3 columns each
        row1 = st.columns([4, 1])
        row2 = st.columns(3)
        row3 = st.columns(3)
        row4 = st.columns(3)
        row5 = st.columns(2)
        row6 = st.columns(3)
        row7 = st.columns(3)

        # Adding unique content with borders to each column
        with row1[0]:
            with st.container(height=450, border=True):
                st.write('Dataset')
                st.dataframe(df_clean_lazada, use_container_width=True, hide_index=True)

        with row1[1]:
            with st.container(height=450, border=True):
                st.write('Kata kata yang sering muncul')
                n_unique_words_lazada = len(df_clean_lazada['content'].str.split(expand=True).stack().unique())
                most_frequent_words__stopword_lazada = text_analyzer_project.most_frequent_words(df_clean_lazada, col='content', n=n_unique_words_lazada)
                st.dataframe(most_frequent_words__stopword_lazada, use_container_width=True, hide_index=True)
                
        
        # Tampilkan DataFrame dengan pengaturan tampilan khusus
        st.write(" ")
        
        # Ganti nilai None atau NaN dengan string kosong
        df_clean_lazada['content'] = df_clean_lazada['content'].fillna('')

        
        with row2[0]:
            with st.container(height=400, border=True):
                st.write('N-gram (4 kata) --> Mengambil 4 kata per unit yang sering muncul')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_4gram = text_analyzer_project.top_ngram(df_clean_lazada, col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_4gram = pd.DataFrame(result_df_top_4gram, columns=['N-gram (4 kata)', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_4gram)

        with row2[1]:
            with st.container(height=400, border=True):
                st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_2gram = text_analyzer_project.combine_top_ngram(df_clean_lazada, col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_2gram_df = pd.DataFrame(result_df_top_2gram, columns=['N-gram 4 kata menjadi 2 kata', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_2gram_df)
        
        with row2[2]:
            with st.container(height=400, border=True):
                st.write('Wordcloud N-gram (4 kata)')
                
                @st.cache_data(persist=True)
                def generate_wordcloud_lazada(df):
                    return text_analyzer_project.generate_wordcloud(df, col='content')
                
                plt_generate_wordcloud_lazada = generate_wordcloud_lazada(df_clean_lazada)
                
                st.pyplot(plt_generate_wordcloud_lazada)
                
        
        st.write(" ")
        
        with row3[0]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Most Influential (Paling Berpengaruh):merujuk pada node (simpul) yang memiliki pengaruh terbesar dalam jaringan. 
                    Node ini mungkin memiliki banyak koneksi (hubungan) dengan node lain atau berada pada posisi strategis yang memungkinkan mereka 
                    untuk memengaruhi banyak bagian dari jaringan.
                    ''')
                
        with row3[1]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Most Important Connection (Koneksi Paling Penting): merujuk pada hubungan atau jalur yang paling penting dalam jaringan. 
                    Koneksi ini mungkin kritis untuk komunikasi atau aliran informasi dalam jaringan.
                    ''')
                
        with row3[2]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Best Connector (Penghubung Terbaik): merujuk pada node yang berfungsi sebagai penghubung utama dalam jaringan, menghubungkan 
                    berbagai bagian jaringan yang mungkin tidak terhubung langsung tanpa kehadiran node tersebut.
                    ''')
        
        st.write(" ")
        
        # Inisiasi ngram
        result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

        # Inisiasi graph
        G = nx.Graph()

        for items, count in result_combine_top_4gram:
            G.add_edge(items[0], items[1], weight=count)

        with row4[0]:
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

        with row4[1]:
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
                
        with row4[2]:
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

        st.write(" ")
        
        with row5[0]:
            with st.container(height=850, border=True):
                st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
                st.markdown('''
                            Noted : 
                            **"Most Common"** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                            most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                            ''')
                
                # @st.cache_data(persist=True)
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata (df, most_common):
                    # Tampilkan DataFrame dengan pengaturan tampilan khusus
                    result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

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
                    nx.draw_networkx_labels(G, pos, font_size=14, ax=ax)

                    # Tambahkan judul dan colorbar
                    plt.title('Network Analysis of Review', fontsize=16)
                    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                    cbar.set_label('Degree Centrality')

                    return fig
                
                
                col_mostcommon1, col_mostcommon2 = st.columns(2)
                
                with col_mostcommon1:
                    # Buat input untuk parameter most_common di Streamlit
                    most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_5')
                    
                with col_mostcommon2:
                    pass
                    # # Buat input untuk parameter most_common di Streamlit
                    # most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=10, step=10, key='most_common_input_6')

                # Panggil fungsi dengan parameter most_common yang diberikan
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata(df_clean_lazada, most_common=most_common_input)

                # Tampilkan plot di Streamlit
                st.pyplot(fig)

        with row5[1]:
            with st.container(height=850, border=True):
                st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata dengan parameter')
                st.markdown('''
                            **"Center Node atau Node Pusat"** adalah titik fokus atau simpul utama dalam sebuah graf yang menjadi pusat perhatian atau 
                            referensi dalam analisis. 
                            
                            
                            
                            **"Depth atau Kedalaman"** dalam konteks graf menunjukkan seberapa jauh Anda ingin mengeksplorasi 
                            dari node pusat. Ini mengacu pada jumlah lapisan atau tingkat kedekatan yang ingin Anda pertimbangkan dalam analisis.
                            ''')
                
                
                
                
                # @st.cache_data(persist=True)
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

                        fig, ax = plt.subplots(figsize=(15, 10.7))
                        nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                        nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                        nx.draw_networkx_labels(subgraph, pos, font_size=14, ax=ax)

                        plt.title('Network Analysis of Review', fontsize=16)
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
                    most_common_input2 = st.number_input('Input Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_7')

                with col_mostcommon21:
                    center_node = st.text_input("Masukkan parameter center node:", value='belanja lazada', key='center_node_input_2')

                with col_mostcommon31:
                    depth = st.number_input('Input Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_8')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_lazada, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
                    
                    
        st.write(" ")
        
        with row6[0]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi jumlah huruf adalah penghitungan seberapa sering sebuah teks memiliki jumlah huruf tertentu. 
                    Misalnya, jika Anda memiliki kumpulan teks, distribusi ini akan menunjukkan seberapa banyak teks yang memiliki, 
                    misalnya, 5 huruf, 10 huruf, dan seterusnya. Distribusi ini memberikan gambaran tentang seberapa panjang atau pendek karakteristik 
                    teks dalam hal jumlah huruf.
                    ''')
                
        with row6[1]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi jumlah kata per teks adalah penghitungan seberapa sering jumlah kata tertentu muncul dalam sebuah teks. 
                    Sebagai contoh, jika Anda menganalisis sekumpulan ulasan produk, distribusi ini akan menunjukkan berapa banyak ulasan yang terdiri 
                    dari, misalnya, 5 kata, 10 kata, dan seterusnya. Hal ini membantu memahami apakah teks cenderung terdiri dari sedikit kata (pendek) 
                    atau banyak kata (panjang).
                    ''')
                
        with row6[2]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi panjang kata rata-rata adalah penghitungan yang menunjukkan seberapa sering kata-kata dalam teks memiliki 
                    panjang tertentu jika dihitung rata-rata. Misalnya, jika sebuah teks terdiri dari 10 kata dengan jumlah total huruf sebanyak 50, 
                    maka panjang kata rata-ratanya adalah 5 huruf per kata. Distribusi ini menunjukkan seberapa sering kata-kata dalam teks cenderung 
                    memiliki panjang tertentu, memberikan wawasan tentang kompleksitas atau kesederhanaan kata yang digunakan dalam teks tersebut.
                    ''')
            
                      
        st.write(" ")
        
        with row7[0]:
            with st.container(height=480, border=True):
                # Panggil fungsi untuk menghasilkan plot
                fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_lazada, 'content', bins=100)
                
                # Tampilkan plot di Streamlit
                st.plotly_chart(fig)
    

        with row7[1]:
            with st.container(height=480, border=True):
                # Panggil fungsi untuk menghasilkan plot
                fig = text_analyzer_project.freq_of_words_plotly(df_clean_lazada, 'content')
                
                # Tampilkan plot di Streamlit
                st.plotly_chart(fig)
                
                
        with row7[2]:
            with st.container(height=480, border=True):
                plt_freq_meanlength_word_lazada = text_analyzer_project.freq_meanlength_word(df_clean_lazada, col='content')
                st.plotly_chart(plt_freq_meanlength_word_lazada)
            
    
    with tab_tokopedia:
        # Pastikan kolom yang berisi tahun ada dalam DataFrame
        if 'year' in df_clean_tokped.columns:
            # Menampilkan filter tahun
            years = df_clean_tokped['year'].unique()  # Ambil tahun unik dari kolom
            selected_years = st.multiselect('Pilih Tahun:', sorted(years), key='year_selection_3')

            # Menampilkan data yang difilter berdasarkan tahun yang dipilih
            if selected_years:
                filtered_df = df_clean_tokped[df_clean_tokped['year'].isin(selected_years)]
                st.write(f"Data untuk tahun {', '.join(map(str, selected_years))}")
                # Subset kolom di dataset
                df_clean_tokped = filtered_df[['content', 'at', 'year']]
            else:
                st.write("Pilih tahun untuk memfilter data berdasarkan tahun")
        else:
            st.error("Kolom 'year' tidak ditemukan dalam DataFrame.")
            
        
        
        # Create rows with 3 columns each
        row1 = st.columns([4, 1])
        row2 = st.columns(3)
        row3 = st.columns(3)
        row4 = st.columns(3)
        row5 = st.columns(2)
        row6 = st.columns(3)
        row7 = st.columns(3)

        # Adding unique content with borders to each column
        with row1[0]:
            with st.container(height=450, border=True):
                st.write('Dataset')
                st.dataframe(df_clean_tokped, use_container_width=True, hide_index=True)

        with row1[1]:
            with st.container(height=450, border=True):
                st.write('Kata kata yang sering muncul')
                n_unique_words_tokped = len(df_clean_tokped['content'].str.split(expand=True).stack().unique())
                most_frequent_words__stopword_tokped = text_analyzer_project.most_frequent_words(df_clean_tokped, col='content', n=n_unique_words_tokped)
                st.dataframe(most_frequent_words__stopword_tokped, use_container_width=True, hide_index=True)
                
        
        # Tampilkan DataFrame dengan pengaturan tampilan khusus
        st.write(" ")
        
        # Ganti nilai None atau NaN dengan string kosong
        df_clean_tokped['content'] = df_clean_tokped['content'].fillna('')

        
        with row2[0]:
            with st.container(height=400, border=True):
                st.write('N-gram (4 kata) --> Mengambil 4 kata per unit yang sering muncul')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_4gram = text_analyzer_project.top_ngram(df_clean_tokped, col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_4gram = pd.DataFrame(result_df_top_4gram, columns=['N-gram (4 kata)', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_4gram)

        with row2[1]:
            with st.container(height=400, border=True):
                st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
                # Memanggil fungsi untuk mendapatkan n-gram
                result_df_top_2gram = text_analyzer_project.combine_top_ngram(df_clean_tokped, col='content', n=4)
                # Konversi list of tuples menjadi DataFrame
                result_df_top_2gram_df = pd.DataFrame(result_df_top_2gram, columns=['N-gram 4 kata menjadi 2 kata', 'Frekuensi'])
                # Tampilkan DataFrame di Streamlit
                st.dataframe(result_df_top_2gram_df)
        
        with row2[2]:
            with st.container(height=400, border=True):
                st.write('Wordcloud N-gram (4 kata)')
                
                @st.cache_data(persist=True)
                def generate_wordcloud_tokped(df):
                    return text_analyzer_project.generate_wordcloud(df, col='content')
                
                plt_generate_wordcloud_tokped = generate_wordcloud_tokped(df_clean_tokped)
                
                st.pyplot(plt_generate_wordcloud_tokped)
                
        
        st.write(" ")
        
        with row3[0]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Most Influential (Paling Berpengaruh):merujuk pada node (simpul) yang memiliki pengaruh terbesar dalam jaringan. 
                    Node ini mungkin memiliki banyak koneksi (hubungan) dengan node lain atau berada pada posisi strategis yang memungkinkan mereka 
                    untuk memengaruhi banyak bagian dari jaringan.
                    ''')
                
        with row3[1]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Most Important Connection (Koneksi Paling Penting): merujuk pada hubungan atau jalur yang paling penting dalam jaringan. 
                    Koneksi ini mungkin kritis untuk komunikasi atau aliran informasi dalam jaringan.
                    ''')
                
        with row3[2]:
            with st.container(height=180, border=True):
                st.markdown('''
                    Best Connector (Penghubung Terbaik): merujuk pada node yang berfungsi sebagai penghubung utama dalam jaringan, menghubungkan 
                    berbagai bagian jaringan yang mungkin tidak terhubung langsung tanpa kehadiran node tersebut.
                    ''')
        
        st.write(" ")
        
        # Inisiasi ngram
        result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

        # Inisiasi graph
        G = nx.Graph()

        for items, count in result_combine_top_4gram:
            G.add_edge(items[0], items[1], weight=count)

        with row4[0]:
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

        with row4[1]:
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
                
        with row4[2]:
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

        st.write(" ")
        
        with row5[0]:
            with st.container(height=850, border=True):
                st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
                st.markdown('''
                            Noted : 
                            **"Most Common"** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                            most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                            ''')
                
                # @st.cache_data(persist=True)
                def Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata (df, most_common):
                    # Tampilkan DataFrame dengan pengaturan tampilan khusus
                    result_combine_top_4gram = text_analyzer_project.combine_top_ngram(df, col='content', n=4, most_common=most_common)

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
                    nx.draw_networkx_labels(G, pos, font_size=14, ax=ax)

                    # Tambahkan judul dan colorbar
                    plt.title('Network Analysis of Review', fontsize=16)
                    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                    cbar.set_label('Degree Centrality')

                    return fig
                
                
                col_mostcommon1, col_mostcommon2 = st.columns(2)
                
                with col_mostcommon1:
                    # Buat input untuk parameter most_common di Streamlit
                    most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_9')
                    
                with col_mostcommon2:
                    pass
                    # # Buat input untuk parameter most_common di Streamlit
                    # most_common_input = st.number_input('Imput Most Common', min_value=10, max_value=100, value=10, step=10, key='most_common_input_10')

                # Panggil fungsi dengan parameter most_common yang diberikan
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata(df_clean_tokped, most_common=most_common_input)

                # Tampilkan plot di Streamlit
                st.pyplot(fig)

        with row5[1]:
            with st.container(height=850, border=True):
                st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata dengan parameter')
                st.markdown('''
                            **"Center Node atau Node Pusat"** adalah titik fokus atau simpul utama dalam sebuah graf yang menjadi pusat perhatian atau 
                            referensi dalam analisis. 
                            
                            
                            **"Depth atau Kedalaman"** dalam konteks graf menunjukkan seberapa jauh Anda ingin mengeksplorasi 
                            dari node pusat. Ini mengacu pada jumlah lapisan atau tingkat kedekatan yang ingin Anda pertimbangkan dalam analisis.
                            ''')
                
                
                
                
                # @st.cache_data(persist=True)
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

                        fig, ax = plt.subplots(figsize=(15, 10.7))
                        nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                        nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                        nx.draw_networkx_labels(subgraph, pos, font_size=14, ax=ax)

                        plt.title('Network Analysis of Review', fontsize=16)
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
                    most_common_input2 = st.number_input('Input Most Common', min_value=10, max_value=100, value=50, step=1, key='most_common_input_11')

                with col_mostcommon21:
                    center_node = st.text_input("Masukkan parameter center node:", value='skill academy', key='center_node_input_3')

                with col_mostcommon31:
                    depth = st.number_input('Input Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_12')

                # Panggil fungsi dan tampilkan plot
                fig = Network_Analisis_Seluruh_Data_N_gram_4_kata_menjadi_2_kata_dengan_parameter(df_clean_tokped, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
                    
                    
        st.write(" ")
        
        with row6[0]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi jumlah huruf adalah penghitungan seberapa sering sebuah teks memiliki jumlah huruf tertentu. 
                    Misalnya, jika Anda memiliki kumpulan teks, distribusi ini akan menunjukkan seberapa banyak teks yang memiliki, 
                    misalnya, 5 huruf, 10 huruf, dan seterusnya. Distribusi ini memberikan gambaran tentang seberapa panjang atau pendek karakteristik 
                    teks dalam hal jumlah huruf.
                    ''')
                
        with row6[1]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi jumlah kata per teks adalah penghitungan seberapa sering jumlah kata tertentu muncul dalam sebuah teks. 
                    Sebagai contoh, jika Anda menganalisis sekumpulan ulasan produk, distribusi ini akan menunjukkan berapa banyak ulasan yang terdiri 
                    dari, misalnya, 5 kata, 10 kata, dan seterusnya. Hal ini membantu memahami apakah teks cenderung terdiri dari sedikit kata (pendek) 
                    atau banyak kata (panjang).
                    ''')
                
        with row6[2]:
            with st.container(height=250, border=True):
                st.markdown('''
                    Distribusi frekuensi panjang kata rata-rata adalah penghitungan yang menunjukkan seberapa sering kata-kata dalam teks memiliki 
                    panjang tertentu jika dihitung rata-rata. Misalnya, jika sebuah teks terdiri dari 10 kata dengan jumlah total huruf sebanyak 50, 
                    maka panjang kata rata-ratanya adalah 5 huruf per kata. Distribusi ini menunjukkan seberapa sering kata-kata dalam teks cenderung 
                    memiliki panjang tertentu, memberikan wawasan tentang kompleksitas atau kesederhanaan kata yang digunakan dalam teks tersebut.
                    ''')
                    
                      
        st.write(" ")
        
        with row7[0]:
            with st.container(height=480, border=True):
                # Panggil fungsi untuk menghasilkan plot
                fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_tokped, 'content', bins=100)
                
                # Tampilkan plot di Streamlit
                st.plotly_chart(fig)
    

        with row7[1]:
            with st.container(height=480, border=True):
                # Panggil fungsi untuk menghasilkan plot
                fig = text_analyzer_project.freq_of_words_plotly(df_clean_tokped, 'content')
                
                # Tampilkan plot di Streamlit
                st.plotly_chart(fig)
                
                
        with row7[2]:
            with st.container(height=480, border=True):
                plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_tokped, col='content')
                st.plotly_chart(plt_freq_meanlength_word_tokped)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    