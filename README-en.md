# Sentimen-Analisis-Marketplace-App
[Sentimen Analisis Marketplace App](https://marketplace-sentiment-apps.streamlit.app/)

![images](https://github.com/AryaHisma/Sentimen-Analisis-Shopee-Lazada-Tokopedia-App/blob/main/assets/gambar/screenshoot.png)


This project focuses on **sentiment analysis** of popular e-commerce apps in Indonesia, namely **Shopee**, **Lazada**, and **Tokopedia**. By utilizing **network analysis**, we not only assess overall sentiment but also explore the relationships between words in user reviews. Through network analysis, we can identify the most influential words, the most important connections, and the best connectors within the word network.

## Dataset
The dataset used in this project comes from **scraping user reviews** on the **Google Play Store**. The dataset displays user reviews that have already undergone **preprocessing**, making the review text ready for analysis. The preprocessing steps include:
- **Lowercasing**: Converting all text to lowercase.
- **Removing emojis**: Removing emoji characters from the text.
- **Text cleaning**: Cleaning the text from unwanted characters, such as irrelevant punctuation marks.
- **Slang transformation**: Converting non-standard or slang words into their formal equivalents.
- **Removing stopwords**: Removing common words that are not significant, such as "and", "the", "of".

### Dataset Columns
The dataset consists of several key columns for analysis, including:
- **content**: Contains customer reviews that have been preprocessed.
- **at**: The date and time when the review was submitted by the customer.
- **year**: The year when the review was published.

## Exploratory Data Analysis (EDA)
Before conducting the word network analysis, we performed **Exploratory Data Analysis (EDA)**, which provides a general overview of data distribution, sentiment patterns, and user characteristics based on the year or time of the review. These visualizations help to better understand the dynamics of user reviews.

## Network Analysis
In this analysis, we use a **network analysis** approach to examine the relationships between frequently occurring words in customer reviews. This allows us to observe the word networks that form positive or negative sentiments. Additionally, we highlight several important characteristics within the word network, such as:
- **Most Influential Words**: Words that appear most frequently and influence the overall sentiment.
- **Most Important Connections**: The most relevant and impactful word connections in the network.
- **Best Connectors**: Words that act as key connectors between other words or clusters of words in the reviews.

## Libraries Used
Below are the key libraries used in this project:
1. **Streamlit**: Used to build an interactive web app, allowing users to view the analysis results in real-time.
2. **Pillow**: For image manipulation, such as resizing and editing images within the web app.
3. **Pandas & Numpy**: Essential libraries for data manipulation and numerical computation in tabular data.
4. **NLTK (Natural Language Toolkit)**: Used for text processing, such as tokenization, stemming, and stopword filtering.
5. **Matplotlib, Plotly, Seaborn & Wordcloud**: Libraries for data visualization, including creating both static and interactive charts.
6. **NLP-ID & Sastrawi**: Specifically used for processing Indonesian text, including stemming and tokenization.
7. **NetworkX**: For creating and analyzing word networks that connect important words in user reviews.

With this combination of analysis techniques, this project not only provides basic sentiment analysis results but also delves deeper into the relationship patterns between words that drive user sentiment toward e-commerce apps in Indonesia.


![images](https://github.com/AryaHisma/Sentimen-Analisis-Shopee-Lazada-Tokopedia-App/blob/main/assets/gambar/alur.jpg)



