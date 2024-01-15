### Part of Speech Tagging - HMM (Viterbi Algorithm), NLP

### (1)Description of how you formulated each problem; 

There are two parts to it:
1. Simplified 
2. HMM

a. Simplified:
The simplified model is defined such that the state to be predicted(hidden state) is not dependent of its previous states but only depends on the emission probability (P(observed state| hidden state) which in this case is P(word | POS)) and the P(hidden state) which is P(POS) here.
We simply calculate the probabilites and find the max of the probabilities of all the hidden states and POS with the max probability is the result for that particular observed state.

b. HMM:
The HMM is based on the (maximum a posteriori (MAP)), we populate the Viterbi dictionary by a tuple(prob,[output List]).

**Calculating the probability:**
Part1: Initial Prob of the 1st row is calculated using emission probability for the current observation * Initialprob[observed]
    Initial probability is the occurrence of a POS at the start of a sentence. and then we find the probability of it (normalize it)
Part2: For length 1 to len(sentence)
    prob = max(transition prob from previous layer) * emission probability for the current observation * viterbiDictionary value of previous state(viterbi[prev_tag])
    choose state with maximum prob, add the POS into the output list
Once all observations are processed, choose the state with the highest final Viterbi path probability as the most likely end state.
Return the output List

### (2) A brief description of how your program works; 
The computation can be divided into three sections:
    1.0 Initial Probability
    1.1 Emission Probability
    1.2 Transition Probability
    1.3 Viterbi algorithm

**1.0 Initial probability:**
We calculate the probability that the first word of the sentence is a particular POS in the self.dict_pos.

**1.1 Emission probability:**
Emission probability is calculated by P(observed word|POS)
For this we go thorough each word and store all the words of a particular POS in the emmisionProb dictionary and maintain a count.
We then normalise this to get the proper probability values.

**1.2 Transition Probability:**
Transition probability is calculated by P(Ti|Ti-1):
Transition Prob dictionary is a number of POS * number of POS (12 x 12)
1st pass: calculate the freq of occurrence of a POS given prev POS in the train file
2nd pass: normalize it to find the probability

**1.3 Viterbi Algorithm**
prob = max(transition prob from previous layer)* emission probability for the current observation * viterbiDictionary value of previous state(viterbi[prev_tag])

### (3) Discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.

1. The accuracy was coming out to be quite low in certain scenarios, when the word was not present in the train set. For such situations we have hardcoded a very small value = 10^-10. This has helped increase the accuracy where the probability does not directly drop to 0 and simply returns the last POS in the POS_list.
2. Accuracy further improved when the assumption was made that the tag to be predicted to be set as Noun. This was one of the design decisions as the occurence of noun in a sentence is quite decent. And it handles the case when a Proper Noun which has a probability of not being in the trainset to be classified accurately.
3. We also take care of sentences which has only 1 word.

### Result

So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct: 
   0. Ground truth:      100.00%              100.00%
         1. Simple:       92.91%               43.15%
            2. HMM:       95.02%               54.00%
