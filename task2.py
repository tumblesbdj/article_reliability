import pandas as pd
import json
from glob import glob

content_path = '/course/data/a1/content/HealthStory/'
engagements_path = '/course/data/a1/engagements/HealthStory.json'
reviews_path = '/course/data/a1/reviews/HealthStory.json'

def satisfactory_count(list):
    count = 0
    for criteria in list:
        if (criteria['answer'] == 'Satisfactory'):
            count += 1
    return count

def task2():

    content_files = glob(content_path + 'story_reviews_*')
    
    content_dict = []

    for file in content_files:
        with open(file) as json_file:
            data = json.load(json_file)['title']
        content_dict.append([str(file)[-24:-5], data])

    content_df = pd.DataFrame(content_dict, columns=['news_id', 'news_title'])
    content_df.sort_values('news_id', inplace=True)

    reviews_df = pd.read_json(reviews_path)

    reviews_df['num_satisfactory'] = reviews_df['criteria'].apply(lambda x: satisfactory_count(x))

    reviews_df.drop(columns=['link','description','original_title', 'reviewers','category','tags',
    'source_link','summary','news_source','criteria'],inplace=True)

    reviews_df.rename(columns={'title':'review_title'}, inplace=True)
    reviews_df.sort_values('news_id', inplace=True)

    merged_df = content_df
    merged_df = merged_df.merge(reviews_df, left_on='news_id', right_on='news_id')
    merged_df.sort_values('news_id', inplace=True)

    merged_df.to_csv('task2.csv', index=False)

    return
