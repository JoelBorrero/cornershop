UNIT_LABELS = (('g', 'Gram'), ('unit', 'Unit'), ('ml', 'Milliliter'))

COMBINATION_FIELDS = ({'id': 'meals', 'label': 'Meals', 'options': True},
                      {'id': 'description', 'label': 'Description', 'type': 'text'})

LOGIN_FIELDS = ({'id': 'username', 'label': 'Username', 'type': 'text'},
                {'id': 'password', 'label': 'Password', 'type': 'password'})

REGISTER_FIELDS = ({'id': 'name', 'label': 'Name', 'type': 'text'},
                   {'id': 'new_username', 'label': 'Username', 'type': 'text'},
                   {'id': 'slack_id', 'label': 'Slack ID', 'type': 'text'},
                   {'id': 'new_password', 'label': 'Password', 'type': 'password'})

MEAL_FIELDS = ({'id': 'name', 'label': 'Name', 'type': 'text'},
               {'id': 'unit_cost', 'label': 'Unit cost', 'type': 'number'},
               {'id': 'unit_label', 'label': 'Unit label', 'type': 'text', 'options': UNIT_LABELS},
               {'id': 'stock', 'label': 'Stock', 'type': 'text'})

MENU_FIELDS = ({'id': 'date', 'label': 'Date', 'type': 'date'},
               {'id': 'combinations', 'label': 'Combinations', 'options': True})
