# Import library
import streamlit as st
from PIL import Image

def about():
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
        with st.container(height=440, border=False):
            col_profil1, col_profil2 = st.columns([1, 4])
            
            with col_profil1:
                # --- IMAGE ---
                image = Image.open("assets/gambar/Untitled copy.png")
                
                # Menggunakan st.image untuk menampilkan gambar dengan ukuran yang diperbesar
                st.image(image, width=260)  # Sesuaikan lebar gambar sesuai kebutuhan
                
                # CSS untuk menempatkan gambar di tengah
                st.markdown("""
                    <style>
                    .centered-image {
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
                # Menampilkan gambar dengan CSS kelas 'centered-image'
                # st.markdown('<img src="assets/gambar/Untitled copy.png" class="centered-image" width="400"/>', unsafe_allow_html=True)
            
            
            with col_profil2:
                st.markdown("# Arya Hisma Maulana")
                
                # Load custom CSS
                st.markdown("""
                <style>
                .profil-header {
                    font-size: 32px;
                    font-weight: bold;
                    color: #ffffff;                         #dd3f3f
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .profil-item {
                    font-size: 18px;
                    color: #ffffff;                  #555
                    margin-bottom: 10px;
                }
                .profil-company {
                    font-weight: bold;
                    color: #333;
                }
                .profil-date {
                    font-style: italic;
                    color: #ffffff;                #777 
                }
                .profil-description {
                    margin-left: 20px;
                    font-size: 16px;
                    color: #ffffff;                    #666
                    line-height: 1.6;
                }
                </style>
                    """, unsafe_allow_html=True)

            # Header
            st.markdown('<div class="job-header">PROFIL</div>', unsafe_allow_html=True)

            # Job details
            st.markdown('''
            <div class="profil-description">
            Seorang data analis dengan pengalaman lebih dari 5 tahun di bidang analisis data, saya memiliki keterampilan mendalam dalam:
            Pembersihan, Transformasi, dan Penyimpanan Data: Menggunakan Tableau Prep dan Python untuk membersihkan, mentransformasi, dan menyimpan data dalam data warehouse, memastikan konsistensi dan aksesibilitas data.
            Visualisasi Data: Membuat visualisasi data interaktif dengan Tableau dan Power BI, mendesain dashboard yang mendukung pengambilan keputusan strategis.
            Uji Statistik dan Machine Learning: Melakukan analisis statistik dan menerapkan algoritma machine learning dengan Python, termasuk uji korelasi, analisis regresi, dan analisis cluster. Mengembangkan model untuk prediksi dan klasifikasi, serta visualisasikan hasilnya untuk komunikasi yang efektif.
            Kombinasi keterampilan teknis ini memungkinkan saya untuk memberikan wawasan yang berharga dan mendukung keputusan berbasis data di berbagai konteks bisnis.
            </div>
        </div>
        ''', unsafe_allow_html=True)
            
            #     # Load custom CSS
            #     st.markdown("""
            #             <style>
            # .profil-header {
            #     font-size: 32px;
            #     font-weight: bold;
            #     color: #dd3f3f;
            #     border-bottom: 3px solid #007bff;  /* Garis bawah warna biru */
            #     padding-bottom: 10px;
            #     margin-bottom: 20px;
            # }
            # .profil-item {
            #     font-size: 18px;
            #     color: #ffffff;
            #     margin-bottom: 10px;
            # }
            # .profil-item strong {
            #     font-weight: bold;
            # }
            # .profil-details {
            #     margin-left: 20px;
            #     font-size: 16px;
            #     color: #ffffff;
            # }
            # </style>
            #             """, unsafe_allow_html=True)

            #     # Header
            #     st.markdown('<div class="profile-header">PROFIL</div>', unsafe_allow_html=True)

            #     # Profile text
            #     st.markdown('''
            #         <div class="profile-text">
            # Seorang data analis dengan pengalaman lebih dari 5 tahun di bidang analisis data, saya memiliki keterampilan mendalam dalam:
            # Pembersihan, Transformasi, dan Penyimpanan Data: Menggunakan Tableau Prep dan Python untuk membersihkan, mentransformasi, dan menyimpan data dalam data warehouse, memastikan konsistensi dan aksesibilitas data.
            # Visualisasi Data: Membuat visualisasi data interaktif dengan Tableau dan Power BI, mendesain dashboard yang mendukung pengambilan keputusan strategis.
            # Uji Statistik dan Machine Learning: Melakukan analisis statistik dan menerapkan algoritma machine learning dengan Python, termasuk uji korelasi, analisis regresi, dan analisis cluster. Mengembangkan model untuk prediksi dan klasifikasi, serta visualisasikan hasilnya untuk komunikasi yang efektif.
            # Kombinasi keterampilan teknis ini memungkinkan saya untuk memberikan wawasan yang berharga dan mendukung keputusan berbasis data di berbagai konteks bisnis.

            # </div>
            #         ''', unsafe_allow_html=True)
                            
                # st.header("Profil")
                # st.markdown('''Seorang profesional Pemasaran Digital dengan pengalaman 
                #             lebih dari 1 tahun dalam mengembangkan dan melaksanakan strategi 
                #             pemasaran online yang berhasil. Memiliki pemahaman mendalam tentang 
                #             berbagai platform digital dan alat analitik. Terampil dalam 
                #             meningkatkan visibilitas online, memperkuat merek, dan meningkatkan 
                #             konversi.''')

        with st.container(border=False):
            # # Load custom CSS
            # st.markdown("""
            #     <style>
            #     .education-header {
            #         font-size: 32px;
            #         font-weight: bold;
            #         color: #dd3f3f;                             #dd3f3f 
            #         border-bottom: 3px solid #007bff;
            #         padding-bottom: 10px;
            #         margin-bottom: 20px;
            #     }
            #     .education-item {
            #         font-size: 18px;
            #         color: #ffffff;                               #555
            #         margin-bottom: 10px;
            #     }
            #     .education-item strong {
            #         font-weight: bold;
            #     }
            #     .education-details {
            #         margin-left: 20px;
            #         font-size: 16px;
            #         color: #ffffff;                                #666
            #     }
            #     </style>
            #     """, unsafe_allow_html=True)

            # # Header
            # st.markdown('<div class="education-header">RIWAYAT PENDIDIKAN</div>', unsafe_allow_html=True)

            # # Education details
            # st.markdown('''
            # <div class="education-item">
            #     <strong>S1 Teknik Sipil Universitas Syiah Kuala</strong>
            #     <div class="education-details">
            #         - Banda Aceh, 2008-2013<br>
            #         - Lulus dengan predikat Pujian, IPK 3.45
            #     </div>
            # </div>
            # ''', unsafe_allow_html=True)
            
            
            # st.header("Riwayat Pendidikan")
            # st.markdown('''
            #             **S1 Teknik Sipil Universitas Syiah Kuala**
            #             - Banda Aceh, 2008-2013
            #             - Lulus dengan predikat Pujian, IPK 3.45
            #             ''')
            
            
            # Load custom CSS
            st.markdown("""
                <style>
                .job-header {
                    font-size: 32px;
                    font-weight: bold;
                    color: #dd3f3f;
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .job-item {
                    font-size: 18px;
                    color: #ffffff;                  #555
                    margin-bottom: 10px;
                }
                .job-company {
                    font-weight: bold;
                    color: #333;
                }
                .job-date {
                    font-style: italic;
                    color: #ffffff;                #777 
                }
                .job-description {
                    margin-left: 20px;
                    font-size: 16px;
                    color: #666;
                    line-height: 1.6;
                }
                </style>
                    """, unsafe_allow_html=True)

            # Header
            st.markdown('<div class="job-header">RIWAYAT PEKERJAAN</div>', unsafe_allow_html=True)

            # Job details
            st.markdown('''
        <div class="job-item">
        <div class="job-company">PT Pembangunan Perumahan (Persero) .Tbk</div>
        <div class="job-date">Jakarta, Sep 2018 - Saat Ini</div>
        <div class="job-description">
            <strong> - Melakukan Pembersihan, Transformasi, dan Penyimpanan Data di Data Warehouse</strong><br>
            Saya bertanggung jawab untuk melakukan pembersihan dan transformasi data menggunakan Tableau Prep. Proses ini mencakup identifikasi dan penghapusan data duplikat, mengatasi data yang hilang, dan standardisasi format data. Saya juga memanfaatkan extension analytics dengan Python untuk mengotomatiskan dan meningkatkan efisiensi proses transformasi data. Setelah data dibersihkan dan ditransformasikan, saya menyimpannya ke dalam data warehouse yang terintegrasi untuk memastikan aksesibilitas dan konsistensi data bagi tim analitik lainnya.
        </div>
        <div class="job-description">
            <strong> - Visualisasi Data</strong><br>
            Saya memiliki pengalaman dalam membuat visualisasi data yang informatif dan interaktif menggunakan Tableau dan Power BI. Saya merancang dashboard yang intuitif dan mudah dipahami, yang membantu dalam pengambilan keputusan strategis berdasarkan data. Visualisasi yang saya buat mencakup berbagai jenis grafik, peta, dan laporan yang memberikan wawasan mendalam mengenai tren dan pola dalam data.
        </div>
        <div class="job-description">
            <strong> - Melakukan Uji Statistik dan Machine Learning</strong><br>
            Dalam pekerjaan saya, saya juga melakukan uji statistik dan penerapan algoritma machine learning menggunakan Python. Saya melakukan analisis statistik seperti uji korelasi, analisis regresi, dan analisis cluster untuk memahami karakteristik dan hubungan dalam data. Selain itu, saya mengembangkan model machine learning untuk prediksi dan klasifikasi. Hasil dari analisis dan model tersebut kemudian saya visualisasikan menggunakan Tableau untuk memudahkan interpretasi dan komunikasi hasil kepada tim dan stakeholder lainnya.
        </div>
        </div>
        ''', unsafe_allow_html=True)
            
            
            # st.header("Riwayat Pekerjaan")
            # st.markdown('''
            #             **PT Pembangunan Perumahan (Persero) .Tbk**
            #             Jakarta, Sep 2018 - Saat Ini
                        
            #             - Melakukan Pembersihan, Transformasi, dan Penyimpanan Data di Data Warehouse
            # Saya bertanggung jawab untuk melakukan pembersihan dan transformasi data menggunakan Tableau Prep. Proses ini mencakup identifikasi dan penghapusan data duplikat, mengatasi data yang hilang, dan standardisasi format data. Saya juga memanfaatkan extension analytics dengan Python untuk mengotomatiskan dan meningkatkan efisiensi proses transformasi data. Setelah data dibersihkan dan ditransformasikan, saya menyimpannya ke dalam data warehouse yang terintegrasi untuk memastikan aksesibilitas dan konsistensi data bagi tim analitik lainnya.

            #             - Visualisasi Data 
            # Saya memiliki pengalaman dalam membuat visualisasi data yang informatif dan interaktif menggunakan Tableau dan Power BI. Saya merancang dashboard yang intuitif dan mudah dipahami, yang membantu dalam pengambilan keputusan strategis berdasarkan data. Visualisasi yang saya buat mencakup berbagai jenis grafik, peta, dan laporan yang memberikan wawasan mendalam mengenai tren dan pola dalam data.

            #             - Melakukan Uji Statistik dan Machine Learning
            # Dalam pekerjaan saya, saya juga melakukan uji statistik dan penerapan algoritma machine learning menggunakan Python. Saya melakukan analisis statistik seperti uji korelasi, analisis regresi, dan analisis cluster untuk memahami karakteristik dan hubungan dalam data. Selain itu, saya mengembangkan model machine learning untuk prediksi dan klasifikasi. Hasil dari analisis dan model tersebut kemudian saya visualisasikan menggunakan Tableau untuk memudahkan interpretasi dan komunikasi hasil kepada tim dan stakeholder lainnya.
            #             ''')
            
            # Load custom CSS
            st.markdown("""
                <style>
                .job-header {
                    font-size: 32px;
                    font-weight: bold;
                    color: #ffffff;                           #dd3f3f
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .job-item {
                    font-size: 18px;
                    color: #ffffff;                        #555
                    margin-bottom: 10px;
                }
                .job-company {
                    font-weight: bold;
                    color: #333;
                }
                .job-date {
                    font-style: italic;
                    color: #ffffff;                           #777
                }
                .job-description {
                    margin-left: 20px;
                    font-size: 16px;
                    color: #ffffff;                        #666
                    line-height: 1.6;
                }
                </style>
                    """, unsafe_allow_html=True)

            # Header
            st.markdown('<div class="job-header">PENGALAMAN PELATIHAN</div>', unsafe_allow_html=True)

            # Job details
            st.markdown('''
        <div class="job-item">
        <div class="job-company">ALGORITMA ACADEMY (Data Analytics Specialization)</div>
        <div class="job-date">Jakarta, Nov 2023 - Jan 2024</div>
        <div class="job-description">
            <strong> - Python for Data Analytics</strong><br>
            <strong> - Exploratory Data Analysis</strong><br>
            <strong> - Data Wrangling and Visualization</strong><br>
            <strong> - SQL Query and Capstone Project</strong><br>
            <strong> - Intoduction to Machine Learning</strong><br>
            </div>

        </div>
        ''', unsafe_allow_html=True)  
            
            st.markdown('''
        <div class="job-item">
        <div class="job-company">Digital Talent Scholarship Kominfo (UI/UX Design)</div>
        <div class="job-date">Jakarta, Agu 2022 - Okt 2022</div>
        <div class="job-description">
            <strong> - UX Design Process</strong><br>
            </div>

        </div>
        ''', unsafe_allow_html=True) 
            
            # Load custom CSS
            st.markdown("""
                <style>
                .job-header {
                    font-size: 32px;
                    font-weight: bold;
                    color: #ffffff;                                #dd3f3f
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .job-item {
                    font-size: 18px;
                    color: #ffffff;                                #555
                    margin-bottom: 10px;
                }
                .job-company {
                    font-weight: bold;
                    color: #ffffff;                                  #333
                } 
                .job-date {
                    font-style: italic;
                    color: #ffffff;                                  #777
                }
                .job-description {
                    margin-left: 20px;
                    font-size: 16px;
                    color: #ffffff;                                 #666
                    line-height: 1.6;
                }
                </style>
                    """, unsafe_allow_html=True)

        #     # Header
        #     st.markdown('<div class="job-header">PENGALAMAN ORGANISASI</div>', unsafe_allow_html=True)

        #     # Job details
        #     st.markdown('''
        # <div class="job-item">
        # <div class="job-company">IKAFT USK JABAJAB</div>
        # <div class="job-date">Jakarta, Sep 2018 - Saat Ini</div>
        # <div class="job-description">
        #     <strong> - Menyelenggarakan musyawarah besar organisasi</strong><br>
        #     <strong> - Menyelenggarakan pelatihan bagi alumni</strong><br>
        #     </div>

        # </div>
        # ''', unsafe_allow_html=True)
            



        # Social Media header
        # Load Font Awesome CSS
        st.markdown("""
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <style>
            .social-button {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 10px 15px;
                margin: 5px;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s, color 0.3s;
                    }
            .social-button:hover {
                background-color: black;
                color: white;
                }
            .social-button i {
                margin-right: 8px;
                }
            </style>
            """, unsafe_allow_html=True)

        st.title("Social Media")

        # Social media buttons
        st.markdown("""
            <a href="https://www.linkedin.com/in/arya-hisma-maulana" class="social-button">
                <i class="fab fa-linkedin"></i> LinkedIn
            </a>
            <a href="https://www.instagram.com/aryahisma" class="social-button">
                <i class="fab fa-instagram"></i> Instagram
            </a>
            <a href="https://github.com/AryaHisma" class="social-button">
                <i class="fab fa-github"></i> GitHub
            </a>
            """, unsafe_allow_html=True)

    else:
        with st.container(height=440, border=False):
            col_profil1, col_profil2 = st.columns([1, 4])
            
            with col_profil1:
                # --- IMAGE ---
                image = Image.open("assets/gambar/Untitled copy.png")
                
                # Menggunakan st.image untuk menampilkan gambar dengan ukuran yang diperbesar
                st.image(image, width=260)  # Sesuaikan lebar gambar sesuai kebutuhan
                
                # CSS untuk menempatkan gambar di tengah
                st.markdown("""
                    <style>
                    .centered-image {
                        display: block;
                        margin-left: auto;
                        margin-right: auto;
                    }
                    </style>
                """, unsafe_allow_html=True)
                
                # Menampilkan gambar dengan CSS kelas 'centered-image'
                # st.markdown('<img src="assets/gambar/Untitled copy.png" class="centered-image" width="400"/>', unsafe_allow_html=True)
            
            
            with col_profil2:
                st.markdown("# Arya Hisma Maulana")
                
                # Load custom CSS
                st.markdown("""
                <style>
                .profil-header {
                    font-size: 32px;
                    font-weight: bold;
                    color: #ffffff;                         #dd3f3f
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .profil-item {
                    font-size: 18px;
                    color: #ffffff;                  #555
                    margin-bottom: 10px;
                }
                .profil-company {
                    font-weight: bold;
                    color: #333;
                }
                .profil-date {
                    font-style: italic;
                    color: #ffffff;                #777 
                }
                .profil-description {
                    margin-left: 20px;
                    font-size: 16px;
                    color: #ffffff;                    #666
                    line-height: 1.6;
                }
                </style>
                    """, unsafe_allow_html=True)

            # Header
            st.markdown('<div class="job-header">PROFIL</div>', unsafe_allow_html=True)

            # Job details
            st.markdown('''
            <div class="profil-description">
            As a data analyst with over 5 years of experience in the field of data analysis, I have in-depth skills in:
            Data Cleaning, Transformation, and Storage : Using Tableau Prep and Python to clean, transform, and store data in a data warehouse, ensuring data consistency and accessibility.
            Data Visualization: Creating interactive data visualizations with Tableau and Power BI, designing dashboards that support strategic decision-making.
            Statistical Testing and Machine Learning: Conducting statistical analyses and applying machine learning algorithms with Python, including correlation tests, regression analysis, and cluster analysis. Developing models for prediction and classification, as well as visualizing results for effective communication.
            This combination of technical skills enables me to provide valuable insights and support data-driven decisions in various business contexts.
            </div>
        </div>
        ''', unsafe_allow_html=True)
            
            #     # Load custom CSS
            #     st.markdown("""
            #             <style>
            # .profil-header {
            #     font-size: 32px;
            #     font-weight: bold;
            #     color: #dd3f3f;
            #     border-bottom: 3px solid #007bff;  /* Garis bawah warna biru */
            #     padding-bottom: 10px;
            #     margin-bottom: 20px;
            # }
            # .profil-item {
            #     font-size: 18px;
            #     color: #ffffff;
            #     margin-bottom: 10px;
            # }
            # .profil-item strong {
            #     font-weight: bold;
            # }
            # .profil-details {
            #     margin-left: 20px;
            #     font-size: 16px;
            #     color: #ffffff;
            # }
            # </style>
            #             """, unsafe_allow_html=True)

            #     # Header
            #     st.markdown('<div class="profile-header">PROFIL</div>', unsafe_allow_html=True)

            #     # Profile text
            #     st.markdown('''
            #         <div class="profile-text">
            # Seorang data analis dengan pengalaman lebih dari 5 tahun di bidang analisis data, saya memiliki keterampilan mendalam dalam:
            # Pembersihan, Transformasi, dan Penyimpanan Data: Menggunakan Tableau Prep dan Python untuk membersihkan, mentransformasi, dan menyimpan data dalam data warehouse, memastikan konsistensi dan aksesibilitas data.
            # Visualisasi Data: Membuat visualisasi data interaktif dengan Tableau dan Power BI, mendesain dashboard yang mendukung pengambilan keputusan strategis.
            # Uji Statistik dan Machine Learning: Melakukan analisis statistik dan menerapkan algoritma machine learning dengan Python, termasuk uji korelasi, analisis regresi, dan analisis cluster. Mengembangkan model untuk prediksi dan klasifikasi, serta visualisasikan hasilnya untuk komunikasi yang efektif.
            # Kombinasi keterampilan teknis ini memungkinkan saya untuk memberikan wawasan yang berharga dan mendukung keputusan berbasis data di berbagai konteks bisnis.

            # </div>
            #         ''', unsafe_allow_html=True)
                            
                # st.header("Profil")
                # st.markdown('''Seorang profesional Pemasaran Digital dengan pengalaman 
                #             lebih dari 1 tahun dalam mengembangkan dan melaksanakan strategi 
                #             pemasaran online yang berhasil. Memiliki pemahaman mendalam tentang 
                #             berbagai platform digital dan alat analitik. Terampil dalam 
                #             meningkatkan visibilitas online, memperkuat merek, dan meningkatkan 
                #             konversi.''')

        with st.container(border=False):
            # # Load custom CSS
            # st.markdown("""
            #     <style>
            #     .education-header {
            #         font-size: 32px;
            #         font-weight: bold;
            #         color: #dd3f3f;                             #dd3f3f 
            #         border-bottom: 3px solid #007bff;
            #         padding-bottom: 10px;
            #         margin-bottom: 20px;
            #     }
            #     .education-item {
            #         font-size: 18px;
            #         color: #ffffff;                               #555
            #         margin-bottom: 10px;
            #     }
            #     .education-item strong {
            #         font-weight: bold;
            #     }
            #     .education-details {
            #         margin-left: 20px;
            #         font-size: 16px;
            #         color: #ffffff;                                #666
            #     }
            #     </style>
            #     """, unsafe_allow_html=True)

            # # Header
            # st.markdown('<div class="education-header">RIWAYAT PENDIDIKAN</div>', unsafe_allow_html=True)

            # # Education details
            # st.markdown('''
            # <div class="education-item">
            #     <strong>S1 Teknik Sipil Universitas Syiah Kuala</strong>
            #     <div class="education-details">
            #         - Banda Aceh, 2008-2013<br>
            #         - Lulus dengan predikat Pujian, IPK 3.45
            #     </div>
            # </div>
            # ''', unsafe_allow_html=True)
            
            
            # st.header("Riwayat Pendidikan")
            # st.markdown('''
            #             **S1 Teknik Sipil Universitas Syiah Kuala**
            #             - Banda Aceh, 2008-2013
            #             - Lulus dengan predikat Pujian, IPK 3.45
            #             ''')
            
            
            # Load custom CSS
            st.markdown("""
                <style>
                .job-header {
                    font-size: 32px;
                    font-weight: bold;
                    color: #dd3f3f;
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .job-item {
                    font-size: 18px;
                    color: #ffffff;                  #555
                    margin-bottom: 10px;
                }
                .job-company {
                    font-weight: bold;
                    color: #333;
                }
                .job-date {
                    font-style: italic;
                    color: #ffffff;                #777 
                }
                .job-description {
                    margin-left: 20px;
                    font-size: 16px;
                    color: #666;
                    line-height: 1.6;
                }
                </style>
                    """, unsafe_allow_html=True)

            # Header
            st.markdown('<div class="job-header">RIWAYAT PEKERJAAN</div>', unsafe_allow_html=True)

            # Job details
            st.markdown('''
        <div class="job-item">
        <div class="job-company">PT Pembangunan Perumahan (Persero) .Tbk</div>
        <div class="job-date">Jakarta, Sep 2018 - Saat Ini</div>
        <div class="job-description">
            <strong> - Performing Data Cleaning, Transformation, and Storage in the Data Warehouse</strong><br>
            I am responsible for data cleaning and transformation using Tableau Prep. This process includes identifying and removing duplicate data, handling missing data, and standardizing data formats. I also leverage Python analytics extensions to automate and enhance the efficiency of the data transformation process. Once the data is cleaned and transformed, I store it in an integrated data warehouse to ensure accessibility and data consistency for other analytics teams.
        </div>
        <div class="job-description">
            <strong> - Visualisasi Data</strong><br>
            I have experience in creating informative and interactive data visualizations using Tableau and Power BI. I design intuitive and easy-to-understand dashboards that aid in strategic decision-making based on data. The visualizations I create include various types of charts, maps, and reports that provide deep insights into trends and patterns within the data.
        </div>
        <div class="job-description">
            <strong> - Melakukan Uji Statistik dan Machine Learning</strong><br>
            In my work, I also perform statistical tests and apply machine learning algorithms using Python. I conduct statistical analyses such as correlation tests, regression analysis, and cluster analysis to understand the characteristics and relationships within the data. Additionally, I develop machine learning models for prediction and classification. The results from these analyses and models are then visualized using Tableau to facilitate the interpretation and communication of findings to the team and other stakeholders.
        </div>
        </div>
        ''', unsafe_allow_html=True)
            
            
            # st.header("Riwayat Pekerjaan")
            # st.markdown('''
            #             **PT Pembangunan Perumahan (Persero) .Tbk**
            #             Jakarta, Sep 2018 - Saat Ini
                        
            #             - Melakukan Pembersihan, Transformasi, dan Penyimpanan Data di Data Warehouse
            # Saya bertanggung jawab untuk melakukan pembersihan dan transformasi data menggunakan Tableau Prep. Proses ini mencakup identifikasi dan penghapusan data duplikat, mengatasi data yang hilang, dan standardisasi format data. Saya juga memanfaatkan extension analytics dengan Python untuk mengotomatiskan dan meningkatkan efisiensi proses transformasi data. Setelah data dibersihkan dan ditransformasikan, saya menyimpannya ke dalam data warehouse yang terintegrasi untuk memastikan aksesibilitas dan konsistensi data bagi tim analitik lainnya.

            #             - Visualisasi Data 
            # Saya memiliki pengalaman dalam membuat visualisasi data yang informatif dan interaktif menggunakan Tableau dan Power BI. Saya merancang dashboard yang intuitif dan mudah dipahami, yang membantu dalam pengambilan keputusan strategis berdasarkan data. Visualisasi yang saya buat mencakup berbagai jenis grafik, peta, dan laporan yang memberikan wawasan mendalam mengenai tren dan pola dalam data.

            #             - Melakukan Uji Statistik dan Machine Learning
            # Dalam pekerjaan saya, saya juga melakukan uji statistik dan penerapan algoritma machine learning menggunakan Python. Saya melakukan analisis statistik seperti uji korelasi, analisis regresi, dan analisis cluster untuk memahami karakteristik dan hubungan dalam data. Selain itu, saya mengembangkan model machine learning untuk prediksi dan klasifikasi. Hasil dari analisis dan model tersebut kemudian saya visualisasikan menggunakan Tableau untuk memudahkan interpretasi dan komunikasi hasil kepada tim dan stakeholder lainnya.
            #             ''')
            
            # Load custom CSS
            st.markdown("""
                <style>
                .job-header {
                    font-size: 32px;
                    font-weight: bold;
                    color: #ffffff;                           #dd3f3f
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .job-item {
                    font-size: 18px;
                    color: #ffffff;                        #555
                    margin-bottom: 10px;
                }
                .job-company {
                    font-weight: bold;
                    color: #333;
                }
                .job-date {
                    font-style: italic;
                    color: #ffffff;                           #777
                }
                .job-description {
                    margin-left: 20px;
                    font-size: 16px;
                    color: #ffffff;                        #666
                    line-height: 1.6;
                }
                </style>
                    """, unsafe_allow_html=True)

            # Header
            st.markdown('<div class="job-header">PENGALAMAN PELATIHAN</div>', unsafe_allow_html=True)

            # Job details
            st.markdown('''
        <div class="job-item">
        <div class="job-company">ALGORITMA ACADEMY (Data Analytics Specialization)</div>
        <div class="job-date">Jakarta, Nov 2023 - Jan 2024</div>
        <div class="job-description">
            <strong> - Python for Data Analytics</strong><br>
            <strong> - Exploratory Data Analysis</strong><br>
            <strong> - Data Wrangling and Visualization</strong><br>
            <strong> - SQL Query and Capstone Project</strong><br>
            <strong> - Intoduction to Machine Learning</strong><br>
            </div>

        </div>
        ''', unsafe_allow_html=True)  
            
            st.markdown('''
        <div class="job-item">
        <div class="job-company">Digital Talent Scholarship Kominfo (UI/UX Design)</div>
        <div class="job-date">Jakarta, Agu 2022 - Okt 2022</div>
        <div class="job-description">
            <strong> - UX Design Process</strong><br>
            </div>

        </div>
        ''', unsafe_allow_html=True) 
            
            # Load custom CSS
            st.markdown("""
                <style>
                .job-header {
                    font-size: 32px;
                    font-weight: bold;
                    color: #ffffff;                                #dd3f3f
                    border-bottom: 3px solid #007bff;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .job-item {
                    font-size: 18px;
                    color: #ffffff;                                #555
                    margin-bottom: 10px;
                }
                .job-company {
                    font-weight: bold;
                    color: #ffffff;                                  #333
                } 
                .job-date {
                    font-style: italic;
                    color: #ffffff;                                  #777
                }
                .job-description {
                    margin-left: 20px;
                    font-size: 16px;
                    color: #ffffff;                                 #666
                    line-height: 1.6;
                }
                </style>
                    """, unsafe_allow_html=True)

        #     # Header
        #     st.markdown('<div class="job-header">PENGALAMAN ORGANISASI</div>', unsafe_allow_html=True)

        #     # Job details
        #     st.markdown('''
        # <div class="job-item">
        # <div class="job-company">IKAFT USK JABAJAB</div>
        # <div class="job-date">Jakarta, Sep 2018 - Saat Ini</div>
        # <div class="job-description">
        #     <strong> - Menyelenggarakan musyawarah besar organisasi</strong><br>
        #     <strong> - Menyelenggarakan pelatihan bagi alumni</strong><br>
        #     </div>

        # </div>
        # ''', unsafe_allow_html=True)
            



        # Social Media header
        # Load Font Awesome CSS
        st.markdown("""
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
            <style>
            .social-button {
                display: inline-flex;
                align-items: center;
                justify-content: center;
                text-decoration: none;
                background-color: white;
                color: black;
                border: 2px solid black;
                border-radius: 5px;
                padding: 10px 15px;
                margin: 5px;
                font-size: 16px;
                font-weight: bold;
                transition: background-color 0.3s, color 0.3s;
                    }
            .social-button:hover {
                background-color: black;
                color: white;
                }
            .social-button i {
                margin-right: 8px;
                }
            </style>
            """, unsafe_allow_html=True)

        st.title("Social Media")

        # Social media buttons
        st.markdown("""
            <a href="https://www.linkedin.com/in/arya-hisma-maulana" class="social-button">
                <i class="fab fa-linkedin"></i> LinkedIn
            </a>
            <a href="https://www.instagram.com/aryahisma" class="social-button">
                <i class="fab fa-instagram"></i> Instagram
            </a>
            <a href="https://github.com/AryaHisma" class="social-button">
                <i class="fab fa-github"></i> GitHub
            </a>
            """, unsafe_allow_html=True)
