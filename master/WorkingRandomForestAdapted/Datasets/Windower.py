import sys
import csv
import Shuffle
import ReduceSampleRate
import numpy

# Constants:
LABEL_INDEX = 8
DATA_START_INDEX = 2
DATA_END_INDEX = 7
SUBJECT_INDEX = 9

WINDOW_WIDTH = DATA_END_INDEX - DATA_START_INDEX + 1
# endof Constants

def make_windows_discard(input, window_size):
    '''
    Load sample data from the given file, take %d (window_size) rows, create a new file with those rows in one single line.
    Takes a file to load from. 
    Takes the amount of samples in each window.

    If the labels are different the whole window gets discarded.

    Creates a file named the same way as the given file with _windowed added at the end.
    Returns the name of the created file.
    '''
    target_file = input.replace(".csv", "_windowed_discard_%s.csv" % str(window_size))

    current_window_counter = int(window_size)
    current_window = []
    current_window_label = "none"

    with open(input, 'rt') as fin, open(target_file, 'w', newline='') as fout: # in python 2 open(target_file, 'wb'); in python 3 open(target_file, 'w', newline='')
        cfin = csv.reader(fin, delimiter=",")
        writer = csv.writer(fout, delimiter=",")
        first_row_copied = False
        for mrow in cfin:
            if not first_row_copied: # We will copy the first line, since it includes the headers
                header = []
                for i in range(DATA_START_INDEX):
                    header.append(mrow[i])
                for i in range(int(window_size)):
                    for j in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                        header.append(mrow[j])
                header.append(mrow[LABEL_INDEX])
                writer.writerow(str(elt) for elt in header)
                first_row_copied = True
                continue

            if current_window_counter >= int(window_size): # on a new line 
                current_window = []
                current_window_label = mrow[LABEL_INDEX]
                for t in range(DATA_START_INDEX):
                    current_window.append(mrow[t])

            if(current_window_label == mrow[LABEL_INDEX]): #if the label from the first row is the same as the current we continue (this is a valid window)
                for i in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                    current_window.append(mrow[i])
            else: #if the label from the first row is different as the current window, we discard this whole window (this is not a valid window and we will start it again)
                current_window_counter = int(window_size)
                continue

            current_window_counter = current_window_counter - 1
            if current_window_counter <= 0: # if this was the last line of the window
                current_window.append(current_window_label)
                writer.writerow(str(elt) for elt in current_window)
                current_window_counter = int(window_size)

    return target_file

def make_windows_transition(input, window_size):
    '''
    Load sample data from the given file, take %d (window_size) rows, create a new file with those rows in one single line.
    Takes a file to load from. 
    Takes the amount of samples in each window.

    If the labels are different a new transition label will be created. (transition from "stand" to "walk" will be labeled as "transition")

    Creates a file named the same way as the given file with _windowed_transition added at the end.
    Returns the name of the created file.
    '''
    
    target_file = input.replace(".csv", "_windowed_transition_%s.csv" % str(window_size))

    current_window_counter = int(window_size)
    current_window = []
    current_window_label = "none"
    label_to_add = ""
    current_line_label = ""

    with open(input, 'rt') as fin, open(target_file, 'w', newline='') as fout: # in python 2 open(target_file, 'wb'); in python 3 open(target_file, 'w', newline='')
        cfin = csv.reader(fin, delimiter=",")
        writer = csv.writer(fout, delimiter=",")
        first_row_copied = False
        for mrow in cfin:
            if not first_row_copied: # We will copy the first line, since it includes the headers
                header = []
                for i in range(DATA_START_INDEX):
                    header.append(mrow[i])
                for i in range(int(window_size)):
                    for j in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                        header.append(mrow[j])
                header.append(mrow[LABEL_INDEX])
                writer.writerow(str(elt) for elt in header)
                first_row_copied = True
                continue

            if current_window_counter >= int(window_size): # on a new line 
                current_window = []
                current_line_label = mrow[LABEL_INDEX]

            current_window_label = mrow[LABEL_INDEX]
            if((label_to_add + current_window_label) == current_line_label): #if the label from the first row is the same as the current we continue
                for i in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                    current_window.append(mrow[i])
            else: #if the label from the first row is different as the current window, we add both labels as a new label
                label_to_add = current_line_label
                current_line_label = label_to_add + current_window_label
                for i in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                    current_window.append(mrow[i])

            current_window_counter = current_window_counter - 1
            if current_window_counter <= 0: # if this was the last line of the window
                current_window.append(current_line_label)
                writer.writerow(str(elt) for elt in current_window)
                current_window_counter = int(window_size)
                label_to_add = ""


    return target_file
    
