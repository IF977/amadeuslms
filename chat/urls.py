from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.GeneralIndex.as_view(), name='manage_general'),
	url(r'^subject/(?P<slug>[\w_-]+)/$', views.SubjectView.as_view(), name='subject_view'),
	url(r'^participants/$', views.GeneralParticipants.as_view(), name='participants_general'),
	url(r'^subject/participants/(?P<subject>[\w_-]+)/$', views.SubjectParticipants.as_view(), name='participants_subject'),
	url(r'^render_message/([\w_-]+)/([\w_-]+)/([\w_-]+)/([\w_-]+)/([\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.render_message, name='render_message'),
	url(r'^favorite/([\w_-]+)/$', views.favorite, name='favorite'),
	url(r'^view_message/([\w_-]+)/$', views.message_viewed, name='view_message'),
	url(r'^load_messages/([\w_-]+)/$', views.load_messages, name='load_messages'),
	url(r'^talk/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.GetTalk.as_view(), name = 'talk'),
	url(r'^send_message/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/(?P<talk_id>[\w_-]+)/(?P<space>[\w_-]+)/(?P<space_type>[\w_-]+)/$', views.SendMessage.as_view(), name = 'create'),
	url(r'^participant/profile/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', views.ParticipantProfile.as_view(), name = 'profile'),
]