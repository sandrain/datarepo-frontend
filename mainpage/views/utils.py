import json, uuid
from faker import Faker
from random import randint

def unpack_dataset_json(dataset):
    dataset.id = dataset.id
    dataset.attributes = json.loads(dataset.properties)
    dataset.sizemb = int(dataset.size / (2**20))
    dataset.filecount = len((json.loads(dataset.structure))['data'])
    dataset.keywords = ', '.join(dataset.attributes['keywords'])
    dataset.icon = 'icons/{:d}.png'.format(dataset.id % 496 + 4)
    return dataset

# generating fake datasets

def generate_fake_dataset_properties(title):
    fake = Faker()
    dataset = {}

    dataset['title'] = title
    dataset['subtitle'] = fake.sentence()
    dataset['description'] = fake.paragraph()
    dataset['keywords'] = fake.words(nb=randint(3,10), unique=True)
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

