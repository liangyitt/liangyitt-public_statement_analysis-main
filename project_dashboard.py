""" Luke Abbatessa, Yitian Liang, Naman Razdan, Jasmine Wong, Yu Xiao, & Yuting Zheng
    DS3500
    Final Project
    December 7, 2022

    Establishes dashboard illustrating data breach corporate apology comparisons

    Consulted matplotlib for different color schemes to use
    https://matplotlib.org/stable/gallery/color/named_colors.html
    Consulted GeeksforGeeks for the documentation for plotly.graph_objects.Scatter
    https://www.geeksforgeeks.org/scatter-plot-in-plotly-using-graph_objects-class/
    Consulted plotly for more information regarding the documentation for html.Label
    https://dash.plotly.com/dash-html-components/label
    Consulted dofactory for information regarding the title attribute of html.Label
    https://www.dofactory.com/html/label/title
    Consulted Python HTML.label Examples for examples where html.Label is being used
    https://python.hotexamples.com/examples/clld.web.util.htmllib/HTML/label/python-html-label-method-examples.html
    Consulted Python Dash styling for Tab layout
    https://dash.plotly.com/dash-core-components/tabs
"""

# Import the necessary libraries/packages
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
from sentiment_stock_plot import *
from textquisite import Textquisite
import matplotlib.colors as mcolors
import matplotlib
from stock_price_plot import *
from dash_bootstrap_templates import load_figure_template

matplotlib.use("TkAgg")

# Instantiate the necessary constants
URL_THEME = dbc.themes.DARKLY

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

COMPANIES = ["British Airways", "DoorDash", "Equifax", "Hilton", "LinkedIn", "Optus", "Pearson", "Target", "T-Mobile",
             "Twitter", "Yahoo"]
COLORS = [color for color in mcolors.CSS4_COLORS]

SEVERITIES = ["All", "High", "Medium", "Low"]

LINESTYLES = ["solid", "dot", "dash", "longdash", "dashdot", "longdashdot"]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "padding": "2rem 1rem",
    "background-color": "#303030",
    "overflow": "scroll",
}

CONTENT_STYLE = {
    "margin-left": "16rem",
    "margin-right": ".5rem",
    "padding": "2rem 1rem",
}

# Initialize a dictionary containing lists of only VADER scores for all files
sent_score_df_dict = read_files(FILES)

# Read in the .csv file containing the stock data for each company as a df
stock_df = pd.read_csv(STOCK_DATA)

# Build a dashboard app
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[URL_THEME, dbc_css])
load_figure_template("DARKLY")

# Establish the sidebar of the dashboard's second tab with six dropdown tools
# (three per company --> one choosing the company, one choosing the plot color, one choosing the plot linestyle)
tab2_sidebar = html.Div(
    [
        html.H4("SELECTIONS"),

        html.P("1st Company to Analyze"),
        dcc.Dropdown(id="company1", options=COMPANIES, value="British Airways", clearable=False),
        html.P("1st Company: Color"),
        dcc.Dropdown(id="color1", options=COLORS, value="red", clearable=False),
        html.P("1st Company: Linestyle"),
        dcc.Dropdown(id="linestyle1", options=LINESTYLES, value="solid", clearable=False),

        html.Br(),
        html.Br(),

        html.P("2nd Company to Analyze"),
        dcc.Dropdown(id="company2", options=COMPANIES, value="LinkedIn", clearable=False),
        html.P("2nd Company: Color"),
        dcc.Dropdown(id="color2", options=COLORS, value="green", clearable=False),
        html.P("2nd Company: Linestyle"),
        dcc.Dropdown(id="linestyle2", options=LINESTYLES, value="dash", clearable=False)],

    style=SIDEBAR_STYLE,
    className="dbc",
)

# Establish the actual content of the dashboard's second tab with six total plots
# (three per company --> one cumulative sentiment score plot, one Heap's Law plot, one stock price plot)
# Supplement the three graphs per company with the company name and a brief description of the company
tab2_content = html.Div([

    dbc.Row(html.H1("Data Breach Corporate Apology Comparisons", style={"textAlign": "center"})),

    dbc.Row(html.Div(id="company1_name")),
    dbc.Row(html.H6(id="company1_description")),
    dbc.Row([
        dbc.Col(dcc.Graph(id="sent_score_lineplot1"), width=4),
        dbc.Col(dcc.Graph(id="heaps_law1"), width=4),
        dbc.Col(dcc.Graph(id="stock_data1"), width=4)
    ]),

    dbc.Row(html.H3(id="company2_name"), align="start"),
    dbc.Row(html.H6(id="company2_description")),
    dbc.Row([
        dbc.Col(dcc.Graph(id="sent_score_lineplot2"), width=4),
        dbc.Col(dcc.Graph(id="heaps_law2"), width=4),
        dbc.Col(dcc.Graph(id="stock_data2"), width=4)
    ])],

    style=CONTENT_STYLE
)

