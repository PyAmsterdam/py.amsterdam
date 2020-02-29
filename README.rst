PyAmsterdam
===========

This is a website of PyAmsterdam powered by pelican_.

How to create events
---------------------

Events are pelican articles written in RST inside `content` directory.

To create an event:

#. Create a meetup.com draft event
#. `copy the `docs/event_template.rst` into the `content` directory and edit accordingly
#. Fill in the `rsvp_url` url from `meetup.com` draft event
#. Push/Merge the code and wait till the website is built and deployed
#. Navigate to the `https://py.amsterdam/<date of event>/<event_name>.html`
#. Get the TXT version for meetup.com

   #. In browser address bar: change the `.html` to txt
   #. Copy the content
   #. Go to your Draft event and paste

#. Release the event on Meetup.com


  All event updates should follow the same process and keep the sites in sync

* metadata

  * Required article metadata:

    * ``:event_type: Meetup`` - one word event type which will show up in calendar grid (Meetup, Workshop, ...etc)
    * ``:date: YYYY-MM-DD`` - when the event is happening

  * Optional metadata

    * ``:rsvp_url:`` - url where attendees can RSVP - displayed in event detail page
    * ``:external_url: https://somewhere-else.com`` - if specified calendar will redirect to the external page directly



.. _pelican: https://blog.getpelican.com/

