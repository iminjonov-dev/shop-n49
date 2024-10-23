from pickle import NONE
from typing import Optional

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages

from shop.forms import CommentModelForm, OrderModelForm, ProductModelForm
from shop.models import Category, Product, Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q


def product_list(request, category_slug:Optional[str] = None):
    categories = Category.objects.all().order_by('id')
    search = request.GET.get('q')
    filter_type = request.GET.get('filter', '')
    if category_slug:
             if filter_type =='expensive':
                products = Product.objects.filter(category__slug=category_slug).order_by('-price')
             elif filter_type =='cheap':
                 products = Product.objects.filter(category__slug=category_slug).order_by('price')
             elif filter_type == 'rating':
                 products = Product.objects.filter(Q(category__slug=category_slug) & Q(rating__get=4)).order_by('-rating')
             else:
                 products = Product.objects.filter(category__slug=category_slug)


    else:
       if filter_type == 'expensive':
           products = Product.objects.all().order_by('-price')
       elif filter_type == 'cheap':
           products = Product.objects.all().order_by('price')
       elif filter_type == 'rating':
           products = Product.objects.filter (Q(rating__get=8)).order_by('-rating')
           print(products)
       else:
           products = Product.objects.all()


    if search:
        products = products.filter(Q(name__icontains=search) | Q(comments__name__icontains=search))

    context  = {
        'products' : products,
        'categories' : categories
    }
    return render(request, 'shop/home.html', context)

def product_detail(request, product_id):
    comments = Comment.objects.filter(product=product_id, is_private=True).order_by('-id')
    categories = Category.objects.all()
    product = Product.objects.get(id=product_id)
    min_price  = product.price * 0.2
    max_price = product.price * 1.8
    similar_product = Product.objects.filter(category=product.category, price__range=[min_price,max_price]).exclude(id=product.id)
    context = {
        'product' : product,
        'comments' : comments,
        'categories' : categories,
        'similar_product' : similar_product
    }
    return render(request, 'shop/detail.html', context)

# def add_comment(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         body = request.POST.get('body')
#         comment = Comment(name=name, email=email, body=body)
#         comment.product = product
#         comment.save()
#         return redirect('product_detail', product_id)
#     else:
#         pass
#     return render(request, 'shop/detail.html')
#


def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method =='POST':
       form = CommentModelForm(request.POST)
       if form.is_valid():
           comment = form.save(commit=False)
           comment.product = product
           comment.save()
           return redirect('product_detail', product_id)

    else:
        form = CommentModelForm()

    context = {
        'form' : form,
        'product' : product
    }


    return render(request, 'shop/detail.html', context)


def add_order(request, product_id):
    global context
    product = get_object_or_404(Product, id=product_id)
    form = OrderModelForm()
    sent = False
    if request.method == 'GET':
        form = OrderModelForm(request.GET)
        if form.is_valid():
            order = form .save(commit=False)
            order.product = product
            if product.quantity >= order.quantity:
                product.quantity -= order.quantity
                product.save()
                order.save()
                sent = True
                messages.add_message(
                    request,
                    level=messages.SUCCESS,
                    massage='Your order has been submitted!'
                )

                return redirect('product_detail', product_id)
            else:
                messages.add_message(
                    request,
                    level=messages.SECCESS,
                    massage='Your order has been submitted!'
                )

            context =  {
             'form': form,
             'product': product,
             'sent': sent

           }
        return render(request, 'shop/detail.html', context)
@login_required
def add_product(request):
    form = Product()
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    context = {
        'form' : form
    }

    return render(request, 'shop/add-product.html', context)

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product:
        product.delete()
        return redirect('product_list')

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product_id)
    return render(request, 'shop/edit_product.html', {'form': form})


