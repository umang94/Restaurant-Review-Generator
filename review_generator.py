from urllib.parse import quote
import requests
from pprint import pprint
from summarizer import summarize
from textblob import TextBlob
import sys

# ID for Hyderabad, India
# TODO : Implement global search with restaurant options
city_id = "6"

# User Inputted Values
restaurant_name = sys.argv[2]
api_key = sys.argv[1]
required_sentiment = sys.argv[3]

#Constants
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": api_key}
baseRequestURL= "https://developers.zomato.com/api/v2.1/"

def search(restaurantName,cityId):
    search_param = "search?entity_id=" + cityId + "&entity_type=city&q=" + quote(restaurantName)
    search_request_url = baseRequestURL + search_param

    # Bunch of try catches to handle invalid inputs gracefully
    try:
        response = requests.get(search_request_url,headers=header)
    except Exception as e:
        raise Exception("Remote Call to Zomato failed")

    search_response = (response.json())
    if(response.status_code != 200):
        raise Exception("Remote call to zomato failed")
    
    if len(search_response['restaurants']) == 0:
        raise Exception("No matching restaurants found in Zomato for restaruant " + restaurantName)

    # Zomato returns the restaurant in order of the closest matches to inputted name, Hence, picking the first one.
    restaurant_match = search_response['restaurants'][0]['restaurant']['name']
    restaurant_id = search_response['restaurants'][0]['restaurant']['id']
    
    return restaurant_match, restaurant_id

def get_reviews(restaurantId):
    url = baseRequestURL +  "reviews?res_id=" + restaurantId
    response = requests.get(url,headers=header)
    review_response = (response.json())

    return review_response["user_reviews"]

def getSummarizedReview(reviews):
    combined_review_text = ""
    for review in reviews:
        combined_review_text += review["review"]["review_text"]
    new_review_list = summarize("Review",combined_review_text)

    pos_reviews = []
    neg_reviews = []
    for summarized_review in new_review_list:
        textBlob = TextBlob(summarized_review)
        if(textBlob.sentiment.polarity > 0):
            pos_reviews.append(summarized_review)
        else:
            neg_reviews.append(summarized_review)


    output_review = None
    if(required_sentiment == "negative"):
        output_review = ("\n".join(neg_reviews))
    else:
        # Default behavior is to generate a positive review
        output_review = ("\n".join(pos_reviews))

    print(output_review)
    return summarized_review


res_name, res_id = search(restaurant_name,city_id)
print("Generating a " + required_sentiment + " review for " + res_name)
reviews = get_reviews(res_id)

getSummarizedReview(reviews)

