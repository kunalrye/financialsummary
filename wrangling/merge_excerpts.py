"""
Takes output from SEC_EDGAR_text and merges all "...excerpt.txt" files together for parsing
"""
import os
import itertools

def join_excerpts(directory):
    """
    join excerpts for same 10-Q for same company together
    :param directory: filepath for directory in which all 10-Q.txt files are
    :return: none
    """
    txt_files = []
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):
                name_path = os.path.join(subdir, file)
                txt_files.append(name_path)
    # split file name by underscore then match the elements of split then open and add
    groups = [list(g) for _, g in itertools.groupby(sorted(txt_files), lambda x: x[0:64])]
    # print(groups)
    for group in groups:
        splitfile = (group[0].rsplit("_"))
        unique = splitfile[2:5]
        unique2 = ''.join(map(str, unique))
        print(unique2)

        # with open(group[1][36:64]+'.txt', 'w') as outfile:
        #     print(group[1][36:64]+'.txt')
    #         for file in group:
    #             with open(file) as fp:
    #                 data = fp.read()
    #                 outfile.write(data)
    #         # add content to txt file
    #     # close txt file
    #     print(outfile)
    # return None

join_excerpts('/Users/kunal/Dropbox/batch_0005')
