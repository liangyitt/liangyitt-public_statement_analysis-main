""" Luke Abbatessa, Yitian Liang, Naman Razdan, Jasmine Wong, Yu Xiao, & Yuting Zheng
    DS3500
    Final Project
    December 7, 2022

    Establishes a custom .json parser for the user to implement
"""

# Import the necessary libraries/packages
import json
from textquisite import Textquisite
from collections import Counter
from sentiment_nltk import *

# Instantiate the necessary constants
STOP_WORDS = ["ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out",
              "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into",
              "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the",
              "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me",
              "were", "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both",
              "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and",
              "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over",
              "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too",
              "only", "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my",
              "against", "a", "by", "doing", "it", "how", "further", "was", "here", "than"]

PUNC = """!()-[]{};:'"\,<>./?@#$%^&*_~—‘’“”–"""


def json_parser(filename, filelabel, text_key, stopfile=None):
    """
      Pre-process a .json file/data file and store it as a dictionary of dictionaries to serve as the state

      Parameters:
          filename - the name of a .json file (a string)
          filelabel - a label for the file (a string)
          text_key - the name of the key within the .json file that holds the text of interest (a string)
          stopfile - stopwords (a list)
      Returns: the state (a dictionary of dictionaries)
    """
    # Read a .json file
    if stopfile is None:
        stopfile = STOP_WORDS
    infile = open(filename, encoding="utf8")
    raw = json.load(infile)
    text = raw[text_key]

    # Divide the text string into sentences
    sentences = tokenize_sent(text)
    # Create a dataframe containing sentiment scores data from VADER sentiment analysis
    nltk_sent_score_df = nltk_score_sent(sentences)

    # Remove instances of "\n" in the text
    words = text.split("\n")
    text = " ".join(words)
    words = text.split(" ")
    # Replace instances of "\ufeff" with an empty string
    words = [word.replace("\ufeff", "") for word in words]
    # Replace special characters with an empty string for each word
    for char in PUNC:
        words = [word.replace(char, "") for word in words]

    # Remove leading and trailing white spaces for elements in words
    words = [word.strip() for word in words]

    # Make each word lowercase
    words = [word.lower() for word in words]

    # Load a list of stop words using the STOP_WORDS constant
    stop_words = Textquisite.load_stop_words(stopfile)

    # Remove stop words from the text
    clean_words = []
    for word in words:
        if word not in stop_words and word != "":
            clean_words.append(word)

    # Implement the state
    results = {
        "filename": str(filename),
        "filelabel": filelabel,
        "wordcount": Counter(clean_words),
        "numwords": len(clean_words),
        "vader_sent_score_df": nltk_sent_score_df,
    }

    # Close the file
    infile.close()

    return results
