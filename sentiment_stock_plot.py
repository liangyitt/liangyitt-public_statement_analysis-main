""" Luke Abbatessa, Yitian Liang, Naman Razdan, Jasmine Wong, Yu Xiao, & Yuting Zheng
    DS3500
    Final Project
    December 7, 2022

    Provides a foundation for creating an average sentiment score vs. stock price percentage change plot
"""
# Import necessary libraries
import pandas as pd
import plotly.graph_objects as go
from data_prep import *
from collections import defaultdict

# Define constants and read in files
FILES = {"data_files/british_airways.json": ["data_files/british_airways.json", "British Airways", "text"],
         "data_files/doordash.json": ["data_files/doordash.json", "DoorDash", "text"],
         "data_files/equifax.json": ["data_files/equifax.json", "Equifax", "text"],
         "data_files/hilton.json": ["data_files/hilton.json", "Hilton", "text"],
         "data_files/linkedin.json": ["data_files/linkedin.json", "LinkedIn", "text"],
         "data_files/optus.json": ["data_files/optus.json", "Optus", "text"],
         "data_files/pearson.json": ["data_files/pearson.json", "Pearson", "text"],
         "data_files/target.json": ["data_files/target.json", "Target", "text"],
         "data_files/tmobile.json": ["data_files/tmobile.json", "T-Mobile", "text"],
         "data_files/twitter.json": ["data_files/twitter.json", "Twitter", "text"],
         "data_files/yahoo.json": ["data_files/yahoo.json", "Yahoo", "text"]}

STOCK_DATA = "stock_data_files/new_stock_data.csv"
stock_df = pd.read_csv(STOCK_DATA)

sent_score_df_dict = read_files(FILES)
COMPANIES = stock_df["CompanyName"].drop_duplicates().tolist()


def extract_avg_sent_score_df(sent_score_dct):
    """
      Calculate average sentiment score and compile a dataframe
      of average sentiment score and company name as columns

      Parameters:
           sent_score_dct - a dictionary containing sentiment scores
      Returns: a dataframe
    """

    # Create an empty dictionary
    avg_ss_dct = {}

    # Calculate the average ss score for each company by iterating over each key in the dictionary
    for key in sent_score_dct:
        # Store the average ss scores in a dictionary
        avg_ss_dct[key] = sent_score_dct[key]["compound"].mean()

    # Create a dataframe
    df = pd.DataFrame.from_dict(avg_ss_dct, orient='index').reset_index()
    df.columns = ["company", "avg_ss"]

    return df


def stock_change_percentile_df(stock_df):
    """
      Calculate stock percentile change and compile a dataframe with the
      percent changes and company names as columns

      Parameters:
          stock_df - a dataframe containing stock data
      Returns: a dataframe
    """

    # Create an empty list
    lst = []

    # Iterate over each company name in COMPANIES (lst)
    for i in range(len(COMPANIES)):
        # Group the stock data by company names
        stock_data = stock_df.groupby("CompanyName").get_group(COMPANIES[i])

        # Filter for desired columns
        filtered_df = stock_data.drop(columns=["Description", "Date", "New_Date"])

        # Convert dataframe values to a list
        data_lst = filtered_df.values.tolist()

        # Slice the first and last value from the list
        data_lst = data_lst[::len(data_lst[-1])]

        # Create a list for the first stock data and last stock data from the data_lst
        stock_lst = [data_lst[0][0], data_lst[1][0]]

        # Convert the list to a series
        stock_series = pd.Series(stock_lst)

        # Calculate percent change and convert back to a list
        percent_change = stock_series.pct_change().tolist()

        # Append the companies names to list
        lst.append([data_lst[0][1], percent_change[1]])

    # Create a dataframe
    df = pd.DataFrame(lst, columns=["company", "stock_pc"])

    return df


def sentiment_vs_stock_plot(info_severity):
    """
      Output the cumulative sentiment score vs stock price plot based on the stolen information sensitivity of the
      user's choice

      Parameters:
          info_severity - level of sensitivity of stolen information (a string)
      Returns: a cumulative sentiment score vs stock price plot
    """
    # Create sent_ss df and stock_pc df
    sent_ss = extract_avg_sent_score_df(sent_score_df_dict)
    stock_pc = stock_change_percentile_df(stock_df)

    # Merge stock_pc and sent_ss df
    merged_df = pd.merge(stock_pc, sent_ss, on=["company"])

    # Create a dictionary from merged_df
    sent_stock_dict = defaultdict(dict)

    for name in COMPANIES:
        sent_stock_dict[name] = merged_df.groupby("company").get_group(name)

    # Initialize a plotly.graph_objects instance
    sent_score_vs_stock_price = go.Figure()

    # Initialize severity levels
    info_severity_dct = {"High": ["British Airways", "Equifax", "Hilton", "Optus", "Target", "T-Mobile"],
                         "Medium": ["DoorDash", "LinkedIn", "Twitter", "Yahoo"], "Low": ["Pearson"]}

    # Initialize colors
    colors_lst = ["#80ccff", "#d0d7de", "#6fdd8b", "#eac54f", "#ffb77c", "#ffaba8", "#d8b9ff",
                  "#ffadda", "#ffb4a1", "#57606a", "#7d4e00"]
    colors_idx = 0

    # If a user is not looking to filter companies, plot all companies with appropriate labels
    if info_severity == "All":

        for name in COMPANIES:
            sent_score_vs_stock_price.add_trace(
                go.Scatter(x=sent_stock_dict[name]["avg_ss"], y=sent_stock_dict[name]["stock_pc"], name=name,
                           line=dict(color=colors_lst[colors_idx])))
            colors_idx += 1

        sent_score_vs_stock_price.update_layout(title="All Companies Sentiment Score vs Stock Percent Change",
                                                xaxis_title="Average Cumulative Sentiment Score",
                                                yaxis_title="Stock Percent Change")

        sent_score_vs_stock_price.update_traces(marker=dict(size=15))

    # If a user is looking to filter companies by info severity, plot relevant companies with appropriate labels
    else:
        companies_lst = info_severity_dct[info_severity]
        for name in COMPANIES:
            if name in companies_lst:
                # Add data point if the company is in the severity bracket
                sent_score_vs_stock_price.add_trace(
                    go.Scatter(x=sent_stock_dict[name]["avg_ss"], y=sent_stock_dict[name]["stock_pc"], name=name,
                               hovertext=name, line=dict(color=colors_lst[colors_idx])))
                colors_idx += 1

            # Update Graph Axis Labels
            sent_score_vs_stock_price.update_layout(title=info_severity +
                                                          " Info Sensitivity Companies Sentiment Score" +
                                                          " vs Stock Percent Change",
                                                    xaxis_title="Average Cumulative Sentiment Score",
                                                    yaxis_title="Stock Percent Change")

            sent_score_vs_stock_price.update_traces(marker=dict(size=15))

    return sent_score_vs_stock_price
