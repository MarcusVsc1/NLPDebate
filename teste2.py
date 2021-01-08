import spacy
from spacy.tokens import Doc
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import pt_core_news_sm

spacy.prefer_gpu()