#!/usr/bin/env python
# coding: utf-8

# <div style="border:solid black 2px; padding: 20px">
# </div>

# Background:

# The project background is to identify patterns that determine whether a video game can be considered successful or not. The project is for a virtual store named "Ice," which sells video games from all over the world. Data related to user and expert reviews, genre, platform (e.g., Xbox or PlayStation), and historical sales data are available from open sources. The goal is to find the most promising games and plan a marketing campaign for 2017 based on the data from 2016.

# The dataset contains abbreviations, such as ESRB, which stands for Entertainment Software Rating Board, an independent regulatory organization that evaluates game content and assigns age ratings such as Teen or Mature. The project aims to utilize this information and other relevant data to identify the patterns that make a video game successful and leverage these insights to improve the store's marketing strategy.

# # Importing The Data

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats as st

data = pd.read_csv("/datasets/games.csv")
data

# # Preparing The Data

# Check data type and number of columns X rows.

data.info()

# Change the column names into lower strings.

data.rename(columns=str.lower, inplace=True)
data
data.isna().sum()

# From above summary, what we could do with the missing values:
# 1. name & genre = remain as the original value or drop since we will not be able to make up the name of the respective 2 games.
# 2. year_of_release = we can try to match the name of the game and fill in manually.
# 3. cirtic_score, user_score & rating = we can use the algorithm based on the number of general sales.
# The missing values in user_score & rating is most likely intentional (no rating and user/critic score are given).

data['name'].unique()
data['year_of_release'].unique()

# Convert year_of_release and critic_score to integer, and user_score to floating.
# We do not convert sales number and user_score to integer since they contains decimal points.

data['year_of_release'] = data['year_of_release'].fillna(0).astype(int)
data['critic_score'] = data['critic_score'].fillna(0).astype(int)

# Replace "tbd" value with NaN

data['user_score'] = data['user_score'].replace('tbd', np.nan)
data['user_score'] = data['user_score'].astype(float)
data.info()

# # Analyzing The Data

data.describe()

year_grouping = data.groupby('year_of_release')['name'].count()
year_grouping 

# We can analyze the data using histogram by excluding the missing values.

plt.bar(year_grouping.index, year_grouping.values)
plt.xlim(1980,2016)

# From above histogram we could conclude that the production of games we rapidly increased during 2000s and reached its peak in 2008-2009.

data['total_sales'] = data[['na_sales', 'eu_sales', 'jp_sales', 'other_sales']].sum(axis=1)
data

platform_grouping = data.groupby(['platform'])[['total_sales']].sum()
platform_grouping.sort_values(by='total_sales', ascending=False)

# Data Timeframe:

# Since the main objective of this project is to determine the most compelling game for the marketing campaign in 2017, it would be best to set the timeframe period from 2011 onwards.
# The main reason we choose 2011 onwards timeframe is because the declining trend since the peak (2008-2009) has started to stabilize during 2011-2015. Given that period we would be able to find a pattern to predict 2017 trend in the market.

filtered_data = data[data['year_of_release'].between(2011,2016)]
filtered_data

platform_grouping = filtered_data.groupby(['platform'])[['total_sales']].sum()
platform_grouping.sort_values(by='total_sales', ascending=False)

platform_grouping = filtered_data.groupby(['platform','year_of_release'])[['total_sales']].sum()
platform_grouping.sort_values(by='year_of_release', ascending=False)

# From above platform data, we can conclude that:
# 1. For the last 3 years (2014-2016), PS4 was the most used game platform and followed by XOne
# 2. Before 2014, PS3 and 3Ds were more demanded.
# 
# Seeing above data, we can narrow the data timeframe further to 2014-2016 and focus on the top 5 platforms.

filtered_data = data[(data['year_of_release'].between(2014, 2016)) & (data['platform'].isin(['PS4', 'XOne', '3DS', 'PS3', 'X360','PC']))]

filtered_data

sales_by_platform = filtered_data.groupby(['platform'])['total_sales'].sum()
sales_by_platform.sort_values(ascending=False)

plt.subplots(figsize=(15,8))
sns.boxplot(x='platform', y='total_sales', data=filtered_data)

plt.xlabel('Platform')
plt.ylabel('Total Sales (in millions)')
plt.title('Total Sales per Platform (2014-2016)')

plt.show()

# Above boxplot shows that there are a lot of values above the upper whisker of the boxplot, this indicates that there are many data points that are larger than the typical range of values in the dataset. In other words, these data points are outliers that fall outside the range of values that are typically seen in the data.

# There are a few possible reasons:
# 1. There are a few games that are extremely successful and have sold many more copies than other games in the same platform. 2. Another possibility is that the data is skewed and does not follow a normal distribution, which can cause the boxplot to be compressed and the whiskers to be shorter, making it easier for data points to fall outside the whiskers.

# We would need to examine the data in more detail to determine the cause of the outliers and whether they are genuine data points or errors in the data.

sales_by_game_platform = filtered_data.groupby(['name', 'platform'])['total_sales'].sum()
sales_by_game_platform= sales_by_game_platform.sort_values(ascending=False)
sales_by_game_platform.head(15)

# From above data we could see the major difference of a game total_sales in each platform (for example: 'Call of Duty: Black Ops and 'Grand Theft Auto V'
# The differences are quite significant and could be double in value.

game_by_genre = filtered_data.groupby('genre')['total_sales'].sum()
game_by_genre = game_by_genre.sort_values(ascending=False)
game_by_genre

# From above data, we can conclude that action, shooter and sports are the most popular game genre in the market.

# # Profiling the data

region_grouping = filtered_data.groupby('platform')[['na_sales', 'eu
