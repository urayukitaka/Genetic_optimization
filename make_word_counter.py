from collections import Counter
import config as c


def initial_word_dict(test_names:list):

    # make initial list
    v_list = []

    for test in test_names:
        size = len(test)
        if size<=2:
            v_list.append(test)
        else:
            for i in range(2, size+1):
                v_list.append(test[:i])

    # counter
    words = dict(Counter(v_list))

    # selct over 1 time
    outwords = {}
    for k,v in words.items():
        if v>1:
            outwords[k] = v
    return outwords

def make_word_dict(test_names:list, word_dict:dict):

    # make initial list
    v_list = []

    for test in test_names:
        size = len(test)
        if size<=2:
            if test not in word_dict.keys():
                v_list.append(test)
        else:
            for i in range(2, size+1):
                v = test[:i]
                if v in word_dict.keys():
                    v = test[len(v):]
                    if len(v)!=0:
                        v_list.append(v)

    # counter
    words = dict(Counter(v_list))

    # selct over 1 time
    outwords = {}
    for k,v in words.items():
        if v>1:
            outwords[k] = v
    return outwords


if __name__ == "__main__":

    # test names
    test_names = c.name

    # make 1st dict
