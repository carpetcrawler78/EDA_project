# Pandas Universal Patterns - Cheat Sheet

Die wichtigsten Patterns für DataFrame-Analysen

---

## 🎯 Die 5 Must-Know Patterns

### 1. Duplikate finden & filtern

```python
# Alle Zeilen mit duplizierten Werten anzeigen
df[df.duplicated(subset='spalte', keep=False)]

# Gruppen mit mehr als N Einträgen
counts = df.groupby('spalte').size()
df[df['spalte'].isin(counts[counts > N].index)]

# Alternative mit value_counts
vc = df['spalte'].value_counts()
df[df['spalte'].isin(vc[vc > N].index)]
```

### 2. Missing Values analysieren

```python
# Prozent Missing pro Spalte
missing_pct = 100 * df.isna().sum() / len(df)

# Zeilen mit NA in bestimmten Spalten
df[df['spalte'].isna()]

# Zeilen OHNE NA
df[df['spalte'].notna()]

# Spalten mit >X% Missing
missing_pct[missing_pct > X]
```

### 3. Groupby → Filter → Map zurück (UNIVERSAL PATTERN!)

```python
# Das Universal Pattern:
grouped = df.groupby('key').agg(...)      # 1. Gruppieren & aggregieren
filter_keys = grouped[bedingung].index    # 2. Keys mit Bedingung extrahieren
result = df[df['key'].isin(filter_keys)]  # 3. Zurück auf Original-DataFrame mappen

# Beispiel: Häuser mit Durchschnittspreis > 500k
avg_price = df.groupby('house_id')['price'].mean()
expensive = avg_price[avg_price > 500000].index
df[df['house_id'].isin(expensive)]

# Beispiel: Kunden mit mehr als 10 Bestellungen
order_counts = df.groupby('customer_id').size()
frequent_customers = order_counts[order_counts > 10].index
df[df['customer_id'].isin(frequent_customers)]
```

### 4. Value Counts für Quick Analysis

```python
# Top N häufigste Werte
df['spalte'].value_counts().head(N)

# Nur Werte mit >X Vorkommen
vc = df['spalte'].value_counts()
frequent = vc[vc > X].index
df[df['spalte'].isin(frequent)]

# Verteilung in Prozent
df['spalte'].value_counts(normalize=True) * 100

# Mit Missing Values (NaN)
df['spalte'].value_counts(dropna=False)
```

### 5. Conditional Filtering kombinieren

```python
# Mehrere Bedingungen mit AND
df[(df['price'] > 100) & (df['bedrooms'] >= 3)]

# OR Bedingung
df[(df['city'] == 'Berlin') | (df['city'] == 'Munich')]

# .isin() für Listen (eleganter als viele OR)
df[df['city'].isin(['Berlin', 'Munich', 'Hamburg'])]

# NOT mit ~ (Tilde)
df[~df['city'].isin(['Berlin'])]

# Komplexe Bedingungen
df[(df['price'] > 100) &
   (df['bedrooms'] >= 3) &
   (df['city'].isin(['Berlin', 'Munich']))]
```

---

## 🔥 Standard-Reihenfolge für EDA

```python
# 1. ÜBERBLICK VERSCHAFFEN
df.shape                      # (rows, columns)
df.info()                     # Datentypen, Memory, Non-Null Count
df.head(10)                   # Erste Zeilen ansehen
df.columns                    # Spaltennamen
df.dtypes                     # Datentypen pro Spalte

# 2. MISSING VALUES
df.isna().sum()                           # Count pro Spalte
missing_pct = 100 * df.isna().sum() / len(df)  # % pro Spalte
df[df.isna().any(axis=1)]                # Alle Zeilen mit mindestens einem NA

# 3. DUPLIKATE
df.duplicated().sum()                    # Wie viele Duplikate?
df[df.duplicated(keep=False)]            # Alle Duplikate anzeigen
df.drop_duplicates()                     # Duplikate entfernen

# 4. VERTEILUNGEN
df['spalte'].value_counts()              # Für kategorische Daten
df['spalte'].describe()                  # Für numerische Daten
df.groupby('key').size()                 # Gruppengröße
df.groupby('key').size().describe()      # Statistik über Gruppengrößen

# 5. OUTLIERS & EXTREME VALUES
df['price'].quantile([0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
df[df['price'] > df['price'].quantile(0.95)]  # Top 5%
df[df['price'] < df['price'].quantile(0.05)]  # Bottom 5%

# 6. KORRELATIONEN (numerisch)
df.corr()                                # Korrelationsmatrix
df.corr()['target_column'].sort_values(ascending=False)
```

---

## 💡 Mental Models

### Pattern A: Komprimieren → Filtern → Expandieren

```python
# Viele Zeilen → Wenige Zeilen → Viele Zeilen
compressed = df.groupby('key').mean()              # DataFrame wird klein
filtered = compressed[compressed['value'] > X]      # Noch kleiner
expanded = df[df['key'].isin(filtered.index)]      # Wieder groß (Original-Zeilen)
```

### Pattern B: Boolean Masking

```python
# Bedingungen erstellen und kombinieren
mask1 = df['price'] > 100
mask2 = df['bedrooms'] >= 3
mask3 = df['city'] == 'Berlin'

# Kombinieren
combined_mask = mask1 & mask2 | mask3  # AND/OR kombinieren
result = df[combined_mask]

# Oder direkt:
result = df[(df['price'] > 100) & (df['bedrooms'] >= 3) | (df['city'] == 'Berlin')]
```

