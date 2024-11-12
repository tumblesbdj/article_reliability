import pandas as pd
import json
from glob import glob
from datetime import datetime
import matplotlib.pyplot as plt

content_path = '/course/data/a1/content/HealthStory/'
engagements_path = '/course/data/a1/engagements/HealthStory.json'
reviews_path = '/course/data/a1/reviews/HealthStory.json'

def task3():
    content_files = glob(content_path + 'story_reviews_*')

    content_dict = []

    for file in content_files:
        with open(file) as json_file:
            data = json.load(json_file)['publish_date']
        content_dict.append([str(file)[-24:-5], data])
    
    content_df = pd.DataFrame(content_dict, columns=['news_id', 'timestamp'])
    content_df.dropna(inplace=True)
    
    content_df['timestamp'] = content_df['timestamp'].apply(lambda x: datetime.fromtimestamp(x))

    content_df['year'] = content_df['timestamp'].apply(lambda x: x.strftime("%Y"))
    content_df['month'] = content_df['timestamp'].apply(lambda x: x.strftime("%m"))
    content_df['day'] = content_df['timestamp'].apply(lambda x: x.strftime("%d"))

    content_df.drop(columns='timestamp', inplace=True)
    content_df.sort_values('news_id', inplace=True)
    content_df.to_csv('task3a.csv', index=False)

    year_df = content_df.groupby(by='year').count()
    year_df.reset_index(inplace = True)

    # plt.bar(year_df['year'], year_df['news_id'])
    # plt.xticks(year_df['year'])
    plt.plot(year_df['year'], year_df['news_id'])
    plt.ylabel('Number of Articles')
    plt.xlabel('Year')
    plt.savefig('task3b.png')

    return