# Establish the sidebar of the dashboard's first tab with one dropdown tool
# (chooses companies to focus on based on the sensitivity of the stolen information involved in the data breaches)
tab1_sidebar = html.Div(
    [
        html.H4("SELECTIONS"),
        html.P("Please selection an option"),
        html.P("below to filter companies by"),
        html.P("sensitivity of information"),
        html.P("leaked in data breach"),
        dcc.Dropdown(id="severity", options=SEVERITIES, value="All", clearable=False),

        html.Br()],

    style=SIDEBAR_STYLE,
    className="dbc",
)

# Establish the actual content of the dashboard's first tab
# (includes a page title, descriptions of the dropdown options, an all-company-total-sentiment-score plot, an
# all-company-sentiment-score-vs-stock-percent-change plot, and a footnote regarding missing stock data)
tab1_content = html.Div([
    dbc.Row(html.H1("General Overview By Leakage Severity", style={"textAlign": "center"})),

    dbc.Row(html.H4("Stolen Information Sensitivity Filter")),

    html.Br(),

    dbc.Row(html.H5("High sensitivity data: complete credit card information, social security numbers, "
                    "driver's licence numbers, and/or passport information.")),

    html.Br(),

    dbc.Row(html.H5("Medium sensitivity data: incomplete credit card information, login credentials, "
                    "physical addresses, phone numbers, birthdays and/or other social media accounts and usernames.")),

    html.Br(),

    dbc.Row(html.H5("Low sensitivity data: names, emails and/or genders.")),

    dbc.Row([
        dcc.Graph(id="all_changing_ss_plot")
    ]),
    dbc.Row([
        dcc.Graph(id="sent_vs_stock")
    ]),

    dbc.Row(html.H6("*DoorDash and Yahoo do not have valid stock data for the dates surrounding their data breaches."))

], style=CONTENT_STYLE)

# Craft the dashboard's display with tab and color specifications
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label="General Companies Overview", children=html.Div([tab1_sidebar, tab1_content])),
        dcc.Tab(label="Dual Company Comparisons", children=html.Div([tab2_sidebar, tab2_content])),
    ], colors={
        "border": "Black",
        "primary": "rgb(0,91,150)",
        "background": "rgb(52,52,52)"})
])


@app.callback(
    Output("company1_name", "children"),
    Input("company1", "value")
)
def display_first_comp_name(company1):
    """
      Output the name of the first company on the dashboard's second tab based on the company of the user's choice

      Parameters:
          company1 - name of a company (a string)
      Returns: a heading on the dashboard with a company's name
    """
    return html.H3(company1)


@app.callback(
    Output("company1_description", "children"),
    Input("company1", "value")
)
def display_first_comp_description(company1):
    """
      Output the description of the first company on the dashboard's second tab based on the company of the user's
      choice

      Parameters:
          company1 - name of a company (a string)
      Returns: text on the dashboard with a company's description
    """
    stock_data = stock_df.groupby("CompanyName").get_group(company1)
    return html.H6(stock_data["Description"])


@app.callback(
    Output("sent_score_lineplot1", "figure"),
    Input("company1", "value"),
    Input("color1", "value"),
    Input("linestyle1", "value")
)
def display_first_sent_score_plot(company1, color1, linestyle1):
    """
      Output the cumulative sentiment score plot of the first company on the dashboard's second tab based on the
      company, plot color, and plot linestyle of the user's choice

      Parameters:
          company1 - name of a company (a string)
          color1 - line plot color (a string)
          linestyle1 - line plot linestyle (a string)
      Returns: a cumulative sentiment score plot
    """
    sent_score = Textquisite.changing_ss_plot(sent_score_df_dict, company1, color1, linestyle1)
    return sent_score


@app.callback(
    Output("sent_score_lineplot2", "figure"),
    Input("company2", "value"),
    Input("color2", "value"),
    Input("linestyle2", "value")
)
def display_second_sent_score_plot(company2, color2, linestyle2):
    """
      Output the cumulative sentiment score plot of the second company on the dashboard's second tab based on the
      company, plot color, and plot linestyle of the user's choice

      Parameters:
          company2 - name of a company (a string)
          color2 - line plot color (a string)
          linestyle2 - line plot linestyle (a string)
      Returns: a cumulative sentiment score plot
    """
    sent_score = Textquisite.changing_ss_plot(sent_score_df_dict, company2, color2, linestyle2)
    return sent_score


