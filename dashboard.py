import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Load bike rental data
df_day = pd.read_csv("https://github.com/Putannia/project-analysis-data/raw/main/day.csv")

# Rename columns
df_day.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'hr': 'hour',
    'weathersit': 'weather_condition',
    'cnt': 'count'
}, inplace=True)

# Map numerical values to meaningful labels
df_day['month'] = df_day['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
df_day['season'] = df_day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
df_day['weekday'] = df_day['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
df_day['weather_condition'] = df_day['weather_condition'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Heavy Rain/Thunderstorm'
})

# Prepare filter components
min_date = pd.to_datetime(df_day['date']).dt.date.min()
max_date = pd.to_datetime(df_day['date']).dt.date.max()

with st.sidebar:
    st.image('https://image.shutterstock.com/image-vector/bike-rental-flat-vector-illustration-260nw-475943188.jpg')

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Convert 'date' to datetime
df_day['date'] = pd.to_datetime(df_day['date'])

# Convert start_date and end_date to datetime.date
start_date = pd.to_datetime(start_date).date()
end_date = pd.to_datetime(end_date).date()

main_df = df_day[
    (df_day['date'].dt.date >= start_date) & 
    (df_day['date'].dt.date <= end_date)
]

# Rest of the code remains unchanged
# ...

# Pertanyaan 1: Pada bulan apa paling banyak yang merental sepeda?
st.subheader('Bulan dengan Peminjaman Sepeda Tertinggi')

# Membuat DataFrame untuk jumlah peminjaman per bulan
monthly_rentals_df = main_df.groupby('month').agg({'count': 'sum'}).reset_index()

# Menampilkan diagram batang untuk jumlah peminjaman per bulan
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='month', y='count', data=monthly_rentals_df, palette='muted')
st.pyplot(fig)

# Menampilkan bulan dengan jumlah peminjaman tertinggi
max_month = monthly_rentals_df.loc[monthly_rentals_df['count'].idxmax(), 'month']
max_count = monthly_rentals_df['count'].max()
st.write(f"Bulan dengan peminjaman sepeda tertinggi adalah {max_month} dengan total {max_count} peminjaman.")

# Pertanyaan 2: Apakah terdapat hubungan antara suhu/kelembapan dengan jumlah peminjaman?
st.subheader('Hubungan antara Suhu/Kelembapan dan Jumlah Peminjaman')

# Menampilkan scatter plot untuk suhu terhadap jumlah peminjaman
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=main_df, x='temp', y='count', palette='coolwarm', marker='o')
plt.title('Hubungan Suhu dengan Jumlah Peminjaman Sepeda')
plt.xlabel('Suhu (Celsius)')
plt.ylabel('Jumlah Peminjaman')
st.pyplot(fig)

# Menampilkan scatter plot untuk kelembapan terhadap jumlah peminjaman
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=main_df, x='hum', y='count', palette='coolwarm', marker='o')
plt.title('Hubungan Kelembapan dengan Jumlah Peminjaman Sepeda')
plt.xlabel('Kelembapan')
plt.ylabel('Jumlah Peminjaman')
st.pyplot(fig)
