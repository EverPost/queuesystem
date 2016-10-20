# coding:utf-8

from django.conf.urls import url
from .import views

urlpatterns = [

    #提交订单 0:预约
    url(r'^submitorder/(?P<type>[0-1])/$',views.submitorder,name='submitorder'),

    #按项目预约 queue/id
    url(r'^(?P<productPk>[0-9]+)/$',views.queuemain,name = 'queuemain'),

    #预约特定的人
    url(r'^(?P<productPk>[0-9]+)/(?P<personPk>[0-9]+)',views.queueperson,name='queueperson'),

    #我的预约/排队 queue/myorder/1
    url(r'^myorder/(?P<type>[0-1])/$',views.myorder,name = 'myorder'),

    url(r'^command/(?P<arg>[a-z]*)/$',views.syncdb),
    # 视图测试
    #url(r'^(?P<testview>[a-z]*[-]*[a-z]*)/$', views.testViews, name='testview')

    #微信测试
    #url(r'wechat/$',views.wechatscope),
    url(r'redirect/$',views.redirect),
    url(r'^login/$',views.wechatscope),
]