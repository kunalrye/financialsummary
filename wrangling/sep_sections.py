"""
Take each text document, and create a dictionary of the document structure by identifying
headers and their respective content
"""
import os
from functools import reduce
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import re


def ilen(iterable):
    return reduce(lambda n_sum, element: n_sum + 1, iterable, 0)


def nested_dict_to_txt(nested_dict, directory):
    """
    Convert the nested dictionary from sep_sections to txt files for each key
    :param nested_dict: nested output from separate_document function
    :param directory: path for directory to save new files to
    :return: .txt files for every key value pair in the dictionary
    """
    for key1, val1 in nested_dict.items():
        file_start = key1
        for key2, val2 in val1.items():
            # write each key2, val2 pair to a new .txt file
            full_file = directory + file_start + key2
            with open(full_file, 'w') as f:
                f.write(val2)
                f.close()


def replace(directory):
    """
    Parse all the files and clean any remaining symbols and small phrases out
    :param directory: filepath for files
    :return: None
    """
    # Create temp file
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(subdir, filename)
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
            # Copy the file permissions from the old file to the new file
            copymode(file_path, abs_path)
            # Remove original file
            remove(file_path)
            # Move new file
            move(abs_path, file_path)

    return None


def separate_document(directory):
    """
    separates document by any header in the file
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
                        if 15 <= len(x) <= 100 and (capital_factor > 0.5):
                            # using length does not solve for all cases effectively
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


def item_one(new_path, file_key, data):
    """
    gets item 1 given readlines data and saves to a new file
    :param readlines_data: lines of a txt file using the readlines function
    :return: None
    """
    parsing = False
    outF = open(new_path + file_key + "_item1.txt", "w")
    for line in data:
        if line.startswith("Item 1. F") or line.startswith("Item 1.F"):
            parsing = True
        elif line.startswith("Item 2.M") or line.startswith("Item 2. M"):
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()


def item_two(new_path, file_key, data):
    """
    gets item 1 given readlines data and saves to a new file
    :param readlines_data: lines of a txt file using the readlines function
    :return: None
    """
    parsing = False
    outF = open(new_path + file_key + "_item2.txt", "w")
    for line in data:
        if line.startswith("Item 2.M") or line.startswith("Item 2. M"):
            parsing = True
        elif line.startswith("Item 3.Q") or line.startswith("Item 3. Q"):
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()

def item_three(new_path, file_key, data):
    """
    gets item 1 given readlines data and saves to a new file
    :param readlines_data: lines of a txt file using the readlines function
    :return: None
    """
    parsing = False
    outF = open(new_path + file_key + "_item3.txt", "w")
    for line in data:
        if line.startswith("Item 3.Q") or line.startswith("Item 3. Q"):
            parsing = True
        elif line.startswith("Item 4.C") or line.startswith("Item 4. C"):
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()


def separate_item(directory):
    """
    separates document by items from the file, and saves file with ending filename being the item number
    :param directory: directory containing the text files
    :return:None
    """

    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                name_path = os.path.join(subdir, filename)
                new_path = str(os.path.join(subdir))
                filename_list = filename.rsplit('_')
                file_key = str(filename_list[0] + "_" + filename_list[1] + "_" + filename_list[3])
                data = open(name_path).readlines()
                item_one(new_path, file_key, data)
                item_two(new_path, file_key, data)
                item_three(new_path, file_key, data)
    return None









#######################################################################################################################
# replace('/Users/kunal/Desktop/test')
# x = separate_document('/Users/kunal/Desktop/test')
# nested_dict_to_txt(x,"/Users/kunal/Desktop/")
separate_item('/Users/kunal/Desktop/test')