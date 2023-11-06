from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_shows_no_recipe_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn('No recipes found', response.content.decode('utf-8'))

    def test_recipe_category_view_returns_status_code_is_404(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_home_template_loads_recipes(self):
        # Need a recipe for this test
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        # Check if recipe title exists in template
        self.assertIn('Recipe Title', response_content)
        # Check if one recipe exists
        self.assertEqual(len(response_context_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        """Test recipe if is_published is False and dont show!"""
        # Need a recipe for this test
        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        response_content = response.content.decode('utf-8')

        # Check if recipe title exists in template
        self.assertIn('No recipes found', response_content)

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
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1})
        )
        response_content = response.content.decode('utf-8')

        # Check if recipe title exists in template
        self.assertIn(needed_title, response_content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe if is_published is False and dont show!"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:category', kwargs={
                'category_id': recipe.category.id  # type: ignore
            })
        )

        # Check if recipe title exists in template
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'

        # Need a recipe for this test
        self.make_recipe(title=needed_title)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1})
        )
        response_content = response.content.decode('utf-8')

        # Check if recipe title exists in template
        self.assertIn(needed_title, response_content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        """Test recipe if is_published is False and dont show!"""
        # Need a recipe for this test
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id})  # type: ignore
        )

        # Check if recipe title exists in template
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertEqual(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
