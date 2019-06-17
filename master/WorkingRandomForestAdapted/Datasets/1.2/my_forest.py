import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.utils.multiclass import unique_labels

# File Paths
FEATURE_HEADERS_START = 0
FEATURE_HEADERS_END = 5
TARGET_HEADERS = 6

def dataset_statistics(dataset):
    """
    Basic statistics of the dataset
    :param dataset: Pandas dataframe
    :return: None, print the basic statistics of the dataset
    """
    print(dataset.describe())

def random_forest_classifier(features, target):
    """
    To train the random forest classifier with features and target data
    :param features:
    :param target:
    :return: trained random forest classifier
    """
    clf = RandomForestClassifier(n_estimators = 32)
    clf.fit(features, target)
    return clf

def one_point_one():
    print("--- Start of experiment 1.1 ---")
    for i in range(10, 101, 10):
        name = ("1.1_shuffled_%dHZ_1000000samples.csv" % i)
        run_forest(name)
    print("--- End of experiment 1.1 ---")

def one_point_two():
    print("--- Start of experiment 1.2 ---")
    train_name = "1.2_train.csv"
    for i in range(1, 10, 1):
        test_name = ("1.2_test_0,%dHZ.csv" % i)
        run_forest_with_test(train_name, test_name)
    print("--- End of experiment 1.2 ---")

def run_forest_with_test(INPUT_PATH, TEST_PATH):
    """
    Main function
    :return:
    """
    # Headers 
    headers = ["x_back","y_back","z_back","x_thigh","y_thigh","z_thigh","label"]
    print("Loading file :: ", INPUT_PATH)
    # Load the csv file into pandas dataframe
    dataset = pd.read_csv(INPUT_PATH)
    dataset = dataset.iloc[:,[2, 3, 4, 5, 6, 7, 8]]
    train_y = dataset.iloc[:,6]
    train_x = dataset.iloc[:,[0, 1, 2, 3, 4, 5]]
    # Load the csv file into pandas dataframe
    dataset = pd.read_csv(TEST_PATH)
    dataset = dataset.iloc[:,[2, 3, 4, 5, 6, 7, 8]]
    test_y = dataset.iloc[:,6]
    test_x = dataset.iloc[:,[0, 1, 2, 3, 4, 5]]

    # Get basic statistics of the loaded dataset
    dataset_statistics(train_x)
    dataset_statistics(test_x)
    
    # Train and Test dataset size details
    print("Train_x Shape :: ", train_x.shape)
    print("Train_y Shape :: ", train_y.shape)
    print("Test_x Shape :: ", test_x.shape)
    print("Test_y Shape :: ", test_y.shape)
    # Create random forest classifier instance
    trained_model = random_forest_classifier(train_x, train_y)
    print("Trained model :: ", trained_model)

    predictions = trained_model.predict(test_x)
 
    print("Test Accuracy  :: ", accuracy_score(test_y, predictions))
    print("Test Macro Precision  :: ", precision_score(test_y, predictions, average='macro'))
    #print("Test Micro Precision  :: ", precision_score(test_y, predictions, average='micro'))
    print("Test Macro Recall  :: ", recall_score(test_y, predictions, average='macro'))
    #print("Test Micro Recall  :: ", recall_score(test_y, predictions, average='micro'))
    print("Test Macro F1  :: ", f1_score(test_y, predictions, average='macro'))
    print("Confusion matrix ", confusion_matrix(test_y, predictions))

def run_forest(INPUT_PATH):
    """
    Main function
    :return:
    """
    # Headers 
    headers = ["x_back","y_back","z_back","x_thigh","y_thigh","z_thigh","label"]
    print("Loading file :: ", INPUT_PATH)
    # Load the csv file into pandas dataframe
    dataset = pd.read_csv(INPUT_PATH)
    dataset = dataset.iloc[:,[2, 3, 4, 5, 6, 7, 8]]
    labelset = dataset.iloc[:,6]
    dataset = dataset.iloc[:,[0, 1, 2, 3, 4, 5]]

    # Get basic statistics of the loaded dataset
    dataset_statistics(dataset)
    dataset_statistics(labelset)
    
    train_x, test_x, train_y, test_y = train_test_split(dataset, labelset, test_size=0.33)
     
    # Train and Test dataset size details
    print("Train_x Shape :: ", train_x.shape)
    print("Train_y Shape :: ", train_y.shape)
    print("Test_x Shape :: ", test_x.shape)
    print("Test_y Shape :: ", test_y.shape)
    # Create random forest classifier instance
    trained_model = random_forest_classifier(train_x, train_y)
    print("Trained model :: ", trained_model)

    predictions = trained_model.predict(test_x)
 
    print("Test Accuracy  :: ", accuracy_score(test_y, predictions))
    print("Test Macro Precision  :: ", precision_score(test_y, predictions, average='macro'))
    print("Test Micro Precision  :: ", precision_score(test_y, predictions, average='micro'))
    print("Test Macro Recall  :: ", recall_score(test_y, predictions, average='macro'))
    print("Test Micro Recall  :: ", recall_score(test_y, predictions, average='micro'))
    print("Confusion matrix ", confusion_matrix(test_y, predictions))

'''
def main():
    """
    Main function
    :return:
    """
    INPUT_PATH = "1.2_train.csv"
    # Headers 
    headers = ["x_back","y_back","z_back","x_thigh","y_thigh","z_thigh","label"]

    # Load the csv file into pandas dataframe
    dataset = pd.read_csv(INPUT_PATH)
    #print(dataset.head())
    #print(dataset.shape)
    dataset = dataset.iloc[:,[2, 3, 4, 5, 6, 7, 8]]
    #print(dataset.head())
    #print(dataset.shape)
    labelset = dataset.iloc[:,6]
    #print(labelset.head())
    #print(labelset.shape)
    dataset = dataset.iloc[:,[0, 1, 2, 3, 4, 5]]
    #print(dataset.head())
    #print(dataset.shape)

    # Get basic statistics of the loaded dataset
    dataset_statistics(dataset)
    dataset_statistics(labelset)
    
    train_x, test_x, train_y, test_y = train_test_split(dataset, labelset, test_size=0.33)
    
    # Train and Test dataset size details
    print("Train_x Shape :: ", train_x.shape)
    print("Train_y Shape :: ", train_y.shape)
    print("Test_x Shape :: ", test_x.shape)
    print("Test_y Shape :: ", test_y.shape)
    # Create random forest classifier instance
    trained_model = random_forest_classifier(train_x, train_y)
    print("Trained model :: ", trained_model)

    predictions = trained_model.predict(test_x)

 
    print("Test Accuracy  :: ", accuracy_score(test_y, predictions))
    print("Test Precision  :: ", precision_score(test_y, predictions))
    print("Test Recall  :: ", recall_score(test_y, predictions))
    print([unique_labels(test_y, predictions)])
    print("Confusion matrix ", confusion_matrix(test_y, predictions))
'''


def main():
    one_point_two()
if __name__ == "__main__":
    main()
