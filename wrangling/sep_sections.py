"""
Take each text document, and create a dictionary of the document structure by identifying
headers and their respective content
"""
import os


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
                        if 15 <= len(x) <= 100: # using length does not solve for all cases effectively
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

x = separate_document('/Users/kunal/Dropbox/XBRLoutput_files_examples/batch_0002')
print(x)