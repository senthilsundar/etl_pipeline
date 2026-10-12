{{ config(materialized='view') }}

with ranked as (
    select
        user_id,
        name,
        gender,
        city,
        state,
        country,
        email,
        age,
        registration_date,
        age_band,
        registration_year,
        registration_month,
        row_number() over (
            partition by state
            order by registration_date desc, email asc
        ) as state_recency_rank
    from {{ ref('dim_users') }}
)
select *
from ranked
where state_recency_rank <= 3
