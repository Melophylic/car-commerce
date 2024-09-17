from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from main.forms import ProductForm
from main.models import Product

def show_main(request):
    products = Product.objects.all()
    product = {
        'name' : 'R34',
        'price': '$100,000',
        'description': 'A cool car',
        'products': products
    }
    return render(request, "main.html", product)

def show_me(request):
    
    me = {
        'nama': 'Muhammad Nadzim Tahara',
        'npm': '2306275430',
        'kelas': 'PBP C 2024'
    }

    return render(request, "main.html", me)

def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, "create_product.html", context)

def show_xml(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")