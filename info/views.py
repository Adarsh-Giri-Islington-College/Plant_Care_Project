from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from . models import Plant_Info, Plant_Form


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

    context = {'plant_info': plant_info}

    return render(request, 'info/display_plant.html', context)


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


def delete_plant(request, pk):
    eachProduct = Plant_Info.objects.get(plant_id=pk)
    eachProduct.delete()
    return redirect('display_plant_info')