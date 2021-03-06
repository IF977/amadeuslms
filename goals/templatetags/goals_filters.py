from django import template
from django.utils.translation import ugettext_lazy as _

from goals.models import MyGoals
from log.models import Log
from students_group.models import StudentsGroup

register = template.Library()

@register.filter(name = 'groups')
def groups(user):
	groups = user.group_participants.values_list('name', flat = True)

	if groups.count() > 0:
		groups = list(groups)

		return ", ".join(groups)
	else:
		return "---"

@register.filter(name = 'log_groups')
def log_groups(user_id):
	groups = StudentsGroup.objects.filter(participants__id = user_id).values_list('name', flat = True)

	if groups.count() > 0:
		groups = list(groups)

		return ", ".join(groups)
	else:
		return "---"

@register.filter(name = 'creation_date')
def creation_date(user, goal):
	log = Log.objects.filter(user_id = user.id, action = 'submit', resource = 'goals', context__contains = {"goals_id": goal.id})

	if log.count() > 0:
		return log[0].datetime

	return ""

@register.filter(name = 'update_date')
def update_date(user, goal):
	log = Log.objects.filter(user_id = user.id, action = 'update_submit', resource = 'goals', context__contains = {"goals_id": goal.id})

	if log.count() > 0:
		return log[0].datetime

	return ""

@register.filter(name = 'my_goals')
def my_goals(user, goal):
	mine = list(MyGoals.objects.filter(user = user, item__goal = goal).values_list('value', flat = True))

	return  ', '.join(str(x) for x in mine)

@register.filter(name = 'log_action')
def log_action(action):
	if action == 'view':
		return _('Visualized')
	elif action == 'create':
		return _('Added')
	elif action == 'update':
		return _('Updated')
	elif action == 'submit':
		return _('Submitted')

	return  '---'

@register.filter(name = 'log_object')
def log_object(log):
	if log.resource == 'my_goals':
		return _('My Goals')

	name = log.context['goals_name']

	return _("%s Instance")%(name)