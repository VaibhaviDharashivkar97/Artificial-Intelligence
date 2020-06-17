import pickle
import sys

import AdaBoost
import DecisionTree
from Data import Data, extractFeatures

MAX_DEPTH = 7
HYPOTHESIS_IN_ENSEMBLE = 2



def train(examples, answers, hypothesisOut, learning_type):
    if learning_type == "dt":
        listing = []
        for i in range(len(answers)):
            listing.append(Data(examples[i], answers[i]))
        tree = DecisionTree.decisionTree(listing, list(listing[0].features.keys()), [], MAX_DEPTH)
        DecisionTree.DecisionTreeNode.display(tree)
        f = open(hypothesisOut, "wb")
        pickle.dump(tree, f)
        f.close()
    elif learning_type == "ada":
        listing = []
        for i in range(len(answers)):
            listing.append(Data(examples[i], answers[i]))
        h,z = AdaBoost.train(listing, HYPOTHESIS_IN_ENSEMBLE)
        h_z = []
        h_z.append(h)
        h_z.append(z)
        f = open(hypothesisOut, "wb")
        pickle.dump(h_z, f)
        f.close()


def main():
    if sys.argv[1] == "train":
        lists = []
        answers = []
        f = open(sys.argv[2], "r")
        for line in f:
            answers.append(line[0:2])
            lists.append(line[3:].strip().split())
        train(lists, answers, sys.argv[3], sys.argv[4])
    elif sys.argv[1] == "predict":
        lists = []
        listing = []
        f = open(sys.argv[2], "rb")
        tree = pickle.load(f)
        f.close()
        file = open(sys.argv[3], "r")
        for line in file:
            lists.append(line.strip().split())
        for i in range(len(lists)):
            listing.append(extractFeatures(lists[i]))
        d = DecisionTree.DecisionTreeNode.decide(tree,listing)
        for i in d:
            print(i)
        # r = AdaBoost.predict(tree, listing)
        # for i in r:
        #     print(i)


if __name__ == '__main__':
    main()
