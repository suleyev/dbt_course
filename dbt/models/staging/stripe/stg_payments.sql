{{
    config(schema="stripe")
}}

WITH payments AS (
    SELECT id AS payment_id
         , orderid AS order_id
         , amount
    FROM stripe.payments
)

SELECT * FROM payments