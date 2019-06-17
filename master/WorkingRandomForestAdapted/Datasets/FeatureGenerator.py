import sys
import csv
import math

START_COLUMN_INDEX = 2
COLUMN_WIDTH = 5

# TIME-DOMAIN

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

# FREQUENCY-DOMAIN

def return_spectral_entropy(input_matrix):
    '''
    Takes a one-dimentional array of values and returns the spectral entropy

    Returns a float representing the SE of the input_matrix
    '''

    output_matrix = []
    output = 0.0
    for num in input_matrix:
        output += math.pow(num, 2)
        
    for num_in in input_matrix:
        output_matrix.append(math.pow(num_in, 2)/output)

    output = 0.0
    for num in output_matrix:
        output += num*math.log(num)
    return (output*-1)

def return_spectral_centroid(input_matrix1, input_matrix2):
    '''
    Takes two one-dimentional array of values and returns the spectral centroid

    Returns a float representing the SC of the two input_matrix
    '''

    output1 = 0.0
    for num in input_matrix1:
        output1 += num
        
    output2 = 0.0
    for num1, num2 in zip(input_matrix1, input_matrix2):
        output2 += num1*num2

    return ooutput1/output2

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

def experimenttwotwo():
    for i in range(2, 101, 1):
        input = ("2.2_%dHZ_windowed_discard_.csv" % i)
        input = input.replace(".csv", "%d.csv" % int(i * 1.5))
        extract_all_data(input)

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
		"countlabels" -> runs count_labels(sys.argv[1])
	three arguments provided: (python Reduce.py dataset.csv reduce 100)
		"divide":
		    "%d" -> runs divide_file(sys.argv[1], sys.argv[3])
		"first":
		    "%d" -> runs take_first_n_lines(sys.argv[1], sys.argv[3])
        "remove":
		    "%s" -> runs remove_label(sys.argv[1], sys.argv[3], )
    four arguments provided: (python Reduce.py dataset.csv substitute sitting laying)
		"substitute":
		    "%d" -> runs substitute_label(sys.argv[1], sys.argv[3], sys.argv[4])
	'''
	if len(sys.argv) < 2: # If no dataset is provided e.g.(python Reduce.py)
		print('USAGE: FileDivision.py (path to data file)')
		sys.exit(1)
	sample_set = sys.argv[1]
	if len(sys.argv) < 3: # If no mode is provided e.g.(python Reduce.py dataset.csv)
		mode_of_execution = sys.argv[1]
		if(mode_of_execution == "twotwo"):
			experimenttwotwo()
		else:
			print('Extracting the following features:')
			extract_all_data(sample_set)

if __name__ == '__main__':
	main()
