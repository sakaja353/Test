from django.test import TestCase
from django.urls import reverse
from recipes.models import Ingredient

class IngredientEmptyListViewTest(TestCase):

    def test_view_displays_none_message(self):
        response = self.client.get(reverse('ingredientlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No ingredients yet')

class IngredientListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Ingredient.objects.create(name='sugar')
        Ingredient.objects.create(name='strawberries')
        Ingredient.objects.create(name='saffron')
        cls.alpha_ordering = [3, 2, 1]

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/ingredientlist/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('ingredientlist'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('ingredientlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/ingredientlist.html')

    def test_view_displays_all(self):
        response = self.client.get(reverse('ingredientlist'))
        self.assertEqual(response.status_code, 200)
        all_ingredients = Ingredient.objects.all()
        for r in all_ingredients:
            self.assertContains(response, str(r))

    def test_view_receives_all(self):
        response = self.client.get(reverse('ingredientlist'))
        self.assertEqual(response.status_code, 200)
        ctx_ingredients = response.context['ingredients']
        all_ingredients = Ingredient.objects.all()
        self.assertEqual(len(all_ingredients), len(ctx_ingredients))
        for r in all_ingredients:
            self.assertIn(r, ctx_ingredients)

    def test_view_lists_alphabetical(self):
        response = self.client.get(reverse('ingredientlist'))
        self.assertEqual(response.status_code, 200)
        ingredients = response.context['ingredients']
        for r, i in zip(ingredients, self.alpha_ordering):
            self.assertEqual(r, Ingredient.objects.get(id=i))
