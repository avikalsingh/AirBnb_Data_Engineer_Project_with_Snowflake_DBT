{% set congifs = [
    {
        "ref"     : "silver_bookings",
        "columns" : "silver_bookings.*",
        "alias"   : "silver_bookings"
    },
    {
        "ref"     : "silver_listings",
        "columns" : "silver_listings.HOST_ID, silver_listings.PROPERTY_TYPE, silver_listings.ROOM_TYPE, silver_listings.CITY, silver_listings.COUNTRY, silver_listings.ACCOMMODATES, silver_listings.BEDROOMS, silver_listings.BATHROOMS, silver_listings.PRICE_PER_NIGHT, silver_listings.PRICE_PER_NIGHT_TAG, silver_listings.CREATED_AT AS LISTING_CREATED_AT",
        "alias"   : "silver_listings",
        "join_on" : "silver_bookings.listing_id = silver_listings.listing_id"
    },
    {
        "ref"     : "silver_hosts",
        "columns" : "silver_hosts.HOST_NAME, silver_hosts.HOST_SINCE, silver_hosts.IS_SUPERHOST, silver_hosts.RESPONSE_RATE, silver_hosts.RESPONSE_RATE_QUALITY, silver_hosts.CREATED_AT AS HOST_CREATED_AT",
        "alias"   : "silver_hosts",
        "join_on" : "silver_listings.host_id = silver_hosts.host_id"
    }
] %}

select
    {% for c in congifs %}
        {{ c['columns'] }}{% if not loop.last %},{% endif %}
    {% endfor %}
from
    {% for c in congifs %}
    {% if loop.first %}
        {{ ref(c['ref']) }} as {{ c['alias'] }}
    {% else %}
        left join {{ ref(c['ref']) }} as {{ c['alias'] }}
        on {{ c['join_on'] }}
    {% endif %}
    {% endfor %}