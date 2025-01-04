from django_cron import CronJobBase, Schedule
from .utils import trimite_notificari_calatorii_viitoare

class TrimiteNotificariCron(CronJobBase):
    RUN_EVERY_MINS = 1440  # Rulează o dată pe zi

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'infotren.trimite_notificari_cron'  # Unic pentru fiecare job cron

    def do(self):
        trimite_notificari_calatorii_viitoare()