from operator import itemgetter
#this functionality is NOT needed. It may help slightly, but you can definitely ignore it completely.
tag_list = ['C', 'D', 'E', 'F', 'I', 'J', 'L', 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W','#','###','***',',', '.','`', ':', '-', "'", '$']
#laplace smoothing
smooth_factor = 0.0002
count_dict = {}


def unique_list(seq, idgetter=None):
   if idgetter is None:
       def idgetter(x): return x
   saw = {}
   ans = []
   for item in seq:
       marker = idgetter(item)
       if marker in saw: continue
       saw[marker] = 1
       ans.append(item)
   return ans
#DO NOT CHANGE!
def read_train_file():
    '''
    HELPER function: reads the training files containing the words and corresponding tags.
    Output: A tuple containing 'words' and 'tags'
    'words': This is a nested list - a list of list of words. See it as a list of sentences, with each sentence itself being a list of its words.
    For example - [['A','boy','is','running'],['Pick','the','red','cube'],['One','ring','to','rule','them','all']]
    'tags': A nested similar to above, just the corresponding tags instead of words.
    '''
    f = open('train','r')
    words = []
    tags = []
    lw = ['###']
    lt = ['###']
    for line in f:
        s = line.rstrip('\n')
        w,t= s.split('/')[0],s.split('/')[1]
        if w=='###':
            lw.append('***')
            lt.append('***')
            words.append(lw)
            tags.append(lt)
            lw=['###']
            lt=['###']
        else:
            lw.append(w)
            lt.append(t)
    words = words[1:]
    tags = tags[1:]
    assert len(words) == len(tags)
    f.close()
    return (words,tags)




#print(read_train_file()[1])
'''for tag in tag_list:
    for sentence_tags in read_train_file()[1]:
        if sentence_tags[1] == tag:
            prior_prob[i] += 1
    i += 1
no_of_sentences = len(read_train_file()[1])
for element in prior_prob:
    element = element/no_of_sentences
print(prior_prob)'''


#NEEDS TO BE FILLED!
def train_func(train_list_words, train_list_tags):

    '''
    This creates dictionaries storing the transition and emission probabilities - required for running Viterbi.
    INPUT: The nested list of words and corresponding nested list of tags from the TRAINING set. This passing of correct lists and calling the function
    has been done for you. You only need to write the code for filling in the below dictionaries. (created with bigram-HMM in mind)
    OUTPUT: The two dictionaries

    HINT: Keep in mind the boundary case of the starting POS tag. You may have to choose (and stick with) some starting POS tag to compute bigram probabilities
    for the first actual POS tag.
    '''


    dict2_tag_follow_tag= {}
    """Nested dictionary to store the transition probabilities
    each tag X is a key of the outer dictionary with an inner dictionary as the corresponding value
    The inner dictionary's key is the tag Y following X
    and the corresponding value is the number of times Y follows X - convert this count to probabilities finally before returning
    """
    dict2_word_tag = {}
    """Nested dictionary to store the emission probabilities.
    Each word W is a key of the outer dictionary with an inner dictionary as the corresponding value
    The inner dictionary's key is the tag X of the word W
    and the corresponding value is the number of times X is a tag of W - convert this count to probabilities finally before returning
    """


    #      *** WRITE YOUR CODE HERE ***

    for tag in tag_list:
        dict2_tag_follow_tag[tag] = dict()
    for k,v in dict2_tag_follow_tag.items():
        for tag in tag_list:
            v[tag] = 0
    for tag in tag_list:
        count_dict[tag] = 0
    for sentence_tags in train_list_tags:
        i = 0
        while i < len(sentence_tags)-1:
            dict2_tag_follow_tag[sentence_tags[i]][sentence_tags[i+1]] += 1
            i += 1
    for sentence_tags in train_list_tags:
        for tag in sentence_tags:
            count_dict[tag] += 1
    length = len(tag_list)
    for k,v in dict2_tag_follow_tag.items():
        for tag in tag_list:
            v[tag] = (v[tag]+smooth_factor)/(count_dict[k]+smooth_factor*length)



    words_temp = []

    for sentence_words in train_list_words:
        words_temp = words_temp + sentence_words
    words_temp = unique_list(words_temp)

    for word in words_temp:
        dict2_word_tag[word] = {}
    for key in dict2_word_tag.keys():
        for tag in tag_list:
            dict2_word_tag[key][tag] = 0
    j = 0


    for sentence_words in train_list_words:
        i =  0
        while i<len(sentence_words) :
            eword = sentence_words[i]
            etag =  train_list_tags[j][i]
            dict2_word_tag[eword][etag] += 1
            i += 1
        j += 1


    for word in words_temp:
        for tag in count_dict.keys():
            dict2_word_tag[word][tag] = (dict2_word_tag[word][tag]+smooth_factor)/(count_dict[tag]+smooth_factor*length)

















    # END OF YOUR CODE
    return (dict2_tag_follow_tag, dict2_word_tag)



#NEEDS TO BE FILLED!
def assign_POS_tags(test_words, dict2_tag_follow_tag, dict2_word_tag):

    '''
    This is where you write the actual code for Viterbi algorithm.
    INPUT: test_words - this is a nested list of words for the TEST set
           dict2_tag_follow_tag - the transition probabilities (bigram), filled in by YOUR code in the train_func
           dict2_word_tag - the emission probabilities (bigram), filled in by YOUR code in the train_func
    OUTPUT: a nested list of predicted tags corresponding to the input list test_words. This is the 'output_test_tags' list created below, and returned after your code
    ends.

    HINT: Keep in mind the boundary case of the starting POS tag. You will have to use the tag you created in the previous function here, to get the
    transition probabilities for the first tag of sentence...
    HINT: You need not apply sophisticated smoothing techniques for this particular assignment.
    If you cannot find a word in the test set with probabilities in the training set, simply tag it as 'N'.
    So if you are unable to generate a tag for some word due to unavailibity of probabilities from the training set,
    just predict 'N' for that word.

    '''



    output_test_tags = []    #list of list of predicted tags, corresponding to the list of list of words in Test set (test_words input to this function)


    #      *** WRITE YOUR CODE HERE ***
    '''
        greedy algorithm
    for sentence in test_words:
        pi = 1
        previous_tag = '###'
        temp_list = []
        for word in sentence:
            current_tag = '###'
            temp_prob = 0
            for tag in tag_list:
                if word in dict2_word_tag:
                    emission_prob = dict2_word_tag[word][tag]
                else:
                    emission_prob = smooth_factor/(count_dict[tag]+smooth_factor*len(tag_list))
                if tag in dict2_tag_follow_tag[previous_tag]:
                    transition_prob = dict2_tag_follow_tag[previous_tag][tag]
                else:
                    transition_prob = (smooth_factor)/(count_dict[previous_tag]+smooth_factor*len(tag_list))
                if temp_prob < pi*emission_prob*transition_prob:
                    temp_prob = pi*emission_prob*transition_prob
                    current_tag = tag
            pi = temp_prob
            previous_tag=current_tag
            temp_list.append(previous_tag)
        output_test_tags.append(temp_list)'''
    #dynamic programming

    for sentence in test_words:
        sen_list = []
        sentence.append('***')
        sen_list.append({'###' : ['###',1]})
        i=1
        for word in sentence:
            sen_list.append({})
            for tag in tag_list:
                sen_list[i][tag] = ['',0]
                for prev_tag, state in sen_list[i-1].items():
                    if word in dict2_word_tag:
                        emission_prob = dict2_word_tag[word][tag]
                    else:
                        emission_prob = (smooth_factor/(count_dict[tag]+(smooth_factor*len(tag_list))))
                    if tag in dict2_tag_follow_tag[prev_tag]:
                        transition_prob = dict2_tag_follow_tag[prev_tag][tag]
                    else:
                        transition_prob = (smooth_factor)/(count_dict[prev_tag]+(smooth_factor*len(tag_list)))
                    vari = state[1]*emission_prob*transition_prob
                    if sen_list[i][tag][1] < vari:
                        sen_list[i][tag][1] = vari
                        sen_list[i][tag][0] = prev_tag
            i += 1
        max = 0
        final_tag = ''
        for tag, value in sen_list[i-1].items():
            if value[1] > max :
                max = value[1]
                final_tag  = value[0]
        final_tag_list = [final_tag]
        i = i-2
        while i > 1:
            final_tag = sen_list[i][final_tag][0]
            final_tag_list.append(final_tag)
            i = i-1

        final_tag_list.reverse()
        output_test_tags.append(final_tag_list)
    #print(len(output_test_tags))


    # END OF YOUR CODE

    return output_test_tags









# DO NOT CHANGE!
def public_test(predicted_tags):
    '''
    HELPER function: Takes in the nested list of predicted tags on test set (prodcuced by the assign_POS_tags function above)
    and computes accuracy on the public test set. Note that this accuracy is just for you to gauge the correctness of your code.
    Actual performance will be judged on the full test set by the TAs, using the output file generated when your code runs successfully.
    '''

    f = open('test_public_labeled','r')
    words = []
    tags = []
    lw = []
    lt = []
    for line in f:
        s = line.rstrip('\n')
        w,t= s.split('/')[0],s.split('/')[1]
        if w=='###':
            words.append(lw)
            tags.append(lt)
            lw=[]
            lt=[]
        else:
            lw.append(w)
            lt.append(t)
    words = words[1:]
    tags = tags[1:]
    assert len(words) == len(tags)
    f.close()
    public_predictions = predicted_tags[:len(tags)]
    assert len(public_predictions)==len(tags)

    correct = 0
    total = 0
    flattened_actual_tags = []
    flattened_pred_tags = []
    for i in range(len(tags)):
        x = tags[i]
        y = public_predictions[i]
        if len(x)!=len(y):
            print(i)
            print(x)
            print(y)
            break
        flattened_actual_tags+=x
        flattened_pred_tags+=y
    assert len(flattened_actual_tags)==len(flattened_pred_tags)
    correct = 0.0
    for i in range(len(flattened_pred_tags)):
        if flattened_pred_tags[i]==flattened_actual_tags[i]:
            correct+=1.0
    print('Accuracy on the Public set = '+str(correct/len(flattened_pred_tags)))



# DO NOT CHANGE!
def evaluate():
    words_list_train = read_train_file()[0]
    tags_list_train = read_train_file()[1]

    dict2_tag_tag = train_func(words_list_train,tags_list_train)[0]
    dict2_word_tag = train_func(words_list_train,tags_list_train)[1]

    f = open('test_full_unlabeled','r')

    words = []
    l=[]
    for line in f:
        w = line.rstrip('\n')
        if w=='###':
            words.append(l)
            l=[]
        else:
            l.append(w)
    f.close()
    words = words[1:]
    test_tags = assign_POS_tags(words, dict2_tag_tag, dict2_word_tag)
    assert len(words)==len(test_tags)

    public_test(test_tags)

    #create output file with all tag predictions on the full test set

    f = open('output','w')
    f.write('###/###\n')
    for i in range(len(words)):
        sent = words[i]
        pred_tags = test_tags[i]
        for j in range(len(sent)-1):
            word = sent[j]
            pred_tag = pred_tags[j]
            f.write(word+'/'+pred_tag)
            f.write('\n')
        f.write('###/###\n')
    f.close()

    print('OUTPUT file has been created')

if __name__ == "__main__":
    evaluate()
