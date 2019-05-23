from django_cron import CronJobBase, Schedule
from . import instascrape, urlcheck


# This file will eventually be used to automate the database refresh
class MyCronJob(CronJobBase):
    # RUN_EVERY_MINS = 2

    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # code = 'tracker.cronjobs.MyCronJob'

    def do(self):
        instascrape.main()


class URLCheckJob(CronJobBase):
    # RUN_EVERY_MINS = 2
    #
    # schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    # code = 'tracker.cronjobs.URLCheckJob'

    def do(self):
        urlcheck.dead_url_check()
