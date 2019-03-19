import sys
import csv

def open_and_filter_file(file_name, target_sample_rate):
    '''
    Load sample data from the given file, return the results as an NDarray.
    '''

    # For efficient subspace sampling, need a 2D NDarray. However, this causes
    # problems handling the category, because NDArrays require all entries to
    # be the same type. The solution chosen here is to map the categories to
    # float values, and use those. Need a map of the values back to the
    # categories for output, and the reverse to translate input
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




def main():
    '''
    Main reduction driver. Read in data files, read in target rate,
    reduce data to target amount
    '''
    if len(sys.argv) < 3:
        print('USAGE: ActivityClassifier.py (path to data file)')
        sys.exit(1)
    sample_set = sys.argv[1]
    target_sampling_rate = sys.argv[2]

    print('Target sample rate: ', target_sampling_rate)
    print('Reading from: ', sample_set)

    open_and_filter_file(sample_set, target_sampling_rate)

if __name__ == '__main__':
    main()
