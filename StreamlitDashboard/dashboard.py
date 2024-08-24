# Import library
import streamlit as st
from PIL import Image
import pandas as pd
from TextPreProcessing import text_analyzer_project
import os
import networkx as nx
import matplotlib.pyplot as plt

def dashboard():
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
    
    
    
    

    st.markdown(''' 
                Berikut ini adalah dashboard sentiment analisis marketplace online dengan fokus aplikasi shopee, lazada dan tokopedia.
                Dataset yang ditampilkan adalah dataset yang sudah dipreprocessing (lower case, remove emoji, text cleaning, slang tranformation dan 
                remove stopwords). Untuk penjelasan lebih lanjut tentang preprocessing data dapat dilihat pada bagian analysis. Pembaca juga dapat 
                melihat exploratory data analisis pada bagian exploratory data analisi.
                Dataset ini terdiri dari beberapa kolom, yaitu : content : berisi review pelanggan pengguna aplikasi yang sudah dipreprocessing, 
                at : tanggal dan waktu review pelanggan pengguna, year : tahun review pelanggan pengguna.
                
                            
                            ''')
    
    
    # Filter berdasarkan tahun
    years = sorted(df_clean_shopee['year'].dropna().unique())  # Mengambil tahun unik
    selected_years = st.multiselect('Pilih Tahun Untuk Melihat Tahun Tertentu yang diinginkan (Bisa Multiple Input):', years, key='year_selection_1')

    if selected_years:
        df_clean_shopee = df_clean_shopee[df_clean_shopee['year'].isin(selected_years)]
        df_clean_lazada = df_clean_lazada[df_clean_lazada['year'].isin(selected_years)]
        df_clean_tokped = df_clean_tokped[df_clean_tokped['year'].isin(selected_years)]
        st.write(f"Data untuk tahun {', '.join(map(str, selected_years))}")
    
    # Layout 3 kolom untuk masing-masing platform
    row1 = st.columns(3)
    
    with row1[0]:
        st.title("Shopee")
            
        with st.container(height=400, border=True):
            st.markdown('''
                        Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di Shopee adalah "belanja shopee', 
                        "gratis ongkir",  "barang tidak", "shopee pay", "perbaikan mohon", "biaya layanan", 
                        dan "biaya penanganan".

                        Kata "belanja shopee" identik dengan sentimen positif bagi shopee. Pengguna sangat senang, sangat terbantu oleh shopee dalam
                        memenuhi kebutuhannya. Kata "belanja shopee" juga sering dikaitkan dengan kata "gratis ongkir". Ada beberapa sentimen negatif 
                        yang diberikan pengguna yaitu adanya minimal belanja dan sering juga voucher gratis ongkir tidak digunakan oleh pengguna.
                        
                        
                        Kata "barang tidak" identik dengan sentimen negatif terhadap aplikasi shopee. Diantaranya : barang tidak sesuai pesanan, 
                        tidak sesuai deskripsi dan tidak sesuai gambar.

                        Kata "shopee pay" tidak terlalu banyak diulas oleh pengguna aplikasi shopee. Namun memiliki komentar positif dari pengguna 
                        aplikasi
                        
                        Kata "biaya layanan" dan "biaya penanganan" tidak banyak dibahas, namun muncul dalam ulasan pengguna shopee yang mengindikasikan
                        sentimen negatif terhadap aplikasi shopee.
                        
                        ''')
        
        
        
        with st.container(height=400, border=True):
            st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            result_df_top_4gram_shopee = text_analyzer_project.combine_top_ngram(df_clean_shopee, col='content', n=4)
            result_df_top_4gram_shopee = pd.DataFrame(result_df_top_4gram_shopee, columns=['N-gram (4 kata)', 'Frekuensi'])
            st.dataframe(result_df_top_4gram_shopee, use_container_width=True)
            
            
            
        with st.container(height=380, border=True):
            st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
            
            @st.cache_data(persist=True)
            def generate_wordcloud_shopee(df):
                return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
            
            plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_shopee)
            st.pyplot(plt_generate_wordcloud_shopee)

    with row1[1]:
        st.title("Lazada")
        
        
        with st.container(height=400, border=True):
            st.markdown('''
                        Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di lazada adalah "belanja lazada", 
                        "tidak sesuai",  "barang tidak", "gratis ongkir", "pengiriman cepat".

                        Kata "belanja lazada" : identik dengan sentimen positif bagi shopee. Pengguna sangat senang, sangat puas berbelanja dilazada.
                        beberapa komentar positif lainnya belanja dilazada tidak ribet, harga murah dan tidak kecewa. Kata "belanja lazada" juga 
                        sering dikaitkan dengan kata "gratis ongkir", "barang tidak", dan "pengiriman cepat.
                        
                        Kata "belanja lazada" yang dikaitkkan dengan "gratis ongkir" menerima ulasan negatif dari pengguna lazada, yaitu perihal minimal
                        belanja dan tidak tersedianya voucher gratis ongkir.
                        
                        Kata "belanja lazada" yang dikaitkan dengan "barang tidak" menerima ulasan negatif dari pengguna, yaitu : barang yang diterima 
                        pengguna tidak sesuai gambar, tidak sesuai deskripsi dan pesanan.
                        
                        Kata "belanja lazada" yang dikaitkan dengan "pengiriman cepat" mendapat ulasan positif dari pengguna dimana kurir yang mengantarkan
                        barang ramah. 
                        
                        ''')
           
        with st.container(height=400, border=True):
            st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            result_df_top_4gram_lazada = text_analyzer_project.combine_top_ngram(df_clean_lazada, col='content', n=4)
            result_df_top_4gram_lazada = pd.DataFrame(result_df_top_4gram_lazada, columns=['N-gram (4 kata)', 'Frekuensi'])
            st.dataframe(result_df_top_4gram_lazada, use_container_width=True)
            
            
        with st.container(height=380, border=True):
            st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
            
            @st.cache_data(persist=True)
            def generate_wordcloud_shopee(df):
                return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
            
            plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_lazada)
            st.pyplot(plt_generate_wordcloud_shopee)

    with row1[2]:
        st.title("Tokopedia")
        
        with st.container(height=400, border=True):
            st.markdown('''
                        Berdasarkan analisis teks dari ulasan pengguna, beberapa aspek utama yang sering dibicarakan di tokopedia adalah "terimakasih tokopedia", 
                        "sangat menbantu",  "skill academy", "pelatihan prakerja".

                        Kata "terimakasih tokopedia" mendapatkan ulasan positif dari penggunanya berupa komentar sangat bagus dan mudah dipahami.
                        Kata "terimakasih tokopedia" terkait langsung dengan kata "skill academy" dan kata "sangat membantu" yang mendapatkan ulasan positif
                        dari para penggunanya. 
                        
                        Kata "terimakasih tokopedia" yang berkaitan dengan kata "skill academy" mendapatkan ulasan netral seperti membeli pelatihan 
                        by ruang guru, kartu prakerja dan pelatihan prakerja.
                        
                        Kata "terimakasih tokopedia" yang berkaitan dengan kata "sangat membantu" mendapatkan ulasan positif seperti sangat membantu 
                        mengikuti pelatihan dan menyelesaikan pelatihan. 
                        ''')
            
        with st.container(height=400, border=True):
            st.write('N-gram 4 kata yang sering muncul dikelompokkan menjadi 2 kata')
            result_df_top_4gram_tokped = text_analyzer_project.combine_top_ngram(df_clean_tokped, col='content', n=4)
            result_df_top_4gram_tokped = pd.DataFrame(result_df_top_4gram_tokped, columns=['N-gram (4 kata)', 'Frekuensi'])
            st.dataframe(result_df_top_4gram_tokped, use_container_width=True)
            
            
            
        with st.container(height=380, border=True):
            st.write('Wordcloud N-gram (4 kata jadi 2 kata)')
            
            @st.cache_data(persist=True)
            def generate_wordcloud_shopee(df):
                return text_analyzer_project.generate_wordcloud_dataframe(df, col='content', max_font_size=60, relative_scaling=0.1)
            
            plt_generate_wordcloud_shopee = generate_wordcloud_shopee(df_clean_tokped)
            st.pyplot(plt_generate_wordcloud_shopee)

    with st.container(height=80, border=True):
        st.markdown('''
            Most Influential (Paling Berpengaruh):merujuk pada node (simpul) yang memiliki pengaruh terbesar dalam jaringan. 
            Node ini mungkin memiliki banyak koneksi (hubungan) dengan node lain atau berada pada posisi strategis yang memungkinkan mereka 
            untuk memengaruhi banyak bagian dari jaringan.
            ''')

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
    
    
    
    with st.container(height=80, border=True):
                st.markdown('''
                    Most Important Connection (Koneksi Paling Penting): merujuk pada hubungan atau jalur yang paling penting dalam jaringan. 
                    Koneksi ini mungkin kritis untuk komunikasi atau aliran informasi dalam jaringan.
                    ''')
    
    
    row3 = st.columns(3)
    
    with row3[0]:
        # Inisiasi ngram
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

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
                
                
                
    with row3[1]:
        # Inisiasi ngram
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

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
                
                
                
    with row3[2]:
        # Inisiasi ngram
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

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
    
    
    
    
    with st.container(height=80, border=True):
                st.markdown('''
                    Best Connector (Penghubung Terbaik): merujuk pada node yang berfungsi sebagai penghubung utama dalam jaringan, menghubungkan 
                    berbagai bagian jaringan yang mungkin tidak terhubung langsung tanpa kehadiran node tersebut.
                    ''')
    
    
    row4 = st.columns(3)
    
    with row4[0]:
        # Inisiasi ngram
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_shopee, col='content', n=4, most_common=50)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

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
                
                
                
    with row4[1]:
        # Inisiasi ngram
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_lazada, col='content', n=4, most_common=50)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

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
                
                
                
    with row4[2]:
        # Inisiasi ngram
            result_combine_top_4gram = text_analyzer_project.combine_top_ngram_most_common(df_clean_tokped, col='content', n=4, most_common=50)

            # Inisiasi graph
            G = nx.Graph()

            for items, count in result_combine_top_4gram:
                G.add_edge(items[0], items[1], weight=count)

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
    
    
    with st.container(height=300, border=True):
                st.write('Network Analisis Seluruh Data N-gram 4 kata menjadi 2 kata')
                st.markdown('''
                            **Noted :**
                            
                            **"Most Common"** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                            most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                            
                            **"Center Node atau Node Pusat"** adalah titik fokus atau simpul utama dalam sebuah graf yang menjadi pusat perhatian atau 
                            referensi dalam analisis.
                            Pilih parameter center node berdasarkan kata yang ada di Most influencial, Most importance 
                            connection dan Best connector**"" (Center node yang diinput default)
                             
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
                        **"Pilih parameter center node berdasarkan kata yang ada di Most influencial, Most importance 
                            connection dan Best connector**"" (Center node yang diinput default)
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
    
    
    with st.container(height=80, border=True):
        st.markdown('''
                    Distribusi frekuensi jumlah huruf adalah penghitungan seberapa sering sebuah teks memiliki jumlah huruf tertentu. 
                    Misalnya, jika Anda memiliki kumpulan teks, distribusi ini akan menunjukkan seberapa banyak teks yang memiliki, 
                    misalnya, 5 huruf, 10 huruf, dan seterusnya. Distribusi ini memberikan gambaran tentang seberapa panjang atau pendek karakteristik 
                    teks dalam hal jumlah huruf.
                        ''')
    
    
    row6 = st.columns(3)
    
    with row6[0]:
        with st.container(height=480, border=True):
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_shopee, 'content', bins=100)
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
    
    
    with row6[1]:
        with st.container(height=480, border=True):
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_lazada, 'content', bins=100)
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
    
    
    with row6[2]:
        with st.container(height=480, border=True):
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_tokped, 'content', bins=100)
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
    
    
    with st.container(height=100, border=True):
        st.markdown('''
                    Distribusi frekuensi jumlah kata per teks adalah penghitungan seberapa sering jumlah kata tertentu muncul dalam sebuah teks. 
                    Sebagai contoh, jika Anda menganalisis sekumpulan ulasan produk, distribusi ini akan menunjukkan berapa banyak ulasan yang terdiri 
                    dari, misalnya, 5 kata, 10 kata, dan seterusnya. Hal ini membantu memahami apakah teks cenderung terdiri dari sedikit kata (pendek) 
                    atau banyak kata (panjang).
                        ''')
    
    
    row6 = st.columns(3)
    
    with row6[0]:
        with st.container(height=480, border=True):
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.freq_of_words_plotly(df_clean_shopee, 'content')
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
    
    
    with row6[1]:
        with st.container(height=480, border=True):
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.freq_of_words_plotly(df_clean_lazada, 'content')
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
    
    
    with row6[2]:
        with st.container(height=480, border=True):
            # Panggil fungsi untuk menghasilkan plot
            fig = text_analyzer_project.freq_of_words_plotly(df_clean_tokped, 'content')
            
            # Tampilkan plot di Streamlit
            st.plotly_chart(fig)
    
    
    with st.container(height=100, border=True):
        st.markdown('''
                    Distribusi frekuensi panjang kata rata-rata adalah penghitungan yang menunjukkan seberapa sering kata-kata dalam teks memiliki 
                    panjang tertentu jika dihitung rata-rata. Misalnya, jika sebuah teks terdiri dari 10 kata dengan jumlah total huruf sebanyak 50, 
                    maka panjang kata rata-ratanya adalah 5 huruf per kata. Distribusi ini menunjukkan seberapa sering kata-kata dalam teks cenderung 
                    memiliki panjang tertentu, memberikan wawasan tentang kompleksitas atau kesederhanaan kata yang digunakan dalam teks tersebut.
                        ''')
    
    
    row6 = st.columns(3)
    
    with row6[0]:
        with st.container(height=480, border=True):
            plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_shopee, col='content')
            st.plotly_chart(plt_freq_meanlength_word_tokped)
    
    
    with row6[1]:
        with st.container(height=480, border=True):
            plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_lazada, col='content')
            st.plotly_chart(plt_freq_meanlength_word_tokped)
    
    
    with row6[2]:
        with st.container(height=480, border=True):
            plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_tokped, col='content')
            st.plotly_chart(plt_freq_meanlength_word_tokped)
    
    
    
    