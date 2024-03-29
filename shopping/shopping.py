import csv
import sys

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
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    # We will use this list as mapping for months
    MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Read data from csv file
    with open(filename) as f:
        reader = csv.DictReader(f)

        for line in reader:
            evidence_list = []
            # Convert the list of evidence values to the appropriate type and append to the evidence list
            evidence_list.append(int(line['Administrative']))
            evidence_list.append(float(line['Administrative_Duration']))
            evidence_list.append(int(line['Informational']))
            evidence_list.append(float(line['Informational_Duration']))
            evidence_list.append(int(line['ProductRelated']))
            evidence_list.append(float(line['ProductRelated_Duration']))
            evidence_list.append(float(line['BounceRates']))
            evidence_list.append(float(line['ExitRates']))
            evidence_list.append(float(line['PageValues']))
            evidence_list.append(float(line['SpecialDay']))
            evidence_list.append((MONTHS.index(line['Month'])))
            evidence_list.append(int(line['OperatingSystems']))
            evidence_list.append(int(line['Browser']))
            evidence_list.append(int(line['Region']))
            evidence_list.append(int(line['TrafficType']))
            visitor_type = 1 if line['VisitorType'] == 'Returning_Visitor' else 0
            evidence_list.append(visitor_type)
            evidence_list.append(0 if line['Weekend'] == 'FALSE' else 1)
            evidence.append(evidence_list)
            
            # Append the revenue value to 'labels'
            labels.append(0 if line['Revenue'] == 'FALSE' else 1)

    return (evidence, labels)
    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Create a KNN model
    model = KNeighborsClassifier(n_neighbors=1)
    
    # Fit model with our training data
    model.fit(evidence, labels)

    return model
    # raise NotImplementedError


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
    correct_positive = 0
    positive_labels = 0
    correct_negative = 0
    negative_labels = 0

    for i in range(len(labels)):
        label = labels[i]
        prediction = predictions[i]
        if label == 1:
            # For each positive label, check if the prediction was correct
            positive_labels += 1
            if label == prediction:
                correct_positive += 1
        elif label == 0:
            # For each negative label, check if the prediction was correct
            negative_labels += 1
            if label == prediction:
                correct_negative += 1

    sensitivity = correct_positive / positive_labels
    specificity = correct_negative / negative_labels

    return (sensitivity, specificity)
    # raise NotImplementedError


if __name__ == "__main__":
    main()
