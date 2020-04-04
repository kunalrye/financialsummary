"""
Randomly selects 75% of the companies for training, the other 25% are for testing
Writes the training company codes to resources/train_companies.txt
Write the testing company codes to resources/test_companies.txt
"""

import random
import os
import math

TRAIN_PROPORTION = 0.75


input_dirpath = os.path.expanduser("../resources/itemized")
comp_names = []

for root, dirs, files in os.walk(input_dirpath):
    for comp_name in dirs:
        comp_names.append(comp_name)


random.seed(130)
k = math.ceil(len(comp_names) * TRAIN_PROPORTION)
train_comps = random.sample(comp_names, k)
test_comps = [comp for comp in comp_names if comp not in train_comps]

with open("../resources/train_companies.txt", 'w') as f:
    for comp in train_comps:
        f.write("%s\n" % comp)


with open("../resources/test_companies.txt", 'w') as f:
    for comp in test_comps:
        f.write("%s\n" % comp)

