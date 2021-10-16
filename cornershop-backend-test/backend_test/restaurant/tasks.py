import os

from celery import shared_task
import slack


@shared_task
def send_reminder(message: str, employee_slack_id: str):
    """
    Sends the individual reminder to each user slack account
    """
    client = slack.WebClient(os.environ.get('SLACK_TOKEN', '###SLACK_TOKEN###'))
    client.chat_postMessage(channel='#test', blocks=message)
