from math import log2


def decisionTree(listing, features, parent_examples, max_depth):
    l = len(listing)
    if l == 0:
        en_values, ln_values = pluralityValue(parent_examples)
        if en_values > ln_values:
            return DecisionTreeNode('en', True)
        else:
            return DecisionTreeNode('nl', True)
    elif check_classification(listing, features):
        return DecisionTreeNode(listing[0].result, True)
    elif len(features) == 0:
        en_values, ln_values = pluralityValue(listing)
        if en_values > ln_values:
            return DecisionTreeNode('en', True)
        else:
            return DecisionTreeNode('nl', True)
    elif max_depth == 0:
        en_values, ln_values = pluralityValue(listing)
        if en_values > ln_values:
            return DecisionTreeNode('en', True)
        else:
            return DecisionTreeNode('nl', True)
    else:
        attribute, children = final_decision(listing, features)
        r = DecisionTreeNode(attribute, False)

        for c in children:
            new_features = []
            new_listing = []
            for i in features:
                if i != attribute:
                    new_features.append(i)
            for i in children[c]:
                new_listing.append(i)
            subTree = decisionTree(new_listing, new_features, listing, max_depth -1)
            r.child[c] = subTree
        return r


def pluralityValue(listing):
    en_values = 0
    ln_values = 0
    for i in listing:
        if i.result == 'en':
            en_values += 1
        else:
            ln_values += 1

    return en_values, ln_values


def check_classification(listing, features):
    for i in range(1, len(listing)):
        if listing[i].result != listing[0].result:
            return False
    return True


def final_decision(listing, attributes):
    children = {}
    list_true = []
    list_false = []
    feature = gain(listing, attributes)
    for i in listing:
        if i.features.get(feature) == True:
            list_true.append(i)
        elif i.features.get(feature) == False:
            list_false.append(i)
    children[True] = list_true
    children[False] = list_false
    return feature, children


# def entropy_overall(listing):
#     en_values, ln_values = pluralityValue(listing)
#     en_values = en_values / len(listing)
#     ln_values = ln_values / len(listing)
#     return -(en_values * log2(en_values) + ln_values * log2(ln_values))

def gain(listing, features):
    # entropy_values = {}
    # Remainder = {}
    Gain = {}
    en_values, ln_values = pluralityValue(listing)
    en_values = en_values / len(listing)
    ln_values = ln_values / len(listing)
    entropy_overall = -(en_values * log2(en_values) + ln_values * log2(ln_values))
    for i in features:
        false_values = []
        true_values = []
        for j in listing:
            if j.features.get(i) == False:
                false_values.append(j.result)
            elif j.features.get(i) == True:
                true_values.append(j.result)
        f_value = 0.0
        t_value = 0.0
        falseCount_en = 0.0
        falseCount_nl = 0.0
        trueCount_en = 0.0
        trueCount_nl = 0.0
        if len(false_values) > 0:
            falseCount_en = false_values.count("en") / len(false_values)
            falseCount_nl = false_values.count("nl") / len(false_values)
        if len(true_values) > 0:
            trueCount_en = true_values.count("en") / len(true_values)
            trueCount_nl = true_values.count("nl") / len(true_values)
        if falseCount_en != 0.0 and falseCount_nl != 0.0:
            f_value = -((falseCount_en * log2(falseCount_en)) + (falseCount_nl * log2(falseCount_nl)))
        else:
            f_value = 0.0
        if trueCount_en != 0.0 and trueCount_nl != 0.0:
            t_value = -((trueCount_en * log2(trueCount_en)) + (trueCount_nl * log2(trueCount_nl)))
        else:
            t_value = 0.0
        if falseCount_en == 0.0 and falseCount_nl!= 0.0:
            f_value = falseCount_nl * log2(falseCount_nl)
        if falseCount_nl == 0.0 and falseCount_en!= 0.0:
            f_value = falseCount_en * log2(falseCount_en)
        if trueCount_en == 0.0 and trueCount_nl!= 0.0:
            t_value = trueCount_nl * log2(trueCount_nl)
        if trueCount_nl == 0.0 and trueCount_en!= 0.0:
            t_value = trueCount_en * log2(trueCount_en)
        # entropy_values[i] = [f_value, t_value]
        r_value = ((true_values.count("en") + true_values.count("nl")) / len(listing) * t_value) + \
                  ((false_values.count("en") + false_values.count("nl")) / len(listing) * f_value)
        # Remainder[i] = r_value
        g_value = entropy_overall - r_value
        Gain[i] = g_value

    return list(Gain.keys())[list(Gain.values()).index(max(Gain.values()))]


class DecisionTreeNode:
    def __init__(self, question, end):
        self.question = question
        self.child = {}
        self.end = end


    def parse(self):
        node = self
        print( ""+node.question+"--->")
        if node.child[True].end == True:
            print( " True: "+node.child[True].question)
        if node.child[True].end == False:
            print(" True: ")
            DecisionTreeNode.parse(node.child[True])
        if node.child[False].end == True:
            print( " False: " + node.child[False].question)
        if node.child[False].end == False:
            print(" False: ")
            DecisionTreeNode.parse(node.child[False])
        return

    def display(self):
        node = self
        print(str(node.question))
        for key in node.child:
            print(str(key) + " = " + str(node.child[key].question))
        for key in node.child:
            DecisionTreeNode.display(node.child[key])

    def stump(self, listing):
        answers = []
        for i in listing:
            d = DecisionTreeNode.decision(self, i.features)
            if d == None:
                answers.append('nl')
            answers.append(d)
        return answers

    def decide(self, listing):
        answers = []
        for i in listing:
            d = DecisionTreeNode.decision(self,i)
            if d == None:
                answers.append('nl')
            answers.append(d)
        return answers


    def decision(self,dict):
        node = self
        while bool (node.child):
            if dict.get(node.question) == False:
                temp = node.child[False]
                if temp.end == True:
                    return temp.question
                else:
                    node = temp
                    continue
            elif dict.get(node.question) == True:
                temp = node.child[True]
                if temp.end == True:
                    return temp.question
                else:
                    node = temp
                    continue

