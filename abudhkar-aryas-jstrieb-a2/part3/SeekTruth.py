# SeekTruth.py : Classify text objects into two categories
#
# Authors: Primary:   Aishwarya Budhkar (abudhkar)
#          Secondary: Jacob Striebel    (jstrieb)
#                     Shubhavi Arya     (aryas)
#
# Based on skeleton code by D. Crandall, October 2021
#

import sys
import re
import numpy as np

def load_file(filename):
    objects=[]
    labels=[]

    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")

            # Remove all special characters except space
            clean_review = re.sub(r"[^a-zA-Z0-9 ]","",parsed[1])

            # Convert file to lowercase
            clean_review = clean_review.lower()
            objects.append(clean_review if len(parsed)>1 else "")

    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to reviews
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each review
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):

    # Dictionary to store all unique worda
    word_dict = {}

    # Dictionary to store unique words in truthful class along with the their count in the class
    truthful_word_count = {}

    # Dictionary to store unique words in deceptive class along with the their count in the class
    deceptive_word_count = {}

    # Total samples in train data of truthful class
    truthful_total_samples = 0

    # Total samples in train data of deceptive class
    deceptive_total_samples = 0

    # Stop words that do appear often and tend to not majorly influence the class
    # Some taken from NLTK reference
    stop_words = ['at','the','i','the','was','be','id','ive','this','was','is','we','were',
    'our','for','a','it','to','after', 'just', 'being', 'over', 'had', 'both', 'through', 'yourselves', 'its', 'before', 'herself'
    'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not',
    'during', 'now', 'him', 'nor', 'did', 'this', 'he','she', 'each', 'further', 'where', 'few',
    'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does',
    'above', 'between', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against',
    'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom',
    'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'dont', 'with', 'than', 'those',
    'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'is', 'am',
    'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other',
    'which', 'you', 'after', 'most', 'such', 'why', 'off', 'yours', 'so', 'the', 'having', 'once', 'jobs','job',
    'im','further','heres','oh','ill','youre','only','couldnt','etc','thus','over','as', 'in','had','of','or','such','this','do','from','all',]

    # Following lines construct the required data structures for posterior probability prediction
    for i in range(0,len(train_data['objects'])):

        # For class truthful
        if(train_data['labels'][i]=='truthful'):
            # For words in the reviews of truthful class
            for word in train_data['objects'][i].split(" "):

                # Not considering stop words
                if(word not in stop_words):

                    # If word not already seen add to unique word dictionary
                    if(word not in word_dict):
                        word_dict[word] = ""

                   # Increment word count if word already seen else add the word to truthful word count dictionary
                    if word in truthful_word_count:
                        truthful_word_count[word] = truthful_word_count[word]+1
                    else:
                        truthful_word_count[word] = 1

            truthful_total_samples +=1

        else:

            # For class deceptive
            # For words in the reviews of deceptive class
            for word in train_data['objects'][i].split(" "):

                # Not considering stop words
                if(word not in stop_words):

                    # Not considering stop words
                    if(word not in word_dict):
                         word_dict[word] = ""

                    # Increment word count if word already seen else add the word to deceptive word count dictionary
                    if word in deceptive_word_count:
                        deceptive_word_count[word] =deceptive_word_count[word]+1
                    else:
                        deceptive_word_count[word] = 1

            deceptive_total_samples+=1

    # Total unique words
    total_words = len(word_dict)

    # P(deceptive) = Number of reviews of class deceptive / Total reviews
    prob_deceptive = deceptive_total_samples/len(train_data['objects'])

    # P(truthful) = Number of reviews of class truthful / Total reviews
    prob_truthful = truthful_total_samples/len(train_data['objects'])

    # Output list
    test_data_labels = []

    # For Laplace smoothing
    # Reference: https://towardsdatascience.com/laplace-smoothing-in-naïve-bayes-algorithm-9c237a8bdece
    alpha = 1.1

    # Code to assign the class for all test samples
    # P(T|w1,w2,w3,w4) = (P(w1,w2,w3,w4|T)*P(T)) / (P(w1,w2,w3,w4))
    # Using Naive Bayes assumption that w1,w2,w3,w4 are independent given T, we can write
    # P(T|w1,w2,w3,w4) = (P(w1|T)*P(w2|T)*P(w3|T)*P(w4|T)*P(T)) / (P(w1,w2,w3,w4))
    # Here: P(T|w1,w2,w3,w4) - Posterior probability
    #       P(w1|T),P(w2|T),P(w3|T),P(w4|T) - Likelihoods
    #       P(T), P(w1,w2,w3,w4) - Priors
    # Similarly, P(D|w1,w2,w3,w4) = (P(w1|D)*P(w2|D)*P(w3|D)*P(w4|D)*P(D)) / (P(w1,w2,w3,w4))

    # Hence, odds ratio:
    # P(T|w1,w2,w3,w4) / P(D|w1,w2,w3,w4) = (P(w1|T)*P(w2|T)*P(w3|T)*P(w4|T)*P(T)) /  (P(w1|D)*P(w2|D)*P(w3|D)*P(w4|D)*P(D)

    # Taking log Odds ratio = (log(P(w1|T)) + log(P(w1|T)) + log(P(w1|T)) + log(P(w1|T)) + log(P(T)))/ (log(P(w1|D)) + log(P(w1|D)) + log(P(w1|D)) + log(P(w1|D)) + log(P(D)))
    for i in range(0,len(test_data['objects'])):

        prob_truthful_test = 1
        prob_deceptive_test = 1

        # For each word of review calculate the likelihood
        for word in test_data['objects'][i].split(" "):

            # Convert to lowercase and remove special characters
            word = word.lower().strip()
            word = re.sub(r"[^a-zA-Z0-9 ]","",word)

            # Ignore stop words
            if(word not in stop_words):

                # Calculate P(T|w1,w2,w3,w4) and P(D|w1,w2,w3,w4). Taking logs to avoid very small numbers.
                # Using laplace smoothing to solve zero probability problem.
                if word in truthful_word_count:
                    # Summation of log of Likelihoods
                    prob_truthful_test += np.log(((truthful_word_count[word])+alpha)/(len(truthful_word_count)
                    + alpha*total_words))
                else:
                    # If word not present in the class instead of 1 or 0 assign probability as below
                    prob_truthful_test +=np.log((alpha)/( len(truthful_word_count) + (total_words*alpha)))

                if word in deceptive_word_count:
                    # Summation of log of Likelihoods
                    prob_deceptive_test += np.log(((deceptive_word_count[word])+alpha)/(len(deceptive_word_count)
                    + total_words*alpha))
                else:
                    # If word not present in the class instead of 1 or 0 assign probability as below
                    prob_deceptive_test += np.log((alpha)/(len(deceptive_word_count)+(total_words*alpha)))

        # Add log of priors
        prob_truthful_test += np.log(prob_truthful)
        prob_deceptive_test += np.log(prob_deceptive)

        # Take the class with max value of posterior probability
        if(prob_deceptive_test!=0):
            if((prob_truthful_test/prob_deceptive_test)<=1):
                test_data_labels.append("truthful")
            else:
                test_data_labels.append("deceptive")
        else:
            test_data_labels.append("truthful")

    return test_data_labels

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(sorted(train_data["classes"]) != sorted(test_data["classes"]) or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))