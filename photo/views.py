from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from .models import Category

from django.shortcuts import render
from .models import Photo, Category

def index(request):
    # Récupération des catégories et sous-catégories
    categories = Category.objects.prefetch_related('subcategories').all()

    # Récupère toutes les photos pour la galerie
    gallery_photos = Photo.objects.all()

    # Récupère uniquement les photos avec une description pour le blog
    blog_photos = Photo.objects.exclude(description__isnull=True).exclude(description__exact='')

    # Context pour le template
    context = {
        'categories': categories,
        'gallery_photos': gallery_photos,
        'blog_photos': blog_photos,
    }

    return render(request, 'index.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Category, SubCategory, Photo

def dashboard(request):
    # Ajouter une catégorie
    if request.method == 'POST' and 'add_category' in request.POST:
        category_name = request.POST.get('category_name')
        if category_name:
            Category.objects.create(name=category_name)

    # Ajouter une sous-catégorie
    if request.method == 'POST' and 'add_subcategory' in request.POST:
        category_id = request.POST.get('category_id')
        subcategory_name = request.POST.get('subcategory_name')
        if category_id and subcategory_name:
            category = get_object_or_404(Category, id=category_id)
            SubCategory.objects.create(category=category, name=subcategory_name)

    # Ajouter une photo
    if request.method == 'POST' and 'add_photo' in request.POST:
        title = request.POST.get('photo_title')
        description = request.POST.get('photo_description')
        subcategory_id = request.POST.get('photo_subcategory_id')
        image = request.FILES.get('photo_image')

        if subcategory_id and image:
            subcategory = get_object_or_404(SubCategory, id=subcategory_id)
            Photo.objects.create(
                title=title,
                description=description,
                image=image,
                subcategory=subcategory
            )

    # Suppression
    if request.method == 'POST' and 'delete_item' in request.POST:
        item_type = request.POST.get('item_type')
        item_id = request.POST.get('item_id')

        if item_type == 'category':
            Category.objects.filter(id=item_id).delete()
        elif item_type == 'subcategory':
            SubCategory.objects.filter(id=item_id).delete()
        elif item_type == 'photo':
            Photo.objects.filter(id=item_id).delete()

    # Récupération des données
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    photos = Photo.objects.all()

    return render(request, 'dashboard.html', {
        'categories': categories,
        'subcategories': subcategories,
        'photos': photos
    })
