#!/usr/bin/env python3

from pymongo import MongoClient
from collections import Counter

def print_nginx_request_logs(nginx_collection):
    '''Prints stats about Nginx request logs.'''
    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")
    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        print(f"\tmethod {method}: {req_count}")
    status_checks_count = nginx_collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_checks_count} status check")

def print_top_ips(nginx_collection):
    '''Prints the top 10 most present IPs in the Nginx logs.'''
    ip_counter = Counter([log['ip'] for log in nginx_collection.find({}, {'ip': 1})])
    print("IPs:")
    for ip, count in ip_counter.most_common(10):
        print(f"\t{ip}: {count}")

def run():
    '''Provides some stats about Nginx logs stored in MongoDB.'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_nginx_request_logs(nginx_collection)
    print_top_ips(nginx_collection)

if __name__ == '__main__':
    run()

