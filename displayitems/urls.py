from django.conf.urls import url

import displayitems.views

urlpatterns = [
    url(r'^display', displayitems.views.rec_html, name='recs'),
    url(r'^update', displayitems.views.get_recs, name='upd'), 
    url(r'^$', displayitems.views.home, name='index'), 
    url(r'^swipe', displayitems.views.swipe, name='swipe'), 
]