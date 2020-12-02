from django.shortcuts import render
from django.shortcuts import render
from django.core.paginator import Paginator

# Create your views here.
import tweepy
import re
from textblob import TextBlob


api_key ="sVVeugJRfE5hPcbLT8bdc8XtV"
api_secret_key = "JuKIhv8i2BHd4YOe0QEIQKFBJevs9bB3ZDP1Jut7EWV002FGw2"
access_token = "1193497106826137601-t1pOMpxi3aASswRIbXe2iZF69Poztj"
access_token_secret = "WPLTU4K2jWyXR67ERcbxtm12bqTZjeq0L1x4NmQTEAwjy"

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def cekSentimen(request):
	katakunci = request.POST['katakunci']

	hasilSearch = api.search(q=str(katakunci), lang="en", count=100)

	def cleaning_text(processed_feature):
	    # Remove all the special characters
	    processed_feature = re.sub(r'\W', ' ', str(processed_feature))

	    # remove all single characters
	    processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

	    # Remove single characters from the start
	    processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 

	    # Substituting multiple spaces with single space
	    processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

	    # Removing prefixed 'b'
	    processed_feature = re.sub(r'^b\s+', '', processed_feature)

	    # Converting to Lowercase
	    processed_feature = processed_feature.lower()

	    return processed_feature

	hasilAnalisis = []

	text = []

	for tweet in hasilSearch:
	    tweet_properties = {}
	    tweet_properties['tanggal'] = tweet.created_at
	    tweet_properties['user'] = tweet.user.screen_name
	    tweet_properties['tweet'] = tweet.text
	    tweet_bersih = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet.text).split())
	    tweet_bersih = re.sub(r'^https?:\/\/.*[\r\n]*', '', tweet_bersih, flags=re.MULTILINE)
		    
	    analysis = TextBlob(tweet_bersih)
	    text.append(analysis) 

	    if analysis.sentiment.polarity > 0:
	        tweet_properties['sentiment'] = 'positif'
	    elif analysis.sentiment.polarity == 0:
	        tweet_properties['sentiment'] = 'netral'
	    else:
	        tweet_properties['sentiment'] = 'negatif'

	    if tweet.retweet_count > 0:
	        if tweet_properties not in hasilAnalisis:
	            hasilAnalisis.append(tweet_properties)
	    else: 
	        hasilAnalisis.append(tweet_properties)
	
	tweet_positif = [t for t in hasilAnalisis if t['sentiment'] == 'positif']
	tweet_netral = [t for t in hasilAnalisis if t['sentiment'] == 'netral']
	tweet_negatif = [t for t in hasilAnalisis if t['sentiment'] == 'negatif']

	jml_positif = len(tweet_positif)
	jml_netral = len(tweet_netral)
	jml_negatif = len(tweet_negatif)


	p1 = Paginator(hasilAnalisis, 8)
	
	p2 = Paginator(text, 8)

	page_number = request.GET.get('page')
	page_obj1 = p1.get_page(page_number)
	page_obj2 = p2.get_page(page_number)

	arrays = zip(page_obj1, page_obj2)

	jmlAll = len(hasilAnalisis)

	context={
	'katakunci':katakunci,
	'jmlPos':'{:0.2f}'.format(jml_positif*100/jmlAll),
	'jmlNet':'{:0.2f}'.format(jml_netral*100/jmlAll),
	'jmlNeg':'{:0.2f}'.format(jml_negatif*100/jmlAll),
	'tweet_positif':tweet_positif,
	'tweet_negatif':tweet_negatif,
	'tweet_netral':tweet_netral,
	'array':arrays,
	}
	return render(request, "sentiment.html", context)


def index(request):
	context ={

	}

	return render(request, "home.html", context)