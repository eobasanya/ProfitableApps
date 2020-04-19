#!/usr/bin/env python
# coding: utf-8

# # Profitable App Store Project
# ---
# This project will determine the most profitable apps on the iOS App Store and Android's Google Play Store. I will be garnering profitability insights from the dapp store/ google play store datasets. Skills from this project include:
#     1. How to import and clean a data set.
#     2. How to use data science techniques to retrieve insights from data sets. 

# # Step 1: Import Data 
# ---
# - In the first step of this project we look to import the data for analysis. Both Google Play Store data for Android and AppStore data for iOS. 

# In[71]:


from csv import reader

### Google Play data set ###
opened_file = open("googleplaystore.csv", encoding='utf8')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

### The App Store data set ###
opened_file = open('AppleStore.csv', encoding='utf8')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In[73]:


def explore_data(dataset, start, end, rows_and_columns = False):
    dataset_slice = dataset[start:end]
    for row in dataset_slice:
        print(row)
        print('\n')  #prints new line for space
        
    if rows_and_columns:
        print('Number of Rows:', len(dataset))
        print('Number of Columns:', len(dataset[0]))

#See first 3 rows of each data set. 
print(ios_header)
print('\n')
explore_data(ios,0,3, True)  


print(android_header)
print('\n')
explore_data(android,0,3, True)  

    


# In[3]:


print(len(android))
del android[10472] 
print(len(android))


# # Step 2A: Clean Data 
# ---
# - In the first step of the project, we clean the data in this data set. 
# - I then explore the data using the **explore function** and determine incorrect or missing data and delete them. 
#     - From the data source, it was determined that there was missing average reviews on line 1072, shifting all columns in that line to the left. It was deleted. 
# - We also identifying duplicate apps located within the data set, and then determining what makes them different. The main differences between the duplicares are the amount of reviews, which also identify when this data was gathered. As a result, the most recent iteration of the duplicate will be kept in the data set, and the others will be deleted. I will do this by deleting the variants that have the least amount of reviews. 
# 

# In[69]:


reviews_max = {}
for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews

    
print('Expected length:', len(android) - 1181)
print('Actual length:', len(reviews_max))


# In[68]:


android_clean = []
already_added = []

for appname in android:
    name = appname[0]
    n_reviews = float(appname[3])

    if (n_reviews == reviews_max[name]) and (name not in already_added):
            android_clean.append(appname)
            already_added.append(name)

explore_data(android_clean, 0, 3, True)
#print('Number of duplicate apps:',len(duplicates))
#print('Number of remaining apps:',len(cleaned))
#print('Duplicate Apps:', duplicates[:3])


# Step 2B: Removing Non-English Apps
# ---
# ___
# After removing the apps that are duplicated and apps with missing data, we now focus on removing non english apps. We will do this by putting to use the ASCII: American Standard Code for Information Interchange 
# 
# - Without diving too much into the ASCII, more information on it can be seen [here](https://www.ascii-code.com/). We will be using it to determine which characters are not a part of the english language, which app names include them in the title, and use this factor to determine non english apps and remove them from the dataset. 

# In[67]:


def english_test(string):
    
    for character in string: 
        if ord(character) > 127:
            return False
    return True 
    
