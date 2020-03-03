'''
Library for querying the SEC Filings API and for obtaining the 10q links. 
'''

import json
import urllib.request
from urllib.parse import urlparse


def query_api(cik, date_from, date_to):
    """
    Queries the SEC-Filings API for a specific company's 10Qs
    :param cik: cik idnetifier of the company
    :param date_from: start date
    :param date_to: end date
    :return: a json oject containig the links to the 10Qs of the company in the date range
    """
    # API Key
    TOKEN = "f172ab24e14a02bd5d673b407b6c02ce4a66671c893abebc26d21fc271924c01"  # replace YOUR_API_KEY with the API key you got from sec-api.io after sign up
    # API endpoint
    API = "https://api.sec-api.io?token=" + TOKEN

    payload = {
        "query": {"query_string": {
            "query": "cik:" + str(cik) + " AND filedAt:{" + date_from + " TO " + date_to + "} AND formType:\"10-Q\""}},
        "from": "0",
        "size": "10",
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    # format your payload to JSON bytes
    jsondata = json.dumps(payload)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes

    # instantiate the request 
    req = urllib.request.Request(API)

    # set the correct HTTP header: Content-Type = application/json
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    # set the correct length of your request
    req.add_header('Content-Length', len(jsondataasbytes))

    # send the request to the API
    response = urllib.request.urlopen(req, jsondataasbytes)

    # read the response 
    res_body = response.read()
    # transform the response into JSON
    filings = json.loads(res_body.decode("utf-8"))
    return filings


def get_10qs(filings):
    """
    Gets the actual html links from the json object returned by query_api()
    :param filings: json object returned from query_api()
    :return: list of direct html links to the 10Qs
    """
    num_filings = int(filings['total']['value'])
    print("FOUND " + str(num_filings) + "10Q REPORTS: ")

    links = []

    for i in range(num_filings):
        print("HTML link is " + filings['filings'][i]['linkToHtml'])
        print("Text link is " + filings['filings'][i]['linkToTxt'])
        htmllink = filings['filings'][i]['linkToHtml']
        txtlink = filings['filings'][i]['linkToTxt']

        data = urllib.request.urlopen(txtlink).read(2000).decode("utf-8")
        data = data.split("\n")
        # lines = data.split("\n") # then split it into lines
        fname = ""
        print("Parsing txt file for 10Q filename")
        for line in data:
            if "<FILENAME>" in line:
                fname = line[10:]
                print("filename found: " + fname)
                break

        orig_url = urlparse(htmllink)
        split_path = orig_url.path.split('/')

        accession_num_contents = split_path[-1].split("-")
        acc_num = ''.join(accession_num_contents[:3])  ##obtains the accession number

        final_path = split_path[:-1]
        final_path.append(acc_num + '/' + fname)
        final_path = '/'.join(final_path)

        new_url = orig_url._replace(path=final_path)
        new_url = new_url.geturl()
        links.append(new_url)
        print("forming direct url....")
        print(new_url)
        print('\n')

    return links
