from django.conf.urls import *
from transitweb import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^management/add_telescope/$', views.add_telescope, name="add_telescope"),
    url(r'^management/add_occult/$', views.add_occult, name="add_occult"),

    url(r'^occultation/(?P<occult_id>[\w\-]+)/subscribe/$', views.subscribe_occult, name="subscribe"),
    url(r'^occultation/(?P<occult_id>[\w\-]+)/$', views.occult_page, name="occultation"),

    url(r'^workspace/observer/$', views.workspace_observer, name='workspace_observer'),
    url(r'^workspace/astronomer/$', views.workspace_astronomer, name='workspace_astronomer'),

    url(r'^accounts/profile/$', views.user_profile, name='user_profile'),
    url(r'^accounts/login/$', views.user_login, name='login'),
    url(r'^accounts/logout/$', views.user_logout, name='logout'),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/update_profile/$', views.edit_profile, name='update_profile'),
    url(r'^accounts/edit_telescope/(?P<telescope_id>[\w\-]+)/$', views.edit_telescope, name='edit_telescope'),
    url(r'^accounts/delete_telescope/(?P<telescope_id>[\w\-]+)/$', views.delete_telescope, name='delete_telescope'),

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
