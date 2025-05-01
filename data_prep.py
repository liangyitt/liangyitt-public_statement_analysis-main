""" Luke Abbatessa, Yitian Liang, Naman Razdan, Jasmine Wong, Yu Xiao, & Yuting Zheng
    DS3500
    Final Project
    December 7, 2022

    Provides a foundation for gathering VADER sentiment scores for a group of files
"""

# Import the necessary libraries/packages
from textquisite import Textquisite
import textquisite_parsers as tp


def read_files(files):
    """
      Create a dictionary containing lists of VADER scores for a group of files

      Parameters:
          files - a group of files (a dictionary)
      Returns: a dictionary of VADER scores
    """
    # Instantiate a Textquisite object
    txt = Textquisite()

    # Initialize an empty list to store states from user's files
    states_lst = []

    # Iterate through dictionary of file information
    for key in files.keys():

        if key.strip().endswith(".txt"):
            if len(files[key]) == 2:
                # Load text with filename and label if the file is a .txt file
                # and the length of the list containing key's values is 2
                state = txt.load_text(files[key][0], files[key][1], label=files[key][1])
                # Add state to states list
                states_lst.append(state)
            else:
                # Make default label based on filename if the list lacks a label
                state = txt.load_text(files[key][0], key.astype(str) - ".txt", label=key.astype(str) - ".txt")
                states_lst.append(state)

        elif key.strip().endswith(".json"):
            if len(files[key]) == 3:
                # Load text with filename, label, and key with the actual text if
                # the file is a .json file and the length of the list containing key's
                # values if 3
                state = txt.load_text(key, files[key][1], text_key=files[key][2], label=files[key][1],
                                      parser=tp.json_parser)
                # Add state to states list
                states_lst.append(state)
            elif len(files[key]) == 2:
                # Make default label based on filename if the list lacks a label
                state = txt.load_text(key, key.astype(str) - ".json", text_key=files[key][1],
                                      label=key.astype(str) - ".json",
                                      parser=tp.json_parser)
                states_lst.append(state)
            else:
                # Return a message to the user saying the data entry (list with file info) was invalid
                print("Your entry for ", str(key), "is invalid. Please check that you have entered ",
                      "[filename, label, text_key].")

        else:
            # Return a message to the user saying the data entry (file type) was invalid
            print("Your entry for ", str(key), "is invalid. Please check that you have entered a valid file type",
                  "(.json or .txt).")

    # Initialize a dictionary containing lists of only VADER scores for all files
    sent_score_df_dict = {}
    # Use each filelabel as the key and VADER sent_score dataframe as the value for each state for sent_score_df_dict
    for state in states_lst:
        sent_score_df_dict[state["filelabel"]] = state["vader_sent_score_df"]

    return sent_score_df_dict
