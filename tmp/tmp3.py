import pandas as pd

df = pd.read_csv('data/eda.csv')
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month

q25, q75 = df['price'].quantile([0.25, 0.75])
df_mid = df[(df['price'] >= q25) & (df['price'] <= q75)]

# TIMING
monthly = df_mid.groupby('month')['price'].mean()
print("MONTHLY (for chart):")
for m, p in monthly.items():
    print(f"  {m}: {p/1000:.0f}")

# GEOGRAPHY
zips = df_mid.groupby('zipcode')['price'].agg(['mean','count'])
zips = zips[zips['count'] >= 30].sort_values('mean', ascending=False)
print("\nTOP ZIPCODES (for chart):")
for zc, row in zips.iterrows():
    print(f"  {zc}: {row['mean']/1000:.0f}")

# GRADE
grades = df_mid.groupby('grade')['price'].mean()
print("\nGRADES (for chart):")
for g, p in grades.items():
    print(f"  {g}: {p/1000:.0f}")
    
corr = df_mid['grade'].corr(df_mid['price'])
print(f"Grade-Price correlation: {corr:.3f}")

# Location influence: Top vs Bottom zipcode (mit >= 30 sales)
zips = df_mid.groupby('zipcode')['price'].agg(['mean','count'])
zips = zips[zips['count'] >= 30]

print(zips)

top = zips['mean'].max()
bottom = zips['mean'].min()
diff_pct = (top - bottom) / bottom * 100

print(f"Top: ${top:,.0f}")
print(f"Bottom: ${bottom:,.0f}")
print(f"Difference: {diff_pct:.1f}%")
