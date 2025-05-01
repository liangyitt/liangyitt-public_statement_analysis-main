""" Luke Abbatessa, Yitian Liang, Naman Razdan, Jasmine Wong, Yu Xiao, & Yuting Zheng
    DS3500
    Final Project
    December 7, 2022

    Tokenizes and performs nltk vader analysis on texts

    Consulted nltk website for documentation on tokenize
    https://www.nltk.org/api/nltk.tokenize.html
    Consulted nltk website for documentation on vader
    https://www.nltk.org/howto/sentiment.html
"""

# Import the necessary libraries/packages
import nltk
nltk.download("punkt")
nltk.download("vader_lexicon")
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

def tokenize_sent(text):
    """
      Divide a text into sentences

      Parameters:
          text - entire text of interest (a string)
      Returns: sentences (a list)
    """

    sentences = sent_tokenize(text)

    return sentences


def nltk_score_sent(sentences):
    """
      Take in a list of sentences, implement VADER sentiment scoring on them and return a df
      containing the following columns of information:
       [sentence: the sentence from the text,
       sent_order: the sentence's index in the text,
       sent_pctile: sentence order percentile in the text,
       neg: negative score,
       neu: neutral score,
       pos: positive score
       compound: compound sentiment score for sentence,
       cum_score: text's cumulative compound sentiment score]

      Parameters:
          sentences - sentences as strings (a list)
      Returns: a dataframe
    """

    # Turn sentences list into a df with each sentence as own row
    df = pd.DataFrame(sentences, columns=["sentence"])

    # Make sentence order the index
    df["sent_order"] = df.index

    # Set max index as text length
    text_length = max(df["sent_order"])

    # Create sentence percentile column by dividing sentence index by text length
    df["sent_pctile"] = df["sent_order"] / text_length

    # Initialize VADER sentiment analyzer
    sia = SentimentIntensityAnalyzer()

    # Store sentiment analysis scores into df
    df["neg"] = df["sentence"].apply(lambda x: sia.polarity_scores(x)["neg"])
    df["neu"] = df["sentence"].apply(lambda x: sia.polarity_scores(x)["neu"])
    df["pos"] = df["sentence"].apply(lambda x: sia.polarity_scores(x)["pos"])
    df["compound"] = df["sentence"].apply(lambda x: sia.polarity_scores(x)["compound"])

    # Turn compound scores into a list
    compound_lst = df["compound"].values.tolist()

    # Initialize empty list to store cumulative compound scores
    cumulative_comp_scores = []

    # Initialize cumulative score to be 0
    cum_score = 0

    for comp_score in compound_lst:
        # Set cum_score as old cum_score + compound score for each sentence's compound score
        cum_score = cum_score + comp_score
        cumulative_comp_scores.append(cum_score)

    # Turn cumulative scores into a column in pandas df
    df["cum_score"] = cumulative_comp_scores

    return df
