"""
Take each text document, and create a dictionary of the document structure by identifying
headers and their respective content
"""
import os
import string
from functools import reduce
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import re


def replace(file_path):
    # Create temp file
    bad_Sents = []
    fh, abs_path = mkstemp()
    with fdopen(fh, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                line = str(line)
                regex = re.compile("[☒_☐@#^&*<>?/\|}{~:]")
                if (regex.search(line)) and len(line) > 150:
                    new_file.write(line)
                elif regex.search(line) is None:
                    new_file.write(line)
                else:
                    bad_Sents.append(line)
    # Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    # Remove original file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)

    return None



def ilen(iterable):
    return reduce(lambda sum, element: sum + 1, iterable, 0)


def separate_document(directory):
    """
    :param directory: directory containing the text files
    :return:nested dict
    """

    full_dict = {}
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                name_path = os.path.join(subdir, filename)
                filename_list = filename.rsplit('_')
                # print(filename_list)
                file_key = filename_list[0] + "_" + filename_list[1] + "_" + filename_list[3]
                with open(name_path) as f:
                    my_list = f.readlines()
                    list2 = list(filter(('\n').__ne__, my_list))
                    my_list = list2
                    headers = []
                    content = []
                    doc_structure = {}
                    # check percent of capital letters in a sentence, if most are capitalized, it is a header
                    for x in my_list:
                        # throw out all "\n" characters from the list, and find all content sections
                        capitals = sum(map(str.isupper, x))
                        str_len = len(x.split())
                        capital_factor = capitals/str_len
                        if 15 <= len(x) <= 100 and (capital_factor > 0.5) and \
                                 (any(char.isdigit() for char in x)) == False:# using length does not solve for all cases effectively
                            headers.append(x)
                        elif len(x) > 100:
                            content.append(x)
                        else:
                            continue
                    # Determine the position of the content relative to the header and map to dictionary
                    for x in my_list:
                        for y in headers:
                            if y in my_list and (my_list.index(y) != my_list.index(my_list[-1])):
                                header_idx = my_list.index(y)
                                content_idx = header_idx + 1
                                doc_structure[y] = my_list[content_idx]
                            elif y in my_list and (my_list.index(y) == my_list[-1]):
                                pass
                    full_dict[file_key] = doc_structure
                    f.close()
    return full_dict

# x = separate_document('/Users/kunal/Desktop/test')
# print(x)

replace('/Users/kunal/Desktop/test/AAPL_0000320193_10Q_20171230_AllItems_excerpt.txt')