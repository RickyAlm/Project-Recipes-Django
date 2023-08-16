from django.shortcuts import get_list_or_404, render

from recipes.models import Recipe

# from utils.recipes.factory import make_recipe


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {
        'recipes': recipes,
        # 'recipes': [make_recipe() for _ in range(10)],
    }

    return render(request, 'recipes/pages/home.html', context=context)


def category(request, category_id):
    recipes = get_list_or_404(Recipe.objects.filter(
        category__id=category_id, is_published=True
    ).order_by('-id'))

    context = {
        'recipes': recipes,
        'title': f'{recipes[0].category.name}',  # type:ignore
    }

    return render(request, 'recipes/pages/category.html', context=context)


def recipe(request, id):
    recipe = Recipe.objects.filter(
        pk=id, is_published=True,).order_by('-id').first()

    context = {
        # 'recipe': make_recipe()
        'recipe': recipe,
        'is_detail_page': True,
    }

    return render(request, 'recipes/pages/recipe-view.html', context=context)
