from application import create_app
from celery.schedules import crontab
from worker  import celery_init_app
from tasks import daily_reminder,monthly_report

app = create_app()
celery_app = celery_init_app(app)


# with app.app_context():
#  for rule in app.url_map.iter_rules():
#         print(rule)

@celery_app.on_after_finalize.connect
def send_email(sender, **kwargs):
        sender.add_periodic_task(
            crontab(hour=6, minute=14),
            daily_reminder,
        )

@celery_app.on_after_finalize.connect
def send_report_email(sender, **kwargs):
        sender.add_periodic_task(
            crontab(hour=6, minute=14, day_of_month=16),
            monthly_report,
        )


if __name__=="__main__":
   app.run(debug=True)