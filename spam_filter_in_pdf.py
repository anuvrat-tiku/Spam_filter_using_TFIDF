from __future__ import print_function

"""
Created by Anuvrat Tiku
"""
from __future__ import division  # Required by py27 compiler to make the division to be floating point
from textract import process
import math
import re


# Method for checking the spam content given the spam_dictionary and tf_idf dictionary
def check_spam(tf_idf, spam_words):
    spam_match = {}
    """
    Check the spam_words list for all spam values and see if they occur often the TF_IDF dictionary
    Store the occurrences and their TF-IDF values in a new dictionary
    """
    for spam in spam_words:
        if spam in tf_idf.keys():
            if spam in spam_match:
                spam_match[spam] += tf_idf[spam]
            else:
                spam_match[spam] = tf_idf[spam]

    """
    Check the spam dictionary
    1. If the spam dictionary is empty, document is not spam
    2. If it has elements, document is spam. Print words and TF-IDF value
    """

    if len(spam_match) == 0:
        print("Document is NOT spam. There were no matching keywords with the TF_IDF dictionary")

    else:
        print("Spam has been detected in the document :")
        print("Spam keyword", "  =>  ", "TF_IDF count")
        for each in spam_match:
            print(each, "        ", spam_match[each])


# Function computes the TF, IDF and TF-IDF values for a file.
def tf_idf_compute(total_count, dicts, spam_words, corpus_length):
    tf = {}
    """
    Compute term frequency of every word as count(word)/total words in corpus
    """
    for w in dicts:
        tf[w] = int(dicts[w]) / int(total_count)

    idf = {}
    """
    Compute Inverse document frequency as logarithm(count(word)/total words in corpus) to the base 2
    """
    for w in dicts:
        idf[w] = math.log((int(corpus_length) / int(dicts[w])), 2)

    """
    Build the TF-IDF dictionary by multiplying the values of TF and IDF dictionaries
    """
    tf_idf = {}
    for w in set(tf) | set(idf):
        tf_idf[w] = tf.get(w, 0) * idf.get(w, 0)

    check_spam(tf_idf, spam_words)


# Returning the length of the passed element : corpus
def get_corpus_length(corpus):
    return len(corpus)


# Build a corpus from a list that has the path to all the files
def build_corpus(arr):
    corpus = []

    """
    For all the files in the list, do the following
    1. Open the file
    2. Tokenize the text in the file
    3. Store it in a temp array
    4. Add the temp array to the main corpus array
    5. Call the length function
    """
    for path in arr:
        text = process(path)
        temp_list = re.findall(r"[\w']+", text)
        corpus = corpus + temp_list

    # Uncomment for verification only
    # print("The spam corpus for IDF calculation is : ", corpus)

    """
    Returns the function that computes the length of the corpus array
    """
    return get_corpus_length(corpus)


def main():
    path = raw_input("Enter path to pdf to be checked")

    """
    Build a list of spam words from the dictionary pdf
    """
    text = process('/home/anuvrattiku/SPRING_2017/CMPE239/Spam_filter/Spams/Spam Dictionary.pdf')
    keywords_list = text.split("\n")

    """
    Remove the first entry from the list because the first word is "Spam Dictionary"
    """
    spam_words = keywords_list[1:]

    """
    Create a dictionary with the count of words from the path of the file to be scanned
    """
    keywords = process(path)
    words = re.findall(r"[\w']+", keywords)

    dicts = {}
    for w in words:
        if w in dicts:
            dicts[w] += 1
        else:
            dicts[w] = 1

    total_count = len(words)

    """
    Build corpus and get length of corpus for IDF calculation
    """
    corpus_path_list = [
        "/home/anuvrattiku/SPRING_2017/CMPE239/Spam_filter/Spams/Document1.pdf",
        "/home/anuvrattiku/SPRING_2017/CMPE239/Spam_filter/Spams/Document2.pdf",
        "/home/anuvrattiku/SPRING_2017/CMPE239/Spam_filter/Spams/Document3.pdf",
        "/home/anuvrattiku/SPRING_2017/CMPE239/Spam_filter/Spams/Document4.pdf",
        "/home/anuvrattiku/SPRING_2017/CMPE239/Spam_filter/Spams/Document5.pdf",
        "/home/anuvrattiku/SPRING_2017/CMPE239/Spam_filter/Spams/Document6.pdf"
    ]

    corpus_length = build_corpus(corpus_path_list)

    tf_idf_compute(total_count, dicts, spam_words, corpus_length)


if __name__ == '__main__':
    main()