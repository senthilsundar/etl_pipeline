select
    name,
    gender,
    city,
    state,
    country,
    email,
    age,
    registration_date,
    case
        when age between 0 and 18 then '0-18'
        when age between 19 and 25 then '19-25'
        when age between 26 and 40 then '26-40'
        else '40+'
    end as age_band,
    extract(year from registration_date) as registration_year,
    extract(month from registration_date) as registration_month
from {{ ref('stg_users') }}
