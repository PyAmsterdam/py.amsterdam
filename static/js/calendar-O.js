document.addEventListener('DOMContentLoaded', function () {
    const eventList = [
        {
            "title": "Path(\"Brookz/PyAmsterdam meetup\")",
            "url": "events/details.html",
            "start": "2020-02-13"
        },
    ];
    let calendarEl = document.getElementById('calendar');
    let calendar = new FullCalendar.Calendar(calendarEl, {
        locale: 'en-gb',
        plugins: ['interaction', 'dayGrid'],
        defaultDate: '2020-02-12',
        editable: true,
        eventLimit: true, // allow "more" link when too many events
        events: eventList
    });

    calendar.render();
});