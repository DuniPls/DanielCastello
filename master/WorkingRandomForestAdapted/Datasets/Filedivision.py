import sys
import csv
import Shuffle 

def divide_file(input, output_size):
	'''
	Load sample data from the given file, divide file, 
	Creates files in the format: "%s_part_%s.csv" % input, str(index).
	Will put header in all files.

	Takes input: input file to divide.
	Takes output_size: amount of lines in output files, ixcluding header.

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
	print(divided_files_list)



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
		"shuffle" -> runs shuffle_file(sys.argv[1])
	three arguments provided: (python Reduce.py dataset.csv reduce 100)
	'''
	if len(sys.argv) < 2: # If no dataset is provided e.g.(python Reduce.py)
		print('USAGE: FileDivision.py (path to data file)')
		sys.exit(1)
	if len(sys.argv) < 3: # If no mode is provided e.g.(python Reduce.py dataset.csv)
		print('USAGE: FileDivision.py (mode of execution)')
		sys.exit(1)
	sample_set = sys.argv[1]
	if len(sys.argv) >= 3: # If ony one argument is provided e.g.(python Reduce.py dataset.csv reduce100)
		mode_of_execution = sys.argv[2]
		if(mode_of_execution == "divide"):
			divide_file(sample_set, 100000)

if __name__ == '__main__':
	main()
