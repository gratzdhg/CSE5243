#!/usr/local/python-2.7.10/bin/python2.7
import scanner

def main():
    path="./reuters"
    filename1="out1.data"
    filename2="out2.data"
    reuters = scanner.Scanner(path)
    reuters.printFileXML1(filename1)
    reuters.printFileXML2(filename2)

main()
