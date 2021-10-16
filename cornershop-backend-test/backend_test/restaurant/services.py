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
             "text": f"Hello everyone!:smile:\nHere we have the *today's menu* ({menu.date}):"
         }
         },
        {"type": "divider"},
    ]
    message.extend([
        {"type": "section",
         "text": {
             "type": "mrkdwn",
             "text": f":knife_fork_plate: *{o.description}*"
         }
         } for o in menu.combinations.all()])
    message.extend(
        [{"type": "divider"},
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
              "url": os.environ.get("BASE_HOST", "http://0.0.0.0:8000") + "/views/menu",
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


def get_menus_info():
    """
    Iterates through nested items to get values as string
    :return: submittable, today_menu, next_menu(If differ)
    """

    def make_dict(menu: dict, combination: object):
        """
        Returns a dict formatted and ready to consume in front view.
        @param: menu: Dict
        @param: combination: Combination model
        """
        return {'id': combination.id, 'index': f'Option {len(menu["combinations"]) + 1}',
                'description': combination.description,
                'values': [f'{m.unit_cost} {m.unit_label} of {m.name}' for m in combination.meals.all()]}

    today_menu, next_menu = {'combinations': []}, {'combinations': []}
    submittable = False
    for menu in Menu.objects.order_by('date'):
        if 'id' not in today_menu:
            if menu.date.day == datetime.now().day:
                today_menu['id'] = menu.id
                today_menu['date'] = menu.date
                for c in menu.combinations.all():
                    today_menu['combinations'].append(make_dict(today_menu, c))
        if 'id' not in next_menu:
            days_diff = (menu.date - datetime.now().date()).days
            if days_diff > 0 or (days_diff == 0 and datetime.now().hour < 11):
                submittable = True
                next_menu['id'] = menu.id
                next_menu['date'] = menu.date
                for c in menu.combinations.all():
                    next_menu['combinations'].append(make_dict(next_menu, c))
    try:
        if today_menu['id'] == next_menu['id']:
            next_menu = None
    except KeyError:
        pass
    return submittable, today_menu, next_menu


def check_date_availability(date: datetime) -> bool:
    """
    Check if the param date is available to perform creation or updates
    @param: date: Date
    """
    return not Menu.objects.filter(date=date).first()
