#!/usr/bin/python2.6
import os
from bs4 import BeautifulSoup
from article import *

path="/home/8/gratzd/Public/CSE5243/lab1/reuters"

def main(path):
    a1 = []
    a2 = []
    for filename in os.listdir(path):
        soup = BeautifulSoup(open(path+"/"+filename),"lxml")
        for text in soup.find_all('reuters'):
            a1.append(Article1(str(text.body),text.topics.find_all('d'),text.places.find_all('d')))
            a2.append(Article2(str(text.body),text.topics.find_all('d'),text.places.find_all('d')))
    return a2

print main(path)
