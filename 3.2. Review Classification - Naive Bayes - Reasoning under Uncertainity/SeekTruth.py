# SeekTruth.py : Classify text objects into two categories
#
# Avishmita Mandal - avmandal
# Yashaswini Sampath - ysampath

import re
import sys
from collections import Counter

import pandas as pd


def load_file(filename):
    objects = []
    labels = []
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(" ", 1)
            labels.append(parsed[0] if len(parsed) > 0 else "")
            objects.append(parsed[1] if len(parsed) > 1 else "")

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


def extract_words_and_count_frequency(input_string, ignoreList):
    words = re.findall(r"\w+", input_string.lower())
    if ignoreList:
        words = [word for word in words if word not in ignoreList]
    word_count = Counter(words)
    return word_count


def data_processing(data):
    word_frequency_deceptive_list = []
    word_frequency_truthful_list = []

    # Maintaining a ignoreList to avoid irrelevant occurances
    ignoreList = [
        "i",
        "me",
        "my",
        "myself",
        "we",
        "our",
        "ours",
        "ourselves",
        "you",
        "you're",
        "you've",
        "you'll",
        "you'd",
        "your",
        "yours",
        "yourself",
        "yourselves",
        "he",
        "him",
        "his",
        "himself",
        "she",
        "she's",
        "her",
        "hers",
        "herself",
        "it",
        "it's",
        "its",
        "itself",
        "they",
        "them",
        "their",
        "theirs",
        "themselves",
        "what",
        "which",
        "who",
        "whom",
        "this",
        "that",
        "that'll",
        "these",
        "those",
        "am",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "having",
        "do",
        "does",
        "did",
        "doing",
        "a",
        "an",
        "the",
        "and",
        "but",
        "if",
        "or",
        "because",
        "as",
        "until",
        "while",
        "of",
        "at",
        "s",
        "t",
        "d",
        "in",
        "to",
        "with",
        "all",
        "when",
        "some",
        "maybe",
        "own",
        "on",
        "for",
        "got",
        "m",
        "like",
        "not",
        "only",
        "than",
        "into",
        "so",
        "ask",
    ]

    # Maintaining a truthful list with frequencies and a separate deceptive list
    for x in range(len(data["objects"])):
        if data["labels"][x] == "deceptive":
            word_frequency_deceptive = extract_words_and_count_frequency(
                data["objects"][x], ignoreList
            )
            word_frequency_deceptive_list.append(word_frequency_deceptive)

        if data["labels"][x] == "truthful":
            word_frequency_truthful = extract_words_and_count_frequency(
                data["objects"][x], ignoreList
            )
            word_frequency_truthful_list.append(word_frequency_truthful)

    # Creating the word and frequency dict of the deceptive data
    merged_deceptive_word_frequency = sum(word_frequency_deceptive_list, Counter())

    word_deceptive_df = pd.DataFrame(
        list(merged_deceptive_word_frequency.items()), columns=["Word", "Frequency"]
    )
    word_deceptive_df = word_deceptive_df.sort_values(by="Frequency", ascending=False)
    word_deceptive_df = word_deceptive_df.reset_index(drop=True)

    word_deceptive_frequency_dict = word_deceptive_df.set_index("Word")[
        "Frequency"
    ].to_dict()

    # Creating the word and frequency dict of the truthful data
    merged_truthful_word_frequency = sum(word_frequency_truthful_list, Counter())

    word_truthful_df = pd.DataFrame(
        list(merged_truthful_word_frequency.items()), columns=["Word", "Frequency"]
    )
    word_truthful_df = word_truthful_df.sort_values(by="Frequency", ascending=False)
    word_truthful_df = word_truthful_df.reset_index(drop=True)

    word_truthful_frequency_dict = word_truthful_df.set_index("Word")[
        "Frequency"
    ].to_dict()

    for word, freq in word_deceptive_frequency_dict.items():
        word_deceptive_frequency_dict[word] += 1
    word_deceptive_frequency_dict["***"] = 1

    for word, freq in word_truthful_frequency_dict.items():
        word_truthful_frequency_dict[word] += 1
    word_truthful_frequency_dict["***"] = 1

    # Calculating prior probabilities
    total_count = len(train_data["labels"])
    deceptive_count = train_data["labels"].count("deceptive")
    truthful_count = train_data["labels"].count("truthful")

    p_deceptive = deceptive_count / total_count
    p_truthful = truthful_count / total_count

    # Creating a new truthful and deceptive PROBABILITY dictionary.
    word_truthful_probability_dict = dict()
    word_deceptive_probability_dict = dict()

    for string, freq in word_deceptive_frequency_dict.items():
        count_word_in_deceptive, count_word_in_truthful = 0, 0
        if string in word_deceptive_frequency_dict:
            count_word_in_deceptive = word_deceptive_frequency_dict[string]

        if string in word_truthful_frequency_dict:
            count_word_in_truthful = word_truthful_frequency_dict[string]

        word_deceptive_probability_dict[string] = count_word_in_deceptive / (
            count_word_in_deceptive + count_word_in_truthful
        )

    for string, freq in word_truthful_frequency_dict.items():
        count_word_in_deceptive, count_word_in_truthful = 0, 0
        if string in word_deceptive_frequency_dict:
            count_word_in_deceptive = word_deceptive_frequency_dict[string]

        if string in word_truthful_frequency_dict:
            count_word_in_truthful = word_truthful_frequency_dict[string]

        word_truthful_probability_dict[string] = count_word_in_truthful / (
            count_word_in_deceptive + count_word_in_truthful
        )

    return (
        p_deceptive,
        p_truthful,
        word_deceptive_probability_dict,
        word_truthful_probability_dict,
    )


def classifier(train_data, test_data):
    (
        p_deceptive,
        p_truthful,
        word_deceptive_probability_dict,
        word_truthful_probability_dict,
    ) = data_processing(train_data)

    # Predict on the test data
    predicted_list = []

    for x in range(len(test_data["objects"])):
        words = re.findall(r"\w+", test_data["objects"][x].lower())

        # Prob of review being in class - deceptive
        p_review_deceptive = p_deceptive
        for word in words:
            if word in word_deceptive_probability_dict:
                p_review_deceptive *= word_deceptive_probability_dict[word]
            else:
                p_review_deceptive *= word_deceptive_probability_dict["***"]

        # Prob of review being in class - truthful
        p_review_truthful = p_truthful
        for word in words:
            if word in word_truthful_probability_dict:
                p_review_truthful *= word_truthful_probability_dict[word]
            else:
                p_review_truthful *= word_truthful_probability_dict["***"]

        if p_review_deceptive > p_review_truthful:
            predicted_list.append("deceptive")
        else:
            predicted_list.append("truthful")

    return predicted_list


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.
    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if (
        sorted(train_data["classes"]) != sorted(test_data["classes"])
        or len(test_data["classes"]) != 2
    ):
        raise Exception(
            "Number of classes should be 2, and must be the same in test and training data"
        )

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {
        "objects": test_data["objects"],
        "classes": test_data["classes"],
    }

    results = classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum(
        [
            (results[i] == test_data["labels"][i])
            for i in range(0, len(test_data["labels"]))
        ]
    )
    print(
        "Classification accuracy = %5.2f%%"
        % (100.0 * correct_ct / len(test_data["labels"]))
    )
