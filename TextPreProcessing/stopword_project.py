import os
import re

class StopWordss:
    def __init__(self, stopword_path=None):
        self.current_dir = os.path.dirname(os.path.realpath(__file__))
        if not stopword_path:
            stopword_path = os.path.join(
                self.current_dir, "../assets", "stopword.txt"
            )
        
        # Debugging: Print the path to check
        print(f"Trying to open stopword file at: {stopword_path}")

        with open(stopword_path) as f:
            self.stopwords = f.read().split('\n')

    def get_stopword(self):
        return self.stopwords

    def remove_stopwordss(self, text):
        stopword = self.get_stopword()
        temp_result = []
        parts = []

        for match in re.finditer(r'[^.,?!\s]+|[.,?!]', text):
            parts.append(match.group())

        for word in parts:
            if word.casefold() not in stopword:
                temp_result.append(word)

        result_cand = ' '.join(temp_result)
        result = re.sub(r' ([^A-Za-z0-9])', r'\1', result_cand)

        return result

# import os
# import re

# class StopWordss:
#     def __init__(self, stopword_path=None):
#         # Dapatkan direktori saat ini dari file yang sedang dieksekusi
#         self.current_dir = os.path.dirname(os.path.realpath(__file__))
        
#         # Jika path tidak disediakan, gunakan path default ke assets/stopword.txt
#         if not stopword_path:
#             stopword_path = os.path.join(
#                 self.current_dir, "../assets", "stopword.txt"
#             )
        
#         # Debugging: Cetak path untuk memverifikasi
#         # print(f"Trying to open stopword file at: {stopword_path}")
        
#         # Pengecekan apakah file stopword ada
#         if not os.path.exists(stopword_path):
#             raise FileNotFoundError(f"Stopword file not found at: {stopword_path}")
        
#         # Buka dan baca file stopword
#         with open(stopword_path) as f:
#             self.stopwords = f.read().split('\n')

#     def get_stopword(self):
#         # Mengembalikan daftar kata stop yang sudah dibaca
#         return self.stopwords

#     def remove_stopwordss(self, text):
#         # Dapatkan daftar kata stop
#         stopword = self.get_stopword()
        
#         # List untuk menyimpan hasil sementara dan bagian teks
#         temp_result = []
#         parts = []

#         # Pecah teks menjadi bagian-bagian menggunakan regex
#         for match in re.finditer(r'[^.,?!\s]+|[.,?!]', text):
#             parts.append(match.group())

#         # Tambahkan kata yang bukan stopword ke dalam hasil sementara
#         for word in parts:
#             if word.casefold() not in stopword:
#                 temp_result.append(word)

#         # Gabungkan hasil sementara menjadi string tunggal
#         result_cand = ' '.join(temp_result)
        
#         # Hilangkan spasi sebelum tanda baca
#         result = re.sub(r' ([^A-Za-z0-9])', r'\1', result_cand)

#         return result

# Contoh penggunaan
if __name__ == "__main__":
    # Instansiasi kelas StopWordss
    sw = StopWordss()

    # Contoh teks untuk diolah
    text = "Ini adalah contoh teks yang akan diproses."

    # Menghapus kata-kata stop
    cleaned_text = sw.remove_stopwordss(text)
    print("Original Text:", text)
    print("Cleaned Text:", cleaned_text)



# import os
# import re

# class StopWordss:
#     def __init__(self, stopword_path=None):
#         self.current_dir = os.path.dirname(os.path.realpath(__file__))
#         if not stopword_path:
#             stopword_path = os.path.join(
#                 self.current_dir, "portofolio_3", "stopword.txt"
#             )
#         with open(stopword_path) as f:
#             self.stopwords = f.read().split('\n')

#     def get_stopword(self):
#         return self.stopwords

#     def remove_stopwordss(self, text):
#         stopword = self.get_stopword()
#         temp_result = []
#         parts = []

#         for match in re.finditer(r'[^.,?!\s]+|[.,?!]', text):
#             parts.append(match.group())

#         for word in parts:
#             if word.casefold() not in stopword:
#                 temp_result.append(word)

#         result_cand = ' '.join(temp_result)
#         result = re.sub(r' ([^A-Za-z0-9])', r'\1', result_cand)

#         return result