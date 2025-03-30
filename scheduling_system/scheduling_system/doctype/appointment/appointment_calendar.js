frappe.views.calendar["Appointment"] = {
    field_map: {
        start: "start_date",
        end: "end_date",
        title: "client_name",
        status: "status",
        allDay: "all_day"
    },
    style_map: {
        'Scheduled': 'warning',
        'Finished': 'success',
        'Canceled': 'danger'
    },
    get_events_method: "frappe.desk.calendar.get_events"
};
