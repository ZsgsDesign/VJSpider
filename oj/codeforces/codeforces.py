# -*- coding:utf-8 -*-

"""
    OJ: CodeForces
    Version: 20190214
    Compatible: CodeMaster / VJCore
    Author: John Zhang
"""

import os
from os import path
import sys
import getopt
import requests
from bs4 import BeautifulSoup
import pymysql

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
    text.replace("\n","\n\n")
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
    AllInfo = soup.find('div', {'class', 'problemindexholder'})
    divs = AllInfo.find_all('div')

    problem_title = (divs[3].get_text())[3:]

    problem_description = divs[12].get_text()
    problem_description = Clear(problem_description)

    problem_input = divs[13].get_text()[5:]
    problem_input = Clear(problem_input)

    problem_output = divs[15].get_text()[6:]
    problem_output = Clear(problem_output)

    Sample = soup.find('div', {'class', 'sample-test'})
    problem_sample_inputs = Sample.find_all('div', {'class', 'input'})
    problem_sample_outputs = Sample.find_all('div', {'class', 'output'})

    pid = recordProblem('CF' + Prob, problem_title,
                        problem_description, problem_input, problem_output, url, 2)

    for i in range(len(problem_sample_inputs)):
        problem_sample_input = problem_sample_inputs[i].get_text()[5:]
        problem_sample_output = problem_sample_outputs[i].get_text()[6:]
        recordSample(pid, problem_sample_input, problem_sample_output)


def recordProblem(pcode, problem_title, problem_description, problem_input, problem_output, origin, OJ):
    db = pymysql.connect("localhost", "root", "root", "codemaster")
    cursor = db.cursor()
    sql = "INSERT INTO problem set `pcode`=%s, `title`=%s, `description`=%s, `input`=%s, `output`=%s, `type`=0,`hint`='', `origin`=%s, `OJ`=%s"
    cursor.execute(sql, (pcode, problem_title, problem_description,
                         problem_input, problem_output, origin, OJ))
    pid = int(cursor.lastrowid)
    db.close()
    return pid


def recordSample(pid, sample_input, sample_output):
    db = pymysql.connect("localhost", "root", "root", "codemaster")
    cursor = db.cursor()
    sql = "INSERT INTO problem_sample set `pid`=%s, `sample_input`=%s, `sample_output`=%s"
    cursor.execute(sql, (pid, sample_input, sample_output))
    db.close()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hp:", ["problem"])
    except getopt.GetoptError:
        print("python codeforces.py -p <prob_id>")
        return
    for opt, arg in opts:
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
