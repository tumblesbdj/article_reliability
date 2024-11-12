import pandas as pd
import json
from glob import glob

content_path = '/course/data/a1/content/HealthStory/'
engagements_path = '/course/data/a1/engagements/HealthStory.json'
reviews_path = '/course/data/a1/reviews/HealthStory.json'

def task1():

    content_files = glob(content_path + 'story_reviews_*')
    article_count = len(content_files)

    reviews_df = pd.read_json(reviews_path)
    review_count = len(reviews_df)

    engagements_df = pd.read_json(engagements_path)
    engagements_df = engagements_df.transpose()
    engagements_df.index.name = 'news_id'

    # Adds all tweets to a set and counts unique values.
    tweets = []

    for column in engagements_df:
        for row in engagements_df[column]:
            tweets.extend(row)

    tweets = set(tweets)
    tweet_count = len(tweets)

    output_dict = {
        "Total number of articles": article_count,
        "Total number of reviews": review_count,
        "Total number of tweets": tweet_count,
    }

    with open("task1.json", "w") as output_file:
        json.dump(output_dict, output_file)

    return
