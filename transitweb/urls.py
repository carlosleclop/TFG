from django.conf.urls import *
from transitweb import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^notifications/mark/$', views.mark_as_read, name="mark_as_read"),
    url(r'^notifications/remove/$', views.remove_notification, name="remove_notification"),

    url(r'^management/add_equipment/$', views.add_equipment, name="add_equipment"),
    url(r'^management/add_occult/$', views.add_occult, name="add_occult"),
    url(r'^notifications/$', views.see_notifications, name="see_notifications"),
    url(r'^occultation/(?P<occult_id>[\w\-]+)/subscribe/$', views.subscribe_occult, name="subscribe"),
    url(r'^occultation/send/(?P<occult_id>[\w\-]+)/(?P<equipment_id>[\w\-]+)$', views.add_result, name="add_result"),
    url(r'^occultation/(?P<occult_id>[\w\-]+)/$', views.occult_page, name="occultation"),

    url(r'^result/(?P<result_id>[\w\-]+)/$', views.see_result, name='see_result'),

    url(r'^workspace/observer/$', views.workspace_observer, name='workspace_observer'),
    url(r'^workspace/astronomer/$', views.workspace_astronomer, name='workspace_astronomer'),

    url(r'^accounts/profile/$', views.user_profile, name='user_profile'),
    url(r'^accounts/login/$', views.user_login, name='login'),
    url(r'^accounts/logout/$', views.user_logout, name='logout'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/update_profile/$', views.edit_profile, name='update_profile'),
    url(r'^accounts/edit_equipment/(?P<equipment_id>[\w\-]+)/$', views.edit_equipment, name='edit_equipment'),
    url(r'^accounts/delete_equipment/(?P<equipment_id>[\w\-]+)/$', views.delete_equipment, name='delete_equipment'),

    url(r'^user/(?P<username>[\w\-]+)/$', views.see_profile, name='see_profile')
]

"""
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^category/(?P<category_name_slug>\w+)$', views.category, name='category'),
    url(r'^add_category/$', views.add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>\w+)/add_page/$', views.add_page, name='add_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
"""
