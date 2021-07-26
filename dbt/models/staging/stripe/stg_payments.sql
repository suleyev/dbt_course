{{
    config(schema="stripe")
}}

WITH payments AS (
    SELECT id AS payment_id
         , orderid AS order_id
         , amount/100 AS amount
    FROM stripe.payments
    WHERE status = 'success'
)

SELECT * FROM payments