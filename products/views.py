from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . models import ProductCategory, ProductCategoryForm, Product, product_form, Review, ReviewForm
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

    form = product_form()
    max_product_price = Product.objects.aggregate(Max('product_price'))['product_price__max']
    categories = ProductCategory.objects.all().distinct()

    context = {
        'products': products,
        'form': form,
        'max_product_price': max_product_price,
        'categories': categories,
        }

    if is_admin(request.user):
        return render(request, 'products/admin_display_product.html', context)
    else:
        return render(request, 'products/display_product.html', context)


def product_detail(request, pk):
    eachProduct = Product.objects.get(product_id=pk)
    has_reviewed = True

    if request.user.is_authenticated:
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


def display_categories(request):
    categories = ProductCategory.objects.all()
    return render(request, 'products/admin_display_category.html', {'categories': categories})


@user_passes_test(is_admin)
def add_category(request):
    if request.method == 'POST':
        form = ProductCategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            if ProductCategory.objects.filter(category_name=category_name).exists():
                error_message = 'Category with this name already exists.'
                context = {
                    'error_message': error_message, 
                } 
                return render(request, 'products/add_category.html', context)
            else:
                category = form.save(commit=False)
                category.save()
                return redirect('display_categories')
    else:
        form = ProductCategoryForm()
    
    return render(request, 'products/add_category.html', {'form': form})


@user_passes_test(is_admin)
def delete_category(request, pk):
    category = ProductCategory.objects.get(category_id=pk)
    category.delete()
    return redirect('display_categories')


@user_passes_test(is_admin)
def add_product(request):
    if request.method == 'POST':
        form = product_form(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.product_for = ','.join(form.cleaned_data.get('product_for', []))
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


def filters(request):
    form = product_form()
    
    max_product_price = Product.objects.aggregate(Max('product_price'))['product_price__max']
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    selected_product_for = request.GET.getlist('product_for')
    selected_category = request.GET.getlist('product_category')

    products = Product.objects.all()
    categories = ProductCategory.objects.all().distinct()
    
    if min_price or max_price:
        products = filter_products_by_price(products, min_price=min_price, max_price=max_price)
    
    if selected_product_for:
        filtered_products = []
        for product_for in selected_product_for:
            filtered_products.extend(products.filter(product_for__contains=product_for.strip()))
        products = filtered_products

    try:
        if selected_category and all(selected_category):
            filtered_categories = []
            for product_category_id in selected_category:
                filtered_categories.extend(products.filter(product_category_id=product_category_id.strip()))
            products = filtered_categories
    except Exception as e:
        selected_category = []


    context = {
        'products': products,
        'categories': categories,
        'form': form,
        'min_price': min_price,
        'max_price': max_price,
        'selected_product_for': selected_product_for,
        'max_product_price': max_product_price,
        'selected_category': selected_category
    }

    return render(request, 'products/display_product.html', context)