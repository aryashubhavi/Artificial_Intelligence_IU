###################################
# CS B551 Spring 2021, Assignment #3
#
# Authors: Aishwarya Budhkar (abudhkar)
#          Jacob Striebel (jstrieb),
#          Shubhavi Arya (aryas)
#
# (Based on skeleton code by D. Crandall)
#

import random
import numpy as np
# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    # Dictionary of Simple Bayes net emission probability from training data

    # Dictionary to store counts of unique words in training data
    unique_words = {}

    # Dictionary to store labels along with the count of each word labelled as that label/class  that occur in training data
    emission_prob = {}

    # Dictionary to store how many times a class/POS has occurred at the start in training data
    ini_prob = {}

    # Dictionary to store the counts for the classes/POS  in training data i.e probability to transit from one to another eg. noun to verb
    trans_prob = {}

    # Dictionary to store how many times a class/POS appeared
    class_prob = {}

    # Dictionary to store how many times a class/POS was followed by another in training data eg. noun followed by verb 5000 times
    prev_follow_prob = {}

    # Total sentences in training data
    total_initial = 0

    # Parts of speech list
    POS = []

    def __init__(self):
        self.prob = {}
        self.unique_words = {}
        self.ini_prob = {}
        self.prev_follow_prob = {}

        # For gibbs sampling
        self.iterations = 500

        self.total_initial = 0

        self.POS = []

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):

        # Alpha for laplace smoothing
        alpha = 1.1
        if model == "Simple":

            # variable to store posterior probability
            post_prob = 0

            # Simple model Fig (b)
            for i in range(len(sentence)):

                # If word present in the emission probability add its probability
                if sentence[i] in self.prob[label[i]]:
                    prob_word_label = (alpha + self.prob[label[i]][sentence[i]]) / (self.class_prob[label[i]] + alpha * len(self.unique_words))
                    post_prob += np.log(prob_word_label)

                # Otherwise add small probability as per laplace smoothing
                else:
                    post_prob += np.log((alpha) / (alpha * len(self.unique_words)))
            return post_prob

        elif model == "HMM":

            # For HMM  model we get Posterior prob = ini_prob*emission of initial word and label + emission* max(transition*prev probabilities of all previous words)of all next words and labels
            post_prob = 0

            # Add log of initial and log of emission probabilities for first word
            if sentence[0] in self.ini_prob and label[0] in self.emission_prob and sentence[0] in self.emission_prob[label[0]]:
                prob_word_label =  np.log(self.ini_prob[sentence[0]] / self.total_initial) + np.log(self.emission_prob[label[0]][sentence[0]] / self.class_prob[label[0]])
                post_prob += np.log(prob_word_label)
            else:
                post_prob = np.log(0.000000000000000000000000000001)

            # For next words add log of transition and log of emission probabilities and log of observed class probability
            for i in range(1,len(sentence)):

                # transition prob
                if sentence[i] in self.trans_prob[label[i]]:
                    prob_word_label = self.trans_prob[label[i]][label[i-1]] / (self.prev_follow_prob[label[i]])
                    post_prob += np.log(prob_word_label)
                else:
                     post_prob = np.log(0.000000000000000000000000000001)

                if sentence[i] in self.prob[label[i]]:
                    prob_word_label = self.emission_prob[label[i]][sentence[i]] / (self.class_prob[label[i]])
                    post_prob += np.log(prob_word_label)
                else:
                    post_prob += np.log(0.000000000000000000000000000001)
            return post_prob

        elif model == "Complex":
              prob = 0
              for i in range(len(sentence)):
                  # Get current label and word
                  current_label = label[i]
                  current_word = sentence[i]

                  # Store joint probability
                  prob = 0

                  # Find emission prob of given label to word
                  if current_word in self.emission_prob[current_label]:
                      label_to_word = np.log(self.emission_prob[current_label][current_word] / self.class_prob[current_label])
                  else:
                      label_to_word = np.log(0.000000000000000000000000000001)

                  # Find initial prob  of given word
                  initial_prob = np.log(self.ini_prob[current_label] / self.total_initial)

                  # Find transition probability to next label
                  if i < len(sentence) - 1 and len(sentence) > 1:
                      next_label = label[i + 1]
                      next_word = sentence[i + 1]

                      if(next_label in self.trans_prob[current_label]):
                          label_to_next_label = np.log(self.trans_prob[current_label][next_label] / self.prev_follow_prob[current_label])
                      else:
                          label_to_next_label = np.log(0.000000000000000000000000000001)

                  # Find transition probability from prev label to current label
                  if i > 0 and len(sentence) > 1:
                      prev_label = label[i - 1]
                      prev_word = sentence[i - 1]

                      if current_label in self.trans_prob[prev_label]:
                          prev_label_to_label = np.log(self.trans_prob[prev_label][current_label] / self.prev_follow_prob[prev_label])
                      else:
                          prev_label_to_label = np.log(0.000000000000000000000000000001)

                  # Find transition probability from prev to prev label to current label
                  if i > 1 and len(sentence) > 2:
                      prev_to_prev_label = label[i - 2]

                      if(current_label in self.trans_prob[prev_to_prev_label]):
                          prev_to_prev_label_to_label = np.log(self.trans_prob[prev_to_prev_label][current_label] / self.prev_follow_prob[prev_to_prev_label])
                      else:
                          prev_to_prev_label_to_label = np.log(0.000000000000000000000000000001)

                  # Find emission probability from prev label to current word
                  if i > 0 and len(sentence) > 1:
                      prev_label = label[i - 1]
                      prev_word = sentence[i - 1]

                      if(current_word in self.emission_prob[prev_label]):
                          prev_label_to_current_word = np.log(self.emission_prob[prev_label][current_word] / self.class_prob[prev_label])
                      else:
                          prev_label_to_current_word = np.log(0.000000000000000000000000000001)

                  # If word at first position of a sentence of length 1 only initial and emission prob applied

                  if i == 0 and len(sentence) == 1:
                    prob = initial_prob + label_to_word

                  # If word at first position of a sentence of length>1, initial, emission and transition probabilities applied

                  elif i == 0 and len(sentence) > 1:
                    prob = initial_prob + label_to_word + label_to_next_label

                  # If word at position 1 and not at last position of a sentence of length>1,
                  # emission_prob for current label to word, emission prob from prev label to current_word
                  # transition prob from prev to current label and transition from current to next applied

                  elif i == 1 and len(sentence) > 1 and i != len(sentence) - 1:
                    prob = prev_label_to_current_word + prev_label_to_label + label_to_word + label_to_next_label

                  # If word at position 1 and at last position of a sentence of length>1,
                  # emission_prob for current label to word, emission prob from prev label to current_word
                  # transition prob from prev to current label applied

                  elif i == 1 and len(sentence) > 1 and i == len(sentence) - 1:
                    prob = prev_label_to_current_word + prev_label_to_label + label_to_word

                  # If word at position>1 and not at last position of a sentence of length>2,
                  # emission_prob for current label to word, emission prob from prev label to current_word
                  # transition prob from prev to current label and transition from current to next
                  # transition prob from prev to prev to current applied

                  elif i > 1 and len(sentence) >2 and i != len(sentence) - 1:
                    prob = prev_label_to_current_word + prev_label_to_label + label_to_word + label_to_next_label + prev_to_prev_label_to_label

                  # If word at last position of a sentence of length>2,
                  # emission_prob for current label to word, emission prob from prev label to current_word
                  # transition prob from prev to prev to current applied
                  # transition prob from prev to current label applied

                  elif i > 1 and len(sentence) > 2 and i == len(sentence)-1:
                    prob = prev_to_prev_label_to_label + prev_label_to_current_word + prev_label_to_label + label_to_word

                  return prob
        else:
            print("Unknown algo!")

    # Do the training!
    #
    def train(self, data):

        for i in range(len(data)):
            # Get the sentence
            words =  data[i][0]

            # Get the labels for each word of sentence
            label = data[i][1]

            # For each word in sentence
            for j in range(len(words)):

                # Add to unique_words dictionary with its proper count
                if words[j] not in self.unique_words:
                    self.unique_words[words[j]] = 1
                else:
                    self.unique_words[words[j]] = self.unique_words[words[j]] + 1

                # Add to POS (part of speech list)
                if label[j] not in self.POS:
                    self.POS.append(label[j])

                # Add to class_prob  dictionary with proper count of occurrence used to calculate emission probability
                if label[j] not in self.class_prob:
                    self.class_prob[label[j]] = 1
                else:
                    self.class_prob[label[j]] = self.class_prob[label[j]] + 1

                # Add the emission count i.e {noun: {Car:4000, Sun: 288 ...},verb:{run:900}..,)
                if label[j] not in self.prob:

                    # Add label if not present
                    self.prob[label[j]] = {}

                    # If word not present, add with count 1
                    if words[j] not in self.prob[label[j]]:
                        self.prob[label[j]][words[j]] = 1
                    # If word present increase count
                    else:
                        self.prob[label[j]][words[j]] = self.prob[label[j]][words[j]] + 1
                else:

                    # If word not present, add with count 1
                    if words[j] not in self.prob[label[j]]:
                        self.prob[label[j]][words[j]] = 1

                    # If word present increase count
                    else:
                        self.prob[label[j]][words[j]] = self.prob[label[j]][words[j]] + 1

        total = 0
        for i in range(len(data)):

           # Get sentence
           words = data[i][0]

           # Get labels for words in sentence
           label = data[i][1]

           # Stores total sentences in training data
           total += 1

           # Count of label being at initial labelition
           if label[0] not in self.ini_prob:
                 self.ini_prob[label[0]] = 1
           else:
                 self.ini_prob[label[0]]  = self.ini_prob[label[0]] + 1

        for i in range(len(data)):
            # Get sentence
            words =  data[i][0]

            # Get labels for words in sentence
            label = data[i][1]

            # Count of transition from one class to another eg. {noun:{noun:100, verb:8000....}}
            for j in range(0, len(label)-1):

                # Add label/POS if not present in dictionary
                if label[j] not in self.trans_prob:

                    self.trans_prob[label[j]] = {}

                    # Add count of how many times a label is followed by another used to calculate transition probability
                    if label[j] not in self.prev_follow_prob:
                        self.prev_follow_prob[label[j]] = 1
                    else:
                        self.prev_follow_prob[label[j]] = self.prev_follow_prob[label[j]] + 1

                    # Create transition count dictionary
                    if label[j+1] not in self.trans_prob[label[j]]:
                        self.trans_prob[label[j]][label[j+1]] = 1
                    else:
                        self.trans_prob[label[j]][label[j+1]] = self.trans_prob[label[j]][label[j+1]] + 1
                else:

                    # Add count of how many times a label is followed by another used to calculate transition probability
                    if label[j] not in self.prev_follow_prob:
                        self.prev_follow_prob[label[j]] = 1
                    else:
                        self.prev_follow_prob[label[j]] = self.prev_follow_prob[label[j]] + 1

                    # Create transition count dictionary
                    if label[j+1] not in self.trans_prob[label[j]]:
                        self.trans_prob[label[j]][label[j+1]] = 1
                    else:
                        self.trans_prob[label[j]][label[j+1]] = self.trans_prob[label[j]][label[j+1]] + 1

        # Emission probability
        self.emission_prob = self.prob

        # Sum of all occurrences of any class at start position used to calculate initial probability
        self.total_initial = (sum(self.ini_prob.values()))

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):

        # Final labels
        final_labels = []

        # For each word in sentence
        for i in range(len(sentence)):
            max1 = 0
            final_label = 'noun'

            # For each word assign label which has maximum emission probability. Noun is used if word not found in training data.
            for  label in (self.prob):
                if sentence[i] in self.prob[label]:
                    prob_word_label = self.prob[label][sentence[i]] / self.class_prob[label]

                    # Store max probability
                    if prob_word_label > max1:
                        max1 = prob_word_label
                        final_label = label
                else:
                    continue
            final_labels.append(final_label)

        return final_labels

    # Used the code that I developed for activity 2
    def hmm_viterbi(self, sentence):
        N = len(sentence)

        # Create viterbi table with all POS
        V_table = { p:[0] * N for p in self.POS }

        # Create backtrack table with all POS
        backtrack_table = { p:[0] * N for p in self.POS }

        states = self.POS

        # For all POS
        for i in states:

            # Fill first column of viterbi table
            if sentence[0] in self.emission_prob[i]:
                V_table[i][0] = (self.ini_prob[i] / self.total_initial) * (self.emission_prob[i][sentence[0]] / self.class_prob[i])
            else:
                V_table[i][0] = (self.ini_prob[i] / self.total_initial) * 0.000000000000000000000000000001

        # For next columns calculate the table values
        for t in range(1,N):
            for j in states:
                max_trans = 0
                last_state = 'noun'
                # Take maximum of transition*previous probability amongst all previous states. Noun by default
                for i in states:
                    if i in self.trans_prob and j in self.trans_prob[i]:
                        result = V_table[i][t-1] * (self.trans_prob[i][j] / self.prev_follow_prob[i])
                    else:
                        result = V_table[i][t-1] * 0.000000000000000000000000000001

                    # Store max probability
                    if result > max_trans:
                        max_trans = result
                        last_state = i

                # Multiply with emission
                if j in self.emission_prob and sentence[t] in self.emission_prob[j]:
                    V_table[j][t] = (self.emission_prob[j][sentence[t]] / self.class_prob[j]) * max_trans
                else:
                    V_table[j][t] = 0.000000000000000000000000000001*max_trans

                # Store the state to backtrack
                backtrack_table[j][t-1] = last_state

        viterbi_seq = [""] * N

        key_max = max(V_table, key = lambda x:V_table[x][N-1])
        viterbi_seq[N-1] = key_max

        # Backtrack to get the sequence
        for i in range(N-2, -1, -1):
            viterbi_seq[i] = backtrack_table[viterbi_seq[i+1]][i]

        return viterbi_seq

    # Compute joint probability
    def joint_prob(self, i, sentence, sample):

        # Get current label and word
        current_label = sample[i]
        current_word = sentence[i]

        # Store joint probability
        prob = 0

        # Find emission prob of given label to word
        if current_word in self.emission_prob[current_label]:
            label_to_word = self.emission_prob[current_label][current_word] / self.class_prob[current_label]
        else:
            label_to_word = 0.000000000000000000000000000001

        # Find initial prob  of given word
        initial_prob = self.ini_prob[current_label] / self.total_initial

        # Find transition probability to next label
        if i < len(sentence) - 1 and len(sentence) > 1:
            next_label = sample[i + 1]
            next_word = sentence[i + 1]

            if next_label in self.trans_prob[current_label]:
                label_to_next_label = self.trans_prob[current_label][next_label]/self.prev_follow_prob[current_label]
            else:
                label_to_next_label = 0.000000000000000000000000000001

        # Find transition probability from prev label to current label
        if i > 0 and len(sentence) > 1:
            prev_label = sample[i - 1]
            prev_word = sentence[i - 1]

            if current_label in self.trans_prob[prev_label]:
                prev_label_to_label = self.trans_prob[prev_label][current_label] / self.prev_follow_prob[prev_label]
            else:
                prev_label_to_label = 0.000000000000000000000000000001

        # Find emission probability from prev label to current word
        if i > 0 and len(sentence) > 1:
            prev_label = sample[i - 1]
            prev_word = sentence[i - 1]

            if current_word in self.emission_prob[prev_label]:
                prev_label_to_current_word = self.emission_prob[prev_label][current_word] / self.class_prob[prev_label]
            else:
                prev_label_to_current_word = 0.000000000000000000000000000001

        # Find transition probability from prev to prev label to current label
        if i > 1 and len(sentence) > 2:
          prev_to_prev_label = sample[i - 2]

          if current_label in self.trans_prob[prev_to_prev_label]:
              prev_to_prev_label_to_label = self.trans_prob[prev_to_prev_label][current_label] / self.prev_follow_prob[prev_to_prev_label]
          else:
              prev_to_prev_label_to_label = 0.000000000000000000000000000001

        # If word at first position of a sentence of length 1 only initial and emission prob applied
        if i == 0 and len(sentence) == 1:
          prob = initial_prob * label_to_word

        # If word at first position of a sentence of length>1, initial, emission and transition probabilities applied
        elif i == 0 and len(sentence) > 1:
          prob = initial_prob * label_to_word * label_to_next_label

        # If word at position 1 and not at last position of a sentence of length>1,
        # emission_prob for current label to word, emission prob from prev label to current_word
        # transition prob from prev to current label and transition from current to next applied
        elif i == 1 and len(sentence) > 1 and i != len(sentence)-1:
          prob = prev_label_to_current_word * prev_label_to_label * label_to_word * label_to_next_label

        # If word at position 1 and at last position of a sentence of length>1,
        # emission_prob for current label to word, emission prob from prev label to current_word
        # transition prob from prev to current label applied

        elif i == 1 and len(sentence) > 1 and i == len(sentence) - 1:
          prob = prev_label_to_current_word * prev_label_to_label * label_to_word

        # If word at position>1 and not at last position of a sentence of length>2,
        # emission_prob for current label to word, emission prob from prev label to current_word
        # transition prob from prev to current label and transition from current to next
        # transition prob from prev to prev to current applied
        elif i > 1 and len(sentence) > 2 and i != len(sentence) - 1:
          prob =  prev_to_prev_label_to_label * prev_label_to_current_word * prev_label_to_label * label_to_word * label_to_next_label

        # If word at last position of a sentence of length>2,
        # emission_prob for current label to word, emission prob from prev label to current_word
        # transition prob from prev to prev to current applied
        # transition prob from prev to current label applied
        elif i > 1 and len(sentence) > 2 and i == len(sentence)-1:
          prob = prev_to_prev_label_to_label * prev_label_to_current_word * prev_label_to_label * label_to_word

        return prob

    # The following lines of code are taken from David's code of activity 3
    def cond_prob(self, i, sentence, conditions):

        joint_probs = {}

        for label in self.POS:
            sample = conditions
            sample.update({i:label})
            joint_probs[label] = self.joint_prob(i, sentence, sample)

        distro = {label: float(joint_probs[label]) / sum(joint_probs.values()) for label in self.POS}
        return distro

    def sample(self, distro):
          dist=list(distro.items())
          return np.random.choice([dist[i][0] for i in range(len(dist))],p=[dist[i][1] for i in range(len(dist))])
    # End of code taken from David's code of activity 3

    def complex_mcmc(self, sentence):

        # Getting first sample from hmm_viterbi as base for gibbs sampling
        first_sample = {v: k for v, k in enumerate(self.hmm_viterbi(sentence))}

        # The following lines of code are taken from David's code of activity 3
        samples = [first_sample]

        # for the number of iterations,
        for i in range(self.iterations):

            # copy the previous sample
            new_sample = samples[-1].copy()

            # for each POS in the sample
            for i in range(len(new_sample)):

                # remove that POS from the sample
                new_sample.pop(i)

                # use the conditional probabilities of the remaining hidden and observed for a biased coin flip.
                distro_var = self.cond_prob(i, sentence, new_sample)
                new_sample.update({i:self.sample(distro_var)})

            # add the sample to the list of samples
            samples.append(new_sample)
        # End of code taken from David's code of activity 3

        # Creating a dictionary to store key, value to count the number of times a label occurs at an position in sentence from among the samples generated
        result = {}
        for sample in samples:
            for key, value in sample.items():
                if (key,value) in result:
                    result[(key,value)] += 1
                else:
                    result[(key,value)] = 1

        # Return the label which occurs the most at that position in sentence from among the samples generated
        labels = []
        for ind in range(len(sentence)):
            max_count = 0
            maximum_freq = ''
            for label in result.items():
                if label[0][0] == ind:
                    if label[1] > max_count:
                        max_count = label[1]
                        maximum_freq = label[0][1]
            labels.append(maximum_freq)
        return labels

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself.
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")