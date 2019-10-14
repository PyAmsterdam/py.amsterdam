document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    locale: 'en-gb',
    plugins: [ 'interaction', 'dayGrid' ],
    defaultDate: '2019-10-12',
    editable: true,
    eventLimit: true, // allow "more" link when too many events
    events: [
      {
        title: 'Meetup',
        url: 'events/details.html',
        start: '2019-10-01'
      },
      {
        title: 'Workshop',
        url: 'events/details.html',
        start: '2019-10-07'
      },
      {
        title: 'Python',
        url: 'events/details.html',
        start: '2019-10-09'
      },
      {
        title: 'Meetup',
        url: 'events/details.html',
        start: '2019-11-16'
      },
      {
        title: 'Google',
        url: 'events/details.html',
        start: '2019-10-28'
      }
      /*{
        title: 'Meeting',
        start: '2019-12-12T10:30:00',
        end: '2019-12-12T12:30:00'
      }*/
    ]
  });

  calendar.render();
});