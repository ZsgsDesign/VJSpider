# -*- coding:utf-8 -*-

"""
    OJ: CodeForces
    Version: 20181207
    Compatible: CodeMaster / VJCore
    Author: John Zhang
"""

import os
from os import path
import sys
import getopt
import requests
from bs4 import BeautifulSoup

Latextag = 0


def GetHtmlText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'utf-8'
        return r.text
    except:
        return ""


def Clear(text):
    flag = True
    while flag:
        flag = False
        try:
            index = text.index('$$$')
            if Latextag == 0:
                pass
            elif Latextag == 1:
                text = text[:index] + text[index + 1:]
            elif Latextag == 2:
                text = text[:index] + text[index + 2:]
            flag = True
        except:
            break
    return text


def FindInfo(Prob, soup, url):
    f = open(path.dirname(path.realpath(__file__))+'/tmp/' + Prob + '.md', 'w', encoding='utf-8')
    AllInfo = soup.find('div', {'class', 'problemindexholder'})
    divs = AllInfo.find_all('div')
    title = '# ' + (divs[3].get_text())[3:]
    f.write('%s\n' % title)
    problem = '## Description:\n' + divs[12].get_text()
    problem = Clear(problem)
    f.write('%s\n' % problem)
    Input = '## Input:\n' + divs[13].get_text()[5:]
    Input = Clear(Input)
    f.write('%s\n' % Input)
    Output = '## Output\n' + divs[15].get_text()[6:]
    Output = Clear(Output)
    f.write('%s\n' % Output)
    Sample = soup.find('div', {'class', 'sample-test'})
    SampleInputs = Sample.find_all('div', {'class', 'input'})
    SampleOutputs = Sample.find_all('div', {'class', 'output'})
    for i in range(len(SampleInputs)):
        SampleInput = SampleInputs[i].get_text()
        SampleOutput = SampleOutputs[i].get_text()
        f.write('## Sample Input:\n```\n%s```\n' % SampleInput[5:])
        f.write('## Sample Output:\n```\n%s```\n' % SampleOutput[6:])
    f.write('### [Origin](%s)\n\n' % url)
    f.close()


def main(argv):
    try:
        opts,args = getopt.getopt(argv,"hp:",["problem"])
    except getopt.GetoptError:
        print("python codeforces.py -p <prob_id>")
        return
    for opt,arg in opts:
        if opt == "-h":
            print("python codeforces.py -p <prob_id>")
            sys.exit(2)
        elif opt in ("-p", "-problem"):
            print()
            crawler(arg)
        else:
            print("python codeforces.py -p <prob_id>")

def crawler(Prob):
    global Latextag
    Prob_contest = Prob[:-1]
    Prob_id = Prob[-1:]

    Latextag = 1

    # 0:'$$$'
    # 1:'$$'
    # 2:'$'

    url = 'http://codeforces.com/contest/' + Prob_contest + '/problem/' + Prob_id
    # print(url)
    html = GetHtmlText(url).replace('<br />', '\n').replace('</p>', '\n')
    soup = BeautifulSoup(html, "html.parser")
    FindInfo(Prob, soup, url)

if __name__ == '__main__':
    main(sys.argv[1:])
