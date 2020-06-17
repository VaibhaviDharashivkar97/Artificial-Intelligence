import math
import random

import DecisionTree


def weighted_majority(h, z):
    en_value = 0
    nl_value = 0
    for i in range(len(h)):
        if h[i] == 'en':
            en_value+=z[i]
        else:
            nl_value+=z[i]
    if en_value>nl_value:
        return 'en'
    else:
        return 'nl'

def predict(h_z, examples):
    res = []
    ans = []
    ada = []
    h = h_z[0]
    z = h_z[1]
    for i in h:
        d = DecisionTree.DecisionTreeNode.decide(i, examples)
        res.append(d)
    for j in range(len(res[0])):
        temp = []
        for i in range(len(res)):
            temp.append(res[i][j])
        ada.append(temp)
    for k in ada:
        ans.append(weighted_majority(k,z))
    return ans



def train(examples, K):
    h = []
    z = []
    for k in range(0, K):
        if not examples:
            return h,z
        weight = []
        for i in range(len(examples)):
            weight.append(1/len(examples))
        tree = DecisionTree.decisionTree(examples, list(examples[0].features.keys()), [], 1)
        h.append(tree)
        total_weight = 0
        error = 0.01
        for j in range(len(examples)):
            ans = DecisionTree.DecisionTreeNode.decision(tree, examples[j].features)
            if ans != examples[j].result:
                error += weight[j]
            if ans == examples[j].result:
                weight[j] = weight[j] * (error / 1-error)
        for i in range(len(examples)):
            z.append(math.log(1-error)/error)
        for i in weight:
            total_weight += i
        for i in weight:
            if i == 0 or total_weight == 0:
                i = 0
            else:
                i = i / total_weight
        dataset = []
        random_number = random.uniform(0, 1)
        sum = 0
        n = len(examples)
        while n > 0:
            for i in range(len(examples)):
                sum += weight[i]
                if sum > random_number:
                    dataset.append(examples[i])
            n -= 1
        examples = dataset
    return h,z

