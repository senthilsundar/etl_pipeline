select *
from {{ ref('dim_users') }}
where age < 0 or age > 120
