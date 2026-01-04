# %% [markdown]
# ## Analysis
# 
# ** Data Flow

# %%



# 1. LOAD & BASIC CLEAN
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('data/eda.csv')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month

# 2. DEFINE MIDDLE-CLASS (Q25-Q75)
q25, q75 = df['price'].quantile([0.25, 0.75])
df_mid = df[(df['price'] >= q25) & (df['price'] <= q75)]
print(f"Middle-Class: ${q25:,.0f} - ${q75:,.0f} ({len(df_mid)} houses)")

# 3. CHART 1: TIMING (Price by Month)
monthly = df_mid.groupby('month')['price'].mean() / 1000
monthly.plot(kind='bar', color='#2E7D32', edgecolor='black', figsize=(10,5))
plt.title('Average Price by Month (Middle-Class)')
plt.xlabel('Month')
plt.ylabel('Price (K $)')
plt.tight_layout()
plt.savefig('chart_timing.png', dpi=150)
plt.show()

# 4. CHART 2: GEOGRAPHY (Top Zipcodes)
zips = df_mid.groupby('zipcode')['price'].agg(['mean','count'])
zips = zips[zips['count'] >= 50].sort_values('mean', ascending=False).head(5)
zip_prices = df_mid.groupby('zipcode')['price'].mean()
top, bottom = zip_prices.max(), zip_prices.min()

(zips['mean']/1000).plot(kind='barh', color='#2E7D32', edgecolor='black', figsize=(10,5))
plt.title('Top 5 Zipcodes - Middle Class')
plt.xlabel('Price (K $)')
plt.ylabel('Zipcode')
plt.tight_layout()
plt.savefig('chart_geography.png', dpi=150)
plt.show()

# 5. CHART 3: QUALITY (Price by Grade)
grades = df_mid.groupby('grade')['price'].mean() / 1000
grades.plot(kind='bar', color='#D4A574', edgecolor='black', figsize=(10,5))
plt.title('Average Price by Grade (Middle-Class)')
plt.xlabel('Grade')
plt.ylabel('Price (K $)')
plt.tight_layout()
plt.savefig('chart_quality.png', dpi=150)
plt.show()

# 6. KEY STATS FOR PPT
print(f"\n=== KEY STATS ===")
print(f"Best month: {monthly.idxmax()} (${monthly.max()*1000:,.0f})")
print(f"Worst month: {monthly.idxmin()} (${monthly.min()*1000:,.0f})")
print(f"Top zipcodes: {zips.index.tolist()}")
print(f"Grade-Price correlation: {df_mid['grade'].corr(df_mid['price']):.2f}")

# =============================================================================
# exact calculations
# =============================================================================

import pandas as pd

# Load data
#df = pd.read_csv('eda.csv')
#df['date'] = pd.to_datetime(df['date'])
#df['month'] = df['date'].dt.month

print("=" * 60)
print("1. MIDDLE-CLASS DEFINITION")
print("=" * 60)
q25 = df['price'].quantile(0.25)
q75 = df['price'].quantile(0.75)
df_mid = df[(df['price'] >= q25) & (df['price'] <= q75)]
print(f"Q25: ${q25:,.0f}")
print(f"Q75: ${q75:,.0f}")
print(f"Total houses: {len(df)}")
print(f"Middle-Class houses: {len(df_mid)} ({len(df_mid)/len(df)*100:.1f}%)")

print("\n" + "=" * 60)
print("2. TIMING - PRICE BY MONTH")
print("=" * 60)
monthly = df_mid.groupby('month')['price'].mean()
best_month = monthly.idxmax()
worst_month = monthly.idxmin()
best_price = monthly.max()
worst_price = monthly.min()
diff_abs = best_price - worst_price
diff_pct = (best_price - worst_price) / worst_price * 100

print(monthly.sort_values(ascending=False).apply(lambda x: f"${x:,.0f}"))
print(f"\nBest month: {best_month} (${best_price:,.0f})")
print(f"Worst month: {worst_month} (${worst_price:,.0f})")
print(f"Difference: ${diff_abs:,.0f} ({diff_pct:.1f}%)")

# Spring/Summer vs Winter
spring_summer = df_mid[df_mid['month'].isin([4,5,6,7])]['price'].mean()
winter = df_mid[df_mid['month'].isin([11,12,1,2])]['price'].mean()
season_diff = (spring_summer - winter) / winter * 100
print(f"\nSpring/Summer avg: ${spring_summer:,.0f}")
print(f"Winter avg: ${winter:,.0f}")
print(f"Seasonal difference: {season_diff:.1f}%")

print("\n" + "=" * 60)
print("3. GEOGRAPHY - TOP ZIPCODES")
print("=" * 60)
zips = df_mid.groupby('zipcode')['price'].agg(['mean', 'count'])
zips = zips[zips['count'] >= 50].sort_values('mean', ascending=False)
print("Top 5 Zipcodes (min 50 sales):")
for i, (zc, row) in enumerate(zips.head(5).iterrows(), 1):
    print(f"  {i}. {zc}: ${row['mean']:,.0f} (n={row['count']:.0f})")

# Location price difference
top_zip_price = zips['mean'].max()
bottom_zip_price = zips['mean'].min()
location_diff = (top_zip_price - bottom_zip_price) / bottom_zip_price * 100
print(f"\nTop zipcode: ${top_zip_price:,.0f}")
print(f"Bottom zipcode: ${bottom_zip_price:,.0f}")
print(f"Location difference: {location_diff:.1f}%")

print("\n" + "=" * 60)
print("4. QUALITY - GRADE CORRELATION")
print("=" * 60)
corr = df_mid['grade'].corr(df_mid['price'])
print(f"Grade-Price correlation: {corr:.3f}")

# Price by grade
grades = df_mid.groupby('grade')['price'].mean()
print("\nPrice by Grade:")
print(grades.apply(lambda x: f"${x:,.0f}"))

# Grade 7 to 8 difference
if 7 in grades.index and 8 in grades.index:
    g7_to_g8 = grades[8] - grades[7]
    print(f"\nGrade 7→8 difference: ${g7_to_g8:,.0f}")

print("\n" + "=" * 60)
print("5. EXPECTED PROFIT (Timing + Quality)")
print("=" * 60)
median_price = df_mid['price'].median()
timing_gain = median_price * (season_diff / 100)
print(f"Median Middle-Class price: ${median_price:,.0f}")
print(f"Timing gain ({season_diff:.1f}%): ${timing_gain:,.0f}")

print("\n" + "=" * 60)
print("SUMMARY FOR PPT")
print("=" * 60)
print(f"Middle-Class: ${q25:,.0f} - ${q75:,.0f}")
print(f"Sample size: {len(df_mid)} houses")
print(f"Best timing: Month {best_month} (+{diff_pct:.1f}% vs worst)")
print(f"Top Zipcode: {zips.index[0]} (${top_zip_price:,.0f})")
print(f"Location impact: {location_diff:.0f}%")
print(f"Grade correlation: {corr:.2f}")