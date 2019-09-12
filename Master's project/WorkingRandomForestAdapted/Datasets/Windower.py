import sys
import csv
import Shuffle
import ReduceSampleRate
import numpy
import math

START_COLUMN_INDEX = 2
COLUMN_WIDTH = 5

# TIME-DOMAIN

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
    '''
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
    '''
    for i in range(50, 1001, 50):
        print('# of windows: ', i)
        print('Output file: ', make_windows_discard(set, i))

def experimenttwotwo():
    for i in range(2, 101, 1):
        input = ("2.2_%dHZ.csv" % i)
        make_windows_discard(input, int(i * 1.5))

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
        mode_of_execution = sys.argv[1]
        if(mode_of_execution == "twotwo"):
            experimenttwotwo()
        if(mode_of_execution == "twothree"):
            experimenttwothree()
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


def return_mean(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the mean

    mean = addition of all the values divided by the amount of values

    Returns a float representing the average of the input_matrix
    '''

    output = 0.0
    n = 0
    for num in input_matrix:
        output += num
        n += 1

    return (output/n)

def return_max(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the highest value

    Returns a float representing the maximum value of the input_matrix
    '''

    output = input_matrix[0]
    for num in input_matrix:
        if output<num:
            output = num

    return output

def return_min(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the lowest value

    Returns a float representing the minimum value of the input_matrix
    '''

    output = input_matrix[0]
    for num in input_matrix:
        if output>num:
            output = num

    return output

def return_range(input_matrix):
    '''
    Takes a one-dimentional array of values and returns its range

    Returns a float representing the difference between the highest and the lowest value in the input_matrix
    '''
    min = return_min(input_matrix)
    max = return_max(input_matrix)

    return (max - min)

def return_magnitude(x, y, z):
    '''
    Takes a three-dimentional vector and returns its magnitude

    Returns a float representing the magnitude of the input vector
    '''
    output = []
    for i, j, k in zip(x, y, z):
        output.append(math.pow(i, 2) + math.pow(j, 2) + math.pow(k, 2))
    return output

def return_root_square_mean(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the root-square mean

    root-square mean = addition of all the squared values divided by the amount of values. Squared root of te result

    Returns a float representing the rooted quared average of the input_matrix
    '''

    output = 0.0
    n = 0
    for num in input_matrix:
        output += math.pow(num, 2)
        n += 1

    output = output/n
    return (math.sqrt(output))

def return_correlation(input_matrix1, input_matrix2):
    '''
    Takes two one-dimentional array of values and returns their correlation

    Returns a float representing the correlation between of the two input_matrix
    '''

    output = 0.0
    n = 0

    mean1 = return_mean(input_matrix1)
    mean2 = return_mean(input_matrix2)

    sd1 = return_standard_deviation(input_matrix1)
    sd2 = return_standard_deviation(input_matrix2)
    if(sd1*sd2 == 0):
        return 0

    for num1, num2 in zip(input_matrix1, input_matrix2):
        output += (num1 - mean1)*(num2-mean2)
        n += 1

    return output/((n-1)*sd1*sd2)

def return_energy(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the signal's strength

    energy = root of the uncorrected variance (the total squared distance to the mean)

    Returns a float representing the energy of the input_matrix
    '''

    output = 0.0

    mean = return_mean(input_matrix)

    for num in input_matrix:
        output += math.pow(num - mean, 2)

    return (math.sqrt(output))

def return_standard_deviation(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the standard deviation

    standard deviation = root of the uncorrected variance (the average squared distance to the mean)

    Returns a float representing the standard deviation of the input_matrix
    '''

    output = 0.0
    n = 0

    mean = return_mean(input_matrix)

    for num in input_matrix:
        output += math.pow(num - mean, 2)
        n += 1

    output = output/n
    return (math.sqrt(output))

def return_skewness(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the skewness

    skewness = how skewed the values are around the mean

    Returns a float representing the skewness of the input_matrix
    '''

    output = 0.0
    n = 0

    mean = return_mean(input_matrix)
    deviation = return_standard_deviation(input_matrix)

    if (deviation == 0):
        return 0

    for num in input_matrix:
        output += math.pow(num - mean, 3)
        n += 1

    output = output/n
    return (output / (math.pow(deviation, 3)))

def return_0_crossing_rate(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the time it crosses 0

    zero crossing rate = the times it went from negative to positive or viceversa

    Returns a float representing the time the input_matrix crosses 0
    '''

    output = 0.0
    n = 0

    first = True
    previous_num = 0.0

    for num in input_matrix:
        if num == 0.0:
            continue
        if first:
            previous_num = num
            first = False
            continue

        if(num * previous_num > 0.0):
            previous_num = num
        else:
            n += 1
            previous_num = num

    return n

def return_mean_crossing_rate(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the time it crosses the mean of the matrix

    mean crossing rate = the times it went from over the mean to under it, or viceversa

    Returns a float representing the time the input_matrix crosses the mean
    '''

    output = 0.0
    n = 0

    mean = return_mean(input_matrix)

    first = True
    previous_num = 0.0

    for num in input_matrix:
        if num == mean:
            continue
        if first:
            previous_num = num
            first = False
            continue

        if((num-mean) * (previous_num-mean) > 0.0):
            previous_num = num
        else:
            n += 1
            previous_num = num
        
    return n

def extract_n_value(input, n, windows = -1):
    '''
    This function will extract the n values in a matrix of shape
    (if n==0 we would extract x1; if n==2 we would extract z1)
    x1y1z1x2y2z2 - repeat

    returns a list 
    '''

    output = []
    columns_to_skip = START_COLUMN_INDEX
    sample_width = n

    skip_last = False
    if windows > 0:
        skip_last = True

    for i in input:
        if columns_to_skip > 0:
            columns_to_skip -= 1
            continue
        if sample_width > 0:
            sample_width -= 1
            continue

        if skip_last:
            windows -= 1

        if windows == 0:
            break
        output.append(float(i))
        sample_width = COLUMN_WIDTH

    return output

def extract_x1(input, size):
    '''
    This function will extract the x1 values in a matrix of shape
    x1y1z1x2y2z2 - repeat

    returns a list 
    '''
    return extract_n_value(input, 0, size)

def extract_y1(input):
    '''
    This function will extract the y1 values in a matrix of shape
    x1y1z1x2y2z2 - repeat

    returns a list 
    '''
    return extract_n_value(input, 1)

def extract_z1(input):
    '''
    This function will extract the z1 values in a matrix of shape
    x1y1z1x2y2z2 - repeat

    returns a list 
    '''
    return extract_n_value(input, 2)

def extract_x2(input):
    '''
    This function will extract the x2 values in a matrix of shape
    x1y1z1x2y2z2 - repeat

    returns a list 
    '''
    return extract_n_value(input, 3)

def extract_y2(input):
    '''
    This function will extract the y2 values in a matrix of shape
    x1y1z1x2y2z2 - repeat

    returns a list 
    '''
    return extract_n_value(input, 4)

def extract_z2(input):
    '''
    This function will extract the z2 values in a matrix of shape
    x1y1z1x2y2z2 - repeat

    returns a list 
    '''
    return extract_n_value(input, 5)

def return_feature(feature, x1, y1, z1, x2, y2, z2):
    '''
    Returns the specified feature from all the inputs
    '''
    output = []
    if(feature == "mean"):
        output.append(return_mean(x1))
        output.append(return_mean(y1))
        output.append(return_mean(z1))
        output.append(return_mean(x2))
        output.append(return_mean(y2))
        output.append(return_mean(z2))
    elif (feature == "standard deviation"):
        output.append(return_standard_deviation(x1))
        output.append(return_standard_deviation(y1))
        output.append(return_standard_deviation(z1))
        output.append(return_standard_deviation(x2))
        output.append(return_standard_deviation(y2))
        output.append(return_standard_deviation(z2))
    elif (feature == "skewness"):
        output.append(return_skewness(x1))
        output.append(return_skewness(y1))
        output.append(return_skewness(z1))
        output.append(return_skewness(x2))
        output.append(return_skewness(y2))
        output.append(return_skewness(z2))
    elif (feature == "mag"):
        mag = return_magnitude(x1, y1, z1)
        output.append(return_max(mag))
        output.append(return_mean(mag))
        output.append(return_standard_deviation(mag))
        mag = return_magnitude(x2, y2, z2)
        output.append(return_max(mag))
        output.append(return_mean(mag))
        output.append(return_standard_deviation(mag))
    elif (feature == "zero cross rate"):
        output.append(return_0_crossing_rate(x1))
        output.append(return_0_crossing_rate(y1))
        output.append(return_0_crossing_rate(z1))
        output.append(return_0_crossing_rate(x2))
        output.append(return_0_crossing_rate(y2))
        output.append(return_0_crossing_rate(z2))
    elif (feature == "mean cross rate"):
        output.append(return_mean_crossing_rate(x1))
        output.append(return_mean_crossing_rate(y1))
        output.append(return_mean_crossing_rate(z1))
        output.append(return_mean_crossing_rate(x2))
        output.append(return_mean_crossing_rate(y2))
        output.append(return_mean_crossing_rate(z2))
    elif (feature == "root square mean"):
        output.append(return_root_square_mean(x1))
        output.append(return_root_square_mean(y1))
        output.append(return_root_square_mean(z1))
        output.append(return_root_square_mean(x2))
        output.append(return_root_square_mean(y2))
        output.append(return_root_square_mean(z2))
    elif (feature == "energy"):
        output.append(return_energy(x1))
        output.append(return_energy(y1))
        output.append(return_energy(z1))
        output.append(return_energy(x2))
        output.append(return_energy(y2))
        output.append(return_energy(z2))
    elif (feature == "range"):
        output.append(return_range(x1))
        output.append(return_range(y1))
        output.append(return_range(z1))
        output.append(return_range(x2))
        output.append(return_range(y2))
        output.append(return_range(z2))
    elif (feature == "correlation"):
        output.append(return_correlation(x1, y1))
        output.append(return_correlation(x1, z1))
        output.append(return_correlation(y1, z1))
        output.append(return_correlation(x2, y2))
        output.append(return_correlation(x2, z2))
        output.append(return_correlation(y2, z2))
    return output
        
def extract_all_data(input):
    '''
    Opens target file and creates the following features for each window:
    mean
    standard deviation
    skewness
    mag(max, mean, stadard deviation)
    zero cross rate
    mean cross rate
    root square mean
    energy
    range
    correlation
    returns the name of the output file, "inputfile_extracted.csv"
    '''
    target_file = input.replace(".csv", "_extracted.csv")


    with open(input, 'rt') as fin, open(target_file, 'w', newline='') as fout: # in python 2 open(target_file, 'wb'); in python 3 open(target_file, 'w', newline='')
        cfin = csv.reader(fin, delimiter=",")
        writer = csv.writer(fout, delimiter=",")
        first_row_copied = False
        for mrow in cfin:
            if not first_row_copied: # We will write the headers in the first line
                header = []
                for i in range(START_COLUMN_INDEX):
                    header.append(mrow[i])
                print("Mean")
                for i in range(6):
                    header.append("mean_%d" % i)
                print("Standard deviation")
                for i in range(6):
                    header.append("sd_%d" % i)
                print("Skewness")
                for i in range(6):
                    header.append("skewness_%d" % i)
                print("Maginitude(max, mean, standard deviation)")
                for i in range(6):
                    header.append("mag_%d" % i)
                print("Zero cross-rate")
                for i in range(6):
                    header.append("zcr_%d" % i)
                print("Mean cross-rate")
                for i in range(6):
                    header.append("mcr_%d" % i)
                print("Root square mean")
                for i in range(6):
                    header.append("rsm_%d" % i)
                print("Energy")
                for i in range(6):
                    header.append("energy_%d" % i)
                print("Range")
                for i in range(6):
                    header.append("range_%d" % i)
                print("Correlation")
                for i in range(6):
                    header.append("correlation_%d" % i)
                header.append(mrow[len(mrow)-1])
                writer.writerow(str(elt) for elt in header)
                first_row_copied = True
                continue

            current_window = []

            #extract all value vectors
            x1=extract_x1(mrow, (len(mrow)-3)/6)
            y1=extract_y1(mrow)
            z1=extract_z1(mrow)
            x2=extract_x2(mrow)
            y2=extract_y2(mrow)
            z2=extract_z2(mrow)

            #copy first two columns
            for i in range(START_COLUMN_INDEX):
                    current_window.append(mrow[i])

            #calculate and copy values:
            feature = "mean"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "standard deviation"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "skewness"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "mag"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "zero cross rate"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "mean cross rate"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "root square mean"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "energy"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "range"            
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)
            feature = "correlation"
            for val in return_feature(feature, x1, y1, z1, x2, y2, z2):
                current_window.append(val)

            #copy label
            current_window.append(mrow[len(mrow)-1])
            
            #write values
            writer.writerow(str(elt) for elt in current_window)


    return target_file

def experimenttwothree():
    for i in range(66, 101, 1):
        input = ("2.2_%dHZ.csv" % i)
        for j in numpy.arange(1.5, 10.5, 0.5):
            output = make_windows_discard(input, int(i * j))
            extract_all_data(output)

if __name__ == '__main__':
    main()
