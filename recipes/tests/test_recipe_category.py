from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 2}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'

        # Need a recipe for this test
        self.make_recipe(
            title=needed_title, category_data=self.make_category()
        )

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        response_content = response.content.decode('utf-8')

        # Check if recipe title exists in template
        self.assertIn(needed_title, response_content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe if is_published is False and dont show!"""
        # Need a recipe for this test
        recipe = self.make_recipe(
            is_published=False, category_data=self.make_category()
        )

        response = self.client.get(
            reverse('recipes:category', kwargs={
                'category_id': recipe.category.id  # type: ignore
            })
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_is_paginated(self):
        category = self.make_category()
        for i in range(8):
            kwargs = {
                'slug': f'r{i}', 'author_data': {'username': f'u{i}'},
            }
            self.make_recipe(category_data=category, **kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(
                reverse('recipes:category', kwargs={
                    'category_id': 1
                    })
                )
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
