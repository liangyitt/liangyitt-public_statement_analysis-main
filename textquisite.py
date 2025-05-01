""" Luke Abbatessa, Yitian Liang, Naman Razdan, Jasmine Wong, Yu Xiao, & Yuting Zheng
    DS3500
    Final Project
    December 7, 2022

    Establishes the reusable NLP library known as Textquisite

    Consulted matplotlib for documentation for matplotlib.pyplot.legend
    https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html
    Consulted statology for placing legend in a certain place in a figure
    https://www.statology.org/matplotlib-legend-position/#:~:text=To%20change%20the%20position%20of%20a%20legend%20in,upper%20left%20corner%20of%20the%20plot%3A%20plt.legend%28loc%3D%27upper%20left%27%29
    Consulted plotly for the documentation for plotly.express.line
    https://plotly.com/python-api-reference/generated/plotly.express.line
    Consulted plotly for coding different graphs using plotly.express
    https://plotly.com/python/figure-labels/
    Consulted DelftStack for the plotly parameters color_discrete_sequence and line_dash_sequence
    https://www.delftstack.com/howto/plotly/plotly-line-chart/#:~:text=We%20can%20also%20change%20the%20line%20style%20of,the%20above%20line%20chart.%20See%20the%20code%20below.
    Consulted plotly for plotting line plots with go.Scatter
    https://plotly.com/python/line-charts/#line-plot-with-goscatter
    Consulted GeeksforGeeks for more information regarding string formatting
    https://www.geeksforgeeks.org/string-formatting-in-python/
"""

# Import the necessary libraries/packages
from collections import defaultdict, Counter
from sentiment_nltk import *
import plotly.graph_objects as go
import nltk

# Instantiate the necessary constants
STOP_WORDS = [
    "ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out", "very",
    "having",
    "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into", "of", "most", "itself",
    "other",
    "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the", "themselves", "until", "below", "are",
    "we",
    "these", "your", "his", "through", "don", "nor", "me", "were", "her", "more", "himself", "this", "down", "should",
    "our", "their", "while", "above", "both", "up", "to", "ours", "had", "she", "all", "no", "when", "at", "any",
    "before",
    "them", "same", "and", "been", "have", "in", "will", "on", "does", "yourselves", "then", "that", "because", "what",
    "over", "why", "so", "can", "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too",
    "only",
    "myself", "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by",
    "doing", "it", "how", "further", "was", "here", "than"
]
PUNC = """!()-[]{};:'"\,<>./?@#$%^&*_~—‘’“”–"""


