# AI Coding Assistant Instructions for EDA Project

## Project Overview
This is an exploratory data analysis (EDA) project on King County housing data. The goal is to analyze housing sales data, derive insights, and provide client-specific recommendations. Key components include data loading, cleaning, statistical analysis, visualization, and presentation.

## Key Files and Structure
- `assignment.md`: Project requirements, client personas, and deliverables
- `workflow.md`: Step-by-step EDA methodology (iterative approach, research questions, cleaning, relationships, presentation)
- `README.md`: Setup instructions (Python 3.11.3, virtual environment, pip install from requirements.txt)
- `EDA.ipynb`: Main analysis notebook with data loading and initial exploration
- `data/`: Directory for CSV files (e.g., `eda.csv` with housing data)
- `REVISION/`: Versioned analysis notebooks (e.g., `01_general_eda.ipynb`, `02_client_selection.ipynb`)
- `tmp/`: Temporary Python scripts for experimentation
- `requirements.txt`: Dependencies (pandas, seaborn, matplotlib, jupyterlab, etc.)

## Coding Patterns and Conventions
- **Data Loading**: Use `pd.read_csv("data/eda.csv")` for housing data; data is pre-saved from database
- **Visualization**: Prefer seaborn over matplotlib for statistical plots; use `plt.rcParams` for consistent styling (white background, 8x5 figure size)
- **Iterative Development**: Follow workflow.md - rough drafts first, then refine plots and code; move working code to functions
- **Client Analysis**: Tailor insights to specific clients (e.g., buyers vs. sellers, budget constraints, location preferences)
- **Documentation**: Use markdown cells in notebooks to explain methodology, interpret results, and document assumptions
- **Data Cleaning**: Handle missing values (impute/remove), outliers, and transformations (log/sqrt for normality)
- **Feature Engineering**: Create derived features (e.g., price per sqft) for better analysis

## Common Workflows
- **Setup Environment**: `python -m venv venv; venv\Scripts\activate; pip install -r requirements.txt`
- **Data Exploration**: Check `df.describe()`, `df.isnull().sum()`, correlation matrices with `sns.heatmap(df.corr())`
- **Hypothesis Testing**: Form research questions (e.g., "Does waterfront affect price?"), visualize relationships
- **Client Recommendations**: Analyze data subsets based on client criteria (e.g., filter by zipcode, price range)
- **Presentation**: Create high-level slides; avoid showing raw code, focus on insights and visuals

## Dependencies and Libraries
- Core: pandas, numpy, matplotlib, seaborn
- Notebook: jupyterlab, ipywidgets
- Database: psycopg2-binary, SQLAlchemy (for data fetching if needed)
- Utilities: missingno (for missing data visualization), python-dotenv

## Best Practices
- Suppress warnings with `warnings.filterwarnings("ignore")` at notebook start
- Use `pd.set_option('display.float_format', lambda x: '%.3f' % x)` for readable floats
- Reference `column_names.md` for data dictionary understanding
- Save intermediate results in `tmp/` during development
- Ensure reproducible environment via requirements.txt

## Example Code Patterns
```python
# Load and initial exploration
df = pd.read_csv("data/eda.csv")
print(df.head())
print(df.describe())

# Correlation analysis
corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Matrix')
plt.show()

# Client-specific filtering (e.g., for buyer with limited budget)
client_df = df[df['price'] < 500000]
sns.scatterplot(data=client_df, x='sqft_living', y='price')
```

Focus on deriving actionable insights from data patterns, not just technical implementation.