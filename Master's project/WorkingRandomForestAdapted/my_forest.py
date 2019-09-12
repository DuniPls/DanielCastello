import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix



# File Paths
INPUT_PATH = "..\1.1_shuffled_10HZ_1000000samples.csv"
OUTPUT_PATH = "..\1.1_shuffled_10HZ_1000000samples_RESULT.csv"



def main():
    """
    Main function
    :return:
    """
    # Load the csv file into pandas dataframe
    dataset = pd.read_csv(INPUT_PATH)
    # Get basic statistics of the loaded dataset
    dataset_statistics(dataset)

if __name__ == "__main__":
    main()