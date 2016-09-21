from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()

def try_increment(dictionary, key):
	key = key.encode('ascii','ignore')
	value = True
	if key in dictionary:
		dictionary[key] += 1
	else:
		dictionary[key] = 1
		value = False
	return value

class Article1:
	def __init__(self, body, topics, places):
		self.topics = topics
		self.places = places
		temp_words = word_tokenize(body)
		self.words = self.featurize(temp_words)

	def __str__(self):
		string = "topics: "+str(self.topics)+" places: "+str(self.places)+" words "+str(self.words)
		string += "\n"
		return string
		
	def featurize(self, word_list):
		d = {}
		for w in word_list:
			try_increment(d,w)
		return d
		
	def contains_word(self, w):
		return w in self.words
		
	def get_features(self):
		return self.words
		
	def get_topics(self):
		return self.topics
		
	def get_places(self):
		return self.places
		
		
class Article2:
	def __init__(self, body, topics, places, idf_dict):
		self.topics = topics
		self.places = places
		temp_words = word_tokenize(body)
		self.words = self.featurize(temp_words, idf_dict)
		
	def contains_word(self, w):
		return w in self.words

 	def __str__(self):
 		string = "topics: "+str(self.topics)+" places: "+str(self.places)+" words "+str(self.words)
		string += "\n"
		return string
		
	def featurize(self, word_list, idf_dict):
		d = {}
		for w in word_list:
			w_stem = wnl.lemmatize(w)
			if not try_increment(d,w_stem):
			 	try_increment(idf_dict, w_stem)
		return d
		
	def adjust_tf_idf(self, word, idf):
		if self.contains_word(word):
			self.words[word] = float(self.words[word]) * float(idf)
		
	def get_features(self):
		return self.words
		
	def get_topics(self):
		return self.topics
		
	def get_places(self):
		return self.places
