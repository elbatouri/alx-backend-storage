#!/usr/bin/env python3
'''Task 10's.
'''


def update_topics(mongo_collection, name, topics):
    '''Changes collection's topics document based on the name.
    '''
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
