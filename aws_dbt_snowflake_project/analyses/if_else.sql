{% set flag = 5 %}

select * from {{ ref('bronze_bookings')}}
{% if flag == 5 %}
    where nights_booked = 5
{% else %}
    where nights_booked != 5
{% endif %}