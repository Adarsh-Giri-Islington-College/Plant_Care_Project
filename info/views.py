from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . models import Plant_Info, Plant_Form
from django.contrib.auth.decorators import user_passes_test
from users.views import is_admin
from favorite.models import Favorite


def display_plant_info(request):
    plant_info = Plant_Info.objects.all()

    page_num = request.GET.get("page")
    paginator = Paginator(plant_info, 60)

    try:
        plant_info = paginator.page(page_num)

    except PageNotAnInteger:
        plant_info = paginator.page(1)
    except EmptyPage:
        plant_info = paginator.page(paginator.num_pages)

    favorite_plants = []
    if request.user.is_authenticated:
        favorite_plants = Favorite.objects.filter(user=request.user).values_list('plant_id', flat=True)

    context = {
        'plant_info': plant_info, 
        'favorite_plants': favorite_plants,
        }
    
    if is_admin(request.user):
        return render(request, 'info/admin_display_plant.html', context)
    else:
        return render(request, 'info/display_plant.html', context)


def plant_detail(request, pk):
    eachPlant = Plant_Info.objects.get(plant_id=pk)
    context = {
        'eachPlant': eachPlant,
    }
    return render(request, 'info/plant_detail.html', context)


@user_passes_test(is_admin)
def add_plant(request):
    if request.method == 'POST':
        form = Plant_Form(request.POST, request.FILES)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.plant_image.name = 'plants_images/' + plant.plant_image.name
            plant.save()
            return redirect('display_plant_info')
    else:
        form = Plant_Form()

    context = {'form': form}
    return render(request, 'info/add_plant.html', context)


@user_passes_test(is_admin)
def update_plant(request, pk):
    plant = get_object_or_404(Plant_Info, plant_id=pk)

    if request.method == 'POST':
        form = Plant_Form(request.POST, request.FILES, instance=plant)
        if form.is_valid():
            plant = form.save(commit=False)
            if 'plant_image' in request.FILES:
                plant.plant_image.name = 'plants_images/' + plant.plant_image.name
            plant.save()
            return redirect('display_plant_info')
    else:  
        form = Plant_Form(instance=plant)
               
    context = {'form': form}
    
    return render(request, 'info/update_plant.html', context)


@user_passes_test(is_admin)
def delete_plant(request, pk):
    eachPlant = Plant_Info.objects.get(plant_id=pk)
    eachPlant.delete()
    return redirect('display_plant_info')


def plant_search(request):
    if request.method == "GET":
        query = request.GET.get('query')
        
        if query:
            plant = Plant_Info.objects.filter(plant_common_name__icontains=query)

            context = {'plant': plant}
            
            if is_admin(request.user):
                return render(request, 'info/admin_display_plant.html', context)
            else:
                return render(request, 'info/display_plant.html', context)
        else:
            return redirect('display_plant_info')  
    else:
        return redirect('display_plant_info')