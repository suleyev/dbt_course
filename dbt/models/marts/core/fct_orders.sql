{{
    config(schema="jaffle_shop")
}}

WITH orders AS (
    SELECT order_id
         , customer_id
    FROM {{ ref('stg_orders') }}
), payments AS (
    SELECT order_id
         , amount
    FROM {{ ref('stg_payments') }}
),
orders_payments AS (
    SELECT o.order_id
         , o.customer_id
         , p.amount
    FROM orders o
    LEFT JOIN payments p USING (order_id)
)

SELECT * FROM orders_payments