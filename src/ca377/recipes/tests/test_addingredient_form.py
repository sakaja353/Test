from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from recipes.models import Ingredient
from recipes.forms import AddIngredientForm

class AddIngredientFormTest(TestCase):

    def test_addingredient_form_valid_data(self):
        form = AddIngredientForm(data={
            'name':'sugar'
        })
        self.assertEqual(len(form.errors), 0)

    def test_addingredient_form_invalid_title_length(self):
        form = AddIngredientForm(data={
            'name':'X'*101
        })
        self.assertIn('name', form.errors)       
        self.assertEqual(len(form.errors), 1)

    def test_addingredient_form_missing_name(self):
        form = AddIngredientForm(data={})
        self.assertIn('name', form.errors)       
        self.assertEqual(len(form.errors), 1)

class AddIngredientViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/addingredient/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('addingredient'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('addingredient'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'recipes/addingredient.html')

    def test_view_redirects_on_ingredient_addition(self):
        response = self.client.post('/recipes/addingredient/', data={
            'name':'sugar'
        })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response['Location'], reverse('ingredientlist'))

    def test_ingredient_addition_success(self):
        before = len(Ingredient.objects.all())
        response = self.client.post('/recipes/addingredient/', data={
            'name':'sugar'
        })
        after = len(Ingredient.objects.all())
        self.assertEqual(before + 1, after)

    def test_ingredient_addition_failure(self):
        before = len(Ingredient.objects.all())
        response = self.client.post('/recipes/addingredient/', data={})
        after = len(Ingredient.objects.all())
        self.assertEqual(before, after)
