3.2. Review Classification - Naive Bayes - Reasoning under Uncertainity

###  (1) a description of how you formulated each problem;

This problem of classifying reviews as deceptive and truthful can be done using the Naive Bayes Classifier. This works well because the words in each review are independent of one another and the conditional probabilty each word is taken into consideration. Which gives quite accurate results as seen in the result.

### (2) a brief description of how your program works; 

Algorithm :
1. In this review classification problem, we implement the concept of Naive Bayes Classifier.
2. The reason we use this classifier is because it works really well in classifying textual datasets in the form of paragraphs even after the limitations mentioned above.
3. We start with the data preprocessing where we take each review and extract the words from it and find a frequency count for the particular class using the "re" library.
4. We ignore certain words by maintaining a "ignoreList" list, these words are not considered for frequency calculation. (These words do not contribute weights for the review to be on the "deceptive" class or the "truthful" class)
5. These frequencies are then stored in a "deceptive dictionary" and "truthful dictionary".
6. Buffer element is introduced for handling the case when a word is not found in either dictionaries. This is very important because we want to penalise the review to not belonging to a particular class as simply ignoring can yeild wrong results.
    6.1. The way we achieve this is we add a dummy string "***" (in our case) to the dictionary with count 1 and we add 1 additional count to each and every word to balance the manipulation. 
7. Calculated the prior probabilities from the training data set, measuring the number of deceptive and truthful reviews.
8. Then we calculate the P(W|deceptive) = (count(W) in deceptive / count(W) in truthful + count(W) in deceptive), and also P(W|truthful) = (count(W) in truthful / count(W) in truthful + count(W) in deceptive) and store them in two separate probability dictionaries.
9. After the training we predict the classes for the train set. We extract the words out of each review and calculate the likelihood of the review being a part of a particular class by P(review|class A) = P(A).P(W1|A).P(W2|A)....
10. We compare which class has a higher probability and classify as that class. (Assumption - under the rare occurance if the probabilities of it being in deceptive and truthful are equal we assume that it would belomg to the truthful class).

### (3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.

Assumptions made :
1. Case insensitive classification is fine, converting all words to lowercase and then training the Naive Bayes Classifier.
2. The words are independent of another. It does not check if two words have the same ordering , i.e the probability of "My husband" and "husband My" would not be different.
    2.1. Limitation : It does not check for any grammatical errors and if there are any typos it would be considered as a different word all together.

Problems faced / Optimisations introduced:
1. Irrelevant words:
    1.1. There were many words such as "the", "they" etc. which had a very high frequency but had nothing to contribute specifically to belonging to a class. So introduced a list of all such words called the ignoreList to ignore it.
2. Tried to optimised by :
    2.1. By blindly cutting down the most frequent words and the least frequent words, but this yeilded in very low accuracy hence removed the logic.
    2.2. By filtering on the length of words with the idea that words with less than or equal to 4 could be irrelevant . But again got low accuracy hence removed the logic.
3. Probability calculation :
    3.1. First the conditional probability was calculated like P(W|deceptive) = P(count(W) in deceptive/ total number of words). This was a problem as this number is very small and multiplying with other probabilities yeilded in 0 for both the truthful and deceptive class and would always predict "truthful", yeilding an accuracy of around 55%.
4. Low accuracy due to not handling new words found in the train set:
    If a word is not found introducing a buffer element as explained above takes care of the case and handles it in a more robust manner.


Result:
Getting an accuracy of 80.75% on the given training data.




