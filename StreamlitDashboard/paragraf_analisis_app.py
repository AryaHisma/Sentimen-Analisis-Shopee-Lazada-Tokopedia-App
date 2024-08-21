# Import library
import streamlit as st
from PIL import Image

import os
import shutil
import pandas as pd


from TextPreProcessing.text_processing_project import TextProcessing
from TextPreProcessing import text_analyzer_project

import networkx as nx
import matplotlib.pyplot as plt




def aplikasi():
    st.title('Paragraf Analisis App')
    
    st.markdown(''' 
                Berikut ini adalah aplikasi untuk paragraf analisis                           
                ''')

    # Load input text
    long_text = st.text_area("Masukkan teks Anda di sini:", height=200)

    # Tombol untuk memproses teks
    st.write("Untuk melihat proses analisis klik tombol 'Proses Teks'")
    if st.button("Proses Teks"):
        if long_text.strip() == "":
            st.warning("Silakan masukkan teks untuk diproses.")
        else:
                      
            # Text preprocessing
            tp = TextProcessing()

            def text_preprocessing(text):
                # Terapkan setiap langkah preprocessing pada teks
                text = tp.remove_unicode_styles(text)
                text = tp.lowercase(text)
                text = tp.remove_emoji(text)
                text = tp.text_cleaning(text)
                text = tp.slang_transform(text)
                text = tp.remove_stopwords(text)
    
                return text
            
            cleaned_text = text_preprocessing(long_text)
            
            # Container for text preprocessing results
            with st.container(height=350, border=True):
                col_text_preprocessing1, col_text_preprocessing2 = st.columns([5, 1])
                
                with col_text_preprocessing1:
                    st.write("Hasil Teks Setelah Diproses:")
                    processed_text = cleaned_text
            
                    st.markdown(
                        f"""
                        <div style="border: 2px solid #4CAF50; padding: 10px; border-radius: 5px;">
                            {processed_text}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                with col_text_preprocessing2:
                    st.write('Most Frequent Word')
                    most_frequent_words_text = text_analyzer_project.most_frequent_words_text(cleaned_text, n=1000000000)
                    st.dataframe(most_frequent_words_text, use_container_width=True, hide_index=True)

            # Container for n-grams and wordcloud
            with st.container(height=500, border=True):
                col_ngram1, col_ngram2 = st.columns([1, 3])
                
                with col_ngram1:
                    st.write('N-gram (2 kata) --> Mengambil 2 kata per unit yang sering muncul')
                    # Memanggil fungsi untuk mendapatkan n-gram
                    result_df_top_2gram = text_analyzer_project.generate_ngrams_text(cleaned_text, n=2, most_common=10000000000000000)
                    # Tampilkan DataFrame di Streamlit
                    st.dataframe(result_df_top_2gram, use_container_width=True)

                with col_ngram2:
                    st.write('Wordcloud')
                    
                    generate_wordcloud_text = text_analyzer_project.generate_wordcloud_text_app(cleaned_text)
                    
                    st.pyplot(generate_wordcloud_text)
            
            
            # Container for Most Influential, Most Important Connection, Best Connector
            with st.container(height=500, border=True):   
                col_mosttext1, col_mosttext2, col_mosttext3 = st.columns(3)
                
                with col_mosttext1:
                    with st.container(height=180, border=True):
                        st.markdown('''
                            Most Influential (Paling Berpengaruh):merujuk pada node (simpul) yang memiliki pengaruh terbesar dalam jaringan. 
                            Node ini mungkin memiliki banyak koneksi (hubungan) dengan node lain atau berada pada posisi strategis yang memungkinkan mereka 
                            untuk memengaruhi banyak bagian dari jaringan.
                            ''')
                        
                with col_mosttext2:
                    with st.container(height=180, border=True):
                        st.markdown('''
                            Most Important Connection (Koneksi Paling Penting): merujuk pada hubungan atau jalur yang paling penting dalam jaringan. 
                            Koneksi ini mungkin kritis untuk komunikasi atau aliran informasi dalam jaringan.
                            ''')
                        
                with col_mosttext3:
                    with st.container(height=180, border=True):
                        st.markdown('''
                            Best Connector (Penghubung Terbaik): merujuk pada node yang berfungsi sebagai penghubung utama dalam jaringan, menghubungkan 
                            berbagai bagian jaringan yang mungkin tidak terhubung langsung tanpa kehadiran node tersebut.
                            ''')

                
                col_mostgraf1, col_mostgraf2, col_mostgraf3 = st.columns(3)
                
                
                def analyze_ngrams_and_network(cleaned_text, n=2):
                    # Inisiasi n-gram
                    top_2gram = text_analyzer_project.top_ngram_text_most(cleaned_text, n)

                    # Inisiasi graph
                    G = nx.Graph()

                    for items, count in top_2gram:
                        G.add_edge(items[0], items[1], weight=count)

                    # Analyze Network Properties
                    most_influential = nx.degree_centrality(G)
                    most_important = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06)
                    best_connector = nx.betweenness_centrality(G)

                    return most_influential, most_important, best_connector
                    # return top_2gram
                
                def display_centrality_results(title, centrality_dict):
                    df_centrality = pd.DataFrame(
                        sorted(centrality_dict.items(), key=lambda x: x[1], reverse=True),
                        columns=['N-gram 2 kata', 'Centrality Score']
                    )
                    st.write(title)
                    st.dataframe(df_centrality, use_container_width=True)
                    
                # Panggil fungsi analyze_ngrams_and_network dan simpan hasilnya ke dalam variabel
                most_influential, most_important, best_connector = analyze_ngrams_and_network(cleaned_text, n=2)


                col_mostgraf1, col_mostgraf2, col_mostgraf3 = st.columns(3)

                with col_mostgraf1:
                    with st.container():
                        display_centrality_results('Most Influential (Paling Berpengaruh) N-gram 2 kata', most_influential)

                with col_mostgraf2:
                    with st.container():
                        display_centrality_results('Most Important Connection (Koneksi Paling Penting) N-gram 2 kata', most_important)

                with col_mostgraf3:
                    with st.container():
                        display_centrality_results('Best Connector (Penghubung Terbaik) N-gram 2 kata', best_connector)

    # Text preprocessing
    tp = TextProcessing()

    def text_preprocessing(text):
        # Terapkan setiap langkah preprocessing pada teks
        text = tp.remove_unicode_styles(text)
        text = tp.lowercase(text)
        text = tp.remove_emoji(text)
        text = tp.text_cleaning(text)
        text = tp.slang_transform(text)
        text = tp.remove_stopwords(text)

        return text
    
    cleaned_text = text_preprocessing(long_text)        
            
    # Container for network analysis
    with st.container(height=1000, border=True):    
        col_network1, col_network2 = st.columns(2)

        with col_network1:
            with st.container(height=950, border=True):
                st.write('Network Analysis of All Data N-gram 2 Words')
                st.markdown('''
                            **Note:** 
                    
                    **Most Common** adalah parameter yang dapat diubah ubah untuk menampilkan jumlah item yang paling sering muncul sejumlah 
                    most common dari hasil analisis n-gram. (Semakin besar most common semakin lama loading data)
                            ''')

                # Cached function for network analysis
                # @st.cache_data
                def Network_Analysis_All_Data_N_gram(cleaned_text, most_common):
                    # Get top n-grams
                    top_2gram = text_analyzer_project.top_ngram_text(cleaned_text, n=2)

                    # Initialize graph
                    G = nx.Graph()

                    for items, count in top_2gram.itertuples(index=False):
                        G.add_edge(items[0], items[1], weight=count)

                    # Layout
                    pos = nx.spring_layout(G, k=0.9)

                    # Degree centrality
                    degree_centrality = nx.degree_centrality(G)
                    node_size = [v * 1000 for v in degree_centrality.values()]
                    node_color = [v for v in degree_centrality.values()]

                    # Plot
                    fig, ax = plt.subplots(figsize=(16, 14.7))
                    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, ax=ax)
                    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)

                    # Add title and colorbar
                    plt.title('Network Analysis of Paragraf', fontsize=16)
                    cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                    cbar.set_label('Degree Centrality')

                    return fig
                
                col_mostcommon1, col_mostcommon2 = st.columns(2)
                
                with col_mostcommon1:
                    # Input for most_common parameter in Streamlit
                    most_common_input = st.number_input('Input Most Common', min_value=2, max_value=100, value=20, step=1, key='most_common_input_1')
                    
                with col_mostcommon2:
                    pass

                # Call the function with the provided most_common parameter
                fig = Network_Analysis_All_Data_N_gram(cleaned_text, most_common=most_common_input)

                # Display plot in Streamlit
                st.pyplot(fig)

        with col_network2:
            with st.container(height=950, border=True):
                st.write('Network Analysis of All Data N-gram 2 Words with Center Node')
                st.markdown('''
                            **Note:**
                            
                            **"Center Node atau Node Pusat"** adalah titik fokus atau simpul utama dalam sebuah graf yang menjadi pusat perhatian atau 
                            referensi dalam analisis. 
                            
                            **"Depth atau Kedalaman"** dalam konteks graf menunjukkan seberapa jauh Anda ingin mengeksplorasi 
                            dari node pusat. Ini mengacu pada jumlah lapisan atau tingkat kedekatan yang ingin Anda pertimbangkan dalam analisis.
                            ''')
                
                st.info('''**"Pilih parameter center node berdasarkan kata yang ada di Most influencial, Most importance 
                            connection dan Best connectorDepth**"" (Center node dikosongkan, silahkan input center node)''')

                # Cached function for network analysis with center node and depth
                # @st.cache_data
                def Network_Analysis_With_Center_Node(cleaned_text, most_common, center_node, depth):
                    # Get top n-grams
                    top_2gram = text_analyzer_project.top_ngram_text(cleaned_text, n=2)

                    # Initialize graph
                    G = nx.Graph()
                    
                    for items, count in top_2gram.itertuples(index=False):
                        G.add_edge(items[0], items[1], weight=count)

                    # Function to get subgraph based on center node and depth
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

                        fig, ax = plt.subplots(figsize=(16, 10))
                        nx.draw_networkx_nodes(subgraph, pos, node_size=node_size, node_color=node_color, cmap=plt.cm.Blues, alpha=0.7, ax=ax)
                        nx.draw_networkx_edges(subgraph, pos, width=1.0, alpha=0.5, ax=ax)
                        nx.draw_networkx_labels(subgraph, pos, font_size=10, ax=ax)

                        plt.title('Network Analysis of Review with Center Node', fontsize=16)
                        cbar = plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), ax=ax)
                        cbar.set_label('Degree Centrality')

                        return fig
                    else:
                        st.error(f"Node '{center_node}' not found in the graph.")
                        return None

                col_mostcommon11, col_mostcommon21, col_mostcommon31 = st.columns(3)

                with col_mostcommon11:
                    most_common_input2 = st.number_input('Input Most Common', min_value=2, max_value=100, value=20, step=1, key='most_common_input_3')

                with col_mostcommon21:
                    center_node = st.text_input("Enter center node parameter:", value='Contoh: Node_A', key='center_node_input_1')


                with col_mostcommon31:
                    depth = st.number_input('Input Depth', min_value=1, max_value=10, value=2, step=1, key='most_common_input_4')

                # Call the function and display the plot
                fig = Network_Analysis_With_Center_Node(cleaned_text, most_common=most_common_input2, center_node=center_node, depth=depth)
                
                if fig:
                    st.pyplot(fig)
                
    
            
    # with st.container(height=850, border=True):
    #     col_distribusi1, col_distribusi2, col_distribusi3 = st.columns(3)
        
    #     with col_distribusi1[0]:
    #         with st.container(height=480, border=True):
    #             # Panggil fungsi untuk menghasilkan plot
    #             fig = text_analyzer_project.plot_letter_frequency_distribution(df_clean_tokped, 'content', bins=100)
                
    #             # Tampilkan plot di Streamlit
    #             st.plotly_chart(fig)


    #     with col_distribusi2[1]:
    #         with st.container(height=480, border=True):
    #             # Panggil fungsi untuk menghasilkan plot
    #             fig = text_analyzer_project.freq_of_words_plotly(df_clean_tokped, 'content')
                
    #             # Tampilkan plot di Streamlit
    #             st.plotly_chart(fig)
                
                
    #     with col_distribusi3[2]:
    #         with st.container(height=480, border=True):
    #             plt_freq_meanlength_word_tokped = text_analyzer_project.freq_meanlength_word(df_clean_tokped, col='content')
    #             st.plotly_chart(plt_freq_meanlength_word_tokped)
                
    
    
    
    
    
    
    
    
    
    
    