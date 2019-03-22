import sys
import csv
import numpy

# filtering functions:


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
    # Just here so the function can be colapsed properly
    return 

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
                if amount_of_rows_copied >= int(amount_of_samples): # once the desired amount of rows has been reached the execution stops (or if the file runs out)
                    break
    # Just here so the function can be colapsed properly
    return 

# endof filtering functions
# setup functions

def limited_reduce_sample_rate_until_5(file_name, limit):
    '''
    Use this function to setup a targeted sample rate reduction from 95.0 - 5.0, each step is -5.0.
    Takes a dataset of assumed 100Hz sample frequency.
    Takes the amount of samples in the outputed file.
    '''
    
    print('Reading from: ', file_name)
    # run 95, 90 ... 5 HZ
    for i in numpy.arange(95.0, 0.0, -5.0):
        target_rate = i
        print('Target sample rate: ', target_rate)
        print('Amount of samples: ', limit)
        open_and_filter_first_n_values_from_file(file_name, str(target_rate), limit)

def limited_reduce_sample_rate_until_1(file_name, limit):
    '''
    Use this function to setup a targeted sample rate reduction from 4.0 - 1.0, each step is -1.0.
    Takes a dataset of assumed 100Hz sample frequency.
    Takes the amount of samples in the outputed file.
    '''
    
    print('Reading from: ', file_name)
    # run 4, 3 ... 1 HZ
    for i in numpy.arange(4.0, 0.0, -1.0):
        target_rate = i
        print('Target sample rate: ', target_rate)
        print('Amount of samples: ', limit)
        open_and_filter_first_n_values_from_file(file_name, str(target_rate), limit)

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
        shuffle_and_filter(file_name, str(target_rate))  # delete after test.
        open_and_filter_file(file_name, str(target_rate))  #Commented out for a test

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
		
def three_quarters_decay(file_name):
    '''
    Use this function to setup a targeted sample rate reduction from 100.0 - 0.0, each step is a reduction of 3/4 of the previous rate.
    Takes a dataset of assumed 100Hz sample frequency.
    '''
    target_rate = 100.0
    print('Reading from: ', file_name)
    # run 100, 75 ... 0,01786 HZ
    for i in numpy.arange(30.0, 0.0, -1.0):
        target_rate = target_rate * 3/4
        print('Target sample rate: ', target_rate)
        open_and_filter_file(file_name, str(target_rate))
				
def three_quarters_decay_limited(file_name, limit):
    '''
    Use this function to setup a targeted sample rate reduction from 100.0 - 0.0, each step is a reduction of 3/4 of the previous rate.
    Takes a dataset of assumed 100Hz sample frequency.
	Takes the amount of samples in the outputed file.
    '''
    target_rate = 100.0
    print('Reading from: ', file_name)
    # run 100, 75 ... 0,01786 HZ
    for i in numpy.arange(30.0, 0.0, -1.0):
        target_rate = target_rate * 3/4
        print('Target sample rate: ', target_rate)
        open_and_filter_first_n_values_from_file(file_name, str(target_rate), limit)

def reduce_sample_rate_to_target(sample, target):
    '''
    Use this function to setup a targeted sample rate reduction from 100 to target frequency.
    Takes a dataset of assumed 100Hz sample frequency.
    Takes the desired frequency.
    '''

    print('Target sample rate: ', target)
    print('Reading from: ', sample)
    open_and_filter_file(sample, target)

def limited_reduce_sample_rate_to_target(sample, target, limit):
    '''
    Use this function to setup a targeted sample rate reduction from 100 to target frequency.
    Takes a dataset of assumed 100Hz sample frequency.
    Takes the desired frequency.
    Takes the maximum amount of lines the output file will have.
    '''

    print('Reading from: ', sample)
    print('Target sample rate: ', target)
    print('Amount of samples: ', limit)
    open_and_filter_first_n_values_from_file(sample, target, limit)

 # endof setup functions

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
        "limitedreduce100" -> runs limited_reduce_sample_rate_until_5(sys.argv[1], 10000)
        "limitedreduce10" -> runs limited_reduce_sample_rate_until_1(sys.argv[1], 1000)
		"exponential" -> runs three_quarters_decay(sys.argv[1])
        "limitedexponential1000" -> runs limited_reduce_sample_rate_until_5(sys.argv[1], 1000)
    three arguments provided: (python Reduce.py dataset.csv reduce 100)
        "reduce" (python Reduce.py dataset.csv reduce 100):
            "%d" -> runs reduce_sample_rate_to_target(sys.argv[1], sys.argv[4])
        "limitedreduce" (python Reduce.py dataset.csv limitedreduce 100):
            "%d" -> runs reduce_sample_rate_to_target(sys.argv[1], sys.argv[4])
        "limitedexponential" (python Reduce.py dataset.csv limitedexponential 1000):
            "%d" -> runs limited_reduce_sample_rate_until_5(sys.argv[1], sys.argv[4])

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

        if(mode_of_execution == "limitedreduce100"):
            limited_reduce_sample_rate_until_5(sample_set, 10000)

        if(mode_of_execution == "limitedreduce10"):
            limited_reduce_sample_rate_until_1(sample_set, 1000)

        if(mode_of_execution == "reduce"):
            if len(sys.argv) >= 4: # If more argumenta are provided e.g.(python Reduce.py dataset.csv reduce 30)
                value_of_execution = sys.argv[3]
                reduce_sample_rate_to_target(sample_set, value_of_execution)

        if(mode_of_execution == "limitedreduce"):
            if len(sys.argv) >= 5: # If more argumenta are provided e.g.(python Reduce.py dataset.csv limitedreduce 30 10000)
                value_of_execution = sys.argv[3]
                second_value_of_execution = sys.argv[4]
                limited_reduce_sample_rate_to_target(sample_set, value_of_execution, second_value_of_execution)

if __name__ == '__main__':
    main()
