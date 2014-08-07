zendesk-check
==============

This python program is meant to check your zendesk queue for unassigned tickets
and perform an action when there are open tickets waiting in a queue.

At WMF OIT, we use it to play a gong sound on a raspberry pi that we have
hooked up to a TV as a dashboard.

We currently run it in a cron every two minutes. 
(The API seems to cache, so give yourself some lag time....)

We tried using espeak on the pi to speak the Subject of the ticket, but that didn't work well.
('say' on osx works much better -- could be a cpu issue)


Requirements
--------------
Special Python libraries:
- requests (tested with 2.3.0)
- simplejson (only for debug output)