@app.callback(
    Output("stock_data1", "figure"),
    Input("company1", "value"),
    Input("color1", "value"),
    Input("linestyle1", "value")
)
def display_first_stock_price_plot(company1, color1, linestyle1):
    """
      Output the stock price plot of the first company on the dashboard's second tab based on the company, plot color,
      and plot linestyle of the user's choice

      Parameters:
          company1 - name of a company (a string)
          color1 - line plot color (a string)
          linestyle1 - line plot linestyle (a string)
      Returns: a stock price plot
    """
    stock_price = graph_stock_data(company1, color1, linestyle1)
    return stock_price


@app.callback(
    Output("company2_name", "children"),
    Input("company2", "value")
)
def display_second_comp_name(company2):
    """
      Output the name of the second company on the dashboard's second tab based on the company of the user's choice

      Parameters:
          company2 - name of a company (a string)
      Returns: a heading on the dashboard with a company's name
    """
    return html.H3(company2)


@app.callback(
    Output("company2_description", "children"),
    Input("company2", "value")
)
def display_second_comp_description(company2):
    """
      Output the description of the second company on the dashboard's second tab based on the company of the user's
      choice

      Parameters:
          company2 - name of a company (a string)
      Returns: text on the dashboard with a company's description
    """
    stock_data = stock_df.groupby("CompanyName").get_group(company2)
    return html.H6(stock_data["Description"])


@app.callback(
    Output("heaps_law1", "figure"),
    Input("company1", "value"),
    Input("color1", "value"),
    Input("linestyle1", "value")
)
def display_first_heaps_law_plot(company1, color1, linestyle1):
    """
      Output the Heap's Law plot of the first company on the dashboard's second tab based on the company, plot color,
      and plot linestyle of the user's choice

      Parameters:
          company1 - name of a company (a string)
          color1 - line plot color (a string)
          linestyle1 - line plot linestyle (a string)
      Returns: a Heap's Law plot
    """
    heaps_law = Textquisite.heaps_law_graph(company1, color1, linestyle1)
    return heaps_law


@app.callback(
    Output("heaps_law2", "figure"),
    Input("company2", "value"),
    Input("color2", "value"),
    Input("linestyle2", "value")
)
def display_second_heaps_law_plot(company2, color2, linestyle2):
    """
      Output the Heap's Law plot of the second company on the dashboard's second tab based on the company, plot color,
      and plot linestyle of the user's choice

      Parameters:
          company2 - name of a company (a string)
          color2 - line plot color (a string)
          linestyle2 - line plot linestyle (a string)
      Returns: a Heap's Law plot
    """
    heaps_law = Textquisite.heaps_law_graph(company2, color2, linestyle2)
    return heaps_law


@app.callback(
    Output("stock_data2", "figure"),
    Input("company2", "value"),
    Input("color2", "value"),
    Input("linestyle2", "value")
)
def display_second_stock_price_plot(company2, color2, linestyle2):
    """
      Output the stock price plot of the second company on the dashboard's second tab based on the company, plot color,
      and plot linestyle of the user's choice

      Parameters:
          company2 - name of a company (a string)
          color2 - line plot color (a string)
          linestyle2 - line plot linestyle (a string)
      Returns: a stock price plot
    """
    stock_price = graph_stock_data(company2, color2, linestyle2)
    return stock_price


@app.callback(
    Output("all_changing_ss_plot", "figure"),
    Input("severity", "value")
)
def display_all_changing_ss_plot(severity):
    """
      Output the cumulative sentiment score plot of all companies on the dashboard's first tab based on the stolen
      information sensitivity of the user's choice

      Parameters:
          severity - level of sensitivity of stolen information (a string)
      Returns: a cumulative sentiment score plot
    """
    fig = Textquisite.all_changing_ss_plot(sent_score_df_dict, severity)

    return fig


@app.callback(
    Output("sent_vs_stock", "figure"),
    Input("severity", "value")
)
def render_sent_vs_stock_plot(severity):
    """
      Output the sentiment score vs stock percent change plot of all companies on the dashboard's first tab based on the
      stolen information sensitivity of the user's choice

      Parameters:
          severity - level of sensitivity of stolen information (a string)
      Returns: a sentiment score vs stock percent change plot
    """
    fig = sentiment_vs_stock_plot(severity)

    return fig


# Run the dashboard app
app.run(debug=True)
