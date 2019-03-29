import sys
import csv
import Shuffle 

def take_first_n_lines(input, number_of_lines):
	'''
	Load sample data from the given file, outputs first int(number_of_lines)
	Creates output in the format: "%s_first_%s.csv" % input, str(number_of_lines).

	Takes input: input file to divide.
	Takes number_of_lines: amount of lines in output file, excluding header.

	Returns file name.
	'''
	target_file = input.replace(".csv", "_%slines.csv" % str(number_of_lines))

	first_row = True
	number_of_lines = int(number_of_lines)

	with open(input, 'rt') as fin, open(target_file, 'w', newline='') as fout:
		cfin = csv.reader(fin)
		cfout = csv.writer(fout, delimiter=",")
		for mrow in cfin:

			if first_row: # First line is a header. Copy it but do not count
				cfout.writerow(str(elt) for elt in mrow)
				first_row = False
				continue

			number_of_lines = number_of_lines - 1
			cfout.writerow(str(elt) for elt in mrow)
			if(number_of_lines <= 0): # if we copied as many lines as the input specifies we will close the current file
				break
	return target_file

def divide_file(input, output_size):
	'''
	Load sample data from the given file, divide file, 
	Creates files in the format: "%s_part_%s.csv" % input, str(index).
	Will put header in all files.

	Takes input: input file to divide.
	Takes output_size: amount of lines in output files, excluding header.

	Returns list of file names.
	'''
	# Construct the final array as a list and then merge
	divided_files_list = []
	output_count = 0
	total_output_files = 0
	file_is_open = False
	first_row = True
	with open(input, 'rt') as fin:
		cfin = csv.reader(fin)
		for mrow in cfin:

			if first_row:# First line is a header. Save it
				header = mrow
				first_row = False
				continue

			if not file_is_open: # if no file is open we open a new file as the next part
				total_output_files = total_output_files + 1
				current_output = open(input.replace(".csv", "_part_%s.csv" % str(total_output_files)), 'w', newline='')
				file_is_open = True
				output_count = 0
				writer = csv.writer(current_output, delimiter=",")
				writer.writerow(str(elt) for elt in header)
				divided_files_list.append(current_output)


			output_count = output_count + 1
			writer.writerow(str(elt) for elt in mrow)
			if(output_count >= int(output_size)): # if we copied as many lines as the input specifies we will close the current file
				file_is_open = False
				current_output.close()
	return divided_files_list

def count_labels(input):
	'''
	Load sample data from the given file, locate labels, 
	Count each ocurrence of each label.

	Takes input: input file to divide.
	Assumes label is in position 8 (LABEL_INDEX = 8).

	Returns dictionary of label:amount.
	'''
	LABEL_INDEX = 8
	labels = dict()

	first_row = True

	with open(input, 'rt') as fin:
		cfin = csv.reader(fin)
		for mrow in cfin:

			if first_row: # First line is a header. Copy it but do not count
				first_row = False
				continue

			if str(mrow[LABEL_INDEX]) in labels:
				labels[str(mrow[LABEL_INDEX])] = labels[str(mrow[LABEL_INDEX])] + 1
			else:
				labels[str(mrow[LABEL_INDEX])] = 1
	for l in labels:
		print(l, labels[l])
	
	return labels

def remove_label(input, label_to_remove, target_file):
	'''
	Load sample data from the given file, copy contents to another file except the label to remove.

	Takes input: input file to divide.
	Takes label_to_remove: label to locate and remove from the file.
	Assumes label is in position 8 (LABEL_INDEX = 8).

	Returns dictionary of label:amount.
	'''
	LABEL_INDEX = 8
	labels = dict()

	first_row = True

	with open(input, 'rt') as fin, open(target_file, 'w', newline='') as fout:
		cfin = csv.reader(fin)
		cfout = csv.writer(fout, delimiter=",")
		for mrow in cfin:

			if first_row: # First line is a header. Copy it but do not count
				writer.writerow(str(elt) for elt in mrow)
				first_row = False
				continue

			if str(mrow[LABEL_INDEX]) == str(label_to_remove):
				continue
			else:
				writer.writerow(str(elt) for elt in mrow)
	for l in labels:
		print(l, labels[l])
	
	return labels

def main():
	'''
	Main division driver. Read in data file, divide file.
	'''

	'''
	Input explanation:

	From now on all inputs to this function will be of the following type:
	no argument provided -> error (python Reduce.py)
	one argument provided -> error (python Reduce.py dataset.csv)
	two arguments provided: (python Reduce.py dataset.csv reduce100)
		"countlables" -> runs count_labels(sys.argv[1])
	three arguments provided: (python Reduce.py dataset.csv reduce 100)
		"divide":
		    "%d" -> runs divide_file(sys.argv[1], sys.argv[3])
		"first":
		    "%d" -> runs take_first_n_lines(sys.argv[1], sys.argv[3])
	'''
	if len(sys.argv) < 2: # If no dataset is provided e.g.(python Reduce.py)
		print('USAGE: FileDivision.py (path to data file)')
		sys.exit(1)
	if len(sys.argv) < 3: # If no mode is provided e.g.(python Reduce.py dataset.csv)
		print('USAGE: FileDivision.py (mode of execution)')
		sys.exit(1)
	sample_set = sys.argv[1]
	if len(sys.argv) == 3:
		mode_of_execution = sys.argv[2]
		if(mode_of_execution == "countlables"):
			count_labels(sample_set)
	if len(sys.argv) >= 4: # If ony one argument is provided e.g.(python Reduce.py dataset.csv reduce100)
		mode_of_execution = sys.argv[2]
		in_value = sys.argv[3]
		if(mode_of_execution == "divide"):
			divide_file(sample_set, in_value)
		if(mode_of_execution == "first"):
			take_first_n_lines(sample_set, in_value)

if __name__ == '__main__':
	main()
