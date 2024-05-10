import streamlit as st
import pickle
from nltk.stem.porter import PorterStemmer
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
import string
import requests 

ps = PorterStemmer()


def transfrom_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)
    text = y[:]
    y.clear()
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()
    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


tfidf = pickle.load((open('vectorizer.pkl', 'rb')))
model = pickle.load(open('model.pkl', 'rb'))
preprocessor = pickle.load(open('preprocess.pkl', 'rb'))

st.title("JUNKEMAIL")
input_mail = st.text_input("Enter this message")


if st.button('Predict'):
    # 1. preprocess
    transformed_mail = transfrom_text(input_mail)
    # 2. vectorizer
    vector_input = tfidf.transform([transformed_mail])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. display
    if result == 1:
        st.header("SPAM")
    else:
        st.header("NOT SPAM")
