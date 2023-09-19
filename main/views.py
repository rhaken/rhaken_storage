from django.shortcuts import render
from django.http import HttpResponseRedirect
from main.forms import ProductForm
from django.urls import reverse
from main.models import Item
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Sum

# Create your views here.
def show_main(request):
    products = Item.objects.all()
    temp = Item.objects.aggregate(total=Sum('amount'))['total']
    if(len(products) == 0):
        temp = 0
    context = {
        'name': 'Rhaken Shaquille Akbar Yanuanda', # Nama kamu
        'class': 'PBP B', # Kelas PBP kamu
        'banyak_jenis_item' : len(products),
        'banyak_item' : temp,
        'products': products
    }

    return render(request, "main.html", context)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_product.html", context)

def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


