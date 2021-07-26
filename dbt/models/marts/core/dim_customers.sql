{{
    config(materialized="table", schema="jaffle_shop")
}}

WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
), orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
), orders_payments AS (
    SELECT order_id
         , amount
    FROM {{ ref('fct_orders') }}
), customer_orders AS (
    SELECT o.customer_id
         , MIN(o.order_date) AS first_order_date
         , MAX(o.order_date) AS most_recent_order_date
         , COUNT(o.order_id) AS number_of_orders
         , SUM(COALESCE(op.amount, 0)) AS lifetime_value
    FROM orders o
    LEFT JOIN orders_payments op USING (order_id)
    GROUP BY 1
), final AS (
    SELECT customers.customer_id
         , customers.first_name
         , customers.last_name
         , customer_orders.first_order_date
         , customer_orders.most_recent_order_date
         , coalesce(customer_orders.number_of_orders, 0) AS number_of_orders
         , lifetime_value
    FROM customers
    LEFT JOIN customer_orders USING (customer_id)
)

SELECT * FROM final