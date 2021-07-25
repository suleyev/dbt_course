import os
import urllib.request

import psycopg2

def download_csv(table_name: str, url: str) -> str:
    response = urllib.request.urlopen(url)
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
