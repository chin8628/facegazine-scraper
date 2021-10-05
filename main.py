#!/usr/bin/python
# -*- coding: utf-8 -*-

from facebook_scraper import get_posts
import schedule
import time
import dbconfig
import json
import math
import datetime
import bson
import logging


def scrape(db):
    logging.info("start scraping process...")

    posts = get_posts("fdininglovers", page=1000, locals="en_US")
    for post in posts:
        save_post(db, post)


def save_post(db, raw_post):
    result = db.posts.find_one({"post_id": raw_post["post_id"]})
    if result is not None:
        logging.info("Duplicated post:", result["post_id"])
        return

    raw_post["created_at"] = datetime.datetime.utcnow()
    raw_post["updated_at"] = datetime.datetime.utcnow()
    db.posts.insert_one(raw_post)

    logging.info(
        "Save post successfully: post_id is %s, post_url is %s",
        raw_post["post_id"],
        raw_post["post_url"],
    )


def wait(x):
    delay = min(10, math.sqrt(math.pow(2, 12) - math.pow(x, 2) / 4))
    time.sleep(delay)


def main():
    logging.info("starting...")
    db = dbconfig.create_db()
    db = dbconfig.setup_collection(db)

    scrape(db)
    # schedule.every(24).hours.do(scrape)

    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(
        filename="Log_Test_File.txt",
        level=logging.INFO,
        format="%(levelname)s: %(asctime)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S",
    )

    main()
