#!/usr/bin/env python3
'''Task 8's module.
'''


def list_all(mongo_collection):
    '''Lists all collection's documents.
    '''
    return [doc for doc in mongo_collection.find()]
