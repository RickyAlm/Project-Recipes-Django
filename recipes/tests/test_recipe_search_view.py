from django.urls import resolve, reverse
from unittest.mock import patch
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertEqual(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        # Need a search field
        response = self.client.get(reverse('recipes:search') + '?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=<Test>'
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Test&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'},
            category_data=self.make_category()
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'},
            category_data=self.make_category()
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_is_paginated(self):
        for i in range(8):
            kwargs = {
                'slug': f'r{i}', 'author_data': {'username': f'u{i}'},
                'title': 'test search'
            }
            self.make_recipe(category_data=self.make_category(), **kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            search_url = reverse('recipes:search')
            response = self.client.get(f'{search_url}?q=test')
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
