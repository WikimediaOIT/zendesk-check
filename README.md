zendesk-check
==============

This program is meant to check your zendesk queue for unassigned tickets
and perform an action when there are open tickets waiting in a queue.

At WMF, we use it to play a gong sound on a raspberry pi that we have
hooked up to a TV as a dashboard.

We currently run it in a cron every minute. (we may decide that's insane)


Requirements
--------------

Special Python libraries:
- requests (tested with 2.3.0)
- simplejson (only for debug output)



