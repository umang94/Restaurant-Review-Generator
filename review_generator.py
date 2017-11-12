from urllib.parse import quote
import requests
from pprint import pprint
from summarizer import summarize
import sys

# ID for Hyderabad, India
city_id = "6"

restaurant_name = sys.argv[2]

api_key = sys.argv[1]
header = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": api_key}


baseRequestURL= "https://developers.zomato.com/api/v2.1/"

def search(restaurantName,cityId):
    search_param = "search?entity_id=" + cityId + "&entity_type=city&q=" + quote(restaurantName)
    search_request_url = baseRequestURL + search_param
    response = requests.get(search_request_url,headers=header)
    search_response = (response.json())
    
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
    summarized_review = ("\n".join(new_review_list))
    print(summarized_review)
    return summarized_review



res_name, res_id = search(restaurant_name,city_id)
print("Generating a review for " + res_name)
reviews = get_reviews(res_id)

getSummarizedReview(reviews)
