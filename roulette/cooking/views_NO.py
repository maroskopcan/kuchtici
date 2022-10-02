from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from .forms import ReceiptRatingForm

from .models import Receipt, Ingredients
#from .forms import ReceiptRatingFrom
from django.contrib.auth.models import User
from django.shortcuts import redirect
from decimal import Decimal
from random import choice
import json


def del_all(request):
    Receipt.objects.all().delete()
    return HttpResponseRedirect(reverse('homepage'))

def roulette(request):
    c = Receipt.objects.all().values_list('pk', flat=True)
    r = choice(c)
    receipt = Receipt.objects.get(pk=r)
    ingr = Ingredients.objects.filter(rec_id=r)
    template = loader.get_template('roulette.html')
    context = {
        'receipt': receipt,
        'ingr': ingr,
    }
    return HttpResponse(template.render(context, request))

# def homepage_view(request):
#     myreceipts = Receipts.objects.all().values()
#     template = loader.get_template('main.html')
#     context = {
#         'myreceipts': myreceipts,
#     }
#     return HttpResponse(template.render(context, request))


class HomepageView(TemplateView):
    template_name = "main.html"
    def get_context_data(self, **kwargs):
        context = super(HomepageView, self). get_context_data(**kwargs)

        myreceipts = Receipts.objects.all().values()
        template = loader.get_template('main.html')

        return context
def upload(request):
    with open('receipts.json', 'rb') as fp:
        receipts_load = json.load(fp)

    for rl in receipts_load:
        p = ""
        for item in rl[4][0]:
            p += item
        r = Receipts(rec_title=rl[1], author='WEB', rating=5, process=p)
        r.save()

        for item in rl[3]:
            i1 = item[2]
            i2 = item[0]
            if i2 == "":
                i2 = 0
            else:
                i2 = Decimal(i2)
            i3 = item[1]
            i = Ingredients(ingr_name=i1, quantity=i2, unit=i3, price=0)
            i.save()
            i.rec_id.add(r)
    return HttpResponseRedirect(reverse('homepage'))


class ListReceiptRatingView(TemplateView):
    template_name = "receipt_rating.html"

    def get_context_data(self, **kwargs):
        context = super(ListReceiptRatingView, self).get_context_data(**kwargs)
        context.update({
            'form': ReceiptRatingForm(),
        })
        return context

    # v main na recepte tlacitko ohodnot recept <a href="{% url 'receipt_rating' receipt.pk %}" class="btn btn-success">Hodnocení</a>