def make_windows_no_discard(input, window_size):
    '''
    Load sample data from the given file, take %d (window_size) rows, create a new file with those rows in one single line.
    Takes a file to load from. 
    Takes the amount of samples in each window.

    If the labels are different a new label will be created. (transition from "stand" to "walk" will be labeled as "standwalk")

    Creates a file named the same way as the given file with _windowed_no_discard added at the end.
    Returns the name of the created file.
    '''
    
    target_file = input.replace(".csv", "_windowed_no_discard_%s.csv" % str(window_size))

    current_window_counter = int(window_size)
    current_window = []
    current_window_label = "none"
    label_to_add = ""
    current_line_label = ""

    with open(input, 'rt') as fin, open(target_file, 'w', newline='') as fout: # in python 2 open(target_file, 'wb'); in python 3 open(target_file, 'w', newline='')
        cfin = csv.reader(fin, delimiter=",")
        writer = csv.writer(fout, delimiter=",")
        first_row_copied = False
        for mrow in cfin:
            if not first_row_copied: # We will copy the first line, since it includes the headers
                header = []
                for i in range(DATA_START_INDEX):
                    header.append(mrow[i])
                for i in range(int(window_size)):
                    for j in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                        header.append(mrow[j])
                header.append(mrow[LABEL_INDEX])
                writer.writerow(str(elt) for elt in header)
                first_row_copied = True
                continue

            if current_window_counter >= int(window_size): # on a new line 
                current_window = []
                current_line_label = mrow[LABEL_INDEX]

            current_window_label = mrow[LABEL_INDEX]
            if((label_to_add + current_window_label) == current_line_label): #if the label from the first row is the same as the current we continue
                for i in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                    current_window.append(mrow[i])
            else: #if the label from the first row is different as the current window, we add both labels as a new label
                label_to_add = current_line_label
                current_line_label = label_to_add + current_window_label
                for i in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                    current_window.append(mrow[i])

            current_window_counter = current_window_counter - 1
            if current_window_counter <= 0: # if this was the last line of the window
                current_window.append(current_line_label)
                writer.writerow(str(elt) for elt in current_window)
                current_window_counter = int(window_size)
                label_to_add = ""


    return target_file

