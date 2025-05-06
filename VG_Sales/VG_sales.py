# This is a Python script to analyze video game sales data.

import pandas as pd
import matplotlib.pyplot as plt

sales = pd.read_csv("C:\\Users\\aley0\\Visual Studio Code\VG_Sales\\vgsales.csv", index_col=0)
print(sales.shape)
sales.head(100)

#----------------------------------------------------------------------------------------------------------------
# Which of the three seventh generation consoles (Xbox 360, Playstation 3, and Nintendo Wii) had the highest total sales globally?
Seventh_gen = sales[sales['Platform'].isin(['X360', 'PS3', 'Wii'])]

# Games for each 7th gen Platform
print(Seventh_gen['Platform'].value_counts())

# Sum of the sales in each region and globaly for each 7th gen platform
sales_7th = Seventh_gen.pivot_table(index='Platform', values=('NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales','Global_Sales'), aggfunc='sum')

sales_7th.loc[sales_7th['Global_Sales'].idxmax(), ['Global_Sales']]


#----------------------------------------------------------------------------------------------------------------
# average sales for games in the most popular three genres in NA, EU, and global
sales['Genre'].unique()
sales['Genre'].value_counts()

# Pivot Table for Genres and Sales
sales_genre = sales.pivot_table(index='Genre', values=['NA_Sales', 'EU_Sales', 'Global_Sales'], 
                                aggfunc='sum')

# Top 3 Genres by Sales
top3_genres = sales_genre.sort_values(by=['Global_Sales'], ascending=False).head(3)

# Plot the Top 3 Genres by Sales
fig, ax = plt.subplots()

ax.bar(top3_genres.index, top3_genres['EU_Sales'], label= 'EU Sales')
ax.bar(top3_genres.index, top3_genres['NA_Sales'], bottom = top3_genres['EU_Sales'], label= 'NA Sales')
ax.bar(top3_genres.index, top3_genres['Global_Sales'], bottom = top3_genres['EU_Sales'] + top3_genres['NA_Sales'], label= 'Global Sales')

ax.set_xlabel('Genres')
ax.set_ylabel('Sales')
ax.set_title('Stacked Global Sales by Genre')

plt.legend()
plt.show()



#----------------------------------------------------------------------------------------------------------------
# Are some genres significantly more likely to perform better or worse in Japan than others? If so, which ones?

# Function to Explore Sales by region
def Top_sales_by_genre(sales, region, top_n):
    genre_sales = sales.pivot_table(index='Genre', values=region, aggfunc='sum')
    top_genres = genre_sales.sort_values(by=region, ascending=False).head(top_n)
    return top_genres

top5_genre_JP = Top_sales_by_genre(sales, 'JP_Sales', 5)
top5_genre_NA = Top_sales_by_genre(sales, 'NA_Sales', 5)
top5_genre_EU = Top_sales_by_genre(sales, 'EU_Sales', 5)

fig, ax = plt.subplots(1, 3, figsize=(15, 5))  # Create a 1x3 grid of subplots

# Plot for Japan
ax[0].bar(top5_genre_JP.index, top5_genre_JP['JP_Sales'], color='gold', label='Top 5 Genres Sales in Japan')
ax[0].set_title('Japan')
ax[0].set_xlabel('Genre')
ax[0].set_ylabel('Sales')
ax[0].legend()

# Plot for North America
ax[1].bar(top5_genre_NA.index, top5_genre_NA['NA_Sales'], color='silver', label='Top 5 Genres Sales in North America')
ax[1].set_title('North America')
ax[1].set_xlabel('Genre')
ax[1].legend()

# Plot for Europe
ax[2].bar(top5_genre_EU.index, top5_genre_EU['EU_Sales'], color='black', label='Top 5 Genres Sales in Europe')
ax[2].set_title('Europe')
ax[2].set_xlabel('Genre')
ax[2].legend()

# Add a title for the entire figure
fig.suptitle('Top 5 Genre Sales by Region', fontsize=16)

# Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.95])  # Leave space for the suptitle

# Show the plot
plt.show()

# Top 1 Genre in Japan
top5_genre_JP.loc[top5_genre_JP['JP_Sales'].idxmax(), ['JP_Sales']]