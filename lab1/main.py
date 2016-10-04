#!/usr/local/python-2.7.10/bin/python2.7
import scanner

def main():
    path="/home/0/srini/WWW/674/public/reuters/"
    filename1="out1.xml"
    filename2="out2.xml"
    reuters = scanner.Scanner(path,filename1,filename2)
    print str(reuters)
#    reuters.printFileXML1(filename1)
#    reuters.printFileXML2(filename2)

main()
