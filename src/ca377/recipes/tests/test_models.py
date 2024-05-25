from django.test import TestCase
from decimal import Decimal
from recipes.models import Recipe, Ingredient, RecipeIngredient

class RecipeTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Boiled egg', instructions='Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.')
        Recipe.objects.create(title='Cheese sandwich', instructions='Butter two slices of bread. Place a slice of cheese between them.')
        Recipe.objects.create(title='Baked beans on toast', instructions='Heat the beans. Toast two slices of bread. Put the beans on the toast.')

    def test_model_title_field(self):
        recipe = Recipe.objects.get(id=1)
        field = recipe._meta.get_field('title')
        field_label = field.verbose_name
        self.assertEqual(field_label, 'title')
        field_type = field.get_internal_type()
        self.assertEqual(field_type, 'CharField')
        max_length = field.max_length
        self.assertEqual(max_length, 100)

    def test_model_instructions_field(self):
        recipe = Recipe.objects.get(id=1)
        field = recipe._meta.get_field('instructions')
        field_label = field.verbose_name
        self.assertEqual(field_label, 'instructions')
        field_type = field.get_internal_type()
        self.assertEqual(field_type, 'TextField')
        max_length = field.max_length
        self.assertEqual(max_length, 5000)

    def test_model_object_name_is_title(self):
        recipe = Recipe.objects.get(id=1)
        expected_object_name = f'{recipe.title}'
        self.assertEqual(str(recipe), expected_object_name)

    def test_model_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), '/recipes/recipedetails/1/')
        recipe = Recipe.objects.get(id=2)
        self.assertEqual(recipe.get_absolute_url(), '/recipes/recipedetails/2/')
        recipe = Recipe.objects.get(id=3)
        self.assertEqual(recipe.get_absolute_url(), '/recipes/recipedetails/3/')

class IngredientTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Ingredient.objects.create(name='sugar')
        Ingredient.objects.create(name='strawberries')
        Ingredient.objects.create(name='saffron')

    def test_model_name_field(self):
        ingredient = Ingredient.objects.get(id=1)
        field = ingredient._meta.get_field('name')
        field_label = field.verbose_name
        self.assertEqual(field_label, 'name')
        field_type = field.get_internal_type()
        self.assertEqual(field_type, 'CharField')
        max_length = field.max_length
        self.assertEqual(max_length, 100)

    def test_model_object_name_is_name(self):
        ingredient = Ingredient.objects.get(id=1)
        expected_object_name = f'{ingredient.name}'
        self.assertEqual(str(ingredient), expected_object_name)

class RecipeIngredientTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Cheese sandwich', instructions='Butter two slices of bread. Place a slice of cheese between them.')
        Ingredient.objects.create(name='cheese')
        r = Recipe.objects.get(id=1)
        i = Ingredient.objects.get(id=1)
        RecipeIngredient.objects.create(
            recipe=r, ingredient=i, unit='g', number=30, calories=100)

    def test_model_recipe_field(self):
        recipeingredient = RecipeIngredient.objects.get(id=1)
        field = recipeingredient._meta.get_field('recipe')
        field_label = field.verbose_name
        self.assertEqual(field_label, 'recipe')
        field_type = field.get_internal_type()
        self.assertEqual(field_type, 'ForeignKey')

    def test_model_ingredient_field(self):
        recipeingredient = RecipeIngredient.objects.get(id=1)
        field = recipeingredient._meta.get_field('ingredient')
        field_label = field.verbose_name
        self.assertEqual(field_label, 'ingredient')
        field_type = field.get_internal_type()
        self.assertEqual(field_type, 'ForeignKey')

    def test_model_unit_field(self):
        recipeingredient = RecipeIngredient.objects.get(id=1)
        field = recipeingredient._meta.get_field('unit')
        field_label = field.verbose_name
        self.assertEqual(field_label, 'unit')
        field_type = field.get_internal_type()
        self.assertEqual(field_type, 'TextField')
        max_length = field.max_length
        self.assertEqual(max_length, 5)

    def test_model_number_field(self):
        recipeingredient = RecipeIngredient.objects.get(id=1)
        field = recipeingredient._meta.get_field('number')
        field_label = field.verbose_name
        self.assertEqual(field_label, 'number')
        field_type = field.get_internal_type()
        self.assertEqual(field_type, 'PositiveSmallIntegerField')

    def test_model_calories_field(self):
        recipeingredient = RecipeIngredient.objects.get(id=1)
        field = recipeingredient._meta.get_field('calories')
        field_label = field.verbose_name
        self.assertEqual(field_label, 'calories')
        field_type = field.get_internal_type()
        self.assertEqual(field_type, 'PositiveIntegerField')
