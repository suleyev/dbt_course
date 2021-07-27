{% docs payments_methods %}
	
One of the following values: 

| status         | definition                                         |
|----------------|----------------------------------------------------|
| bank_transfer  | The payment was made by transfer to a bank account |
| coupon         | The payment was made using a promotional coupon    |
| credit_card    | The payment was made using a credit card           |
| gift_card      | The payment was made using a gift card             |



{% enddocs %}

{% docs payments_statuses %}
	
One of the following values: 

| status         | definition                                       |
|----------------|--------------------------------------------------|
| fail           | Unsuccessful payment attempt                     |
| success        | Successful payment attempt                       |

{% enddocs %}