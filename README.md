## Movie Rating Prediction using Twitter Sentiment Analysis

A System to Predict Movie Rating based on Sentiment of tweets about a movie.  
* Used **Twitter API** to collect tweets about a movie.  
* Used **Python** for **Data cleaning**.  
* Used **Naive Bayes Classiﬁer** to classify sentiment of tweets.  
* Calculated rating of movie based on sentiment classiﬁcations. 

#### **Modules of Proposed System**
##### **Tweet Collection**  
Twitter data can be accessed through the public API provided by the Twitter. These APIs can be accessed only by authentication requests, which must be signed with valid login ID and password. Twitter provides authentication keys for extractions of the tweets. We have to follow some steps to create Authentication keys.

i. Create application on twitter.  
ii. Manage Application 
iii. Change the permissions to read and write.  
iv. Retrieve Authentication keys.

Tweet Extracted from twitter having complete information like date of tweet, tweet ID, user ID, re Tweet count etc. 
Twitter API was used to fetch all the tweets related to a particular movie and all the news and comments related to a particular movie.

##### **Tweet Classification**
* Tweets were tokenized into different tokens separated by space and compare each token with our predefined set of positive and negative bag of words. 
* After the comparison of tokens we find the total number of positive and negative tokens in the tweet. 
* Count the total number of positive and negative tokens in the tweet and label them as p and n respectively. 
* Calculate the value of ratio as total number of positive tokens to the total number of positive and negative token. 
* Naïve bayes classifier was used for sentiment analysis of a tweet, which will classify a tweet into various categories . 
* For every word in the text, we get the number of times that word occurred in the reviews for a given class, add 1 to smooth the value,    and divide by the total number of words in the class (plus the class_count to also smooth the denominator). 

##### **Rating Calculation** 
Every label carries a rating score with it which is used to calculate the overall score of a movie based on labels of its tweets. 
