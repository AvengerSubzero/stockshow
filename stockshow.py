#!/usr/bin/env python#
#Script to grab stock data and display
from __future__ import print_function
import json
import requests
import prettytable
import os.path
import sys
import argparse
import pdb

def getCompanyList(args):
    if args.file is not None:
        if os.path.exists(args.file):
            with open(args.file) as f:
                content = f.readlines()
            content = [company.strip() for company in content]
            return content
        else:
            #return example list
            return ['NFLX', 'NVDA']
    elif args.list is not None:
        return args.list

def parseArgs():
    parser=argparse.ArgumentParser(
            description='''Script to print stock data using google finance''',
            epilog="""Happy Trading"""
    )
    parser.add_argument('-f', '--file', type=str, help='provide filename with list of stock symbols')
    parser.add_argument('-l', '--list', nargs='+', help='provide list of stock symbols on the terminal')
    return parser.parse_args()

def main():
    args = parseArgs()

    company_list = getCompanyList(args)

    if company_list:
        tbl = prettytable.PrettyTable(["Company", "Last Price", "Opening", "Change"])
    #iterate through list and get stock data
    for company in company_list:
        request = 'https://finance.google.com/finance?q='+company+'&output=json'
        rsp = requests.get(request)

        if rsp.status_code in (200,0):
            if "iid" in rsp.content:
                fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
                tbl.add_row([fin_data['name'], fin_data['l'], fin_data['op'], fin_data['c']])
    print(tbl)

main()