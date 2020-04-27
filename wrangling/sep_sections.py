"""
Take each text document and replace the lines with cleaned text (removal of symbols, short lines, etc)
using replace() then separate each document into sections by ITEM using separate_item().
"""
import os
from functools import reduce
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove
import re
from nltk import tokenize
import nltk.data
from nltk.tokenize import sent_tokenize


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


def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))


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
                        nline = str(line.lower())
                        line = str(line)
                        split_text = line.rsplit()
                        regex = re.compile("[☒_☐@#^&*<>?/\|}{~:]")
                        if (len(nline) <= 300) and (nline.startswith(" item") or nline.startswith(" part") or
                                        nline.startswith("item") or nline.startswith("part")):
                            new_file.write(line)
                        elif (regex.search(line)) and len(line) > 10000:
                            continue
                        elif line.startswith("[DATA_TABLE_REMOVED]") or line.endswith("[DATA_TABLE_REMOVED]"):
                            continue
                        elif len(split_text) <= 3 and hasNumbers(line):
                            continue
                        elif line.startswith("("):
                            continue
                        elif "forward-looking" in line or "FORWARD-LOOKING" in line:
                            new_file.write(line)
                        elif regex.search(line) is None:
                            new_file.write(line)
                        else:
                            continue
            # Copy the file permissions from the old file to the new file
            copymode(file_path, abs_path)
            # Remove original file
            remove(file_path)
            # Move new file
            move(abs_path, file_path)

    return None


def separate_document(directory):
    """
    separates document by any header in the file, replaced by separate_item
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
    :param new_path: the new path that the file is being saved to
    :param file_key: the key made for the file so that filename is unique
    :param data: the string data from parsing that is being iterated over in separate_item
    :return: None
    """
    # edge cases are where there is a space before the line starts or there is a space after the item
    # and before the title of that item or without a period after the ITEM 2
    parsing = False
    outF = open(new_path + file_key + "_item1.txt", "w")
    for line in data:
        line2 = line.lower()
        if line2.startswith("item 1. F") or line2.startswith("item 1.F") or line2.startswith("item 1")\
                or line2.startswith(' item 1'):
            parsing = True
        elif line2.startswith("item 2.M") or line2.startswith("item 2. M") or line2.startswith("item 2")\
                or line2.startswith(" item 2"):
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()


def item_two(new_path, file_key, data):
    """
    gets item 2 given readlines data and saves to a new file
    :param new_path: the new path that the file is being saved to
    :param file_key: the key made for the file so that filename is unique
    :param data: the string data from parsing that is being iterated over in separate_item
    :return: None
    """
    parsing = False
    outF = open(new_path + file_key + "_item2.txt", "w")
    for line in data:
        line2 = line.lower()
        if line2.startswith("item 2.M") or line2.startswith("item 2. M") or line2.startswith(" item 2")\
                or line2.startswith("item 2"):
            parsing = True
        elif line2.startswith("item 3.Q") or line2.startswith("item 3. Q") or line2.startswith(" item 3")\
                or line2.startswith("item 3"):
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()


def item_three(new_path, file_key, data):
    """
    gets item 3 given readlines data and saves to a new file
    :param new_path: the new path that the file is being saved to
    :param file_key: the key made for the file so that filename is unique
    :param data: the string data from parsing that is being iterated over in separate_item
    :return: None
    """
    parsing = False
    outF = open(new_path + file_key + "_item3.txt", "w")
    for line in data:
        line2 = line.lower()
        if line2.startswith("item 3.Q") or line2.startswith("item 3. Q") or line2.startswith(" item 3")\
                or line2.startswith("item 3"):
            parsing = True
        elif line2.startswith("item 4.C") or line2.startswith("item 4. C") or line2.startswith(" item 4")\
                or line2.startswith("item 4"):
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()


def item_four(new_path, file_key, data):
    """
    gets item 4 given readlines data and saves to a new file
    :param new_path: the new path that the file is being saved to
    :param file_key: the key made for the file so that filename is unique
    :param data: the string data from parsing that is being iterated over in separate_item
    :return: None
    """
    parsing = False
    outF = open(new_path + file_key + "_item4.txt", "w")
    for line in data:
        line2 = line.lower()
        if line2.startswith("item 4.C") or line2.startswith("item 4. C") or line2.startswith(" item 4")\
                or line2.startswith("item 4"):
            parsing = True
        elif line2.startswith("part II") or line2.startswith("part ii") or line2.startswith(" part ii"):
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()


def part_two(new_path, file_key, data):
    """
    gets part 2 given readlines data and saves to a new file
    :param new_path: the new path that the file is being saved to
    :param file_key: the key made for the file so that filename is unique
    :param data: the string data from parsing that is being iterated over in separate_item
    :return: None
    """
    parsing = False
    outF = open(new_path + file_key + "_part2.txt", "w")
    for line in data:
        line2 = line.lower()
        if line2.startswith("part ii") or line2.startswith("part ii.") or line2.startswith(" part ii"):
            parsing = True
        elif line2.startswith("SIGNATURE"):
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()


