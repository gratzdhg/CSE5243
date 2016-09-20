#!/usr/local/python-2.7.10/bin/python2.7
import scanner

def main():
    path="./reuters"
    reuters = scanner.Scanner(path)
    print str(reuters)

main()
