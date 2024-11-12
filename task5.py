import pandas as pd
import json
from glob import glob
import matplotlib.pyplot as plt

content_path = '/course/data/a1/content/HealthStory/'
engagements_path = '/course/data/a1/engagements/HealthStory.json'
reviews_path = '/course/data/a1/reviews/HealthStory.json'

def unique_elements(list):
    temp_list = []
    count = 0
    for element in list:
        if element not in temp_list:
            count += 1
            temp_list.append(element)
    return count

def task5():
    engagements_df = pd.read_json(engagements_path)
    engagements_df = engagements_df.transpose()
    engagements_df.index.name = 'news_id'

    reviews_df = pd.read_json(reviews_path)
    reviews_df.drop(columns=['title', 'link','description','original_title', 'reviewers','category','tags','source_link','summary','news_source', 'criteria'],inplace=True)

    merged_df = reviews_df
    merged_df = merged_df.merge(engagements_df, left_on='news_id', right_on='news_id')
    merged_df['total_tweets'] = (merged_df['tweets'] + merged_df['replies'] + merged_df['retweets']).apply(lambda x: unique_elements(x))

    png_df = merged_df.groupby(by='rating').mean()
    png_df.reset_index(inplace=True)

    plt.bar(png_df['rating'], png_df['total_tweets'])
    plt.ylabel('Average No. Of Tweets')
    plt.xlabel('Credibility Rating')

    plt.savefig('task5.png')
    return
