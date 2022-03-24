# CSCI-B 551 Assignment 2: Games and Bayesian Classifiers

Authors: Aishwarya Budhkar (abudhkar), Shubhavi Arya (aryas), Jacob Striebel (jstrieb)

Date: Fri 5 Nov 2021

## 1. Raichu

### 1.1. Problem Formulation

We formulated the automatic-Raichu-playing problem as an adversarial search problem in the style of Russell & Norvig (2009), chapter 5. Russell & Norvig present two-player games of full information as being able to be formalized as consisting of an initial state and five functions: player, actions, result, terminal-test, and utility. We describe how we understand each of these six elements with respect to the Raichu problem in the next six subsections.

#### 1.1.1. Initial State

The initial state consists of the player whose turn it is and an N by N board with each square either empty or containing a game piece. Implementation wise, both of these pieces of information needed to create the initial state are read off the command line.

#### 1.1.2. Player

The player function takes as input a game state and returns the player whose turn it is to move a piece. The "player" that is returned contains information specifying the color of the player and whether the player is the min or max.

#### 1.1.3. Actions

The actions function takes as input the current game state (which encodes the board and the player whose turn it is) and returns a set of all legal moves in that state.

#### 1.1.4. Result

The result function takes as input a state and an action and returns the successor state that is reached when the specified action is taken from the specified state. The successor state encodes the new game board and the fact that it is now the other player's turn.

#### 1.1.5. Terminal-Test

The terminal-test function takes a game state as input and returns whether this is an end state: that is, whether all the pieces of one color have been captured or whether a stalemate has occurred.

#### 1.1.6. Utility

The utility function takes as input a terminal state and returns the game's total payoff for the max player. For the Raichu problem, because we usually cannot generate a full game tree, we define the utility function so that any state can be "treated" as a terminal state. In this way we can do an iterative-deepening search.

### 1.2. How the Program Works

Our program uses the minimax algorithm described in chapter 5 of Russell & Norvig (2009), but not the pure minimax that must explore the full game tree, nor minimax with alpha-beta pruning which must explore at least half of all nodes in the full game tree. We use minimax with a depth cutoff, where once the cutoff depth is reached, we consider all states at that depth to be terminal and we calculate each state's utility based on the number and type of pieces on the board owned by each player. We assign 1 point to Pichus, 4 points to Pikachus, and 16 points to Raichus (since we have no experience playing the game, these point assignments are based on untrained intuition, but they were certainly good enough to beat the random opponent on the tank server). We only use depth cutoffs that give the min player the last move; in this way, we hope to make our proxy terminal states more quiescent.

Starting with a depth cutoff of 2, we search progressively deeper, outputting the best move at the end of our search of each successive depth. The progressively deepening search will only terminate once the game tree is fully expanded. The program only reaches this condition in a tractable amount of time for tiny game boards and at the very end of the end game, so our program relies on its parent process killing it once the time limit is reached.

### 1.3. Discussion

The most time-consuming component of solving the problem was writing and debugging the actions function, which must return exactly all the legal moves that can be made from a given state. Once this was done, implementing and debugging the minimax search with cutoff took an additional about half as much time as creating the actions function took.

A final comment is that our implementation is not organized exactly according to the adversrial search abstraction of Russell & Norvig in the sense that the six elements of Russell & Norvig are, although all present in our program, not always demarcated: for example, our actions function encapsulates the functionality of both Russell & Norvig's actions and results functions.

## 2. The Game of Quintris

### 2.1  Approach
Implemented Expectimax with heuristic to create a good AI.  
Only explored the tree till depth (number of empty cells 367). After that used heuristic to estimate the score.  
For heuristic, used the aggregate min distance, bumpiness, number of holes, number of wells, number of edge positions filled, number of colums filled in base row and number of row clears.  
At start, I assigned approx weights to the heuristic parameters and also tried to use the Genetic algorithm to estimate the weights but was not able to get it right so that the bot scores high.

### 2.2 Problem formulation

