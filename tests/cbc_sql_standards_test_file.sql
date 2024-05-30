with raw_source as (

    select *
    from {{ source('SRC_WINTEAMS', 'SCHEDULES_DAILY') }}

                   ),

    final as (

    select
        "ID"::varchar  as schedules_daily_id,
        "CATEGORIESDETAILID"::varchar  as categories_detail_id,
        "INVOICEDETAILID"::varchar  as invoice_detail_id,
        "NONBILLABLETYPEID"::varchar  as non_billable_type_id,
        "RECORDTYPEID"::varchar  as record_type_id,
        "SCHEDULEDETAILSID"::varchar  as schedule_details_id,
        "TTMSTATUSID"::varchar  as ttm_status_id,
        "FORCEOTTOTHISJOB"::boolean  as force_otto_this_job,
        "ISCONFIRMED"::boolean  as is_confirmed,
        "ISPUBLISHED"::boolean  as is_published,
        "ACCEPTEDTYPEFORPSTT"::varchar  as accepted_type_for_pst_t,
        "ADJUSTEDWORKDATE"::varchar  as adjusted_work_date,
        "BILLINGPAYRATE"::varchar  as billing_pay_rate,
        "BILLRATE"::varchar  as bill_rate,
        "DATECHANGED"::varchar  as date_changed,
        "DATECONFIRMED"::boolean  as date_confirmed,
        "DOUBLETIMEHOURS"::varchar  as double_time_hours,
        "EMPLOYEENUMBER"::varchar  as employee_number,
        "HOURS"::varchar  as hours,
        "INTIME"::varchar  as in_time,
        "INVOICEDESCRIPTION"::varchar  as invoice_description,
        "JOBNUMBER"::varchar  as job_number,
        "LASTNOTIFIEDDATE"::varchar  as last_notified_date,
        "LUNCH"::varchar  as lunch,
        "NEXTDAY"::varchar  as next_day,
        "NOTES"::varchar  as notes,
        "OUTTIME"::varchar  as out_time,
        "OVERTIMEHOURS"::varchar  as overtime_hours,
        "PAYRATE"::varchar  as pay_rate,
        "SPECIALBILLRATE"::boolean  as special_bill_rate,
        "SPECIALINVOICEDESCRIPTION"::varchar  as special_invoice_description,
        "SPECIALPAYRATE"::boolean  as special_pay_rate,
        "SPECIALTIERDESCRIPTION"::varchar  as special_tier_description,
        "SYSTEMNOTES"::varchar  as system_notes,
        "TIERDESCRIPTION"::varchar  as tier_description,
        "UPDATEDTOTKHOURS"::varchar  as updated_to_tk_hours,
        "UPLOAD_TIME"::timestamp  as upload_time,
        "USERNAME"::varchar  as username,
        "WORKDATE"::date  as work_date,
        "WORKTICKET"::varchar  as work_ticket,
        "_AB_SOURCE_FILE_LAST_MODIFIED"::varchar  as ab_source_file_last_modified,
        "_AB_SOURCE_FILE_URL"::varchar  as ab_source_file_url

    from raw_source

                   )

select * from final
