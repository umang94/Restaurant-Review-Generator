# Review Generator for Restaurant

A small utility to generate a new review for a restaurant based on the existing reviews of the restaurant. It queries zomato to fetch the latest five reviews of the restaurant and summarizes the latest five reviews to generate a new review.

# Pre-requisites

Preferred Python version: 3.3
## Python dependencies
1. urllib
2. requests: http://docs.python-requests.org/en/master/#
3. summarizer: https://pypi.python.org/pypi/summarizer/0.0.7
4. textblob: https://textblob.readthedocs.io/en/dev/quickstart.html 

`$ pip3 install urllib,requests,summarizer,textblob`
## Zomato API keys

Generate an API key for yourself at https://developers.zomato.com/api 

# Usage
## Positive review
`python3 review_generator.py "YOUR_API_KEY" "Restaurant Name" "postive"`
## Negative review
`python3 review_generator.py "YOUR_API_KEY" "Restaurant Name" "negative"`





