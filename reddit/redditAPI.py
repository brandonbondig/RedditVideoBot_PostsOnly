from turtle import width
from regex import E
import requests as re
import json

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"




def getPost(subreddit, post_num: int = 5):

    with open('./config.json') as f:
        config = json.load(f)
    
    # Authentication.
    # Please create a reddit API app and insert info accordingly.
    auth = re.auth.HTTPBasicAuth(
        config['CLIENT_ID'], config['CLIENT_SECRET']
    )

    # Insert your Reddit username and pass accordingly.

    data = {
        "grant_type": "password",
        "username": config['USERNAME'],
        "password": config['PASSWORD'],
    }

    headers = {"User-Agent": "MyBot/0.0.1"}

    # Fetching access token from the reddit API
    # Expires in 1 hour.
    res = re.post(
        "https://www.reddit.com/api/v1/access_token",
        auth=auth,
        data=data,
        headers=headers,
    )

    # The fetched token.
    try:
        TOKEN = res.json()["access_token"]
        headers = {**headers, **{"Authorization": f"bearer {TOKEN}"}}
    except Exception as e:
        print(f'{bcolors.FAIL}ERROR: {e}{bcolors.ENDC}' )
        print(f"{bcolors.FAIL}Check if you filled the config.json file with the correct information{bcolors.ENDC}")
    
    
    # Requesting to reddit API.
    res = re.get(f"https://oauth.reddit.com/r/{subreddit}/hot", headers=headers)

    # Accessing the post url.
    url = res.json()["data"]["children"][post_num]["data"]["url"]

    # Relevent info from the chosen post.
    post_title = res.json()["data"]["children"][post_num]["data"]["title"]
    post_text = res.json()["data"]["children"][post_num]["data"]["selftext"]
    post_nsfw = res.json()["data"]["children"][post_num]["data"]["over_18"]
    name = res.json()["data"]["children"][post_num]["data"]["name"]

    # Info for the initial print.
    num_comments = res.json()["data"]["children"][post_num]["data"]["num_comments"]
    upvote_ratio = res.json()["data"]["children"][post_num]["data"]["upvote_ratio"]
    upvotes = res.json()["data"]["children"][post_num]["data"]["ups"]

    print(f"{bcolors.OKCYAN}{bcolors.BOLD}{post_title}{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Number of comments: {bcolors.OKGREEN}{num_comments} {bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Upvotes: {bcolors.OKGREEN}{upvotes}{bcolors.ENDC}")
    print(f"{bcolors.OKBLUE}Upvote Ratio: {bcolors.OKGREEN}{upvote_ratio}{bcolors.ENDC}")
    print('_____________________')

    return post_title, post_text, url, post_nsfw, name
