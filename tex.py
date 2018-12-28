import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
from collections import Counter
import csv
import re

class TwitterClient(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
		access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)

    return input_txt
# creating object of TwitterClient Class
api = TwitterClient()
# calling function to get tweets
tweets = api.get_tweets(query = 'Thor movie', count = 500)
print("\nFirst 200 sample tweets")
print(tweets[0:200])
# Read in the training data.
with open("train.tsv", 'r') as file:
    reviews = list(csv.reader(file,delimiter='\t'))
    #for row in reviews :
    #   print(row[3])

    def get_text(reviews, score):
    # Join together the text in the reviews for a particular tone.
    # We lowercase to avoid "Not" and "not" being seen as different words, for example.
        return " ".join([r[2].lower() for r in reviews if r[3] == score])

    def count_text(text):
        # Split text into words based on whitespace.  Simple but effective.
        words = re.split("\s+", text)
        # Count up the occurence of each word.
        return Counter(words)

    somewhat_negative_text = get_text(reviews,'1')
    negative_text = get_text(reviews,'0')
    neutral_text=get_text(reviews,'2')
    somewhat_positive_text = get_text(reviews,'3')
    positive_text = get_text(reviews,'4')

    # Generate word counts for negative tone.
    negative_counts = count_text(negative_text)
    #print(negative_counts)
    # Generate word counts for positive tone.
    positive_counts = count_text(positive_text)

    somewhat_negative_counts = count_text(somewhat_negative_text)
    neutral_counts = count_text(negative_text)
    somewhat_positive_counts = count_text(somewhat_positive_text)


    print("\nNegative text sample: {0}".format(negative_text[:100]))
    print("Positive text sample: {0}".format(positive_text[:100]))
    print("Some what negative text sample: {0}".format(somewhat_negative_text[:100]))
    print("Some what positive text sample: {0}".format(somewhat_positive_text[:100]))
    print("Neutral text sample: {0}".format(neutral_text[:100]))

    def get_y_count(score):
        # Compute the count of each classification occuring in the data.
        return len([r for r in reviews if r[3] == str(score)])

    # We need these counts to use for smoothing when computing the prediction.
    positive_review_count = get_y_count(4)
    print("\nPositive review count : ",positive_review_count)

    negative_review_count = get_y_count(0)
    print("Negative Review count : ",negative_review_count)

    neutral_review_count=get_y_count(2)
    print("Neutral review count : ",positive_review_count)

    somewhat_positive_review_count = get_y_count(3)
    print("Somewhat Positive review count : ",positive_review_count)

    somewhat_negative_review_count = get_y_count(1)
    print("Somewhat Negative  review count : ",positive_review_count)
    


    # These are the class probabilities (we saw them in the formula as P(y)).
    prob_positive = positive_review_count / len(reviews)
    prob_negative = negative_review_count / len(reviews)

    prob_neutral = neutral_review_count / len(reviews)
    prob_somewhat_positive = somewhat_positive_review_count /len(reviews)
    prob_somewhat_negative = somewhat_negative_review_count/len(reviews)

    def make_class_prediction(text, counts, class_prob, class_count):
        prediction = 1
        text_counts = Counter(re.split("\s+", text))
        for word in text_counts:
            # For every word in the text, we get the number of times that word occured in the reviews for a given class, add 1 to smooth the value, and divide by the total number of words in the class (plus the class_count to also smooth the denominator).
            # Smoothing ensures that we don't multiply the prediction by 0 if the word didn't exist in the training data.
            # We also smooth the denominator counts to keep things even.
            prediction *=  text_counts.get(word) * ((counts.get(word, 0) + 1) / (sum(counts.values()) + class_count))
        # Now we multiply by the probability of the class existing in the documents.
        return prediction * class_prob

    # As you can see, we can now generate probabilities for which class a given review is part of.
    # The probabilities themselves aren't very useful -- we make our classification decision based on which value is greater.
    print("\nReview: {0}".format(reviews[1][2]))
    print("\nNegative prediction: {0}".format(make_class_prediction(reviews[1][2], negative_counts, prob_negative, negative_review_count)))
    print("Positive prediction: {0}".format(make_class_prediction(reviews[1][2], positive_counts, prob_positive, positive_review_count)))
    print("Neutral prediction: {0}".format(make_class_prediction(reviews[1][2], neutral_counts, prob_neutral, neutral_review_count)))
    print("Some what Positive prediction: {0}".format(make_class_prediction(reviews[1][2], somewhat_positive_counts, prob_somewhat_positive, somewhat_positive_review_count)))
    print("Some what Negative prediction: {0}".format(make_class_prediction(reviews[1][2], somewhat_negative_counts, prob_somewhat_negative, somewhat_negative_review_count)))

    def make_decision(text, make_class_prediction):
        # Compute the probabilities.
        negative_prediction = make_class_prediction(text, negative_counts, prob_negative, negative_review_count)
        positive_prediction = make_class_prediction(text, positive_counts, prob_positive, positive_review_count)
        neutral_prediction  = make_class_prediction(text, neutral_counts, prob_neutral, neutral_review_count)
        somewhat_positive_prediction = make_class_prediction(text, somewhat_positive_counts, prob_somewhat_positive, somewhat_positive_review_count)
        somewhat_negative_prediction = make_class_prediction(reviews[0][2], somewhat_negative_counts, prob_somewhat_negative, somewhat_negative_review_count)
        # We assign a classification based on which probability is greater.
        m= max(negative_prediction,positive_prediction,negative_prediction,somewhat_negative_prediction,somewhat_positive_prediction)
        if m==negative_prediction:
            return 1
        elif m==positive_prediction:
            return 5
        elif m==neutral_prediction:
            return 3
        elif m==somewhat_positive_prediction:
            return 4
        elif m==somewhat_negative_prediction:
            return 2
        else :
            return 0

test=[]
for i in tweets:
    test.append(i["text"])
predictions = [make_decision(r[2], make_class_prediction) for r in test]

print("\nFirst 50 predictions")
print(predictions[0:50])
print("\n=====Rating=====")
print(sum(predictions)/len(predictions))