def make_average_windows_discard(input, window_size):
    '''
    Load sample data from the given file, take %d (window_size) rows, create a new file with those rows in one single line.
    Takes a file to load from. 
    Takes the amount of samples averaged in each window.

    If the labels are different the whole window gets discarded.

    Creates a file named the same way as the given file with _windowed added at the end.
    Returns the name of the created file.
    '''
    
    target_file = input.replace(".csv", "_windowed_average_%s.csv" % str(window_size))

    current_window_counter = int(window_size)
    current_window = []
    current_window_label = "none"
    current_window_values = numpy.zeros(WINDOW_WIDTH)

    with open(input, 'rt') as fin, open(target_file, 'w', newline='') as fout: # in python 2 open(target_file, 'wb'); in python 3 open(target_file, 'w', newline='')
        cfin = csv.reader(fin, delimiter=",")
        writer = csv.writer(fout, delimiter=",")
        first_row_copied = False
        for mrow in cfin:
            if not first_row_copied: # We will copy the first line, since it includes the headers
                header = []
                for i in range(DATA_START_INDEX):
                    header.append(mrow[i])
                for j in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                    header.append(mrow[j])
                header.append(mrow[LABEL_INDEX])
                writer.writerow(str(elt) for elt in header)
                first_row_copied = True
                continue

            if current_window_counter >= int(window_size): # on a new line 
                current_window = []
                current_window_label = mrow[LABEL_INDEX]
                current_window_values = numpy.zeros(WINDOW_WIDTH)

            if(current_window_label == mrow[LABEL_INDEX]): #if the label from the first row is the same as the current we continue (this is a valid window)
                for i in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                    current_window_values[i - DATA_START_INDEX] = current_window_values[i - DATA_START_INDEX] + float(mrow[i])
            else: #if the label from the first row is different as the current window, we discard this whole window (this is not a valid window and we will start it again)
                current_window_counter = int(window_size)
                continue

            current_window_counter = current_window_counter - 1
            if current_window_counter <= 0: # if this was the last line of the window
                for i in range(WINDOW_WIDTH):
                    current_window.append(current_window_values[i] / float(window_size)) # we append the average of every value
                current_window.append(current_window_label)
                writer.writerow(str(elt) for elt in current_window)
                current_window_counter = int(window_size)

    return target_file


def make_windows_experiment(set):
    '''
    Use this function to setup a windower.
    Takes a dataset.

    Makes a windowed dataset from 2, 3, ... 10; 12, 14 .. 20, 25, 30, 35, 40; 50, 60 ... 100.
    '''

    print('Reading from: ', set)
    for i in range(2, 10):
        print('# of windows: ', i)
        print('Output file: ', make_windows_discard(set, i))
    for i in range(10, 20, 2):
        print('# of windows: ', i)
        print('Output file: ', make_windows_discard(set, i))
    for i in range(20, 40, 5):
        print('# of windows: ', i)
        print('Output file: ', make_windows_discard(set, i))
    for i in range(40, 101, 10):
        print('# of windows: ', i)
        print('Output file: ', make_windows_discard(set, i))

def main():
    '''
    Main windower driver. Read in data files, join data and labels in windows.
    '''

    '''
    Input explanation:

    From now on all inputs to this function will be of the following type:
    no argument provided -> error (python Shuffle.py)
    one argument provided -> error (python Shuffle.py dataset.csv)
    two arguments provided: (python Shuffle.py dataset.csv reduce100)
        "windows" -> runs make_windows_experiment(sys.argv[1])
    three arguments provided: (python Shuffle.py dataset.csv reduce 100)
        "discardwindow":
            "%d" -> make_windows_discard(sys.argv[1], sys.argv[3])
        "window":
            "%d" -> make_windows_no_discard(sys.argv[1], sys.argv[3])
        "average":
            "%d" -> make_average_windows_discard(sys.argv[1], sys.argv[3])
    '''
    if len(sys.argv) < 2: # If no dataset is provided e.g.(python Reduce.py)
        print('USAGE: Windower.py (path to data file)')
        sys.exit(1)
    if len(sys.argv) < 3: # If no mode is provided e.g.(python Reduce.py dataset.csv)
        print('USAGE: Windower.py (mode of execution)')
        sys.exit(1)
    sample_set = sys.argv[1]
    if len(sys.argv) == 3:
        mode_of_execution = sys.argv[2]
        if(mode_of_execution == "windows"):
            make_windows_experiment(sample_set)
    if len(sys.argv) >= 4: # If ony one argument is provided e.g.(python Reduce.py dataset.csv reduce100)
        mode_of_execution = sys.argv[2]
        in_value = sys.argv[3]
        if(mode_of_execution == "discardwindow"):
            make_windows_discard(sample_set, in_value)
        if(mode_of_execution == "window"):
            make_windows_no_discard(sample_set, in_value)
        if(mode_of_execution == "average"):
            make_average_windows_discard(sample_set, in_value)

if __name__ == '__main__':
    main()
