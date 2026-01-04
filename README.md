# King County Housing - Exploratory Data Analysis

## Project

Analysis of King County (Washington, USA) housing data to provide recommendations for a real estate client.

## Client

Bonnie Brown (Seller) - Wants to sell house soon, high profit, middle-class neighborhood.

## Key Insights

1. Timing: Spring/Summer (April-July) shows higher prices and sales volume
2. Location: Distance to Seattle correlates negatively with price (r = -0.3)
3. Renovation: Renovated houses sell for approx. 40% more

## Recommendations

1. List property between April and July
2. Price within middle-class range (Q25-Q75)
3. Consider quality improvements if grade below 7

## Files

- 01_general_eda.ipynb - Data cleaning, EDA, hypothesis testing
- 02.1_bonnie_analysis.ipynb - Client selection and recommendations
- BonnieBrown_Market analysis.pptx - Presentation slides

## Setup
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Data

Export from database (see assignment.md), place CSV in data/ folder.