print(english_test('Instagram'))
print(english_test('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(english_test('Instachat 😜'))


# As mentioned previously, the ASCII codes characters as a respective ASCII number. 'a' is 97 and 'A' is 65. all characters used within the english language end at 127. Thus, anything over 127 is tagged as a non english character as it iterates over each character in the input string passed through the function. 
# 
# We can see that there's a slight problem however, as emojis are over 127 in their ASCII designation. Thus we will have to make slight edits to this rule. 

# In[66]:


def english_app(string):
    non_ascii = 0
    for character in string: 
        if ord(character) > 127:
            non_ascii += 1 
    if non_ascii > 3:
        return False
    return True 
print(english_app('Instagram'))
print(english_app('爱奇艺PPS -《欢乐颂2》电视剧热播'))
print(english_app('Instachat 😜'))


# - I have decided to update the criteria of what is classified as an english app and what isn't, increasing the counter to 3 instead of only one character over 127. 
# - As a result, apps with up to 3 emojis will be kept as English apps. Otherwise, app titles with fall names in another language (more than 3 characters within the name) will be classified as non english. 
# - We will now apply it to our data set and determine how many apps remain that are english 

# In[140]:


android_english = []
android_nonenglish = []
ios_english = []
ios_nonenglish = []

for app in android_clean:
    name = app[0] 
    if english_app(name) == True:
        android_english.append(app)
    else:
        android_nonenglish.append(app)

for app in ios:
    name = app[0] 
    if english_app(name) == True:
        ios_english.append(app)
    else:
        ios_nonenglish.append(app)

explore_data(android_english, 0,1, True)
#explore_data(android_nonenglish, 0,1, True)
print('\n')
explore_data(ios_english, 0,1, True)
print('\n')

#explore_data(ios_nonenglish, 0,1, True)
print('Number of English Android Apps:', len(android_english))
print('Number of Non - English Android Apps:', len(android_nonenglish))
print('\n')

print('Number of English ios Apps:', len(ios_english))
print('Number of Non - English ios Apps:', len(ios_nonenglish))
            


# Step 2C: Removing Paid Apps
# ---
# ___
# This analysis will be focused on apps that are free and gain revenue form in app purchases and advertising. I've chosen this decision as there will need to be a deeper analysis per genre to determine profitability of apps per genre. As someone is more than likely to buy certain apps more than others. Paying 5 dollars for a Bible App might be viewed as less valuable than paying 5 dollars for a well made financial responsibility app. The quality of the app begins to become a more significant factor in the price than the genre itself, which is our focus. 
# 
# In addition, it is not certain that paid apps bring in more revenue than non paid apps. There are microtrasactions in free mobile games that has generated hundreds of millions, and there are paid apps that have less than a million purchases. There are also paid apps with in app purchases which affects our analysis in determining app profitability given the data we are currently using.  
# 
# As a result, I will remove paid apps and focus on analysing free apps. This will be done by identifying the columns associated with the app cost on both android and iOS. 
# 

# In[114]:


ios_freeapps = []
android_freeapps = []

for app in android_english:
    app_cost = app[6]
    if app_cost == 'Free': 
        android_freeapps.append(app)
for app in ios_english:
    app_cost = app[5]
    if app_cost == '0':
        ios_freeapps.append(app)
        
print(android_freeapps[0])
print(ios_freeapps[0])
print('Number of Free Android Apps:', len(android_freeapps))
print('Number of Free iOS apps:', len(ios_freeapps))
android_final = android_freeapps
ios_final = ios_freeapps


# Step 3A: Profitability Analysis 
# ---
# ___
# As mentioned previously This analysis will be focused on apps that are free and gain revenue form in app purchases and advertising. 
# 
# To minimize the risk of developing an unsuccessful app we will be looking to focus on 3 seperate steps. 
#    1. Build minimal version of an android app for Google Play
#    2. Determine reception, if positive develop further. 
#    3. If app is profitable after 6 months develop an app for iOS and add to the App Store. 
#    
# Since our goal is to be as profitable as possible in our app development, we will look to find the most successful app genres on both platforms. As this might be an indicator of a uniqely successful idea.

# In[307]:


android_final = android_freeapps
ios_final = ios_freeapps
def freq_table(dataset, index):
    table = {}
    total = 0 
    for row in dataset: 
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else : 
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key]/total) * 100
        table_percentages[key] = percentage
        
    return table_percentages
            
def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
display_table(ios_final, -5)


# In the above we use the frequency table to determine the percentage of iOS apps per genre. iOS apps can be seen as more of a games and entertainment platform. Where below, we see that the highest catogory is family. At first glance Android might seem to be more of a family platform, however taking a second look at the family category we see that this might not be the case. As a variety of games apps are categorized as family. This highlights the issue with the google play categorizations, and the lack of clearly defined delineations.  
# 
# ![Image](https://www.lowyat.net/wp-content/uploads/2015/06/Google-Play-Store-Family-Category.jpg)	

# In[123]:


display_table(android_final, 1) # Category column


# In[308]:


display_table(android_final, -4) #genres column 


# We see that in the second column included that identifies category on the google play story, it includes many more categories listed. With the highest percentage of apps in a particular genre being tools. More information on how Google expects developers to identify categories can be seen [here](https://support.google.com/googleplay/android-developer/answer/113475?hl=en). 

# Most Popular Users By genre (App Store
# ---
# ___
# To start, we'll be performing an analys is on the most popular apps by genre. Due to the iOS data set not including install data, we will aim to use the average number of ratings  per genre as a proxy. As a result, we will need to name a frequency table in order to calculate the averages manually, as average number of ratings per genre  is not included in the data set. 

