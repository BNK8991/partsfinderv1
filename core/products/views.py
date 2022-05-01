import json
from django.shortcuts import get_object_or_404, render
from sympy import source
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from .models import Category, Product, SubCategory


# Create your views here.
def index(request):
    categories = Category.objects.all()

    return render(request, 'base.html', {"categories": categories})


def getProductByCategory(request, id):
    categories = Category.objects.all()
    if id:
        category = get_object_or_404(categories, id=id)
        products_microCenter = Product.objects.filter(
            category=category, source='microcenter').order_by("price")
        products_centerComputer = Product.objects.filter(
            category=category,  source='centralcomputer').order_by("price")
        filterCategory = SubCategory.objects.filter(
            category=category).order_by("id")
    template = "filterproduct.html"
    context = {"products_microCenter": products_microCenter,
               "products_centerComputer": products_centerComputer,
               "categories": category,
               "filter": filterCategory
               }
    return render(request, template, context)


def getAllProducts(request):
    products_microCenter = Product.objects.filter(
        source='microcenter').order_by("price")
    products_centerComputer = Product.objects.filter(
        source='centralcomputer').order_by("price")
    template = "products.html"
    context = {"products_microCenter": products_microCenter,
               "products_centerComputer": products_centerComputer}
    return render(request, template, context)


def search(request):
    q = request.GET['q']
    products_microCenter = Product.objects.filter(
        name__icontains=q).filter(source='microcenter').order_by('-id')
    products_centerComputer = Product.objects.filter(
        name__icontains=q).filter(source='centralcomputer').order_by('-id')
    template = "products.html"
    context = {"products_microCenter": products_microCenter,
               "products_centerComputer": products_centerComputer}

    return render(request, template, context)


@csrf_exempt
def searchByFilter(request):
    id_sub = request.POST['id_sub']
    id_cat = request.POST['id_cat']
    name = request.POST['name']
    products_microCenter = Product.objects.filter(
        name__icontains=name).filter(source='microcenter').filter(category=int(id_cat)).order_by('-id')
    products_centerComputer = Product.objects.filter(
        name__icontains=name).filter(source='centralcomputer').filter(category=int(id_cat)).order_by('-id')
    if products_microCenter:
        lst_microCenter = []
        for product in products_microCenter:
            obj_micro = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'urls': product.urls,
                'thumbnail': product.thumbnail,
                'available': product.available,
                'created_at': product.created_at,
                'updated_at': product.updated_at,
                'source': "microcenter"
            }
            lst_microCenter.append(obj_micro)
    else:
        lst_microCenter = []
    if products_centerComputer:
        lst_centerComputer = []
        for product in products_centerComputer:
            obj_center = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'urls': product.urls,
                'thumbnail': product.thumbnail,
                'available': product.available,
                'created_at': product.created_at,
                'updated_at': product.updated_at,
                'source': "microcenter"
            }
            lst_centerComputer.append(obj_center)
    else:
        lst_centerComputer = []
    context = {"products_microCenter": lst_microCenter,
               "products_centerComputer": lst_centerComputer}
    return HttpResponse(json.dumps(context, cls=DjangoJSONEncoder), content_type="application/json")
