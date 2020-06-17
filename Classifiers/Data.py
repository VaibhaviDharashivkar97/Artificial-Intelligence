def extractFeatures(line_list):
    dict = {
        "contains_a": contains_word(line_list, 'a'),
        "contains_the": contains_word(line_list, 'the'),
        "contains_of": contains_word(line_list, 'of'),
        "contains_and": contains_word(line_list, 'and'),
        "contains_in": contains_word(line_list, 'in'),
        "contains_een": contains_word(line_list, 'een'),
        "contains_het": contains_word(line_list, 'het'),
        "contains_de": contains_word(line_list, 'de'),
        "contains_substring_aa": contains_substring(line_list, 'aa'),
        "contains_substring_en": contains_substring(line_list, 'en')
    }

    return dict


def contains_substring(line_list, word):
    for i in line_list:
        if word in i:
            return True
    return False


def contains_word(line_list, word):
    for i in line_list:
        if i == word:
            return True
    return False



class Data:
    def __init__(self, line_list, result):
        self.line_list = line_list
        self.result = result
        self.features = extractFeatures(line_list)