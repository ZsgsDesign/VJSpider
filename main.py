# -*- coding:utf-8 -*-

"""
    Project: VJSpider
    Version: 20181207
    Compatible: CodeMaster / VJCore
    Author: John Zhang
"""

import os
import sys
import getopt
import requests
from bs4 import BeautifulSoup

ojs=[]

def traverse(f):
    global ojs
    fs = os.listdir(f)
    for f1 in fs:
        tmp_path = os.path.join(f,f1)
        if os.path.isdir(tmp_path):
            print("- " + f1)
            ojs.append(f1)

def main(argv):
    global ojs
    print("Welcome to VJSpider----------")
    print("----- available online judeges -----")
    print()
    traverse("oj/")
    print()
    print("------------------------------------")
    print()
    OJ = input("OJ: ")
    if not OJ in ojs:
        print("\nfailed")
        return
    Prob = input("Problem: ")
    try:
        ret=os.system("python OJ/" + OJ + "/" + OJ + ".py -p "+Prob)
    except:
        ret=-1
    if ret==0:
        print("successful")
    else:
        print("failed")


if __name__ == '__main__':
    main(sys.argv[1:])