# In[302]:


import operator
genres_ios = freq_table(ios_final, -5)
genres_data = {}

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[6])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)
    
       

    


# Popular iOS App
# ---
# ___
# 
# Based on this list, we can see that the top 3 categories that have the highest average number of ratings are Reference, Music and social networking. Let's take a closer look at this category to see the respective apps that lie within them. 

# In[142]:


for app in ios_final:
    if app[-5] == 'Reference':
        print(app[2], ':', app[6]) #print name and number of ratings


# In[303]:


for app in ios_final:
    if app[-5] == 'Music':
        print(app[2], ':', app[6]) # print name and number of ratings
        


# In[143]:


for app in ios_final:
    if app[-5] == 'Social Networking':
        print(app[2], ':', app[6]) #print name and number of ratings
        


# It seems quite clear that for profitability on iOS, these app categories should be considered first. Some of the most popular apps in these categories are religious apps, dictionaries, music streaming services, music identification, and messaging apps. 

# Most Popular Users By genre (Google Play Store)
# ---
# ___
# 
# In this scenario, google play data set does indeed have user install data. As a result we will use this as a method to determine popularity. 

# In[306]:


display_table(android_final, 5) # the Installs columns


# Though the user install data is a great start to identify popularity, it's is not precise enough to determine where within each bracket these percentages lie. For example, we are unsure of how many of 100,000+ percentages lies at 200,000, 300,000 or 400,000. However for our purposes, this gives a good snapshot of the breakdown in installs. Let's now breakdown the average number of installs by category to determine which category has the highest average number  of user installs. 
# 

# In[309]:


categories_android = freq_table(android_final, 1)
for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:            
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# Based on the android install data within the android data set the following apps stand out with the highest average number of user installs:
#     - Communication
#     - Social
#     - Photography
#     - Productivity
#     - Games
#     - Entertainment 
#     - Books & Reference 
# 
# You can already begin to see some similarities. The iOS data showed that Books and Reference, communication, and music were at the top within the google play store. Depending on categorization styles, both social and communication can be seen as the same category, and music can be considered within an entertainment category (which is not included within the android data set. 

# In[311]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                      or app[5] == '500,000,000+'
                                      or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])# A look at communication apps for android


# In[315]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                      or app[5] == '5,000,000+'
                                      or app[5] == '10,000,000+'):
        print(app[0], ':', app[5]) # A look at the books and reference apps for android.


# In[316]:


for app in android_final:
    if app[1] == 'GAME' and (app[5] == '1,000,000+'
                                      or app[5] == '5,000,000+'
                                      or app[5] == '10,000,000+'):
        print(app[0], ':', app[5]) # A look at the gaming apps for android.


# In[155]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'GAME') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# We can see that there are some similarities between iOS data and Google Play Store data, however there are a much higher number of gaming apps on Android than there are on iOS. Outside of this difference, both platforms show that communication, social media, and books and reference are lucrative categories to get into, as they draw the largest number of users. 

# Conclusion
# ---
# ___
# 

# This initial project began with a desire to develop a successful mobile app. Before embarking on this endeavor we begin by determining the most profitable apps, with a focus on users leading to profitability. Data sets were obtained from both Apple's App store and google's Google play store to get a wide enough understanding on what genres are popular irrespective of platform. The focus was on free apps, as paid apps bring a factor of quality into the equation that we were not looking to analyse for this project. To minimize the risk of developing an unsuccessful app we looked to focus on 3 seperate steps.
# 
# 1. Build minimal version of an android app for Google Play
# 2. Determine reception, if positive develop further.
# 3. If app is profitable after 6 months develop an app for iOS and add to the App Store. 
# 
# The first step began with an exraction of the data and a cleaning of the data. The data was cleaned by removing missing or incorrect indeces, removing duplicate entries seen within the data, removing as many non - english apps as possible, and removing paid apps. All of this was done on both the iOS data set and android data set. 
# 
# An analysis was then performed. It was determined that irrespective of the two platforms, communication, social media, and books/reference were 3 of the most popular categories. Outliers included gaming apps, which was significantly prevalent on the Google Play store. Due to communication and social media apps being highly competitive currently, an app focusing on books/reading has a high chance of being successful, with a focus on religion proving to be the most popular within this category. Features such as daily quotes, progress tracking, and more would need to be added to said app in order to remain competitive. With this data based approach, the likelihood of developing a successful app has increased.  
