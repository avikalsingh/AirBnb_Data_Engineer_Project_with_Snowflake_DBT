{# {% set incremental_flag = 1 %}
{% set incremental_col = 'CREATED_AT' %} #}

{{ config(materialized = 'incremental') }}

select * from {{ source('staging', 'bookings') }}

{# {% if incremental_flag == 1 %} #}
    {# where {{ incremental_col }} > (select coalesce(max({{ incremental_col }}), '1900-01-01') from {{ this }}) #}

{% if is_incremental() %}
    where CREATED_AT > (select coalesce(max(CREATED_AT), '1900-01-01') from {{ this }})
{% endif %}