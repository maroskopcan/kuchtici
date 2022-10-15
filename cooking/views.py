from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from .forms import ReceiptRatingForm
from .models import Receipt, Ingredients, ReceiptRating
# from .forms import ReceiptRatingFrom
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from decimal import Decimal
from random import choice
import json, requests
from bs4 import BeautifulSoup


def update_rec_form(request, id):
    t = request.POST['rec_t']
    a = request.POST['rec_a']
    receipt = Receipt.objects.get(id=id)
    receipt.rec_title = t
    receipt.author = a
    receipt.save()
    return HttpResponseRedirect(reverse('homepage'))

def add_ingredients(request, id):
    i1 = request.POST['i_name']
    i2 = request.POST['i_quant']
    i3 = request.POST['i_unit']
    i4 = 0
    i = Ingredients(ingr_name=i1, quantity=i2, unit=i3, price=i4)
    i.save()
    i.rec_id.add(id)
    red = redirect("/update_rec/"+str(id))
    return red

def update_rec(request, id):
    upd_ = Receipt.objects.get(id=id)
    ingr = Ingredients.objects.filter(rec_id = id)
    #rat = ReceiptRating.objects.get(receipt=id)
    template = loader.get_template('update_rec.html')
    context = {
        'upd_': upd_,
        'ingr': ingr,
         #'rat': rat,
    }
    return HttpResponse(template.render(context, request))

def update_rec_form(request, id):
    t = request.POST['rec_t']
    a = request.POST['rec_a']
    receipt = Receipt.objects.get(id=id)
    receipt.rec_title = t
    receipt.author = a
    receipt.save()
    return HttpResponseRedirect(reverse('admin_tools'))

def delete_rec(request, id):
    del_ = Receipt.objects.get(id=id)
    del_.delete()
    return redirect("admin_tools")

def add_receipt_form(request):
    x = request.POST['recepis']
    y = request.POST['autor']
    z = request.POST['ratex']
    rece_ = Receipt(rec_title=x, author=y, rating=z)
    rece_.save()
    return HttpResponseRedirect(reverse('admin_tools'))

def scrap(request):
    url = request.POST['url_name']
    receipts = scrap_main(url)
    p = ""
    for item in receipts[3][0]:
        p += item
    r = Receipt(rec_title=receipts[0], author='WEB', rating=5, process=p)
    r.save()
    for item in receipts[2]:
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
    return redirect("admin_tools")

def del_all(request):
    Receipt.objects.all().delete()
    return redirect('/admin_tools')
    # Receipt.objects.all().delete()
    # return HttpResponseRedirect(reverse('homepage'))

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
    return redirect('/admin_tools')

class ListReceiptRatingView(TemplateView):
    template_name = "receipt_rating.html"

    def get_context_data(self, **kwargs):
        context = super(ListReceiptRatingView, self).get_context_data(**kwargs)
        context.update({
            'form': ReceiptRatingForm(),
        })
        return context
                            # v main na recepte tlacitko ohodnot recept
                            # <a href="{% url 'receipt_rating' receipt.pk %}" class="btn btn-success">Hodnocení</a>

def main(request):
    return render(request, 'main.html')

def receipt(request):
    return render(request, 'roulette.html')

def about(request):
    return HttpResponse(redirect('about'))

def admin_tools(request):
    myreceipts = Receipt.objects.all().values()
    template = loader.get_template('admin_tools.html')
    context = {
        'myreceipts': myreceipts,
    }
    return HttpResponse(template.render(context, request))

def scrap_main(url):
    page = requests.get(url)
    soup_load = BeautifulSoup(page.text, "html.parser")
    receipt = []
    title = soup_load.find('title').text
    title = title.replace("  - Recepty.cz - On-line kuchařka", "")
    s1 = ["li", "class", "ingredient-assignment__group"]
    s2 = ["div", "class", "ingredient-assignment__desc"]
    lc = [2,4,5,6]
    ingredients = scrap_receipt(soup_load, s1, s2, lc)
    s1 = ["div", "class", "cooking-process__item-wrapper"]
    s2 = ["div", "class", "cooking-process__item"]
    lc = 5
    cooking_process = scrap_process(soup_load, s1, s2, lc)
    receipt.append(title)
    receipt.append(url)
    receipt.append(ingredients)
    receipt.append(cooking_process)
    return receipt

def scrap_receipt(soup, search1, search2, list_code):
    items_list = []
    for li in soup.find_all(search1[0], {search1[1]: search1[2]}):
        ingr = li.find_all(search2[0], {search2[1]: search2[2]})
        for item in ingr:
            items = []
            ingr_split = item.text.split("\n")
            if ingr_split[1].strip() != "":
                items.append("")
                items.append("")
                items.append(ingr_split[1].strip())
            else:
                for i in list_code:
                    try:
                        items.append(ingr_split[i].strip())
                    except IndexError:
                        print("Scrap se nezdaril, index Error")
                items[0] = items[0].replace(",", ".")
                try:
                    x = float(items[0])
                    items[0] = x
                except:
                    pass
            items_list.append(items)
    return items_list

def scrap_process(soup, search1, search2, list_code):
    items_list = []
    for li in soup.find_all(search1[0], {search1[1]: search1[2]}):
        ingr = li.find_all(search2[0], {search2[1]: search2[2]})
        items = []
        for item in ingr:
            ingr_split = item.text.split("\n")
            items.append(ingr_split[list_code].strip())
        items_list.append(items)
    return items_list


