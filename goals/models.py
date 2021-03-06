from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

from topics.models import Resource
from users.models import User

class Goals(Resource):
	presentation = models.TextField(_('Presentation'), blank = True)
	limit_submission_date = models.DateTimeField(_('Submission Limit Date'), null = True, blank = True)

	class Meta:
		verbose_name = _('Goal')
		verbose_name_plural = _('Goals')

	def __str__(self):
		return self.name

	def access_link(self):
		if self.show_window:
			return reverse_lazy('goals:window_submit', args = (), kwargs = {'slug': self.slug})

		return reverse_lazy('goals:submit', args = (), kwargs = {'slug': self.slug})

	def update_link(self):
		return 'goals:update'

	def delete_link(self):
		return 'goals:delete'

	def delete_message(self):
		return _('Are you sure you want delete the %s topic goals specification')%(self.topic.name)

class GoalItem(models.Model):
	description = models.CharField(_('Description'), max_length = 255, blank = True)
	ref_value = models.IntegerField(_('Referential Value'))
	order = models.PositiveSmallIntegerField(_('Order'), null = True)
	goal = models.ForeignKey(Goals, verbose_name = _('Goal'), related_name = 'item_goal')

	class Meta:
		ordering = ['order']

class MyGoals(models.Model):
	value = models.IntegerField(_('My Value'))
	user = models.ForeignKey(User, verbose_name = _('User'), related_name = 'user_goals')
	item = models.ForeignKey(GoalItem, verbose_name = _('Goal'), related_name = 'mine_goals')
	create_date = models.DateTimeField(_('Create Date'), auto_now_add = True)
	last_update = models.DateTimeField(_('Last Update'), auto_now = True)