-- import

with source as (
    select 
        "Date",
        "Close",
        "simbolo"
    from 
        {{ source ('dbsalesrender', 'commodities') }}
),


-- renamed or change type

renamed as (

    select 
        cast("Date" as date) as data,
        "Close" as valor_fechamento,
        simbolo
    from 
        source
)

-- select * from

select * from renamed