{{ config(schema='jaffle_shop') }}
{% set payment_methods = ['coupon', 'gift_card', 'bank_transfer', 'credit_card'] %}


WITH payments AS (
    SELECT created AS payment_date
         , paymentmethod AS payment_method
         , amount
    FROM stripe.payments
)

SELECT payment_date
    {% for payment_method in payment_methods %}
     , SUM(CASE WHEN payment_method = '{{ payment_method }}' THEN amount ELSE 0 END) AS {{ payment_method }}_total
    {% endfor %}
FROM payments
GROUP BY 1
ORDER BY 1 DESC