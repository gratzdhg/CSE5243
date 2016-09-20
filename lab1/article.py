import re
import nltk
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

class Article1:
	def __init__(self, body, topics, places):
		self.topics = topics
		self.places = places
		temp_words = re.split(' ', body)
		self.words = self.featurize(temp_words)
		
	def featurize(self, word_list):
		d = {}
		for w in word_list:
			if w in d.keys():
				d[w] += 1
			else:
				d[w] = 1
		return d
		
	def get_features(self):
		return self.words
		
	def get_topics(self):
		return self.topics
		
	def get_places(self):
		return self.places
		
		
class Article2:
	def __init__(self, body, topics, places):
		self.topics = topics
		self.places = places
		temp_words = nltk.word_tokenize(body)
		self.words = self.featurize(temp_words)
		
	def featurize(self, word_list):
		d = {}
		for w in word_list:
			w1 = wnl.lemmatize(w)
			if w1 in d.keys():
				d[w1] += 1
			else:
				d[w1] = 1
		return d
		
	def get_features(self):
		return self.words
		
	def get_topics(self):
		return self.topics
		
	def get_places(self):
		return self.places
