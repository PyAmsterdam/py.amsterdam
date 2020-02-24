PyAmsterdam
===========

This is a website of PyAmsterdam powered by pelican_.

How to create events
---------------------

Events are pelican articles written in RST inside `content` directory.

An event consists of these blocks:

* title

.. code-block:: rst

    Event title
    ===========

* metadata

  * Required article metadata:

    * ``:event_type: Meetup`` - one word event type which will show up in calendar grid (Meetup, Workshop, ...etc)
    * ``:date: YYYY-MM-DD`` - when the event is happening

  * Optional metadata

    * ``:rsvp_url:`` - url where attendees can RSVP - displayed in event detail page
    * ``:external_url: https://somewhere-else.com`` - if specified calendar will redirect to the page



.. _pelican: https://blog.getpelican.com/

