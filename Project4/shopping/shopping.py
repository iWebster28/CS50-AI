import csv
import sys
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - 0. Administrative, an integer
        - 1. Administrative_Duration, a floating point number
        - 2. Informational, an integer
        - 3. Informational_Duration, a floating point number
        - 4. ProductRelated, an integer
        - 5. ProductRelated_Duration, a floating point number
        - 6. BounceRates, a floating point number
        - 7. ExitRates, a floating point number
        - 8. PageValues, a floating point number
        - 9. SpecialDay, a floating point number
        - 10. Month, an index from 0 (January) to 11 (December)
        - 11. OperatingSystems, an integer
        - 12. Browser, an integer
        - 13. Region, an integer
        - 14. TrafficType, an integer
        - 15. VisitorType, an integer 0 (not returning) or 1 (returning)
        - 16. Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    
    data = []
    evidence = []
    labels = []
    fields = {}

    # Read all rows of csv into data list
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row) 

    data_np = np.array(data)

    # Dictionary for accessing fields mor easily
    for i in range(len(data_np[0, :])):
        fields[data_np[0, i]] = i # Enable dictionary behaviour with np array

    # print(fields)
    # print(labels)
    # print(evidence)

    # Ensure correct types

    # Enumerate months from 0-11 (Jan-Dec)
    months = ["Jan", "Feb", "Mar", "Apr", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for row in range(1, len(data_np[:, fields["Month"]])):
        # print(data_np[row, fields["Month"]])
        data_np[row, fields["Month"]] = months.index(data_np[row, fields["Month"]])

    # Set visitor types to 0 (false) or 1 (true)
    data_np[data_np == "Returning_Visitor"] = 1
    data_np[data_np == "New_Visitor"] = 0
    data_np[data_np == "Other"] = 0

    # print('VisitorType', data_np[1:, fields["VisitorType"]])

    # Set TRUE/FALSE to 0/1
    data_np[data_np == "TRUE"] = 1
    data_np[data_np == "FALSE"] = 0

    # Assert VisitorType, Weekend and Revenue are all ints (should be 0/1)
    other_cols = ["VisitorType", "Weekend", "Revenue"]
    for col in other_cols:
        # print(col, data_np[1:, fields[col]])
        data_np[1:, fields[col]] = data_np[1:, fields[col]].astype(int, copy = False)

    # Assert ints
    int_cols = ["Administrative", "Informational", "ProductRelated", "Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend"]
    for col in int_cols:
        # print(col, data_np[1:, fields[col]])
        data_np[1:, fields[col]] = data_np[1:, fields[col]].astype(int, copy = False)

    # Assert floats
    float_cols = ["Administrative_Duration", "Informational_Duration", "ProductRelated_Duration", "BounceRates", "ExitRates", "PageValues", "SpecialDay"]
    for col in float_cols:
        # print(data_np[1:, fields[col]])
        data_np[1:, fields[col]] = data_np[1:, fields[col]].astype(float, copy = False)    

    evidence = data_np[1:, 0:17] #"1" to omit row headers
    labels = data_np[1:, 17] # last col is labels

    # print(evidence[0])
    # print(labels[0])

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    




def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    




if __name__ == "__main__":
    main()
