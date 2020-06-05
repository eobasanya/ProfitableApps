# ProfitableApps
An Analysis on What Makes A Profitable App. Using App Store & Google Play Store Data Sets
Skills from this project include:
1. Data Wrangling: How to import, clean, and load a data set
2. Data Analytics: How to use data science techniques to retrieve insights from data sets. 

#Step 1: Import Data
In the first step of this project we look to import the data for analysis. Both Google Play Store data for Android and AppStore data for iOS.

#Step 2A: Clean Data #
In the first step of the project, we clean the data in this data set.
I then explore the data using the explore function and determine incorrect or missing data and delete them.
From the data source, it was determined that there was missing average reviews on line 1072, shifting all columns in that line to the left. It was deleted.
We also identifying duplicate apps located within the data set, and then determining what makes them different. The main differences between the duplicares are the amount of reviews, which also identify when this data was gathered. As a result, the most recent iteration of the duplicate will be kept in the data set, and the others will be deleted. I will do this by deleting the variants that have the least amount of reviews.
