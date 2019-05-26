from django_cron import CronJobBase, Schedule
from . import instascrape, urlcheck


# This file will eventually be used to automate the database refresh
class URLCheckJob(CronJobBase):
    # Set higher to limit how often it can be run
    RUN_EVERY_MINS = .5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tracker.cronjobs.URLCheckJob'

    def do(self):
        urlcheck.dead_url_check()


class InstaScrapeJob(CronJobBase):
    RUN_EVERY_MINS = .5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'tracker.cronjobs.InstaScrapeJob'

    def do(self):
        instascrape.main()