### Pattern C: Method Chaining

```python
# Mehrere Operationen hintereinander
result = (df
    .dropna(subset=['important_col'])           # NAs entfernen
    .query('price > 100 & bedrooms >= 3')       # Filtern
    .groupby('category')                         # Gruppieren
    .agg({'price': 'mean', 'quantity': 'sum'})  # Aggregieren
    .sort_values('price', ascending=False)       # Sortieren
    .head(10)                                    # Top 10
)
```

---

## 📋 Quick Reference Table

| Task | Code | Output |
|------|------|--------|
| **Missing %** | `100 * df.isna().sum() / len(df)` | Series |
| **Duplikate** | `df.duplicated(subset='col', keep=False)` | Boolean Series |
| **Top N Werte** | `df['col'].value_counts().head(N)` | Series |
| **Gruppen filtern** | `df['key'].isin(df.groupby('key').size()[lambda x: x > 1].index)` | Boolean Series |
| **Outliers (Top 5%)** | `df[df['col'] > df['col'].quantile(0.95)]` | DataFrame |
| **Multiple AND** | `df[(cond1) & (cond2)]` | DataFrame |
| **Multiple OR** | `df[(cond1) | (cond2)]` | DataFrame |
| **NOT** | `df[~condition]` | DataFrame |
| **Unique Count** | `df['col'].nunique()` | int |
| **Gruppengröße** | `df.groupby('key').size()` | Series |

---

## 🔍 Wichtige Unterschiede

### `.isna()` vs `.isnull()`
- **Identisch!** Beide machen dasselbe
- Empfehlung: Nutze `.isna()` (moderner)

### `.size()` vs `.count()`
```python
df.groupby('key').size()    # Zählt alle Zeilen (inkl. NaN) → Series
df.groupby('key').count()   # Zählt non-NA pro Spalte → DataFrame
```

### `.duplicated()` Parameter
```python
df.duplicated(keep='first')   # Erstes behalten (Standard)
df.duplicated(keep='last')    # Letztes behalten
df.duplicated(keep=False)     # ALLE als True markieren
```

### `.value_counts()` vs `.groupby().size()`
```python
df['col'].value_counts()      # Sortiert nach Häufigkeit (absteigend)
df.groupby('col').size()      # Sortiert nach Index (aufsteigend)
```

---

## 🎓 Advanced Patterns

### Lambda in Chains
```python
# Lambda für inline Filterung
df[df.groupby('key')['value'].transform('mean') > 100]

# Lambda in .agg()
df.groupby('key').agg(lambda x: x.max() - x.min())

# Lambda mit .filter()
df.groupby('key').filter(lambda x: len(x) > 5)
```

### Query für lesbare Filter
```python
# Statt:
df[(df['price'] > 100) & (df['bedrooms'] >= 3)]

# Nutze .query():
df.query('price > 100 and bedrooms >= 3')

# Mit Variablen:
min_price = 100
df.query('price > @min_price')
```

### Transform für Group-Operations
```python
# Durchschnitt pro Gruppe zu jeder Zeile hinzufügen
df['group_avg'] = df.groupby('category')['price'].transform('mean')

# Zeilen über Gruppendurchschnitt
df[df['price'] > df.groupby('category')['price'].transform('mean')]
```

---

## ⚡ Performance Tipps

```python
# LANGSAM: .apply() mit Lambda
df['new'] = df['old'].apply(lambda x: x * 2)

# SCHNELL: Vectorized Operations
df['new'] = df['old'] * 2

# LANGSAM: Iteration über Zeilen
for idx, row in df.iterrows():
    df.at[idx, 'new'] = row['old'] * 2

# SCHNELL: Vectorized oder .apply() auf Spalten
df['new'] = df['old'] * 2
```

---

## 📌 Häufige Fehler vermeiden

```python
# ❌ FALSCH: Boolean ohne .index
counts = df.groupby('key').size() > 1
df[df['key'].isin(counts)]  # isin() sucht nach True/False!

# ✅ RICHTIG: .index verwenden
counts = df.groupby('key').size() > 1
df[df['key'].isin(counts[counts].index)]

# ❌ FALSCH: Einzelnes & statt &&
df[(df['a'] > 1) and (df['b'] < 5)]  # Error!

# ✅ RICHTIG: & verwenden
df[(df['a'] > 1) & (df['b'] < 5)]

# ❌ FALSCH: Assignment auf Slice
df[df['price'] > 100]['new_col'] = 'expensive'  # SettingWithCopyWarning!

# ✅ RICHTIG: .loc verwenden
df.loc[df['price'] > 100, 'new_col'] = 'expensive'
```

---

## 💾 Datentypen

| Python | NumPy Array | Pandas Series |
|--------|-------------|---------------|
| Built-in | Schnell, homogen | Schnell, mit Index |
| Gemischte Typen ✅ | Nur 1 Typ | Nur 1 Typ |
| Position Index | Position Index | **Label + Position** |
| `[1, 2, 3]` | `np.array([1,2,3])` | `pd.Series([1,2,3])` |
| Langsam (loops) | Sehr schnell (vectorized) | Sehr schnell |

### Wann was?
- **List**: Allgemeine Daten, gemischte Typen, klein
- **NumPy Array**: Mathematik, ML, große numerische Daten
- **Pandas Series**: Eine Spalte aus DataFrame, Labels wichtig

---

**Erstellt: 2026-01-01**
**Für: EDA & Data Analysis mit Pandas**
