from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from recipes.forms import AddRecipeIngredientForm
from recipes.models import Recipe, Ingredient, RecipeIngredient

class AddRecipeIngredientFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Cheese sandwich', instructions='Butter two slices of bread. Place a slice of cheese between them.')
        Ingredient.objects.create(name='cheese')
        r = Recipe.objects.get(id=1)
        i = Ingredient.objects.get(id=1)
        RecipeIngredient.objects.create(
            recipe=r, ingredient=i, unit='g', number=30, calories=100)

    def test_addrecipeingredient_form_valid_data(self):
        r = Recipe.objects.get(id=1)
        i = Ingredient.objects.get(id=1)
        form = AddRecipeIngredientForm(data={
            'recipe':r,
            'ingredient':i,
            'unit':'g',
            'number':30,
            'calories':100
        })
        self.assertEqual(len(form.errors), 0)

    def test_addrecipeingredient_form_missing_recipe(self):
        r = Recipe.objects.get(id=1)
        i = Ingredient.objects.get(id=1)
        form = AddRecipeIngredientForm(data={
            'ingredient':i,
            'unit':'g',
            'number':30,
            'calories':100
        })
        self.assertIn('recipe', form.errors)       
        self.assertEqual(len(form.errors), 1)

    def test_addrecipeingredient_form_invalid_number(self):
        r = Recipe.objects.get(id=1)
        i = Ingredient.objects.get(id=1)
        form = AddRecipeIngredientForm(data={
            'recipe':r,
            'ingredient':i,
            'unit':'g',
            'number':'cat',
            'calories':100
        })
        self.assertIn('number', form.errors)       
        self.assertEqual(len(form.errors), 1)

    def test_addrecipeingredient_form_invalid_calories(self):
        r = Recipe.objects.get(id=1)
        i = Ingredient.objects.get(id=1)
        form = AddRecipeIngredientForm(data={
            'recipe':r,
            'ingredient':i,
            'unit':'g',
            'number':30,
            'calories':'cat'
        })
        self.assertIn('calories', form.errors)       
        self.assertEqual(len(form.errors), 1)

class AddRecipeIngredientViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Cheese sandwich', instructions='Butter two slices of bread. Place a slice of cheese between them.')
        Ingredient.objects.create(name='cheese')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/addrecipeingredient/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('addrecipeingredient'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('addrecipeingredient'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'recipes/addrecipeingredient.html')

    def test_view_redirects_on_recipeingredient_addition(self):
        response = self.client.post('/recipes/addrecipeingredient/', data={
            'recipe':1,
            'ingredient':1,
            'unit':'g',
            'number':30,
            'calories':100
        })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response['Location'], reverse('recipelist'))

    def test_recipeingredient_addition_success(self):
        before = len(RecipeIngredient.objects.all())
        response = self.client.post('/recipes/addrecipeingredient/', data={
            'recipe':1,
            'ingredient':1,
            'unit':'g',
            'number':30,
            'calories':100
        })
        after = len(RecipeIngredient.objects.all())
        self.assertEqual(before + 1, after)

    def test_recipeingredient_addition_failure(self):
        before = len(RecipeIngredient.objects.all())
        response = self.client.post('/recipes/addrecipeingredient/', data={
            'recipe':1,
            'ingredient':1,
            'unit':'g',
            'number':30,
            'calories':'cat'
        })
        after = len(RecipeIngredient.objects.all())
        self.assertEqual(before, after)
