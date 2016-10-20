from  django.conf.urls import url,include

urlpatterns = [
    url(r'^notransation/$','demos.views.testtransaction'),
    url(r'^withtransation/$', 'demos.views.testtransaction'),
]