def forward_looking(new_path, file_key, data):
    """
    extracts information about forward looking statements to a text file
    :param new_path: the new path that the file is being saved to
    :param file_key: the key made for the file so that filename is unique
    :param data: the string data from parsing that is being iterated over in separate_item
    :return: None
    """
    parsing = False
    outF = open(new_path + file_key + "_fls.txt", "w")
    for line in data:
        line2 = line.lower()
        if "forward-looking" in line2:
            parsing = True
        elif len(line2) <= 150:
            parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()



def specific_item(new_path, file_key, data, item):
    """
    extracts information about forward looking statements to a text file
    :param new_path: the new path that the file is being saved to
    :param file_key: the key made for the file so that filename is unique
    :param data: the string data from parsing that is being iterated over in separate_item
    :param item: number indicating the specific section, items 1->4 are 1 to 4, part 2 is 5 and fls 6
    :return: None
    """
    parsing = False
    file_ending = {1:"_item1.txt", 2: "_item2.txt", 3: "_item3.txt", 4: "_item4.txt", 5: "_part2.txt", 6: "_fls.txt"}

    outF = open(new_path + file_key + file_ending[item], "w")
    for line in data:
        line2 = line.lower()
        if item == 1:
            if line2.startswith("item 1. F") or line2.startswith("item 1.F") or line2.startswith("item 1")\
                or line2.startswith(' item 1'):
                parsing = True
            elif line2.startswith("item 2.M") or line2.startswith("item 2. M") or line2.startswith("item 2")\
                or line2.startswith(" item 2"):
                parsing = False
        if item == 2:
            if line2.startswith("item 2.M") or line2.startswith("item 2. M") or line2.startswith(" item 2")\
                or line2.startswith("item 2"):
                parsing = True
            elif line2.startswith("item 3.Q") or line2.startswith("item 3. Q") or line2.startswith(" item 3")\
                or line2.startswith("item 3"):
                parsing = False
        if item == 3:
            if line2.startswith("item 3.Q") or line2.startswith("item 3. Q") or line2.startswith(" item 3")\
                or line2.startswith("item 3"):
                parsing = True
            elif line2.startswith("item 4.C") or line2.startswith("item 4. C") or line2.startswith(" item 4")\
                or line2.startswith("item 4"):
                parsing = False
        if item == 4:
            if line2.startswith("item 4.C") or line2.startswith("item 4. C") or line2.startswith(" item 4")\
                or line2.startswith("item 4"):
                parsing = True
            elif line2.startswith("part II") or line2.startswith("part ii") or line2.startswith(" part ii"):
                parsing = False
        if item == 5:
            if line2.startswith("part ii") or line2.startswith("part ii.") or line2.startswith(" part ii"):
                parsing = True
            elif line2.startswith("SIGNATURE"):
                parsing = False
        if item == 6:
            if "forward-looking" in line2:
                parsing = True
            elif len(line2) <= 150:
                parsing = False
        if parsing:
            # write line to output file
            outF.write(line)
            outF.write("\n")
    outF.close()


def post_item_tokenize(directory):
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
                with open(file_path, encoding='utf-8', errors='ignore') as old_file:
                    data = old_file.readlines()
                    for line in data:
                        line = sent_tokenize(line)
                        for sentence in line:
                            new_file.write(sentence + '\n')
            # Copy the file permissions from the old file to the new file
            copymode(file_path, abs_path)
            # Remove original file
            remove(file_path)
            # Move new file
            move(abs_path, file_path)

    return None
    

def separate_item(directory, tokenized):
    """
    separates document by items from the file, and saves file with ending filename being the item number
    :param directory: directory containing the text files
    :param tokenized: boolean whether or not you would like the files to be tokenized in the output
    :return: None
    """

    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.txt'):
                name_path = os.path.join(subdir, filename)
                filename_list = filename.rsplit("_")
                company = str(filename_list[0])
                new_path = str("resources" + "/itemized/" + company + "/")
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
                filename_list = filename.rsplit('_')
                file_key = str(filename_list[0] + "_" + filename_list[1] + "_" + filename_list[3])
                data = open(name_path).readlines()
                # item_one(new_path, file_key, data)
                # item_two(new_path, file_key, data)
                # item_three(new_path, file_key, data)
                # item_four(new_path,file_key, data)
                # part_two(new_path, file_key, data)
                # forward_looking(new_path, file_key, data)
                specific_item(new_path, file_key, data, 1)
                specific_item(new_path, file_key, data, 2)
                specific_item(new_path, file_key, data, 3)
                specific_item(new_path, file_key, data, 4)
                specific_item(new_path, file_key, data, 5)
                specific_item(new_path, file_key, data, 6)
                print(company + " completed separating into sections")

                if tokenized:
                    items = str((os.path.join(subdir) + "/itemized/"))
                    post_item_tokenize(items)
                else:
                    continue

    return None


#######################################################################################################################

