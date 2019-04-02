'''
Classify activities based on sensor data. The classification is done using a
random forest. The forests are printed followed by a confusion matrix and
classification efficiency statistics
'''

#
#   Copyright (C) 2017   Ezra Erb
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License version 3 as published
#   by the Free Software Foundation.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#   I'd appreciate a note if you find this program useful or make
#   updates. Please contact me through LinkedIn or github (my profile also has
#   a link to the code depository)
#
import sys
import csv
import random
import datetime
from collections import defaultdict
import numpy as np
from RandomForest import RandomForest
from ConfusionMatrix import ConfusionMatrix

def load_sample_data(file_name):
    '''
    Load sample data from the given file, strip columns that are not useful for
    classification, return the results as an NDarray.
    '''

    # For efficient subspace sampling, need a 2D NDarray. However, this causes
    # problems handling the category, because NDArrays require all entries to
    # be the same type. The solution chosen here is to map the categories to
    # float values, and use those. Need a map of the values back to the
    # categories for output, and the reverse to translate input
    cat_to_id = {}
    id_to_cat = {}

    # Construct the final array as a list and then merge
    sample_set = []
    with open(file_name, 'rt') as fin:
        ''' When using my_dataset change to second line '''
        #cfin = csv.reader(fin, delimiter=';')
        cfin = csv.reader(fin)
        LABEL_INDEX = -1
        for mrow in cfin:
            if LABEL_INDEX == -1: # Once we know our label index we are over the first line. Label will only equal -1 during the firt execution
                for l in range(len(mrow)): # We look for the column with "label" in it, that will be the index of our labels from now on.
                    if str(mrow[l]) == "label":
                        LABEL_INDEX = l
                        break # I don't think the break does anything, since label will always be tha last column.
                continue
            category = mrow[LABEL_INDEX]
            record_id = -1.0 # Invalid value
            if category in cat_to_id.keys():
                record_id = cat_to_id[category]
            else:
                record_id = float(len(cat_to_id.keys())) # Indexed from zero
                cat_to_id[category] = record_id
                id_to_cat[record_id] = category

            # Row contains several columns containing data spcific to each
            # individual measured. Since this data has perfect corrolation,
            # taking multiple is useless for classification. Take the last
            # one, Body Mass Index.
            samples = [float(i) for i in mrow[2:(LABEL_INDEX-1)]]
            samples.append(record_id) # Correct category becomes last column
            sample_set.append(samples)
    return (np.array(sample_set), id_to_cat)

def filter_sample_set(sample_set):
    '''
    This method converts a big sample sant and reduces it to make testing the
    code easier. It randomly samples from each combination of BMI and category.
    '''

    # Split the list into sublists based on BMI/result comobs
    split_lists = defaultdict(list)

    for data in sample_set:
        sublist_type = (data[0], data[-1])
        split_lists[sublist_type].append(data)

    output_samples = []
    for data in split_lists.itervalues():
        # https://www.safaribooksonline.com/library/view/python-cookbook/0596001673/ch02s09.html
        sublist_size = len(data)
        for dummy in range(10):
            wanted_sample = random.randrange(sublist_size)
            output_samples.append(data[wanted_sample])
            data[wanted_sample] = data[sublist_size - 1]
            sublist_size = sublist_size - 1
    return np.array(output_samples)

def run_train(train_set, number_of_trees):
    RF = RandomForest(train_set, number_of_trees)

    return RF

def run_test(ids, test_set, forest):
    CM = ConfusionMatrix(ids.values())
    for sample in test_set:
            classified_category = forest.classify_activity(sample)
            CM.add_result(int(sample[-1]), classified_category)

    return CM

def run_everything(set_name):
    (sample_set, id_to_cat) = load_sample_data(set_name) # load data
    np.random.shuffle(sample_set) # shuffle data
    test_sample_count = int(sample_set.shape[0] / 5) # find how many samples equate to 20% of samples
    test_samples = sample_set[:test_sample_count] # establish train set as first 80% of samples
    training_samples = sample_set[test_sample_count:]# establish test set as las 20% of samples
    sys.setrecursionlimit(5000) # Set the recursion limit very high so our computer doesn't think the random forest is an infinite loop
    forest = run_train(training_samples, 7) # train the random forest with 7 trees
    matrix = run_test(id_to_cat, test_samples, forest) # Create the confusion matrix from the random forest using the test set
    print(matrix) # print the matrix
    matrix.report_stats() # print the confusion matrix precision/recall

def make_windows_experiment(set):
    '''
    Use this function to setup a window experiment, compare different windowed implementations to see which is more efficient.
    Takes a dataset, will add "_windowed_discard_%d" %d will be all the different window sizes:
       Window sizes: 2, 3, ... 10; 12, 14 .. 20, 25, 30, 35, 40; 50, 60 ... 100.

    Prints all confusion matrixes
    '''
    for i in range(2, 10):
        current_dataset = set.replace(".csv", "_windowed_discard_%s.csv" % str(i))
        print('Reading from: ', current_dataset)
        print('# of windows: ', i)
        run_everything(current_dataset)

    for i in range(10, 20, 2):
        current_dataset = set.replace(".csv", "_windowed_discard_%s.csv" % str(i))
        print('Reading from: ', current_dataset)
        print('# of windows: ', i)
        run_everything(current_dataset)    
    for i in range(20, 40, 5):
        current_dataset = set.replace(".csv", "_windowed_discard_%s.csv" % str(i))
        print('Reading from: ', current_dataset)
        print('# of windows: ', i)
        run_everything(current_dataset)    
    for i in range(40, 101, 10):
        current_dataset = set.replace(".csv", "_windowed_discard_%s.csv" % str(i))
        print('Reading from: ', current_dataset)
        print('# of windows: ', i)
        run_everything(current_dataset)

def main():
    '''
    Main classification driver. Read in data files, classify the sensor data
    they contain, and evaluate the performance of the classifier
    '''
    if len(sys.argv) < 2:
        print('USAGE: ActivityClassifier.py (path to data file)')
        sys.exit(1)

    '''
    (sample_set, id_to_cat) = load_sample_data(sys.argv[1])
    # TESTING: Reduce the number of samples
    # sample_set = filter_sample_set(sample_set)
    Uncomment this section for original code.
    # Divide the samples into two, training and test. Keep 25% for test
    np.random.shuffle(sample_set)
    test_sample_count = int(sample_set.shape[0] / 4)
    test_samples = sample_set[:test_sample_count]
    training_samples = sample_set[test_sample_count:]

    sys.setrecursionlimit(5000) 

    # Default of 9 trees
    #random_forest = RandomForest(training_samples, 9)
    random_forest = RandomForest(training_samples, 36)
    # print(random_forest) # Uncomment to see the random forest visualization.

    confusion_matrix = ConfusionMatrix(id_to_cat.values())

    for sample in test_samples:
        classified_category = random_forest.classify_activity(sample)
        confusion_matrix.add_result(int(sample[-1]), classified_category)

    print(confusion_matrix)
    confusion_matrix.report_stats()
    '''

    #make_windows_experiment(sys.argv[1])
    run_everything(sys.argv[1])
    

if __name__ == '__main__':
    main()
