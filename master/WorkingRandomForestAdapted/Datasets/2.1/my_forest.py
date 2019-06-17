import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.utils.multiclass import unique_labels

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

def one_point_three():
    print("--- Start of experiment 1.3 ---")
    for i in range(100, 101, 10):
        train_name = ("1.3_train_%dHZ.csv" % i)
        run_forest_with_test_size(train_name, 33333, True)
        run_forest_with_test_size(train_name, 0.1, False)
    print("--- End of experiment 1.3 ---")
    
def two_point_one():
    print("--- Start of experiment 2.1 ---")
    for i in range(50, 1001, 50):
        train_name = ("data_textlabels_windowed_discard_%d_extracted.csv" % i)
        run_forest(train_name)
    print("--- End of experiment 2.1 ---")

def run_forest_with_test_size(INPUT_PATH, TEST_SIZE, SIZE_OR_PERCENTAGE):
    """
    Main function
    :return:
    """
    print("Loading file :: ", INPUT_PATH)
    f=open("13_METRICS.txt", "a+")
    g=open("13_MATRICES.txt", "a+")
    f.write(INPUT_PATH + "\n")
    g.write(INPUT_PATH + "\n")
    # Load the csv file into pandas dataframe
    dataset = pd.read_csv(INPUT_PATH)
    dataset = dataset.iloc[:,[2, 3, 4, 5, 6, 7, 8]]
    labelset = dataset.iloc[:,6]
    dataset = dataset.iloc[:,[0, 1, 2, 3, 4, 5]]

    # Get basic statistics of the loaded dataset
    #dataset_statistics(train_x)
    #dataset_statistics(test_x)

    if (SIZE_OR_PERCENTAGE == True):
        percentage = float(TEST_SIZE / dataset.shape[0])
        train_x, test_x, train_y, test_y = train_test_split(dataset, labelset, test_size=percentage)
    else:
        train_x, test_x, train_y, test_y = train_test_split(dataset, labelset, test_size=float(TEST_SIZE))
    
    # Train and Test dataset size details
    print("Train_x Shape :: ", train_x.shape)
    print("Train_y Shape :: ", train_y.shape)
    print("Test_x Shape :: ", test_x.shape)
    print("Test_y Shape :: ", test_y.shape)
    f.write(str("Size\t;\t" + str(train_x.shape[0]) + "\t;\t" + str(test_x.shape[0]) + "\n"))
    g.write(str("Size\t;\t" + str(train_x.shape[0]) + "\t;\t" + str(test_x.shape[0]) + "\n"))
    # Create random forest classifier instance
    trained_model = random_forest_classifier(train_x, train_y)
    print("Trained model :: ", trained_model)

    predictions = trained_model.predict(test_x)
 
    print("Test Accuracy  :: ", accuracy_score(test_y, predictions))
    print("Test Macro Precision  :: ", precision_score(test_y, predictions, average='macro'))
    print("Test Macro Recall  :: ", recall_score(test_y, predictions, average='macro'))

    f.write(str("Metrics\t;\t" + str(accuracy_score(test_y, predictions)) + "\t;\t" +
           str(precision_score(test_y, predictions, average='macro')) + "\t;\t" +
          str(recall_score(test_y, predictions, average='macro')) + "\n"))

    print("Confusion matrix ", confusion_matrix(test_y, predictions))
    g.write(str(str(confusion_matrix(test_y, predictions)) + "\n"))

def run_forest_with_test(INPUT_PATH, TEST_PATH):
    """
    Main function
    :return:
    """
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
    #dataset_statistics(train_x)
    #dataset_statistics(test_x)
    
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
    print("Loading file :: ", INPUT_PATH)
    f=open("21_METRICS.txt", "a+")
    g=open("21_MATRICES.txt", "a+")
    f.write(INPUT_PATH + "\n")
    g.write(INPUT_PATH + "\n")
    # Load the csv file into pandas dataframe
    dataset = pd.read_csv(INPUT_PATH)
    dataset = dataset.iloc[:,[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                             21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 
                             38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 
                             55, 56, 57, 58, 59, 60, 61, 62]]
    labelset = dataset.iloc[:,60]
    dataset = dataset.iloc[:,[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                             21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 
                             38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 
                             55, 56, 57, 58, 59]]

    train_x, test_x, train_y, test_y = train_test_split(dataset, labelset, test_size=0.33)
     
    # Train and Test dataset size details
    print("Train_x Shape :: ", train_x.shape)
    print("Train_y Shape :: ", train_y.shape)
    print("Test_x Shape :: ", test_x.shape)
    print("Test_y Shape :: ", test_y.shape)
    f.write(str("Size\t;\t" + str(train_x.shape[0]) + "\t;\t" + str(test_x.shape[0]) + "\n"))
    g.write(str("Size\t;\t" + str(train_x.shape[0]) + "\t;\t" + str(test_x.shape[0]) + "\n"))
    # Create random forest classifier instance
    trained_model = random_forest_classifier(train_x, train_y)
    print("Trained model :: ", trained_model)

    predictions = trained_model.predict(test_x)
 
    print("Test Accuracy  :: ", accuracy_score(test_y, predictions))
    print("Test Macro Precision  :: ", precision_score(test_y, predictions, average='macro'))
    print("Test Micro Precision  :: ", precision_score(test_y, predictions, average='micro'))
    print("Test Macro Recall  :: ", recall_score(test_y, predictions, average='macro'))
    print("Test Micro Recall  :: ", recall_score(test_y, predictions, average='micro'))
    
    f.write(str("Metrics\t;\t" + str(accuracy_score(test_y, predictions)) + "\t;\t" +
           str(precision_score(test_y, predictions, average='macro')) + "\t;\t" +
          str(recall_score(test_y, predictions, average='macro')) + "\n"))

    print("Confusion matrix ", confusion_matrix(test_y, predictions))
    g.write(str(str(confusion_matrix(test_y, predictions)) + "\n"))
    f.close()
    g.close()

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
    two_point_one()
if __name__ == "__main__":
    main()
