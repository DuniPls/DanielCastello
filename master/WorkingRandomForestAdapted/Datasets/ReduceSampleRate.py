import sys
import csv
import numpy

def open_and_filter_file(file_name, target_sample_rate):
    '''
    Load sample data from the given file, create a new file with given sample rate.
    Takes a file to load from. 
    Takes a sample rate, meaning how many of the samples in the given file will be kept. 
    Assumes a base sample rate of 100.0 Hz.

    Does not return anything, creates a file named "my_dataset_%sHZ.csv" % str(target_sample_rate)
    '''

    target_file = "my_dataset_%sHZ.csv" % str(target_sample_rate.replace(".", ","))

    row_counter = float(target_sample_rate) / 100.0
    total_row_counter = 0.0

    with open(file_name, 'rt') as fin, open(target_file, 'w', newline='') as fout: # in python 2 open(target_file, 'wb'); in python 3 open(target_file, 'w', newline='')
        cfin = csv.reader(fin, delimiter=",")
        writer = csv.writer(fout, delimiter=",")
        first_row_copied = False
        for mrow in cfin:
            if not first_row_copied: # We will copy the first line, since it includes the headers
                writer.writerow(str(elt) for elt in mrow)
                first_row_copied = True
                continue
            total_row_counter = total_row_counter + row_counter
            if total_row_counter >= 1.0:
                writer.writerow(str(elt) for elt in mrow)
                total_row_counter = total_row_counter - 1.0


def open_and_filter_first_n_values_from_file(file_name, target_sample_rate, amount_of_samples):
    '''
    Load sample data from the given file, create a new file with given sample rate.
    Takes a file to load from. 
    Takes a sample rate, meaning how many of the samples in the given file will be kept. 
    Takes a fixed amount of samples to place in the output file.
    Assumes a base sample rate of 100.0 Hz.

    Does not return anything, creates a file named "my_dataset_%sHZ_%ssamples.csv" % str(target_sample_rate) % str(amount_of_samples)
    '''

    target_file = "my_dataset_%sHZ_%ssamples.csv" % (str(target_sample_rate.replace(".", ",")), str(amount_of_samples))

    row_counter = float(target_sample_rate) / 100.0
    total_row_counter = 0.0

    amount_of_rows_copied = 0

    with open(file_name, 'rt') as fin, open(target_file, 'w', newline='') as fout: # in python 2 open(target_file, 'wb'); in python 3 open(target_file, 'w', newline='')
        cfin = csv.reader(fin, delimiter=",")
        writer = csv.writer(fout, delimiter=",")
        first_row_copied = False
        for mrow in cfin:
            if not first_row_copied: # We will copy the first line, since it includes the headers
                writer.writerow(str(elt) for elt in mrow)
                first_row_copied = True
                continue
            total_row_counter = total_row_counter + row_counter
            if total_row_counter >= 1.0:
                writer.writerow(str(elt) for elt in mrow)
                total_row_counter = total_row_counter - 1.0
                amount_of_rows_copied = amount_of_rows_copied + 1
                if amount_of_rows_copied >= amount_of_samples: # once the desired amount of rows has been reached the execution stops (or if the file runs out)
                    break

def reduce_sample_rate_until_5(file_name):
    '''
    Use this function to setup a targeted sample rate reduction from 95.0 - 5.0, each step is -5.0.
    Takes a dataset of assumed 100Hz sample frequency.
    '''
    
    print('Reading from: ', file_name)
    # run 95, 90 ... 5 HZ
    for i in numpy.arange(95.0, 0.0, -5.0):
        target_rate = i
        print('Target sample rate: ', target_rate)
        open_and_filter_file(file_name, str(target_rate))

def reduce_sample_rate_until_1(file_name):
    '''
    Use this function to setup a targeted sample rate reduction from 4.0 - 1.0, each step is -1.0.
    Takes a dataset of assumed 100Hz sample frequency.
    '''
    
    print('Reading from: ', file_name)
    # run 4, 3 ... 1 HZ
    for i in numpy.arange(4.0, 0.0, -1.0):
        target_rate = i
        print('Target sample rate: ', target_rate)
        open_and_filter_file(file_name, str(target_rate))

def reduce_sample_rate_to_target(sample, target):
    '''
    Use this function to setup a targeted sample rate reduction from 100 to target frequency.
    Takes a dataset of assumed 100Hz sample frequency.
    Takes the desired frequency.
    '''

    print('Target sample rate: ', target)
    print('Reading from: ', sample)
    open_and_filter_file(sample, target)

def main():
    '''
    Main reduction driver. Read in data files, read in target rate,
    reduce data to target amount
    '''

    '''
    Input explanation:

    From now on all inputs to this function will be of the following type:
    no argument provided -> error (python Reduce.py)
    one argument provided -> error (python Reduce.py dataset.csv)
    two arguments provided: (python Reduce.py dataset.csv reduce100)
        "reduce100" -> runs reduce_sample_rate_until_5(sys.argv[1])
        "reduce10" -> runs reduce_sample_rate_until_1(sys.argv[1])
    three arguments provided: (python Reduce.py dataset.csv reduce 100)
        "reduce" (python Reduce.py dataset.csv reduce 100):
            "%d" _ runs reduce_sample_rate_to_target(sys.argv[1], sys.argv[4])
    '''

    if len(sys.argv) < 2: # If no dataset is provided e.g.(python Reduce.py)
        print('USAGE: ReduceSamplingRate.py (path to data file)')
        sys.exit(1)
    if len(sys.argv) < 3: # If no mode is provided e.g.(python Reduce.py dataset.csv)
        print('USAGE: ReduceSamplingRate.py (mode of execution)')
        sys.exit(1)
    sample_set = sys.argv[1]
    if len(sys.argv) >= 3: # If ony one argument is provided e.g.(python Reduce.py dataset.csv reduce100)
        mode_of_execution = sys.argv[2]
        if(mode_of_execution == "reduce100"):
            reduce_sample_rate_until_5(sample_set)

        if(mode_of_execution == "reduce10"):
            reduce_sample_rate_until_1(sample_set)

        if(mode_of_execution == "reduce"):
            if len(sys.argv) >= 4: # If more argumenta are provided e.g.(python Reduce.py dataset.csv reduce 30)
                value_of_execution = sys.argv[3]
                reduce_sample_rate_to_target(sample_set, value_of_execution)

if __name__ == '__main__':
    main()
