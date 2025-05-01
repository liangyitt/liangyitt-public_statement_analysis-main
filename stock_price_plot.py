""" Luke Abbatessa, Yitian Liang, Naman Razdan, Jasmine Wong, Yu Xiao, & Yuting Zheng
    DS3500
    Final Project
    December 7, 2022

    Graphs stock price plot
"""

# Import the necessary libraries/packages
import plotly.graph_objects as go
import pandas as pd

# Instantiate the necessary constants
STOCK_DATA = "stock_data_files/new_stock_data.csv"

# Read in the .csv file containing the stock data for each company as a df
stock_df = pd.read_csv(STOCK_DATA)


def graph_stock_data(company, color, linestyle):
    """
      Output the stock price plot based on the company, plot color, and plot linestyle of the user's choice

      Parameters:
          company - name of a company (a string)
          color - line plot color (a string)
          linestyle - line plot linestyle (a string)
      Returns: a stock price plot
    """
    # Initialize a plotly.graph_objects instance
    fig = go.Figure()

    # Plot an empty graph if the chosen company doesn't have stock data available
    if company == "DoorDash" or company == "Yahoo":
        fig.update_layout(title="No Stock Data Available For " + str(company) + " During Breach")

    # Plot a line plot comparing companies' timelines following data breaches to their stock prices otherwise
    else:
        stock_data = stock_df.groupby("CompanyName").get_group(company)
        fig.add_trace(go.Scatter(x=stock_data["New_Date"], y=stock_data["Close"],
                                 line=dict(color=color, dash=linestyle)))

        fig.update_xaxes(title="Date and Date Description")
        fig.update_yaxes(title="Closing Stock Price")
        fig.update_layout(title=str(company) + " Stock Fluctuations")
        fig.update_layout(transition_duration=500)

    return fig
