{{ config(
    materialized='incremental',
    unique_key='email',
    incremental_strategy='delete+insert'
) }}

with source_data as (
    select * from {{ ref('int_users_enriched') }}
),

candidates as (
    select s.*
    from source_data s
    {% if is_incremental() %}
    left join {{ this }} t
        on s.email = t.email
    where t.email is null
       or s.registration_date > t.registration_date
    {% endif %}
),

ranked as (
    select
        *,
        row_number() over (
            partition by email
            order by registration_date desc, name asc
        ) as record_rank
    from candidates
)

select
    md5(lower(email)) as user_id,
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
    registration_month
from ranked
where record_rank = 1
