from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . models import Product, product_form, Review, ReviewForm
from django.db.models import Avg
from users.views import is_admin


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

    if is_admin(request.user):
        return render(request, 'products/admin_display_product.html', context)
    else:
        return render(request, 'products/display_product.html', context)


def product_detail(request, pk):
    eachProduct = Product.objects.get(product_id=pk)

    has_reviewed = True

    if Review.objects.filter(product=eachProduct, user=request.user).exists():
        has_reviewed = False

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            user = request.user  
            comment = form.cleaned_data['comment']
            rating = form.cleaned_data['rating']
            review = Review.objects.create(user=user, product=eachProduct, comment=comment, rating=rating)
            return redirect('product_detail', pk=pk) 
    else:
        form = ReviewForm()
    
    ordered = False
    if request.user.is_authenticated:
        ordered = request.user.order_set.filter(products=eachProduct, payment__payment_status='done').exists()

    reviews = Review.objects.filter(product=eachProduct)
    if reviews.exists():
        overall_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    else:
        overall_rating = None

    rating_range = range(5)

    context = {
        'eachProduct': eachProduct,
        'form': form, 
        'product': eachProduct,
        'overall_rating': overall_rating,
        'ordered': ordered,
        'rating_range': rating_range, 
        'has_reviewed': has_reviewed,
    }

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
            products = Product.objects.filter(product_name__icontains=query) | Product.objects.filter(product_id__icontains=query)

            context = {'products': products}
            
            if is_admin(request.user):
                return render(request, 'products/admin_display_product.html', context)
            else:
                return render(request, 'products/display_product.html', context)
        else:
            return redirect('display_products')  
    else:
        return redirect('display_products')
          

def filter_products_by_price(products, min_price=None, max_price=None):
    if min_price is not None:
        products = products.filter(product_price__gte=min_price)
    if max_price is not None:
        products = products.filter(product_price__lte=max_price)
    return products


def filter_by_price(request):
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    
    if min_price or max_price:
        products = filter_products_by_price(products, min_price=min_price, max_price=max_price)

    context = {
        'products': products,
    }

    return render(request, 'products/display_product.html', context)