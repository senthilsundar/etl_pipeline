with source as (
    select * from "user_pipeline"."main"."clean_users"
),
cleaned as (
    select
        trim(cast(name as varchar)) as name,
        lower(trim(cast(gender as varchar))) as gender,
        trim(cast(city as varchar)) as city,
        'Alabama' as state,
        trim(cast(country as varchar)) as country,
        lower(trim(cast(email as varchar))) as email,
        cast(age as integer) as age,
        cast(registration_date as timestamp) as registration_date
    from source
)
select * from cleaned