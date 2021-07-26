{{
    config(schema="jaffle_shop")
}}

WITH customers AS (
    SELECT id AS customer_id
         , first_name
         , last_name
    FROM jaffle_shop.customers
)

SELECT * FROM customers