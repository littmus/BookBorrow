from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                        url(r'^join/$', 'account.views.join_view'),
                        url(r'^join_ok/$', 'account.views.join_ok'),
                        url(r'^login/$', 'account.views.login_view'),
                        url(r'^login_ok/$', 'account.views.login_ok'),
                        url(r'^logout_ok/$', 'account.views.logout_ok'),
)