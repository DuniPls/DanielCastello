import pandas
import numpy
import sys
import csv


def shuffle_file(file_name):
    '''
    Load sample data from the given file, shuffle rows, create a new file with shuffled information.
    Takes a file to load from. 

    Does not return anything, creates a file named the same way as the given file with _shuffled added at the end.
    '''

    target_file = "%s_shuffled.csv" % str(file_name)

    cfin = pandas.read_csv(file_name, index_col = 0)
    output = cfin.reindex(numpy.random.permutation(cfin.index))
    output.to_csv("%s_shuffled.csv" % str(file_name), sep=',')


def main():
    '''
    Main shuffle driver. Read in data files, shuffle file.
    '''

    '''
    Input explanation:

    From now on all inputs to this function will be of the following type:
    no argument provided -> error (python Shuffle.py)
    one argument provided -> error (python Shuffle.py dataset.csv)
    two arguments provided: (python Shuffle.py dataset.csv reduce100)
        "shuffle" -> runs shuffle_file(sys.argv[1])
    three arguments provided: (python Shuffle.py dataset.csv reduce 100)
    '''
    if len(sys.argv) < 2: # If no dataset is provided e.g.(python Reduce.py)
        print('USAGE: Shuffle.py (path to data file)')
        sys.exit(1)
    if len(sys.argv) < 3: # If no mode is provided e.g.(python Reduce.py dataset.csv)
        print('USAGE: Shuffle.py (mode of execution)')
        sys.exit(1)
    sample_set = sys.argv[1]
    if len(sys.argv) >= 3: # If ony one argument is provided e.g.(python Reduce.py dataset.csv reduce100)
        mode_of_execution = sys.argv[2]
        if(mode_of_execution == "shuffle"):
            shuffle_file(sample_set)

if __name__ == '__main__':
    main()
