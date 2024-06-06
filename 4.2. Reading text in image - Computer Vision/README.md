# 4.2. Reading text in image - Computer Vision
### (1)Description of how you formulated each problem; 

There are two parts to it:
1. Simplified
2. HMM

a.Simplified:
The simplified can be predicted by just considering the emission probability matrix.
and returning the highest probability in that row. i.e given a test character the probability it belongs to one in TRAINLETTERS

b. HMM:
The HMM is based on the (maximum a posteriori (MAP)), we populate the Viterbi dictionary by a tuple(prob,[output List]).
**Calculating the probability:**
Part1: Initial Prob of the 1st row is calculated using emission probability for the current observation * Initialprob[observed]
    Initial probability is the occurrence of word[i] at the start of a sentence. and then we find the probability of it(normalize it)
Part2: For length 1 to len(test letters)
    prob = max(transition prob from previous layer)* emission probability for the current observation * viterbiDictionary value of previous state(viterbi[prev_char])
    choose state with maximum prob, add the character into the output list
Once all observations are processed, choose the state with the highest final Viterbi path probability as the most likely end state.
Return the output List

### (2) A brief description of how your program works; 
The computation can be divided into three sections:
    1.1 Emission Probability
    1.2 Transition Probability
    1.3 Viterbi algorithm

**1.1 Emission probability:**
Emission probability is calculated by P(observerdTestImage|GivenTrainImage)
Since some images are noisy we try to differentiate them by assigning different weights based on the density level of images. Initially, we run both train and test images which help us determine the density % based on the no of pixels denoted by "*".
Emissionprob dictionary is a len(testImagelen)*TRAIN_LETTERS.
We have 4 conditions when evaluating two images:
    a.If both pixels match: eg * and *
    b.If both blank spaces match: " and "
    c.If the pixel is present in the train but not in the test
    d.if the pixel is not present in the train but in the test, this indicates noise

Each of the above counts is calculated after evaluation of different weights we have assigned, after different permutations and combinations of calculation probability like using: math.log to minimize the computation
math.pow
assigning weights

**1.2 Transition Probability:**
Transition probability is calculated by P(Ti|Ti-1):
Transition Prob dictionary is a TRAIN_LETTERS * TRAIN LETTERS
1st pass: calculate the freq of occurrence of a char given prev char in the train file
2nd pass: normalize it to find the probability

**1.3 Viterbi Algorithm**
prob = max(transition prob from previous layer)* emission probability for the current observation * viterbiDictionary value of previous state(viterbi[prev_char])

### (3) Discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.

1. Emission probability: we tried calculating the probability by just calculating the match count i.e. if train[h][w]==test[h][w] it performed very badly as it matched many spaces. Later replaced that by considering different weights for different comparisons (such as pixels, and blanks).
2. Designing the dictionary for Viterbi algo computation, we designed it to store a tuple of prob and output list
3. The Emission probability calculation after different permutations and combination of calculation probability like using : 
        math.log to minimize the compute
        math.pow
        assigning weights
