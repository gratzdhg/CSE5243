import os
from bs4 import BeautifulSoup
from article import *
import math

class Scanner:
    def __init__(self,path):
        self.rep1 = []
        self.rep2 = []
        self.idf_table = {}
        for filename in os.listdir(path):
            soup = BeautifulSoup(open(path+"/"+filename),"lxml")
            for xml in soup.find_all('reuters'):
                topicList = []
                placesList = []
                for topic in xml.topics.find_all('d'):
                    topicList.append(topic.get_text())
                for place in xml.places.find_all('d'):
                    placesList.append(place.get_text())
                body = xml.find('text').get_text()
                self.rep1.append(Article1(body,topicList,placesList))
                self.rep2.append(Article2(body,topicList,placesList,self.idf_table))
                
        print "Done featurizing articles" ###
        
        self.finish_idf()
        for article in self.rep2:
            word_list = article.get_features()
            for w in word_list:
                article.adjust_tf_idf(w,self.idf_table[w])

    def __str__(self):
        string = ""
        for element in self.rep1:
            string = string + str(element)
        string += '\n'
        for element in self.rep2:
            string += str(element)
        return string+'\n'
        
    def finish_idf(self):
        for word in self.idf_table:
            N = len(self.rep2)
            i = math.log(N/float(self.idf_table[word]))    #this uses natural logarithm, which may or may not be desirable.
            self.idf_table[word] = i

    def printFileXML(self, filename, repList):
        outFile = open(filename, 'w')
        for doc in repList:
            outFile.write("<document>\n\t<topicList>\n")
            for topic in doc.get_topics():
                outFile.write("\t\t<topic>"+str(topic)+"</topic>\n")
            outFile.write("\t</topicList>\n\t<placeList>\n")
            for place in doc.get_places():
                outFile.write("\t\t<place>"+str(place)+"</place>\n")
            outFile.write("\t</placeList>\n\t<featureVector>\n")
            d = doc.get_features()
            for word in d:
                try:
                    outFile.write("\t\t<feature>"+str(word)+" : "+str(d[word])+"</feature>\n")
                except UnicodeEncodeError:
                    print str(word)+" lost"
            outFile.write("\t</featureVector>\n</document>\n")
        outFile.close()

    def printFileXML2(self, filename):
        self.printFileXML(filename, self.rep2)

    def printFileXML1(self, filename):
        self.printFileXML(filename, self.rep1)




