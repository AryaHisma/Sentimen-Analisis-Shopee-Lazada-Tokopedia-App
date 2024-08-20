from nlp_id.tokenizer import Tokenizer, PhraseTokenizer
import re, string
# from nlp_id.stopword import StopWord
from nlp_id.lemmatizer import Lemmatizer
from stopword_project import StopWordss
from lemma_project import Lemmatizer
from stopword_project import StopWordss

'''
Tahapan Text Preprocessing :
    Lowercase
    Tokenization
    Text Cleaning
    Stops Removal
    Stemming and or lemmatizing
'''
class Preprocessor:
    def lowercase(self, text):
        '''
        convert text to lowercase
        '''
        return text.lower()
    
    def text_cleaning(self, text):
        '''
        cleaning text by removing punctuation, numbers and whitespace
        '''
        # Menghilangkan angka
        text = re.sub("\d+", "", text)
        
        # Menghilangkan tanda baca
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Menghilangkan whitespace
        text = text.strip()
        text = re.sub("  ", " ", text)
        
        # menghilangkan tautan
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        text = url_pattern.sub(r'', text)
        
        return text
  
    
    # def tokenize(self, text, Phrase=False):
    #     '''
    #     Tokenize text into words or phrases
    #     '''
    #     if Phrase:
    #         tokenizer = PhraseTokenizer()
    #     else:
    #         tokenizer = Tokenizer()
    #     return tokenizer.tokenize(text)
    
       
    def remove_stopwords(self, text):
        '''
        Remove stopwords from tokens
        '''
        stopword = StopWordss()
        return stopword.remove_stopwordss(text)
    
    
    def lemmatizing (self, text):
        '''
        Lemmatize or stemming tokens
        '''
        lemmatizer = Lemmatizer()
        hasil = lemmatizer.lemmatize(text)
        return hasil
        
        
        
# if __name__ == '__main__':
#     data = '''Kementerian Kesehatan (Kemenkes) RI mencatat adanya penurunan angka kejadian malaria berkisar 25 ribu kasus dalam kurun setahun terakhir, meskipun hingga saat ini Indonesia masih menempati posisi kedua kasus tertinggi di Asia setelah India.
# "Malaria di Indonesia memang termasuk yang tertinggi di Asia, nomor dua setelah India. Kasus malaria di tahun 2023 sebanyak 418.546 kasus, menurun dibandingkan tahun 2022 yaitu 443.530 kasus," kata Direktur Pencegahan dan Pengendalian Penyakit Menular Kemenkes Imran Pambudi saat dikonfirmasi di Jakarta, Kamis.
# World Malaria Report 2023 melaporkan India dan Indonesia masih menyumbang sekitar 94 persen kematian akibat malaria di seluruh kawasan WHO Asia Tenggara.
# Namun jika dilihat pada rentang waktu satu dekade terakhir, kasus malaria di Indonesia justru mengalami peningkatan sejak 2015 yang kala itu mencapai 217.025 kasus. Menurut Imran, peningkatan kasus ini disebabkan membaiknya sistem pencatatan dan pelaporan surveilans malaria di rumah sakit dan puskesmas, serta tingginya peningkatan penemuan kasus malaria yang dilakukan oleh kader malaria, terutama di daerah endemis tinggi.
# "Tahun 2023 jumlah tes yang dilakukan sekitar 3 juta tes, terutama pada masyarakat di wilayah endemis tinggi," ujarnya.
# Imran memastikan capaian program malaria saat ini masih dalam jalur yang sesuai, dibuktikan dengan tercapainya target eliminasi malaria di kabupaten/kota sesuai dengan target yang ditetapkan dalam Rencana Pembangunan Jangka Menengah Nasional (RPJMN).
# "Di mana misalnya, tahun 2023 dari target 385 kabupaten/kota, eliminasi malaria capaiannya sebanyak 389 kabupaten/kota. Target 2024 adalah 405 dan per Maret 2024 mencapai 393 kabupaten/kota yang telah berhasil mencapai eliminasi malaria," katanya.
# Pihaknya terus melakukan upaya identifikasi daerah yang sudah rendah untuk segera didorong mencapai eliminasi. Namun pada masa ke depan ini, kata Imran, upaya penanggulangan malaria akan lebih menantang karena daerah-daerah yang belum mencapai eliminasi adalah wilayah yang hard rock, dimana daerah yang belum mencapai eliminasi adalah daerah yang masih endemis malaria, terutama di kawasan timur Indonesia.
# Menurut data Kemenkes, pada 2023 ditemukan 418.546 kasus malaria di Indonesia, sebanyak 369.119 diantaranya ditemukan di Papua, Papua Tengah, Papua Selatan, dan Papua Pegunungan.
# "Kawasan Papua dan Nusa Tenggara merupakan daerah dengan kasus malaria tertinggi di Indonesia. Selain itu wilayah Sumba dan Kabupaten Penajam Paser Utara, Kalimantan Timur juga masih merupakan daerah penularan malaria," katanya.
# "Oleh karena konsentrasi kasus terjadi di Papua, maka upaya penanggulangan juga diprioritaskan di Papua, dengan melakukan berbagai intervensi percepatan penurunan kasus," kata Imran.'''
    
    
    
    
    
#     preprocessor = Preprocessor()
#     data_lowercase = preprocessor.lowercase(data)
#     data_clean = preprocessor.text_cleaning(data_lowercase)
#     data_stopwords = preprocessor.remove_stopwords(data_clean)
#     data_lemmitized = preprocessor.lemmatizing(data_stopwords)
#     print(data_lemmitized)
    
    

         
         