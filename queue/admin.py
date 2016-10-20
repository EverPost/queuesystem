# coding:utf-8
from django.contrib import admin

# Register your models here.
from .models import *

class QueuenorderAdmin(admin.ModelAdmin):
    fields = ('user','number')
    list_display = ('user','number','create_time')
    search_fields = ('user',)

class ProductAdmin(admin.ModelAdmin):
    fields = ('name', 'des', 'image')
    list_display = ('id','name', 'des')
    search_fields = ('name',)

class PersonAdmin(admin.ModelAdmin):
    fields = ('name', 'des', 'product','icon')
    list_display = ('name', 'des','product')
    search_fields = ('name',)

class QueuenumberAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        #如果重置->修改时间为当前时间 号码设置为默认值
        if change:
            if obj.isreset:
                obj.create_time = timezone.now()
                obj.currentnumber = 1
                obj.lastqueuenumber = 1
                obj.isacceivequeue = True
                obj.isreset = False
                obj.save()
            else:
                old = self.model.objects.get(pk=obj.pk)
                obj.lastqueuenumber = old.lastqueuenumber
                obj.save()
        else:
            obj.save()
    fields = ('isacceivequeue','isreset', 'lastqueuenumber', 'currentnumber','create_time')
    list_display = ('isacceivequeue', 'lastqueuenumber', 'currentnumber', 'create_time')

class ApintmentorderAdmin(admin.ModelAdmin):
    fields = ('user','product','person','ordertime')
    list_display = ('user','product','person','ordertime')
    search_fields =  ('user','product','person')

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('user','nickname','sex')
    search_fields =  ('user','nickname')

admin.site.register(CustomUser,CustomUserAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Person,PersonAdmin)
admin.site.register(ApointmentOrder,ApintmentorderAdmin)
admin.site.register(Queuenumber,QueuenumberAdmin)
admin.site.register(QueueOrder,QueuenorderAdmin)
admin.site.register(Access_token)