import re, string, json, os
import emoji

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import nltk

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

from typing import List
from nlp_id.lemmatizer import Lemmatizer 
from nlp_id.tokenizer import Tokenizer, PhraseTokenizer
from nlp_id.postag import PosTag 
# from stopword_project import StopWordss
import pandas as pd
from unidecode import unidecode
import streamlit as st

@st.cache_data(persist=True)
def download_nltk_resources():
    # Menentukan path di mana resource akan diunduh
    nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
    if not os.path.exists(nltk_data_path):
        os.makedirs(nltk_data_path)

    # Mengunduh resource dan menentukan direktori target
    nltk.download('punkt', download_dir=nltk_data_path)
    nltk.download('stopwords', download_dir=nltk_data_path)
    
# Panggil fungsi untuk mengunduh resource yang diperlukan
download_nltk_resources()

class TextProcessing:
    def __init__(self) -> None:
        # Panggil fungsi download_nltk_resources untuk memastikan resource telah diunduh
        download_nltk_resources()
        
        # Inisialisasi stopwords setelah memastikan resource telah tersedia
        self.stopword_en = stopwords.words('english')
        self.stopword_id = stopwords.words('indonesian')
        
    
    def remove_unicode_styles(_self, text: str, *args) -> str:
        return unidecode(text)     
    
    
    def lowercase(_self, data:str):
        data = data.lower()
        return data
    
    
    def remove_emoji(self, text: str) -> str:
        # Menggunakan emoji.replace_emoji jika tersedia
        # atau gunakan emoji.demojize jika replace_emoji tidak ada
        return emoji.replace_emoji(text, replace=' ')
    
    
    def remove_emoji_text(self, text: str) -> str:
        # Konversi emoji menjadi deskripsi teks
        text_with_descriptions = emoji.demojize(text)
        # Hapus deskripsi emoji (dalam format :name_of_emoji:)
        return emoji.replace_emoji(text_with_descriptions, replace=' ')
    
       
    # @st.cache_data   
    def text_cleaning(self, data: str) -> str:
        # number
        data = re.sub(r'\d+', " ", data)
        
        # @pattern
        at_pattern = re.compile(r'@\S+')
        data = at_pattern.sub(r' ', data)
        
        # tanda ￼
        data = re.sub(r'\￼{2,}', ' ', data)
        
        # tanda ðŸ‘
        data = re.sub(r'\ðŸ‘{2,}', ' ', data)
        
        # tanda AAAA+++
        data = re.sub(r'AAAA\++', ' ', data)
        
        # tanda »
        data = re.sub(r'»', ' ', data)
        
        # tanda ' 
        data = re.sub(r'\' ', ' ', data)
        
        # tanda -
        data = re.sub(r'-', ' ', data)
        
        # tanda --
        data = re.sub(r'--', ' ', data)
        
        # tanda ðŸ‘ŒðŸ
        data = re.sub(r'ðŸ‘ŒðŸ', ' ', data)
        
        # url
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        data = url_pattern.sub(r' ', data)
        
        # Anda bisa memasukkan semua karakter yang ingin digantikan dalam kurung siku
        pattern = r'[!@#$%^&*()_\-+=|\\{}\[\]:";\'/?<>.,~`]'
        # Mengganti tanda baca dengan spasi
        data = re.sub(pattern, ' ', data)
        
        # punctuation
        data = data.translate(str.maketrans(" ", " ", string.punctuation))
        
        # Membuat tabel translasi untuk mengganti setiap tanda baca dengan spasi
        translation_table = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        # Menggunakan translate untuk mengganti tanda baca dengan spasi
        data = data.translate(translation_table)
        
        # whitespace
        data = data.strip()

        return data
    
    
    def token_slang(self, data:str, lib="standar"):
        if lib == "standar":
            result = word_tokenize(data)
        elif lib == "kumparan":
            token_ = Tokenizer()
            result = token_.tokenize(data)
        return result

    
    def remove_stopwords(self, text, stopword_path=None):
        # Dapatkan direktori saat ini dari file yang sedang dieksekusi
        current_dir = os.path.dirname(os.path.realpath(__file__))
    
        # Jika path tidak disediakan, gunakan path default ke assets/stopword.txt
        if not stopword_path:
            stopword_path = os.path.join(
            current_dir, "../assets", "stopword.txt"
            )
    
        # Debugging: Cetak path untuk memverifikasi
        # print(f"Trying to open stopword file at: {stopword_path}")
    
        # Pengecekan apakah file stopword ada
        if not os.path.exists(stopword_path):
            raise FileNotFoundError(f"Stopword file not found at: {stopword_path}")
    
        # Buka dan baca file stopword
        with open(stopword_path) as f:
            stopwords = f.read().split('\n')
    
        # List untuk menyimpan hasil sementara dan bagian teks
        temp_result = []
        parts = []

        # Pecah teks menjadi bagian-bagian menggunakan regex
        for match in re.finditer(r'[^.,?!\s]+|[.,?!]', text):
            parts.append(match.group())

        # Tambahkan kata yang bukan stopword ke dalam hasil sementara
        for word in parts:
            if word.casefold() not in stopwords:
                temp_result.append(word)

        # Gabungkan hasil sementara menjadi string tunggal
        result_cand = ' '.join(temp_result)
    
        # Hilangkan spasi sebelum tanda baca
        result = re.sub(r' ([^A-Za-z0-9])', r'\1', result_cand)

        return result
    
        
    # def stopword_removal(self, data, lib="kumparan"):
    #     if lib == 'standar':
    #         stopwords = self.stopword_en

    #         resultwords  = [word for word in data if word not in stopwords]
    #         result = ' '.join(resultwords)
    #     elif lib == 'kumparan':
    #         sw = remove_stopwords()
    #         result = sw.remove_stopwordss(data)        
        return result

    # def stemming(self, data:str):
    #     st = PorterStemmer()
    #     return st.stem(data)
    
    
    def stemming(self, data:str):
        st = StemmerFactory()
        stem = st.create_stemmer()
        return stem.stem(data)    
    
    
    def lemmatize(self, data:str):
        lemmatizer = Lemmatizer()
        result = lemmatizer.lemmatize(data)
        return data
    
    
    def slang_transform(self, data: str):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        slang_path = os.path.join(current_dir, "../assets", "slang_sorted.json")
        with open(slang_path) as f:
            slang_dict = json.load(f)
        tokens = self.token_slang(data)

        result = []
        for token in tokens:
            if token in slang_dict:
                token = slang_dict[token]
            result.append(token)

        result = ' '.join(result)
        return result
    
    


if __name__ == "__main__":
    test = "tolong diperbaiki pelayanan sellernya jangan sesukanya ngirim barang minta warna apa dikirimnya warna laen minta ukuran ngirimnya ukuran yg ga sesuai pesanan kalo gitu siapa yg mau make ngecewain banget"

    mod = TextProcessing()
    
    # hasil = mod.remove_emoji(hasil)
    hasil = mod.text_cleaning(test)
    # hasil = mod.slang_transform(hasil)
    hasil = mod.remove_stopwords(hasil)
    # hasil = mod.stemming(hasil)
    hasil = mod.token_slang(hasil, lib="kumparan")

    # hasil = mod.slang_transform(hasil)

    print(hasil)

