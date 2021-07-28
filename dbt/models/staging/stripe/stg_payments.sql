{{
    config(schema="stripe")
}}

WITH payments AS (
    SELECT id AS payment_id
         , orderid AS order_id
         , {{ cents_to_dollars('amount', 4) }} AS amount
    FROM {{ source('stripe', 'payments') }}
    WHERE status = 'success'
)

SELECT * FROM payments