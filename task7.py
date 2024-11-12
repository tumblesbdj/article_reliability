import pandas as pd
import json
import numpy as np
import math
import matplotlib.pyplot as plt

content_path = '/course/data/a1/content/HealthStory/'
engagements_path = '/course/data/a1/engagements/HealthStory.json'
reviews_path = '/course/data/a1/reviews/HealthStory.json'

reviews_df = pd.read_json(reviews_path)
reviews_df.sort_values('news_id', inplace=True)
reviews_df.drop(columns=['link','description','original_title', 'reviewers','category',
'tags','source_link','summary','criteria', 'title', 'news_source'],inplace=True)
reviews_df['real_news'] = reviews_df['rating']>=3
reviews_df.set_index('news_id', inplace=True)

def count_real(news_ids):

    real_count = 0
    fake_count = 0

    for item in news_ids:
        value = reviews_df.real_news.get(item, np.nan)
        if value == True:
            real_count += 1
        if value == False:
            fake_count += 1

    return (real_count, fake_count)

def task7():
    
    word_df = pd.read_json('task6.json', lines=True).transpose()
    word_df.reset_index(inplace=True)
    word_df.set_axis(axis='columns', labels=['word', 'news_ids'], inplace=True)

    false_total = int(reviews_df.groupby(by='real_news').count()['rating'].loc[False])
    real_total = int(reviews_df.groupby(by='real_news').count()['rating'].loc[True])

    word_df['(Real, Fake) Count'] = word_df['news_ids'].apply(count_real)

    word_df['num_articles'] = word_df['news_ids'].apply(lambda x: int(len(x)))
    word_df.loc[word_df['num_articles'] > 10]

    word_df.to_csv('testing.csv')

    word_df['Preal(w)'] = word_df['(Real, Fake) Count'].apply(lambda x: x[0]/real_total if x[0] > 0 else np.nan)
    word_df['Pfalse(w)'] = word_df['(Real, Fake) Count'].apply(lambda x: x[1]/false_total if int(x[1]) > 0 else np.nan)

    word_df.dropna(inplace=True)

    word_df['Oreal(w)'] = word_df['Preal(w)'].apply(lambda x: x/(1-x))
    word_df['Ofalse(w)'] = word_df['Pfalse(w)'].apply(lambda x: x/(1-x))

    word_df['OR(w)'] = word_df['Ofalse(w)'] / word_df['Oreal(w)']

    word_df['log_odds_ratio'] = word_df['OR(w)'].apply(math.log)

    word_df.drop(columns=['news_ids', '(Real, Fake) Count', 'num_articles', 'Preal(w)', 'Pfalse(w)', 'Oreal(w)', 'Ofalse(w)', 'OR(w)'], inplace=True)
    word_df.to_csv('task7a.csv', index=False)
    
    plt.hist(x=word_df['log_odds_ratio'],bins='auto')

    plt.ylabel('Frequency')
    plt.xlabel('Odd Ratio (log)')

    plt.savefig('task7b.png')

    plt.cla()
    plt.clf()

    word_df.sort_values(by='log_odds_ratio', inplace=True)
    output_df = word_df.head(15).append(word_df.tail(15))

    plt.scatter(output_df['word'], output_df['log_odds_ratio'])

    plt.xticks(output_df['word'], rotation = 90)
    plt.ylabel('log_odds_ratio')
    plt.xlabel('Words')

    plt.savefig('task7c.png', bbox_inches='tight')
    return
