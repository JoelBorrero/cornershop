import json
import os

from celery import shared_task
import slack

from backend_test.restaurant.models import Employee, Menu
from backend_test.restaurant.services import check_slack_users


@shared_task
def send_message(message: list, employee_slack_id: str, employee_name: str = 'everyone'):
    """
    Sends the individual reminder to each user slack account
    """
    client = slack.WebClient(os.environ.get('SLACK_TOKEN', '###SLACK_TOKEN###'))
    message[0]['text']['text'] = message[0]['text']['text'].replace('everyone', employee_name)
    try:
        client.chat_postMessage(channel=employee_slack_id, blocks=message)
    except slack.errors.SlackApiError:
        print('Slack Id', employee_slack_id, 'not found')


@shared_task
def send_slack_reminders(menu_id: int, menu_uuid: str):
    """
    This function allows to send in delay the task, to use as much celery workers as can,
    so all the tasks runs next to the other one
    @param: menu_id: INT: The id of the menu that will be notified to users
    """
    menu = Menu.objects.filter(id=menu_id).first()
    message = [
        {"type": "section",
         "text": {
             "type": "mrkdwn",
             "text": f"Hello everyone!:smile:\nHere we have the *today's menu* ({menu.date}):"
         }
         },
        {"type": "divider"}
    ]
    message.extend([
        {"type": "section",
         "text": {
             "type": "mrkdwn",
             "text": f":knife_fork_plate: *{o.description}*"
         }
         } for o in menu.combinations.all()])
    message.extend([{"type": "divider"},
                    {"type": "section",
          "text": {
              "type": "mrkdwn",
              "text": "Do you want to order right now?"
          },
          "accessory": {
              "type": "button",
              "text": {
                  "type": "plain_text",
                  "text": "Go to page"
              },
              "url": f'{os.environ.get("BASE_HOST", "http://0.0.0.0:8000")}/views/menu/{menu_uuid}',
              "action_id": "button-action"
          }
          }
         ])
    check_slack_users()
    #  TODO Use client here to avoid re-creating it on each request
    for employee in Employee.objects.all():
        if employee.slack_id:
            send_message.delay(message, employee.slack_id, employee.first_name)
