{% set congigs = [
    {
        "ref"     : "obt",
        "columns" : "GOLD_obt.BOOKING_ID, GOLD_obt.LISTING_ID, GOLD_obt.HOST_ID, GOLD_obt.TOTAL_AMOUNT, GOLD_obt.NIGHTS_BOOKED, GOLD_obt.BOOKING_AMOUNT, GOLD_obt.SERVICE_FEE, GOLD_obt.CLEANING_FEE, GOLD_obt.ACCOMMODATES, GOLD_obt.BEDROOMS, GOLD_obt.BATHROOMS, GOLD_obt.PRICE_PER_NIGHT, GOLD_obt.RESPONSE_RATE",
        "alias"   : "GOLD_obt"
    }
] %}

select
    {{ congigs[0]['columns'] }}
from
    {{ ref(congigs[0]['ref']) }} as {{ congigs[0]['alias'] }}