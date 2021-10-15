import os
import json
from datetime import datetime

import slack

from .models import Employee, Menu
from .serializers import MealSerializer, CombinationSerializer
from .tasks import send_reminder


def send_slack_reminders(menu_id):
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
             "text": "Hello everyone!:smile:\nHere we have the *today's menu*:"
         }
         },
        {"type": "divider"},
    ]
    message.extend([
        {"type": "section",
         "text": {
             "type": "mrkdwn",
             "text": f":knife_fork_plate: *{o.description}*"
         },
         "accessory": {
             "type": "button",
             "text": {
                 "type": "plain_text",
                 "text": "I want it"
             },
             "value": "click_me_123"
         }
         } for o in menu.combinations.all()])
    message.extend(
        [{"type": "divider"},
         {"type": "section",
          "text": {
              "type": "mrkdwn",
              "text": "Do you want to order on page?"
          },
          "accessory": {
              "type": "button",
              "text": {
                  "type": "plain_text",
                  "text": "Go to page"
              },
              "value": "click_me_123",
              "url": "http://0.0.0.0:8000/views/menu",
              "action_id": "button-action"
          }
          }
         ]
    )
    #  TODO Use token as environ variable
    #  TODO Use client here to avoid re-creating it on each request
    # client = slack.WebClient(os.environ.get('SLACK_TOKEN', 'xoxb-2593331801751-2605065321397-tBklm6beIrBH6oTmvvnoqL2J'))
    for employee in Employee.objects.all()[:1]:
        # send_reminder.delay(message, employee.slack_id)
        send_reminder.delay(json.dumps(message), employee.slack_id)


def get_next_menu_info():
    """
    Iterates through nested items to get values as string
    """
    output = []
    for menu in Menu.objects.order_by('date'):
        days_diff = (menu.date - datetime.now().date()).days
        if days_diff > 0 or (days_diff == 0 and datetime.now().hour < 11):
            for c in menu.combinations.all():
                output.append({'name': f'Option {len(output) + 1}',
                               'values': [f'{m.unit_cost} {m.unit_label} of {m.name}' for m in c.meals.all()]})
            break
    return output