# Instantiate a Textquisite class
class Textquisite:

    def __init__(self):
        """ Constructor for the Textquisite class """
        self.data = defaultdict(dict)

    def _save_results(self, label, results):
        """
          Turn the state into a dictionary of dictionaries whose keys are the names of the attributes of each file and
          whose values are the actual attributes

          Parameters:
              label - identifier of a file (a string)
              results - the state (a dictionary of dictionaries)
          Returns: nothing, just edits the state
        """
        for key, value in results.items():
            self.data[key][label] = value

    @staticmethod
    def load_stop_words(stopfile=None, delimiter=","):
        """
          Load a list of stop words with which the user can use to filter a file of interest

          Parameters:
              stopfile - stopwords (a list)
              delimiter - a separator of elements of a file (a string)
          Returns: a list of stopwords
        """
        # Return the defaulted list of stopwords
        if stopfile is None:
            stopfile = STOP_WORDS
        if stopfile == STOP_WORDS:
            return stopfile
        # Return an empty string if there is no defaulted list
        elif stopfile is None:
            return []
        # Read in a stopfile and transform it into a list of stopwords otherwise
        else:
            with open(stopfile, encoding="utf8") as infile:
                text = infile.read()
                words = text.split(delimiter)
                words = [word.strip() for word in words]
                return words

    @staticmethod
    def _default_parser(filename, filelabel):
        """
          Pre-process a generic text file and store it as a dictionary of dictionaries to serve as the state

          Parameters:
              filename - the name of a text file (a string)
              filelabel - a label for the file (a string)
          Returns: the state (a dictionary of dictionaries)
        """
        with open(filename, encoding="utf8") as infile:

            # Read a text file
            text = infile.read()

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
            stop_words = Textquisite.load_stop_words()

        # Remove stop words from the text
        clean_words = []
        for word in words:
            if word not in stop_words and word != "":
                clean_words.append(word)

        # Join all text in list and create word tokens for the joined text
        combined_text = " ".join(clean_words)
        word_tokens = nltk.wordpunct_tokenize(combined_text)

        # Create empty set and empty lists
        uniq_words = set()
        total_words = []
        distinct_words = []

        # Iterate over each index and token in the work_tokens and
        # add each token into uniq_words set and add each number into total_words list
        # and add the length of the uniq_words into distinct_words list
        for i, token in enumerate(word_tokens):
            uniq_words.add(token)
            total_words.append(i)
            distinct_words.append(len(uniq_words))

        # Implement the state
        results = {
            "filename": str(filename),
            "filelabel": filelabel,
            "wordcount": Counter(clean_words),
            "numwords": len(clean_words),
            "vader_sent_score_df": nltk_sent_score_df,
            "distinctwords": distinct_words,
            "totalwords": total_words
        }

        return results

    def load_text(self, filename, filelabel, text_key=None, label=None, parser=None):
        """
          Register a text file with the NLP framework

          Parameters:
              filename - the name of a file (a string)
              filelabel - a label for the file (a string)
              text_key - the key of a json file holding the actual text (a string)
              label - identifier of a file (a string)
              parser - a parser used to pre-process and store a file as the state (a function)
          Returns: the state (a dictionary of dictionaries)
        """

        # Use the default parser when there is no parser defined
        if parser is None:
            results = Textquisite._default_parser(filename, filelabel)
        # Use the desired parser otherwise
        else:
            results = parser(filename, filelabel, text_key)

        # Save the results in the format of the state
        self._save_results(label, results)

        return results

    @staticmethod
    def changing_ss_plot(states_df_dict, key, color, linestyle):
        """
          Overlay a line plot comparing the sentence order percentile of a text to its cumulative sentiment score

          Parameters:
              states_df_dict - dictionary in the format {filename: vader_ss_df} (a dictionary)
              key - key in states_df_dct (a string)
              color - the color of the chart (a string)
              linestyle - the linestyle of the chart (a string)
          Returns: the plot
        """

        # Plot an apology's sentence order percentile as x and cumulative sentiment score as y
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=states_df_dict[key]["sent_pctile"], y=states_df_dict[key]["cum_score"],
                                 line=dict(color=color, dash=linestyle)))

        fig.update_layout(title=f"{key} VADER Total Sentiment Score",
                          xaxis_title="Sentence Order %",
                          yaxis_title="Cumulative Sentiment Score")

        return fig

    @staticmethod
    def all_changing_ss_plot(states_df_dict, info_severity):

        """
          Overlay a line plot comparing the sentence order percentile of a text to all companies' cumulative sentiment
          scores

          Parameters:
              states_df_dict - dictionary in the format {filename: vader_ss_df} (a dictionary)
              info_severity - level of sensitivity of stolen information (a string)
          Returns: the plot
        """

        # Initialize colors
        colors_lst = ["#80ccff", "#d0d7de", "#6fdd8b", "#eac54f", "#ffb77c", "#ffaba8", "#d8b9ff",
                      "#ffadda", "#ffb4a1", "#57606a", "#7d4e00"]

        colors_idx = 0

        # Initialize severity levels
        info_severity_dct = {"High": ["British Airways", "Equifax", "Hilton", "Optus", "Target", "T-Mobile"],
                             "Medium": ["DoorDash", "LinkedIn", "Twitter", "Yahoo"], "Low": ["Pearson"]}

        # Plot apologies' sentence order percentile as x and cumulative sentiment score as y
        fig = go.Figure()

        # If the user is not looking to filter, plot all companies with appropriate labels
        if info_severity == "All":

            for key in states_df_dict:
                fig.add_trace(go.Scatter(x=states_df_dict[key]["sent_pctile"], y=states_df_dict[key]["cum_score"],
                                         name=key, line=dict(color=colors_lst[colors_idx])))
                colors_idx += 1

            fig.update_layout(title="All Companies VADER Total Sentiment Score",
                              xaxis_title="Sentence Order %",
                              yaxis_title="Cumulative Sentiment Score")

        # If the user is looking to filter by info severity, plot all relevant companies with appropriate labels
        else:
            companies_lst = info_severity_dct[info_severity]

            for key in states_df_dict:

                if key in companies_lst:
                    fig.add_trace(go.Scatter(x=states_df_dict[key]["sent_pctile"], y=states_df_dict[key]["cum_score"],
                                             name=key, hovertext=key, line=dict(color=colors_lst[colors_idx])))

                colors_idx += 1

            fig.update_layout(title=str(info_severity) + " Info Sensitivity Changing Sentiment Score Throughout Text",
                              xaxis_title="Sentence Order %",
                              yaxis_title="Cumulative Sentiment Score")

        return fig

    @staticmethod
    def heaps_law_graph(filelabel, color, linestyle):
        """
          Overlay a line plot comparing the total number of words of a text to the number of distinct words

          Parameters:
              filelabel - a label for a text of interest (a string)
              color - line plot color (a string)
              linestyle - line plot linestyle (a string)
          Returns: the plot
        """

        # Register one of the company apologies with the NLP framework
        txt = Textquisite()
        txt.load_text("data_files/" + filelabel + ".txt", filelabel)

        # Gather the apology's distinct words and total words
        distinct_words = list(txt.data["distinctwords"].values())
        total_words = list(txt.data["totalwords"].values())

        # Initialize a plotly.graph_objects instance
        fig = go.Figure()

        # Plot a line plot comparing the apology's total words to its distinct words
        fig.add_trace(go.Scatter(x=total_words[0], y=distinct_words[0],
                                 line=dict(color=color, dash=linestyle)))

        fig.update_layout(title=f"{filelabel} Heap's Law Graph",
                          xaxis_title="Total Words",
                          yaxis_title="Distinct Words")

        return fig
