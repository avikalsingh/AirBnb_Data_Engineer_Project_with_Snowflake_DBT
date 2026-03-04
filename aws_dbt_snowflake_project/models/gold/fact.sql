{% set congigs = [
    {
        "table" : "AIRBNB.GOLD.OBT",
        "columns" : "GOLD_obt.BOOKING_ID, GOLD_obt.LISTING_ID, GOLD_obt.HOST_ID, GOLD_obt.TOTAL_AMOUNT, GOLD_obt.NIGHTS_BOOKED, GOLD_obt.BOOKING_AMOUNT, GOLD_obt.SERVICE_FEE, GOLD_obt.CLEANING_FEE, GOLD_obt.ACCOMMODATES, GOLD_obt.BEDROOMS, GOLD_obt.BATHROOMS, GOLD_obt.PRICE_PER_NIGHT, GOLD_obt.RESPONSE_RATE",
        "alias" : "GOLD_obt"
    },
    {
        "table" : "AIRBNB.GOLD.DIM_LISTINGS",
        "columns" : "",
        "alias" : "DIM_LISTINGS",
        "join_condition" : "GOLD_obt.LISTING_ID = DIM_LISTINGS.LISTING_ID"
    },
    {
        "table" : "AIRBNB.GOLD.DIM_HOSTS",
        "columns" : "",
        "alias" : "DIM_HOSTS",
        "join_condition" : "GOLD_obt.HOST_ID = DIM_HOSTS.HOST_ID"
    }
    ]%}



select
    {{ congigs[0]['columns'] }}
from
    {% for config in congigs %}
    {% if loop.first %}
        {{ config['table'] }} as {{ config['alias'] }}
    {% else %}
        left join {{ config['table'] }} as {{ config['alias'] }} 
        on {{ config['join_condition'] }}
    {% endif %}
    {% endfor %}