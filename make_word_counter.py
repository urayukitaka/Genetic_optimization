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


def make_list_words(test_name:str, word_dict:dict):

    # initialize output
    out = []
    v = test_name

    while len(v)!=0:

        # flag, cut off by dictionary
        flg = 0

        # reverse v
        for i in reversed(range(2, len(v)+1)):
            # if word from 1st, append to dictionary
            if v[:i] in word_dict.keys():
                out.append(v[:i])
                # update v, backword of word
                v = v[i:]
                # flg
                flg = 1

        # if flag is 1, go to next loop
        if flg==1:
            pass
        else:
            # if whole v is in dictionary, append to dict and break
            if v in word_dict.keys():
                out.append(v)
                break
            # elif v is not in dictionary, and data is exist, append 1st word and update to backword of wrod
            elif (v not in word_dict.keys()) & (len(v)!=0):
                out = out + list(v[0])
                v = v[1:]
            elif len(v)==0:
                break

    return out


＃ for debug
if __name__ == "__main__":

    # test names
    test_names = c.name

    # make 1st dict
    dict1st = initial_word_dict(test_names=test_names)
    # 2nd dict
    dict2nd = make_word_dict(test_names=test_names, word_dict=dict1st)

    # word dict
    word_dict = dict1st | dict2nd

    print("Result of word dict")
    print(word_dict)
    print("")

    # make list of word
    word_lists = [make_list_words(test_name=test_name, word_dict=word_dict) for test_name in test_names]
    print("Result of word list")
    print(word_lists)
