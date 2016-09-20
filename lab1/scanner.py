import os
from bs4 import BeautifulSoup
from article import *

class scanner:
    def __init__(self,path):
        self.rep1 = []
        self.rep2 = []
        for filename in os.listdir(path):
            soup = BeautifulSoup(open(path+"/"+filename),"lxml")
            for text in soup.find_all('reuters'):
                self.rep1.append(Article1(str(text.body),text.topics.find_all('d'),text.places.find_all('d')))
                self.rep2.append(Article2(str(text.body),text.topics.find_all('d'),text.places.find_all('d')))
 
