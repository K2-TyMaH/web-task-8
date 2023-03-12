import sys
from pprint import pprint

import redis
from redis_lru import RedisLRU
from mongoengine import connect
from mongoengine.queryset.visitor import Q

from src.models import Author, Quote


connect(host='mongodb+srv://tymah:13572468@mycluster.6ekshk8.mongodb.net/testdb9?retryWrites=true&w=majority', ssl=True)

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)

def commander(command, value):
    match command:
        case 'name':
            find_author(value)
        case 'tag':
            find_tag(value)
        case 'tags':
            tags = value.strip().split(',')
            for tag in tags:
                find_tag(tag.strip())
        case 'info':
                find_all_info(value)
        case _:
            print(f'Wrong command "{command}"')


def c_parser(value):
    com, val = value.strip().split(':')
    return com, val


@cache
def find_author(author):
    author_id = Author.objects(fullname__icontains=author).first()
    if author_id:
        author_id = author_id.id

    information = Quote.objects(author=author_id)
    if information:
        for item in information:
            print("-------------------")
            pprint(item.quote)
    else:
        print('Found nothing. Try again.')


@cache
def find_tag(tag):
    information = Quote.objects(tags__icontains=tag)
    if information:
        for item in information:
            print("-------------------")
            pprint(item.quote)
    else:
        print('Found nothing. Try again.')


@cache
def find_all_info(value):
    author_id = Author.objects(fullname__icontains=value).first()
    if author_id:
        author_id = author_id.id
    information = Quote.objects(Q(tags__icontains=value) | Q(author=author_id))

    if information:
        for item in information:
            print("-------------------")
            pprint(item.to_mongo().to_dict())
    else:
        print('Found nothing. Try again.')


if __name__ == '__main__':
    while True:
        inputted = input('====> ')
        if inputted != 'exit':
            try:
                com, val = c_parser(inputted)
                commander(com, val)
            except ValueError:
                print('Wrong format. Needed {command}:{value}')
        else:
            sys.exit(0)

