#
# generate mockup records in sql format.
# - python37
#

import sys, os, getopt
import uuid
import json
from faker import Faker
from random import randint

user_count = 10
dataset_count = 100

# essential fields:
# - username, email
def generate_sys_user(count):
    fake = Faker()

    print('-- populate sys_user: {:d} records --'.format(count))

    for i in range(1, count+1):
        p = fake.profile()
        username = p['username']
        email = p['mail']
        displayname = p['name']
        bio = "{:s} working for {:s}".format(p['job'], p['company'])

        print("insert into sys_user (username,email,displayname,bio) "
              "values ('{:s}','{:s}','{:s}',\"{:s}\");"
              .format(username, email, displayname, bio))

#
def generate_dataset_properties():
    fake = Faker()
    d = {}

    d['title'] = fake.sentence()
    d['subtitle'] = fake.sentence()
    d['description'] = fake.paragraph()
    d['keywords'] = fake.words(nb=randint(3,10), unique=True)
    d['institution'] = fake.company()
    d['url'] = fake.url()

    return json.dumps(d)

#
def generate_dataset_files():
    fake = Faker()
    n_files = randint(4, 128);
    files = []
    word = fake.word()

    for i in range(n_files):
        name = 'data.{:s}.{:d}.csv'.format(word, i)
        size = randint(2**10, 2**30)
        files.append({'name': name, 'size': size })

    return files

# essential fields:
# - uuid, owner, json.properties, json.structure
def generate_sys_dataset(count):
    fake = Faker()

    print('-- populate sys_dataset: {:d} records --'.format(count))

    for i in range(1, count+1):
        uuid_str = str(uuid.uuid4())
        owner = randint(1, user_count)
        created = str(fake.date_time_between(start_date='-1y'))
        properties = generate_dataset_properties()

        files = generate_dataset_files()
        structure = json.dumps({'data': files})
        size = sum(f['size'] for f in files)

        d_type = randint(0, 7)
        category = randint(0, 50)

        print("insert into sys_dataset "
              "(uuid,owner_id,size,properties,structure,created,category,type) "
              "values ('{:s}',{:d},{:d},'{:s}','{:s}','{:s}',{:d},{:d});"
              .format(uuid_str, owner, size, properties, structure,
                      created, category, d_type))

        for f in files:
            print("insert into sys_file (dataset_id, name, size) "
                  "values ({:d},'{:s}',{:d});"
                  .format(i, f['name'], f['size']))

#
def usage():
    print("usage: generate.py [options]")
    print(" available options:")
    print(" -h, --help           print help message")
    print(" -d, --dataset=<N>    generate <N> datasets (default: 10)")
    print(" -u, --user=<N>       generate <N> users (default: 10)")

#
def main(argv):
    global user_count
    global dataset_count

    try:
        opts, args = getopt.getopt(argv, "hu:d:o:",
                       ["help", "--dataset=", "--ouput=", "--user="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    if len(args) > 0:
        usage()
        sys.exit(1)

    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit(0)
        elif opt in ("-d", "--dataset"):
            dataset_count = int(arg)
        elif opt in ("-u", "--user"):
            user_count = int(arg)
        else:
            usage()
            sys.exit(1)

    Faker.seed(123)

    print('start transaction;')

    generate_sys_user(user_count)
    generate_sys_dataset(dataset_count)

    print('commit;')

    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])

