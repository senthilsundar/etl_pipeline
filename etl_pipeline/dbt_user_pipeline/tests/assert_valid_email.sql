select *
from {{ ref('dim_users') }}
where email not like '%_@_%._%'
