#coding:utf-8
from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.db import transaction
# Create your views here.

def testtransaction(request):
    try:
        model = TestTransteaction.objects.all()[0]
    except Exception:
        return HttpResponse('do not exit')
    else:
        model.number += 1
        model.save()
        model.number += 1
        model.save()
        return HttpResponse(model.number)

@transaction.atomic
def testWithTransaction(request):
    try:
        model = TestTransteaction.objects.all()[0]
    except Exception:
        return HttpResponse('do not exit')
    else:
        model.number += 1
        model.save()
        raise TestTransteaction.DoesNotExist
        model.number += 1
        model.save()
        return HttpResponse(model.number)