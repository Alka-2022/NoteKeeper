# api/cron.py
from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail
from django.utils import timezone
from api.models import YourTaskModel

class DailyTaskSummaryEmail(CronJobBase):
    RUN_AT_TIMES = ['23:59']  # Run the job at the end of the day

    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'api.daily_task_summary_email'

    def do(self):
        # Collect tasks created, edited, and done in the last 24 hours
        start_of_day = timezone.now() - timezone.timedelta(days=1)
        created_tasks = YourTaskModel.objects.filter(created_at__gte=start_of_day)
        edited_tasks = YourTaskModel.objects.filter(edited_at__gte=start_of_day)
        done_tasks = YourTaskModel.objects.filter(done=True, done_at__gte=start_of_day)

        # Prepare the email body
        email_subject = 'Daily Task Summary'
        email_body = f'''
        Tasks Created:
        {', '.join(str(task) for task in created_tasks)}

        Tasks Edited:
        {', '.join(str(task) for task in edited_tasks)}

        Tasks Done:
        {', '.join(str(task) for task in done_tasks)}
        '''

        # Send the email
        send_mail(email_subject, email_body, 'ralka4776@gmail.com', ['ralka4776@gmail.com'])
