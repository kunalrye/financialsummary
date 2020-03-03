"""
Take each text document, and create a dictionary of the document structure by identifying
headers and their respective content
"""
import re
from collections import defaultdict

## NOT DONE YET!

def structure_txt(files):
    """
    :param files: list of files that need to be structured
    :return: nested dict with filename as key; then key,value pairing is subheading and content
    """
    for file in files:

        f = ("/Users/kunal/Dropbox/batch_0005/001/AAPL_0000320193_10Q_20171230_Item2_excerpt.txt")

        with open("/Users/kunal/Dropbox/batch_0005/001/AAPL_0000320193_10Q_20171230_Item2_excerpt.txt") as f:
            my_list = f.readlines()
            # remove all '\n' characters from the list
            list2 = list(filter(('\n').__ne__, my_list))
            my_list = list2
            headers = []
            content = []
            doc_structure = {}
            # figure out what is a header and what is not
            for x in my_list:
                # print(x)
                if 15 <= len(x) <= 100:
                    headers.append(x)
                elif len(x) > 100:
                    content.append(x)
                else:
                    continue
            # iterate through list and create dictionary of the file
            for x in my_list:
                for y in headers:
                    if y in my_list and (my_list.index(y) != my_list.index(my_list[-1])):
                        header_idx = my_list.index(y)
                        content_idx = header_idx + 1
                        doc_structure[y] = my_list[content_idx]
                    elif y in my_list and (my_list.index(y) == my_list[-1]):
                        break
            print(doc_structure)