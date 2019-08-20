import bs4 as bs
#import urllib
import urllib.request
import re
import nltk
import heapq
import time
#from urllib import request, parse  # this is the library you need

def find_text(urlstr):
    scraped_data = urllib.request.urlopen(urlstr)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article,'lxml')

    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text

    return article_text

def create_summary(article_text, numsentence):
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    article_text = re.sub(r'\s+', ' ', article_text)

    # Removing special characters and digits
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

    sentence_list = nltk.sent_tokenize(article_text)

    stopwords = nltk.corpus.stopwords.words('english')

    word_frequencies = {}
    for word in nltk.word_tokenize(formatted_article_text):
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)

    sentence_scores = {}
    for sent in sentence_list:
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_frequencies.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]


    summary_sentences = heapq.nlargest(numsentence, sentence_scores, key=sentence_scores.get)

    summary = ' '.join(summary_sentences)
    return summary

def post_to_vr(url, data):
    data = data.encode() #turn to bytes
    req = urllib.request.Request(url, data=data) #send request
    response = urllib.request.urlopen(req) #receive response
    return response.read()

if __name__ == '__main__':
    url = 'http://dm0007.dreamlandmetaverse.com:9252/lslhttp/197fe91b-1311-487d-bca9-aa453699ddce/'
    article_url1 = 'https://en.wikipedia.org/wiki/Artificial_intelligence'
    article_url2 = 'https://www.sciencedirect.com/science/article/pii/S0957417419305226'


    text = find_text(article_url2)

    summary = create_summary(text, 4)


    print(summary)
    #feedback = post_to_vr(url, summary)
    #print(feedback)
