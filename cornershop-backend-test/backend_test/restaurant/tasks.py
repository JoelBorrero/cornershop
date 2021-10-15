import os

from celery import shared_task
import slack


@shared_task
def send_reminder(message, employee_slack_id):
    """
    Sends the individual reminder to each user slack account
    """
    client = slack.WebClient(os.environ.get('SLACK_TOKEN', 'xoxb-2593331801751-2605065321397-tBklm6beIrBH6oTmvvnoqL2J'))
    client.chat_postMessage(channel='#test', blocks=message)
