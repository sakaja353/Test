from django.test import TestCase
from recipes.models import Recipe, Ingredient, RecipeIngredient

class RecipeDetailsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Cheese sandwich', instructions='Butter two slices of bread. Place a slice of cheese between them.')
        Ingredient.objects.create(name='cheese')
        r = Recipe.objects.get(id=1)
        i = Ingredient.objects.get(id=1)
        RecipeIngredient.objects.create(
            recipe=r, ingredient=i, unit='g', number=30, calories=100)

    def test_view_uses_correct_template(self):
        recipe = Recipe.objects.get(id=1)
        url = recipe.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipedetails.html')

    def test_view_displays_all_details(self):
        recipe = Recipe.objects.get(id=1)
        url = recipe.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '30 g cheese (100 calories)')
        self.assertContains(response, 'Butter two slices of bread')
        self.assertContains(response, 'Place a slice of cheese between them')
