Hello,
first of all thanks for the time you spend on my coding challenge, I really appreciate your
effort. I tried to do a self explaining code, with comments where I found it necessary.
Let me start with some excuses, of course my time was limited for the task, which is not an
excuse, but because of the tight schedule I dropped some habits / requirements, in normal
circumstances I would do the next things differently:

 - Use TDD - I did not used unit testing at all. - In the given time with asyncio would be hard.
 - Use automated FT. - I did every functional testing manually, without any documentation.
 - I may left TODOs in my code.
 - I did not provided a super long documentation (expect this file)

Not implemented:
 - Web interface - UPDATE, I did finished it. By default listen on localhost:8080

Changes from requirements:
 - Checking period is not configurable from command line, as I did the period config per website

About the design:
At the begging I was planning to use some threads with a working queue, where I would push the
checks and than threads would pull work from there and do the checks. Which may work, but than
I started to think. I know a service called Pingdom, doing exactly you asked in the challenge.
The service is really famous and there are tons of users with tons of checks. So I started to
wonder how could be this program a better fit for that big volumes. That's why I came up with
a separated "Scheduler" and "Worker" (or server and client, sorry for the not unified naming),
between the Scheduler (which you can start with -s option) and Worker I used a single protocol,
which is based on pickle. I have my webpage class and objects are passed between Scheduler and
Worker. While this is really easy to use, maybe not the best solution as some extra info is
passed around on the network without a good reason (expect the super simple implementation).
I implemented the scheduler so that you can anytime drop in a new worker. To keep the
implementation simple in these cases the Round Robin load balancing I use between the workers
is restarted from the first worker - again, this is not the best solution, but the simplest I
came up with. In the scheduler I used asyncore to have an efficient networking side.
Despite I concentrated on the horizontal scaleability, I did not solved a couple of things,
before the program could go into real production use. For example the scheduler does not have
any possibilities for fail overs or load balancing, of course by design you can setup different
"clusters" with their own schedulers and distribute the urls between them. If I stuck with
the Pingdom example, every customer could have it's own Scheduler with auto-scaled workers.
Scaling could be done on url numbers or network usage of the worker node.
I tried to make the program fail safe, but I'm sure that I have unhandled error cases, I
mentioned already, no proper testing was done.

Some technical things:
 python 2.7
 cPickle
 http2
 re
 socket
 time
 logging
 asyncore
 argparser
 sys

Thanks a lot for reading, don't forget to check command line options with -h.