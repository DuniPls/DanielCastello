import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import csv
import math

def take_array_from_file(file_name, x_pos = 2, y_pos = 4, amount = 10000, start = 1):
    
    array = []

    DATA_START_INDEX = x_pos
    DATA_END_INDEX = y_pos
    DATA_SIZE = amount

    with open(file_name, 'rt') as fin:
        cfin = csv.reader(fin)
        data_amount = 0
        skip_amount = 0
        first_row = True
        for mrow in cfin:
            if skip_amount < start: # First line is a header, skip it as well as many lines as stated
                skip_amount += 1
                continue

            data_amount += 1
            if data_amount >= DATA_SIZE:
                break

            vec = []
            for i in range(DATA_START_INDEX, DATA_END_INDEX + 1):
                vec.append(float(mrow[i]))

            array.append(vec)

    return array

def plot_3D_vec_array(array):
    '''
    Takes a 3D vector array and plots each vector for 0.01s
    '''

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    for arr in array:
        x = arr[0]
        y = arr[1]
        z = arr[2]
        arrow = [x, y, z]
        origin = [0, 0, 0]
        X, Y, Z = zip(origin) 
        U, V, W = zip(arrow)
        ax.quiver(X,Y,Z,U,V,W)
        ax.set_xlim([10, -10])
        ax.set_ylim([10, -10])
        ax.set_zlim([10, -10])
        plt.draw()
        plt.pause(0.01)
        ax.cla()

def main():
	'''
	Main division driver. Read in data file, plot it.
	'''

	'''
	Input explanation:

	From now on all inputs to this function will be of the following type:
	no argument provided -> error (python Reduce.py)
	one argument provided -> error (python Reduce.py dataset.csv)
	two arguments provided: (python Reduce.py dataset.csv reduce100)
		"plot" -> runs plot_3D_vec_array(the data array extracted from the input file)
	'''
	if len(sys.argv) < 2: # If no dataset is provided e.g.(python Reduce.py)
		print('USAGE: DataVisualizer.py (path to data file)')
		sys.exit(1)
	if len(sys.argv) < 3: # If no mode is provided e.g.(python Reduce.py dataset.csv)
		print('USAGE: DataVisualizer.py (mode of execution)')
		sys.exit(1)
	sample_set = sys.argv[1]
	if len(sys.argv) == 3:
		mode_of_execution = sys.argv[2]
		if(mode_of_execution == "plot"):
			plot_3D_vec_array(take_array_from_file(sample_set, amount = 400, start = 3713434))


if __name__ == '__main__':
	main()