import pandas as pd
import json
from glob import glob
import re
from nltk.corpus import stopwords
import string

content_path = '/course/data/a1/content/HealthStory/'
engagements_path = '/course/data/a1/engagements/HealthStory.json'
reviews_path = '/course/data/a1/reviews/HealthStory.json'

stop_words = stopwords.words("english")

# Help from: https://towardsdatascience.com/cleaning-text-data-with-python-b69b47b97b76
def clean_text(x):
    x = x.lower()
    x = ' '.join([word for word in x.split(' ') if word not in stop_words])
    x = x.encode('ascii', 'ignore').decode()
    x = re.sub(r'https*\S+', ' ', x)
    x = re.sub(r'@\S+', ' ', x)
    x = re.sub(r'#\S+', ' ', x)
    x = re.sub(r'\'\w+', '', x)
    x = re.sub('[%s]' % re.escape(string.punctuation), ' ', x)
    x = re.sub(r'\w*\d+\w*', '', x)
    x = re.sub(r'\s{2,}', ' ', x)
    x = re.sub('(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)', '', x)
    return x

def task6():
    
    content_files = glob(content_path + 'story_reviews_*')
    content_files = sorted(content_files)

    content_dict = []

    for file in content_files:
        with open(file) as json_file:
            data = json.load(json_file)['text']
        content_dict.append([str(file)[-24:-5], data])

    content_df = pd.DataFrame(content_dict, columns=['news_id', 'text'])

    content_df['text'] = content_df['text'].apply(clean_text)

    content_df['words'] = content_df['text'].apply(lambda x: list(set(x.split(" "))))

    content_df.drop(columns=['text'], inplace=True)

    word_dict = {}
    for i in range(len(content_df)):
        for word in content_df.iloc[i, 1]:
            if word in word_dict.keys():
                word_dict[word].append(content_df.iloc[i, 0])
            else:
                word_dict[word] = [content_df.iloc[i, 0]]

    word_dict.pop('')

    sorted_word_dict = dict(sorted(word_dict.items()))

    with open("task6.json", "w") as output_file:
        json.dump(sorted_word_dict, output_file)
    return
