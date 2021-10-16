import hashlib
import os
import json
from datetime import datetime

import slack
from django.contrib.auth.hashers import make_password

from .models import Employee, Menu


def check_slack_users():
    """
    Iterates through Slack users and create/update it as Employee
    """
    client = slack.WebClient(os.environ.get('SLACK_TOKEN', '###SLACK_TOKEN###'))
    users = client.users_list()
    for user in users.data['members']:
        if not user['is_bot'] and not user['id'] == 'USLACKBOT':
            employee, created = Employee.objects.update_or_create(slack_id=user['id'], defaults={
                'first_name': user['profile']['real_name_normalized'], 'username': user['name']})
            if created:  # Verified to don't reset password
                employee.password = make_password(user['name'])
                employee.save()


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


def check_date_availability(menu_id: int, date: datetime) -> bool:
    """
    Check if the param date is available to perform creation or updates.
    Menu_id is requested to verify if found date refers to the same menu
    @param: menu_id: int
    @param: date: datetime
    """
    menu = Menu.objects.filter(date=date).first()
    return menu.id == menu_id if menu else True


def make_hash(date: datetime) -> str:
    """
    Returns a UUID for the date and the current timestamp
    """
    data = bytes(str(date) + str(datetime.now()), encoding='ascii')
    return hashlib.sha256(data).hexdigest()
