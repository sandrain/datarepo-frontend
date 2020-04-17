import json, uuid
from faker import Faker
from random import randint


def clean_recieved_val(val):
    if val.strip() == '':
        return None
    else:
        return val.strip()

def clean_keywords(keywords):
    cleaned_keywords = []
    for keyword in keywords:
        if keyword.strip()!='':
            cleaned_keywords.append(keyword.strip())
    return cleaned_keywords

def make_keywords_list(keywords):
    if keywords is None:
        return []
    else:
        keywords = keywords.split(",")
        return keywords

def unpack_dataset_json(dataset):
    dataset.id = dataset.id
    dataset.attributes = json.loads(dataset.properties)
    dataset.sizemb = int(dataset.size / (2**20))
    dataset.filecount = len((json.loads(dataset.structure))['data'])
    dataset.keywords = ', '.join(dataset.attributes['keywords'])
    dataset.icon = 'icons/{:d}.png'.format(dataset.id % 496 + 4)
    return dataset

# generating fake datasets

def generate_fake_dataset_properties(title, subtitle = None, description = None, keywords = None):
    fake = Faker()
    dataset = {}

    dataset['title'] = title
    
    if subtitle is None:
        dataset['subtitle'] = fake.sentence()
    else:
        dataset['subtitle'] = subtitle
    
    if description is None:
        dataset['description'] = fake.paragraph()
    else:
        dataset['description'] = description
    if keywords is None:
        dataset['keywords'] = fake.words(nb=randint(3,10), unique=True)
    else:
        dataset['keywords'] = keywords

    dataset['institution'] = fake.company()
    dataset['url'] = fake.url()

    return json.dumps(dataset)

def generate_fake_dataset_files():
    fake = Faker()
    n_files = randint(4, 128);
    files = []
    word = fake.word()

    for i in range(n_files):
        name = 'data.{:s}.{:d}.csv'.format(word, i)
        size = randint(2**10, 2**30)
        files.append({'dataset': None, 'name': name, 'size': size })

    return files

