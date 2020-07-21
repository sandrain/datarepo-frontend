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

data = []

def addslashes(s):
    l = ["\\", '"', "'", "\0", ]
    for i in l:
        if i in s:
            s = s.replace(i, '')
    return s

# essential fields:
# - username, email
def generate_sys_user(count):
    fake = Faker()

    users = []

    for i in range(1, count+1):
        p = fake.profile()
        username = p['username']
        email = p['mail']
        displayname = p['name']
        bio = addslashes("{:s} working for {:s}".format(p['job'], p['company']))

        user = {
                'model': 'mainpage.SysUser',
                'pk': i,
                'fields' : {
                    'username': username,'email': email,'displayname': displayname,'bio': bio
                }
            }
        #users.append(user)
        data.append(user)

    #print(json.dumps(users))


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

    return d

#
def generate_dataset_files():
    fake = Faker()
    n_files = randint(2, 10);
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

    datasets = []
    sys_files = []

    for i in range(1, count+1):
        uuid_str = str(uuid.uuid4())
        owner = randint(1, user_count)
        created = str(fake.date_time_between(start_date='-1y'))
        properties = generate_dataset_properties()

        files = generate_dataset_files()
        structure = {'data': files}
        size = sum(f['size'] for f in files)

        d_type = randint(0, 7)
        category_ids = [1,2,3,4,7,8,9,10,11,12,13,14,15,16,17,20,21,22,24,25,29,30,32,33,36,37,38,42,43,45,46,47,54,58,59,60,61,62,63,70,71,72,73,74,75,77,79,96,97,98,99]
        category = randint(0, 50)

        dataset = {
                'model': 'mainpage.SysDataset',
                'pk': i,
                'fields' : {
                    'uuid': uuid_str,'owner_id': owner,'size':size,'properties':properties,'structure':structure,'created':created,'categories': [category_ids[category]],'type':d_type
                }
            }

        #datasets.append(dataset)
        data.append(dataset)

        for f in files:
            _file = {
                'model': 'mainpage.SysFile',
                'fields' : {
                    'dataset_id': i, 'name': f['name'], 'size': f['size']
                }
            }

            #sys_files.append(_file)
            data.append(_file)


    print(json.dumps(data))
    #print(json.dumps(sys_files))

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

    generate_sys_user(user_count)
    generate_sys_dataset(dataset_count)

    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1:])

