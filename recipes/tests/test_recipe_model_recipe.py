from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe(category_data=self.make_category())
        return super().setUp()

    def make_recipe_no_defaults(self, slug_content='recipe-slug-02'):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Description',
            slug=slug_content,
            preparation_time=10,
            preparation_time_unit='Minutes',
            servings=5,
            servings_unit='Portions',
            preparation_steps='Recipe Preparation Steps',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_slug_name_is_not_repeated(self):
        # Receives the slug from the make_recipe method.
        needed = self.recipe.slug

        with self.assertRaises(ValidationError, msg='The slugs are repeating'):
            self.make_recipe_no_defaults(needed)

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_steps_is_html,
            msg='Recipe preparation_steps_is_html is not False',
        )

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False'
        )

    def test_recipe_string_representation_is_name_field(self):
        needed = 'Testing Representation'

        self.recipe.title = needed
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), needed,

            msg='Recipe string representation must be ' f'"{needed}" but '
            f'"{str(self.recipe.title)}" was received.'
        )
