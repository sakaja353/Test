from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from recipes.forms import AddRecipeForm
from recipes.models import Recipe

class AddRecipeFormTest(TestCase):

    def test_addrecipe_form_valid_data(self):
        form = AddRecipeForm(data={
            'title':'Boiled egg',
            'instructions':'Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.'
        })
        self.assertEqual(len(form.errors), 0)

    def test_addrecipe_form_invalid_title_length(self):
        form = AddRecipeForm(data={
            'title':'X'*101,
            'instructions':'Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.'
        })
        self.assertIn('title', form.errors)       
        self.assertEqual(len(form.errors), 1)

    def test_addrecipe_form_missing_title(self):
        form = AddRecipeForm(data={
            'instructions':'Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.'
        })
        self.assertIn('title', form.errors)
        self.assertEqual(len(form.errors), 1)

    def test_addrecipe_form_invalid_instructions_length(self):
        form = AddRecipeForm(data={
            'title':'Boiled egg',
            'instructions':'X'*5001
        })
        self.assertIn('instructions', form.errors)       
        self.assertEqual(len(form.errors), 1)

    def test_addrecipe_form_missing_instructions(self):
        form = AddRecipeForm(data={
            'title':'Boiled egg'
        })
        self.assertIn('instructions', form.errors)       
        self.assertEqual(len(form.errors), 1)

class AddRecipeViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/addrecipe/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('addrecipe'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('addrecipe'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'recipes/addrecipe.html')

    def test_view_redirects_on_recipe_addition(self):
        response = self.client.post('/recipes/addrecipe/', data={
            'title':'Boiled egg',
            'instructions':'Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.'
        })
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(response['Location'], reverse('recipelist'))

    def test_recipe_addition_success(self):
        before = len(Recipe.objects.all())
        response = self.client.post('/recipes/addrecipe/', data={
            'title':'Boiled egg',
            'instructions':'Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.'
        })
        after = len(Recipe.objects.all())
        self.assertEqual(before + 1, after)

    def test_recipe_addition_failure(self):
        before = len(Recipe.objects.all())
        response = self.client.post('/recipes/addrecipe/', data={
            'instructions':'Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.'
        })
        after = len(Recipe.objects.all())
        self.assertEqual(before, after)
