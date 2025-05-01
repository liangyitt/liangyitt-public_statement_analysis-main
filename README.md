# public_statement_analysis
**Project Overview**  
This project examines the aftermath of data breaches by investigating 11 notable breaches that occurred in the past decade (British Airways, DoorDash, Equifax, Hilton, LinkedIn, Optus, Pearson, Target, T-Mobile, Twitter, and Yahoo). The researchers collected each company’s breach timeline, corporate apology statements, and corresponding stock price data. They then analyzed how the sentiment of these apologies relates to stock fluctuations following the breaches.

**Data and Methodology**  
1. **Data Collection**  
   - The team gathered key dates for each breach (e.g., the day before public disclosure, the day the breach was made public, the day a formal response was issued, and one day after the response).  
   - They retrieved official apology statements from corporate announcements or news coverage.  
   - Stock price data from Yahoo Finance was used to assess market responses around these critical dates.

2. **Analytical Approach**  
   - **Sentiment Analysis (VADER):** Used to generate cumulative sentiment scores for each apology, illustrating how tone evolves from the start to the end of each statement.  
   - **Heaps’ Law Analysis:** Provided insights into language usage and vocabulary richness in each apology.  
   - **Stock Price Fluctuations:** Compared closing prices before and after each breach and corporate response, calculating percentage changes.  
   - **Interactive Dashboard:** Built in Plotly Dash with two main tabs:  
     - **General Overview by Data Sensitivity:** Groups companies by the sensitivity of breached data (high, medium, or low) and shows each one’s cumulative sentiment scores alongside stock price changes.  
     - **Dual Company Comparisons:** Lets users select two companies to compare side by side, including their cumulative sentiment scores, Heaps’ Law plots, and stock charts.

**Key Findings**  
1. In 8 out of 11 apology statements, the cumulative sentiment score increased by the end, suggesting that most companies tried to leave a more positive impression in their closing remarks.  
2. Overall, there was no strong correlation between a company’s sentiment scores and subsequent percentage drops in stock price. For most companies, stock prices trended downward after the breach, regardless of whether the apology was more positively or negatively worded.  
3. **Twitter** was an outlier: its stock price barely dipped after the breach was disclosed and actually climbed after the apology. Possible reasons include:  
   - The vulnerability was disclosed earlier, so investors were already aware.  
   - The leaked data (phone numbers and email addresses) was moderately sensitive.  
   - Twitter’s stock was heavily influenced by other events at that time (e.g., acquisition negotiations), overshadowing the breach’s immediate impact.