Initial State: An empty board of size 15*25  
Successors: An placement of given piece such that it touches the floor or a piece below it and does not intersect with other pieces   
Goal state: To place the pieces in such a way that a row of pieces is formed which when formed gets cleared to give us a point  
Heuristic: Used the difference in number of holes, aggregate min height, number of row clears,base filled, wells, edges filled and bumpiness from current state to successor to estimate the score.  
Lower the number of holes,height,wells, bumpiness better is the chance of having a full row. Higher number of edge filled, base filled, row clears is desired.

### 2.5 Expectimax
Returns the moves associated with Max player AI which fetches the higest score among its successors which are chance nodes (representing chance of a piece being picked.). the chance nodes select avg of their successors which are max nodes.   
The search tree is explored till a depth after which the heuristic function is used to estimate the score.   
Tried three different types of functions with the parameters: row clears, number of holes, aggregate min height and bumpiness,etc.

1. Only evaluate current state. This did not work at all.
2. Evaluate differences in params from current state to the next state.
3. Evaluate differences in params from current to next, next to next using the next piece given and averaging for all columns as column for next piece is unknown.

Both 2 and 3 give only small scores but 3 is computationally expensive. Perhaps better params would work.

### 2.4 Problems faced:
Finding the successors was time-consuming.    
Finding the correct heuristic didn't work out.   
Also, tried to estimate weight with neural network and genetic algorithm but perhaps more interesting parameters are needed to solve the problem as the approaches didn't work well.

## 3. Truth be Told

### 3.1 Approach
It is classic Naive Bayes classifier problem as mentioned in the assignment  
We need to compute the Odds ratio and accordingly assign the class truthful T or deceptive D.

According to Bayes Theorem,  
P(T|w1,w2,w3,w4) = (P(w1,w2,w3,w4|T)*P(T)) / (P(w1,w2,w3,w4))

Using Naive Bayes assumption that w1,w2,w3,w4 are independent given T, we can write  
P(T|w1,w2,w3,w4) = (P(w1|T)*P(w2|T)*P(w3|T)*P(w4|T)*P(T)) / (P(w1,w2,w3,w4))

Here: P(T|w1,w2,w3,w4) - Posterior probability  
P(w1|T),P(w2|T),P(w3|T),P(w4|T) - Likelihoods  
P(T), P(w1,w2,w3,w4) - Priors

Similarly, P(D|w1,w2,w3,w4) = (P(w1|D)*P(w2|D)*P(w3|D)*P(w4|D)*P(D)) / (P(w1,w2,w3,w4))

Hence, odds ratio:  
P(T|w1,w2,w3,w4) / P(D|w1,w2,w3,w4) = (P(w1|T)*P(w2|T)*P(w3|T)*P(w4|T)*P(T)) /  (P(w1|D)*P(w2|D)*P(w3|D)*P(w4|D)*P(D))

Constructed three dictionaries using training data to store all unique words, truthful class unique words with their counts and deceptive class unique words with their counts  
For each word in test review to be classified, used the above mentioned formula to compute the Odds ratio and assign to appropriate class.  
Priors:  
P(T) = total_samples of truthful class/total samples in training data  
P(D) = total_samples of deceptive class/total samples in training data  
Likelihood:  
For each word w, P(w|T) = count of word in truthful class/ total unique words in truthful class

### 3.2 Problems faced
The accuracy after doing the above was around 53%.  
So, I decided to clean the data. Converted data to lowercase and removed all special characters except space.  
After that the accuracy increased to 67%.

If word is not present in the train dataset, I was assigning probability 1.  
So, I tried to find techniques to improves Naive Bayes classifier accuracy and realized assigning.    
1/0 probability when word is not present leads to zero probability problem and decided to use Laplace Smoothing.  
Reference: https://towardsdatascience.com/laplace-smoothing-in-naïve-bayes-algorithm-9c237a8bdece

The likelihood changes as follows to account for words in test data not present in the training data:   
P(w|T) = (Word count in truthful class + alpha) / (Total unique words in truthful class + total unique words in training data *alpha)

Here with alpha=1.1, I got the highest accuracy of 81.75%

Representing probabilities as log-probabilities to avoid tiny numbers, got accuracy of 87.25%.

## References

Stuart Russell and Peter Norvig (2009). Artificial Intelligence: A Modern Approach. Prentice Hall, 3rd ed.  
https://towardsdatascience.com/laplace-smoothing-in-naïve-bayes-algorithm-9c237a8bdece      
