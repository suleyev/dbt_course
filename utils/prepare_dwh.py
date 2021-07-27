import os
import urllib.request
from datetime import datetime

import psycopg2

def prepare_tables(curs: psycopg2._psycopg.cursor):
    sql = """
        create schema jaffle_shop;
        create schema stripe;
        
        create table jaffle_shop.customers(
          id integer,
          first_name varchar(50),
          last_name varchar(50)
        );
        
        create table jaffle_shop.orders(
          id integer,
          user_id integer,
          order_date date,
          status varchar(50),
          _etl_loaded_at timestamp default current_timestamp
        );
        
        create table stripe.payments(
          id integer,
          orderid integer,
          paymentmethod varchar(50),
          status varchar(50),
          amount integer,
          created date,
          _batched_at timestamp default current_timestamp
        );
    """
    curs.execute(sql)

def download_csv(table_name: str, url: str) -> str:
    ct = datetime.now()
    response = urllib.request.urlopen(url)
    if table_name in ('jaffle_shop.orders', 'stripe.payments'):
        res = [l.decode('utf-8').replace('\n', ',{}\n'.format(ct)) for l in response.readlines()]
        res[-1] = res[-1] + ',{}'.format(ct)
    else:
        res = [l.decode('utf-8') for l in response.readlines()]
    file_name = '{}.csv'.format(table_name)
    with open(file_name, mode='w') as csv_file:
        for x in res:
            csv_file.write(x)
    return file_name

def insert_csv_to_db(curs: psycopg2._psycopg.cursor, table_name, csv_file_name):
    sql = """
        TRUNCATE TABLE {}
    """.format(table_name)
    curs.execute(sql)
    sql = """
        COPY {} FROM STDOUT WITH CSV HEADER
    """.format(table_name)
    with open(csv_file_name, 'r') as f:
        curs.copy_expert(sql, f)

if __name__ == '__main__':
    data_table_dict = {
        'jaffle_shop.orders': 'http://dbt-tutorial-public.s3-us-west-2.amazonaws.com/jaffle_shop_orders.csv',
        'jaffle_shop.customers': 'http://dbt-tutorial-public.s3-us-west-2.amazonaws.com/jaffle_shop_customers.csv',
        'stripe.payments': 'http://dbt-tutorial-public.s3-us-west-2.amazonaws.com/stripe_payments.csv'
    }
    print('Connecting to DB...')
    with psycopg2.connect("host='localhost' port='5432' dbname='dbt_project' user='dbt' password='dbtcourse'") as conn, \
            conn.cursor() as curs:
        print('Connection established')
        print('Creating tables')
        prepare_tables(curs=curs)
        for table_name, url in data_table_dict.items():
            print('Downloading csv file for {} table'.format(table_name))
            csv_file_name = download_csv(table_name, url)
            print('Inserting data')
            insert_csv_to_db(curs=curs,
                             table_name=table_name,
                             csv_file_name=csv_file_name)
            print('Data successfully inserted into {}'.format(table_name))
            os.remove(csv_file_name)
            print('CSV file removed from disk')
