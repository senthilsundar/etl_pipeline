

with source_data as (
    select * from "user_pipeline"."main"."int_users_enriched"
),

candidates as (
    select s.*
    from source_data s
    
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