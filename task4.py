import pandas as pd
import json
from glob import glob
import matplotlib.pyplot as plt
import numpy as np

content_path = '/course/data/a1/content/HealthStory/'
engagements_path = '/course/data/a1/engagements/HealthStory.json'
reviews_path = '/course/data/a1/reviews/HealthStory.json'

def task4():

    content_files = glob(content_path + 'story_reviews_*')
    
    content_dict = []

    for file in content_files:
        with open(file) as json_file:
            data = json.load(json_file)['title']
        content_dict.append([str(file)[-24:-5], data])

    content_df = pd.DataFrame(content_dict, columns=['news_id', 'news_title'])
    content_df.sort_values('news_id', inplace=True)

    reviews_df = pd.read_json(reviews_path)
    reviews_df.sort_values('news_id', inplace=True)
    reviews_df.drop(columns=['link','description','original_title', 'reviewers','category',
    'tags','source_link','summary','criteria'],inplace=True)

    merged_df = content_df
    merged_df = merged_df.merge(reviews_df, left_on='news_id', right_on='news_id')
    merged_df.sort_values('news_id', inplace=True)
    merged_df['news_source'].replace('', np.nan, inplace=True)

    merged_df.dropna(how='any', inplace=True)

    count_df = merged_df.groupby(by='news_source').count()
    count_df.reset_index(inplace=True)

    mean_df = merged_df.groupby(by='news_source').mean()
    mean_df.reset_index(inplace=True)

    output_df = pd.DataFrame()

    output_df['news_source'] = count_df['news_source']
    output_df['num_articles'] = count_df['news_id']
    output_df['avg_rating'] = mean_df['rating']
    output_df.sort_values(by='news_source')

    output_df.to_csv('task4a.csv', index=False)

    png_df = output_df[output_df.num_articles >= 5]
    png_df.sort_values(by='avg_rating', inplace=True)

    plt.bar(png_df['news_source'], png_df['avg_rating'])
    plt.xticks(png_df['news_source'], rotation = 90)
    plt.ylabel('Average Credibility Rating')
    plt.xlabel('News Source')

    plt.savefig('task4b.png', bbox_inches='tight')
    return
