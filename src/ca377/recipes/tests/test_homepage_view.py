from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, Ingredient, RecipeIngredient

class HomePageViewTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Boiled egg', instructions='Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.')
        Recipe.objects.create(title='Cheese sandwich', instructions='Butter two slices of bread. Place a slice of cheese between them.')
        Recipe.objects.create(title='Baked beans on toast', instructions='Heat the beans. Toast two slices of bread. Put the beans on the toast.')

        Ingredient.objects.create(name='sugar')
        Ingredient.objects.create(name='strawberries')
        Ingredient.objects.create(name='saffron')

    def test_view_recipes_count(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        num_recipes = response.context['num_recipes']
        self.assertEqual(num_recipes, len(Recipe.objects.all()))
        self.assertContains(response, 'Recipes: {:d}'.format(num_recipes))

    def test_view_ingredients_count(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        num_ingredients = response.context['num_ingredients']
        self.assertEqual(num_ingredients, len(Ingredient.objects.all()))
        self.assertContains(response, 'Ingredients: {:d}'.format(num_ingredients))
