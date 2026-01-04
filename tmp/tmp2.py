# %% [markdown]
# ## Data Cleaning: Remove Irrelevant Columns & Visualize Distributions
# 
# **Dropped columns:**
# - `id`, `id.1`, `house_id`: Just identifiers, no analytical value
# 
# **For each remaining column:** Boxplot (outliers) + Histogram (distribution)

# %%
import matplotlib.pyplot as plt

# Columns to drop
drop_cols = ['id', 'id.1', 'house_id']
df_clean = df.drop(columns=[c for c in drop_cols if c in df.columns])

# Plot numeric columns: Boxplot + Histogram side by side
numeric_cols = df_clean.select_dtypes(include='number').columns

for col in numeric_cols:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 3))
    
    # Boxplot
    ax1.boxplot(df_clean[col].dropna(), vert=False)
    ax1.set_title(f'{col} - Boxplot')
    
    # Histogram
    ax2.hist(df_clean[col].dropna(), bins=30, color='steelblue', edgecolor='black')
    ax2.set_title(f'{col} - Histogram')
    
    plt.tight_layout()
    plt.show()