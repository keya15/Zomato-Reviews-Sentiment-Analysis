from flask import Flask, request, render_template
import json
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import math
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
from nltk.corpus import stopwords
import nltk

vds = SentimentIntensityAnalyzer()

app = Flask(__name__)
f = open('reviews.json')
file = json.loads(f.read())


    
@app.route('/' , methods = ["GET" , "POST"])
def home():
     display = "none"
     return render_template('index.html' , display = display)

         
@app.route('/p' ,  methods = ["GET" , "POST"])
def home2():
    display = "flex"
    res_name = request.form['sec']
    res = [d.get(res_name, None) for d in file]
    flat_list = []
    for element in res:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    list_reviews = [x for x in flat_list if x is not None]
    # Using regular expression to match emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
    list_reviews = [emoji_pattern.sub(r'', text) for text in list_reviews]

    nltk.download('stopwords')
    # get the list of stopwords
    stop_words = set(stopwords.words('english'))
    # remove stopwords from the list of sentences
    filtered_list = []
    for sentence in list_reviews:
        filtered_sentence = []
        for word in sentence.split():
            if word.lower() not in stop_words:
                filtered_sentence.append(word)
        filtered_list.append(' '.join(filtered_sentence))


    

    df = pd.DataFrame(filtered_list)
    df.rename(columns={0:'reviews'}, inplace=True)
    def label(text):
        score = vds.polarity_scores(text)
        coumpound_score = score['compound']
        if coumpound_score >= 0.05:
            return 'Positive'
        elif coumpound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'
    df['label'] = df['reviews'].apply(lambda x: label(x))
    label_counts = df['label'].value_counts()
    lst_of_count = [label_counts['Positive'], label_counts['Negative'], label_counts['Neutral']]
    plt.pie(lst_of_count, labels=['Positive', 'Negative', 'Neutral'], autopct='%1.1f%%', shadow=True, startangle=140)
    filename = f'{res_name}_1.png'
    filepath = 'static/images/' + filename
    plt.savefig(filepath)

    # get positive reviews
    positive_reviews = df[df['label'] == 'Positive']['reviews'].values
    # join all positive reviews into a single string
    positive_reviews_text = " ".join(positive_reviews)
    # split the text into words
    words = positive_reviews_text.split()
    # count the frequency of each word
    word_frequencies = {}
    for word in words:
        if word in word_frequencies:
            word_frequencies[word] += 1
        else:
            word_frequencies[word] = 1
    # sort the words by frequency in descending order
    sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    # get the top 20 frequent words
    top_words = dict(sorted_word_frequencies[:20])
    # generate word cloud
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white').generate_from_frequencies(top_words)
    # plot the word cloud
    plt.figure(figsize = (2,2), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    filename = f'{res_name}_2.png'
    filepath = 'static/images/' + filename
    plt.savefig(filepath)

    # get positive reviews
    positive_reviews = df[df['label'] == 'Negative']['reviews'].values
    # join all positive reviews into a single string
    positive_reviews_text = " ".join(positive_reviews)
    # split the text into words
    words = positive_reviews_text.split()
    # count the frequency of each word
    word_frequencies = {}
    for word in words:
        if word in word_frequencies:
            word_frequencies[word] += 1
        else:
            word_frequencies[word] = 1
    # sort the words by frequency in descending order
    sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    # get the top 20 frequent words
    top_words = dict(sorted_word_frequencies[:20])
    # generate word cloud
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white').generate_from_frequencies(top_words)
    # plot the word cloud
    plt.figure(figsize = (2,2), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    filename = f'{res_name}_3.png'
    filepath = 'static/images/' + filename
    plt.savefig(filepath)

    # get positive reviews
    positive_reviews = df[df['label'] == 'Neutral']['reviews'].values
    # join all positive reviews into a single string
    positive_reviews_text = " ".join(positive_reviews)
    # split the text into words
    words = positive_reviews_text.split()
    # count the frequency of each word
    word_frequencies = {}
    for word in words:
        if word in word_frequencies:
            word_frequencies[word] += 1
        else:
            word_frequencies[word] = 1
    # sort the words by frequency in descending order
    sorted_word_frequencies = sorted(word_frequencies.items(), key=lambda x: x[1], reverse=True)
    # get the top 20 frequent words
    top_words = dict(sorted_word_frequencies[:20])
    # generate word cloud
    wordcloud = WordCloud(width = 800, height = 800, background_color ='white').generate_from_frequencies(top_words)
    # plot the word cloud
    plt.figure(figsize = (2,2), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    filename = f'{res_name}_4.png'
    filepath = 'static/images/' + filename
    plt.savefig(filepath)

    fig=plt.figure()
    plt.rcParams['figure.facecolor'] = 'white'
    label=['Negative', 'Neutral', 'Positive']
    # The numbers are the portion of area
    val=[34,    #100-66  
        33,    #66-33
        33]    # 33-0
    label.append('')
    val.append(100)
    def half_donut(dr): # dr is an integer but means a % rate
        colors=['#FF0000', '#FFC000', '#FFFF00'] # Colors for each group
        wedges, labels=plt.pie(val, labels=label, colors=colors, wedgeprops=dict(width=0.4, edgecolor='w'))
        angle=math.radians(180 * dr / 100) # The angle of the arrow pointing at, in radian unit
        plt.annotate(f'{dr}%',  
                    xy=(math.cos(angle) * -1, math.sin(angle)),       # Arrow sharp position
                    xytext = (-0.2, 0),                                # Metric number position
                    arrowprops=dict(facecolor='black', shrink=0.05),   # Arrow style
                    fontsize=15
                    )
        wedges[-1].set_visible(False)
        filename = f'{res_name}_5.png'
        filepath = 'static/images/' + filename
        plt.savefig(filepath)
    sentiment_scores = []
    for review in df['reviews']:
        score = vds.polarity_scores(review)['compound']
        sentiment_scores.append(score)
    # add sentiment scores to DataFrame
    df['sentiment_score'] = sentiment_scores
    # calculate average sentiment score and multiply by 100
    avg_sentiment_score = df['sentiment_score'].mean() * 100
    half_donut(int(avg_sentiment_score))

    # Sample data
    review_labels = df['label']
    # Define a list of colors for each label
    label_colors = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'yellow'}
    # Get the unique labels and their counts
    unique_labels, label_counts = np.unique(review_labels, return_counts=True)
    # Set up the bar chart
    fig, ax = plt.subplots()
    ax.bar(unique_labels, label_counts, color=[label_colors[label] for label in unique_labels])
    ax.set_xlabel('Labels')
    ax.set_ylabel('Count')
    filename = f'{res_name}_6.png'
    filepath = 'static/images/' + filename
    plt.savefig(filepath)

    return render_template('index.html' , display = display,sen_score=avg_sentiment_score, filename1=f'{res_name}_1.png', filename2=f'{res_name}_2.png',filename3=f'{res_name}_3.png',filename4=f'{res_name}_4.png',filename5=f'{res_name}_5.png',filename6=f'{res_name}_6.png')

if __name__ == '__main__':
    app.run(debug=True)
