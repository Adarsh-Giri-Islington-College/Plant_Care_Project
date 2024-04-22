from django.shortcuts import render, redirect, get_object_or_404
from . models import Favorite
from info.models import Plant_Info
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required
def display_favorite(request):
    if request.user.is_authenticated:
        favorite_plant = Favorite.objects.filter(user=request.user)

        paginator = Paginator(favorite_plant, 60)  
        page_number = request.GET.get('page')
        try:
            favorite_plant = paginator.page(page_number)
        except PageNotAnInteger:
            favorite_plant = paginator.page(1)
        except EmptyPage:
            favorite_plant = paginator.page(paginator.num_pages)

        context = {
            'favorite_plant': favorite_plant
        }

        return render(request, 'favorite/favorite.html', context)
    else:
        return redirect('login')


@login_required
def add_favorite(request, pk):
    plant = get_object_or_404(Plant_Info, pk=pk)
    
    favorite_plant = Favorite.objects.filter(user=request.user)
    existing_favorite = Favorite.objects.filter(user=request.user, plant=plant).exists()
    if not existing_favorite:
        Favorite.objects.create(user=request.user, plant=plant)
        return redirect('display_plant_info')

    return redirect('display_plant_info')
    

def delete_favorite(request, pk):
    favorite = get_object_or_404(Favorite, favorite_id=pk)
    
    if favorite.user == request.user:
        favorite.delete()
    
    return redirect('display_favorite')