from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . models import Product
from . models import product_form
from users.models import User


def is_admin(user):
    return user.is_authenticated and user.user_role == User.ADMIN


def display_products(request):
    products = Product.objects.all()

    page_num = request.GET.get("page")
    paginator = Paginator(products, 60)

    try:
        products = paginator.page(page_num)

    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {'products': products}

    return render(request, 'products/display_product.html', context)


def product_detail(request, pk):
    eachProduct = Product.objects.get(product_id=pk)

    context = {'eachProduct': eachProduct}

    return render(request, 'products/product_detail.html', context)


@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = product_form(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.product_image.name = 'products_images/' + product.product_image.name
            product.save()
            return redirect('display_products')
    else:
        form = product_form()

    context = {'form': form}
    return render(request, 'products/add_product.html', context)


@user_passes_test(is_admin)
def update_product(request, pk):
    eachProduct = Product.objects.get(product_id=pk)

    if request.method == 'POST':
        form = product_form(request.POST, request.FILES, instance=eachProduct)
        if form.is_valid():
            product = form.save(commit=False)
            if 'product_image' in request.FILES:
                product.product_image.name = 'products_images/' + product.product_image.name
            product.product_for = ','.join(form.cleaned_data.get('product_for', []))
            product.save()
            return redirect('display_products')
    else:  
        initial_product_for = eachProduct.product_for.split(',') if eachProduct.product_for else []
        form = product_form(instance=eachProduct, initial={'product_for': initial_product_for})
               
    context = {'form': form}
    
    return render(request, 'products/update_product.html', context)


@user_passes_test(is_admin)
def delete_product(request, pk):
    eachProduct = Product.objects.get(product_id=pk)
    eachProduct.delete()
    return redirect('display_products')


def search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        
        if query:
            products = Product.objects.filter(product_name__icontains=query)

            context = {'products': products}
            
            return render(request, 'search.html', context)
        else:
            print("No Products")
            return render(request, 'search.html', {})



        