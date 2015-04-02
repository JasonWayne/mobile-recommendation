# encoding: utf-8

import MySQLdb

CREATE_ITEMS_TABLE = """
    CREATE TABLE items 
    (
        item_id integer,
        item_geohash char(8),
        item_category integer
    )"""
    
CREATE_USERS_TABLE = """
    CREATE TABLE users
    (
        user_id int, 
        item_id int,
        behavior_type int,
        user_geohash char(8),
        item_category int,
        time char(15)
    )
"""

CREATE_USER518_TABLE = """
    CREATE TABLE user_518
    (
        user_id int, 
        item_id int,
        behavior_type int,
        user_geohash char(8),
        item_category int,
        time char(15)
    )
"""

CREATE_USERS_FILTERED_TABLE = """
    CREATE TABLE users_filtered
    SELECT * FROM users WHERE item_id IN
    (SELECT DISTINCT(item_id) FROM items)
"""

db = MySQLdb.connect("localhost", "root", "", "mobile_recommendation")
cursor = db.cursor()
cursor.execute(CREATE_USERS_FILTERED_TABLE)

db.close()
