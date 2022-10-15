from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, FormView, UpdateView
from .forms import ReceiptRatingForm, ReceiptRatingUpdateForm
from .models import Receipt, Ingredients, ReceiptRating
#from .forms import ReceiptRatingFrom
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
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

def homepage_view(request):
   myreceipts = Receipt.objects.all().values()
   template = loader.get_template('main.html')
   context = {
       'myreceipts': myreceipts,
   }
   return HttpResponse(template.render(context, request))

# class HomepageView(TemplateView):
#     template_name = "main.html"
#     def get_context_data(self, **kwargs):
#         context = super(HomepageView, self).get_context_data(**kwargs)
#
#         myreceipts = Receipt.objects.all().values()
#         template = loader.get_template('main.html')
#         return context





def upload(request):
    with open('receipts.json', 'rb') as fp:
        receipts_load = json.load(fp)

    for rl in receipts_load:
        print(rl)
        p = ""
        for item in rl[4][0]:
            p += item
        r = Receipt(rec_title=rl[1], author='WEB', rating=5, process=p)
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
        #product = get_object_or_404(Receipt, pk=kwargs["receipt_pk"])
        user = get_user_model().objects.first()

        context.update({
            'form': ReceiptRatingForm(),
            'receipt': receipt
        })
        return context
#
#     # v main na recepte tlacitko ohodnot recept <a href="{% url 'receipt_rating' receipt.pk %}" class="btn btn-success">Hodnocení</a>



class DeleteReceiptRatingView(UserPassesTestMixin, View):

    def test_func(self):
        receipt_rating = get_object_or_404(ReceiptRating, pk=self.kwargs["pk"])
        return self.request.user == receipt_rating.user

    def get(self, request, pk, *args, **kwargs):
        receipt_rating = get_object_or_404(ReceiptRating, pk=pk)
        receipt_rating.delete()
        return redirect(request.META.get('HTTP_REFERER', 'main'))


# class ListReceiptRatingView(PermissionRequiredMixin, LoginRequiredMixin, FormView):
#     template_name = "receipt_rating.html"
#     form_class = ReceiptRatingForm
#     permission_required = "cooking.view_receiptrating"
#
#     def get_initial(self):
#         receipt = self.get_object()
#         return {"receipt": receipt,  "user": self.request.user}
#
#     def get_object(self):
#         return get_object_or_404(Receipt, pk=self.kwargs["receipt_pk"])
#
#     def get_context_data(self, **kwargs):
#         context = super(ListReceiptRatingView, self).get_context_data(**kwargs)
#         receipt = self.get_object()
#         user = self.request.user
#         context.update({
#             "receipt": receipt,
#         })
#         return context
#
#     def post(self, request, *args, **kwargs):
#         receipt = self.get_object()
#         user = self.request.user
#
#         form_data = {
#             "user": user.pk,
#             "receipt": receipt.pk,
#             "text": request.POST.get("text"),
#             "score": request.POST.get("score")
#         }
#
#         bounded_form = ReceiptRatingForm(data=form_data)
#         if not bounded_form.is_valid():
#             context = self.get_context_data()
#             context["form"] = bounded_form
#             return TemplateResponse(request, template=self.template_name, context=context)
#
#         ReceiptRating.objects.create(
#             user=bounded_form.cleaned_data["user"],
#             receipt=bounded_form.cleaned_data["receipt"],
#             text=bounded_form.cleaned_data["text"],
#             score=bounded_form.cleaned_data["score"]
#         )
#
#         return self.get(request, *args, **kwargs)

class ReceiptRatingUpdateView(UpdateView):
    template_name = "update_receipt_rating.html"
    form_class = ReceiptRatingUpdateForm
    model = ReceiptRating

    def get_success_url(self):
        return reverse("list_receipt_rating", args=[self.object.product.id, ])


def main(request):
    return render(request, 'main.html')

def receipt(request):
    return render(request, 'roulette.html')