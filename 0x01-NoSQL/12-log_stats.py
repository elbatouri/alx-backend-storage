#!/usr/bin/env python3
"""
Script to provide statistics about Nginx logs stored in MongoDB
"""

import pymongo


def connect_db():
    """Connect to MongoDB and return the connection"""
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client.logs
    collection = db.nginx
    return collection


def count_logs(collection):
    """Count the number of logs"""
    return collection.count_documents({})


def count_methods(collection):
    """Count the number of logs for each method"""
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
                    {"method": method}) for method in methods}
    return method_counts


def count_status_check(collection):
    """Count the number of logs with method GET and path /status"""
    return collection.count_documents({"method": "GET", "path": "/status"})


def main():
    """Main function"""
    collection = connect_db()

    # Count total logs
    total_logs = count_logs(collection)
    print(f"{total_logs} logs")

    # Count methods
    print("Methods:")
    method_counts = count_methods(collection)
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")

    # Count status check
    status_check_count = count_status_check(collection)
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    main()
