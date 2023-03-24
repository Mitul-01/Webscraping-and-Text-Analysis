import pandas as pd  #data maniplulation
import requests  #for sending HTTP requests
from bs4 import BeautifulSoup #for web scraping
import nltk #for natural language processing
import re #for string manipulation.
from nltk.sentiment.vader import SentimentIntensityAnalyzer  #for sentiment analysis
from nltk.tokenize import word_tokenize  #for tokenize
from nltk.corpus import stopwords     #for all stopwords         
from nltk.tokenize import RegexpTokenizer #tokenize a string or text based on a regular expression 
from nltk.stem import WordNetLemmatizer   #for lemmatize a word
from textblob import TextBlob #for processing textual data
import warnings 
warnings.filterwarnings('ignore')


def getdetails(url):
    page = requests.get(url, headers={"User-Agent": "XY"})
    soup = BeautifulSoup(page.content, "html.parser")
    article_text = soup.find('div', class_='td-post-content').get_text()
    #create a tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    #tokenize the text
    tokens = tokenizer.tokenize(article_text)
    #read in txt file containing stopwords
    stopwords_file = open("All_stopwords.txt", "r") #All_stopwords is a text file which made by me which have all the 5 stopwords provided from company
    #create a set of stopwords
    All_stopwords = set()
    #loop through the text file
    for line in stopwords_file:
        line = line.replace("\n", "")
        All_stopwords.add(line)
    #remove stopwords
    filtered_tokens = [w for w in tokens if not w in All_stopwords]
    #create a lemmatizer
    lemmatizer = WordNetLemmatizer()
    #lemmatize the tokens
    lemmatized_tokens = [lemmatizer.lemmatize(w) for w in filtered_tokens] 
    #calculate word count
    word_count = len(lemmatized_tokens)
    #calculate avg word length
    avg_word_length = 0
    for i in lemmatized_tokens:
        avg_word_length += len(i)
    avg_word_length = avg_word_length/word_count
    #calculate syllable count per word
    syllable_count_per_word = 0
    for i in lemmatized_tokens:
        syllable_count_per_word += len(i.split('-'))
    syllable_count_per_word = syllable_count_per_word/word_count
    #calculate personal pronouns
    personal_pronouns = 0
    for w in lemmatized_tokens:
        if w in ["I", "me", "you", "he", "him", "she", "her", "it", "we", "us", "they", "them"]:
            personal_pronouns += 1
    #create a function to calculate the positive and negative scores
    sid = SentimentIntensityAnalyzer()
    polarity_score = sid.polarity_scores(article_text)
    #calculate positive and negative score
    positive_score = polarity_score['pos']
    negative_score = polarity_score['neg']
    #sentiment analysis such as polarity and subjectivity
    text = TextBlob(article_text)
    polarity = text.sentiment.polarity
    subjective = text.sentiment.subjectivity
    #calculate complex word count
    complex_words = 0
    for w in lemmatized_tokens:
        syllable_count = len(w.split('-'))
        if syllable_count > 2:
            complex_words += 1
    #calculate average sentence length
    sentences = article_text.split('.')
    avg_sentence_length = 0
    for s in sentences:
        avg_sentence_length += len(s.split())
    avg_sentence_length = avg_sentence_length/len(sentences)
    #calculate the Gunning Fog Index
    fog_index = 0.4 * (avg_sentence_length +(100 * complex_words/word_count))
    #complex word percentage
    complex_words_percentage = (complex_words/word_count)*100
    #calculate the average number of words per sentence
    avg_words_per_sentence = word_count/len(sentences)
    
    return[positive_score,negative_score,polarity,subjective,avg_sentence_length,complex_words_percentage,fog_index,avg_words_per_sentence,complex_words,
            word_count, syllable_count_per_word, personal_pronouns, avg_word_length]

#reading excel files cotaining all the links 
output = pd.read_excel("Output Data Structure.xlsx")

#putting all the scores or values in front of the url links 
for i in output.index:
    try:
        result = getdetails(output["URL"][i])
        if len(result)==13:
            for jdx,j in enumerate(output.columns[2:]):
                output[j][i]=result[jdx]
    except Exception as e:
        print(e)
        pass

#converting output file to excel
output.to_excel('final Output.xlsx', index=False)
    
