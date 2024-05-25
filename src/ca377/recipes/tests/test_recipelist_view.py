from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe

class RecipeEmptyListViewTest(TestCase):

    def test_view_displays_none_message(self):
        response = self.client.get(reverse('recipelist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes yet')

class RecipeListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(title='Boiled egg', instructions='Put the egg in a saucepan of water. Bring to the boil. Simmer for 3-4 m.')
        Recipe.objects.create(title='Cheese sandwich', instructions='Butter two slices of bread. Place a slice of cheese between them.')
        Recipe.objects.create(title='Baked beans on toast', instructions='Heat the beans. Toast two slices of bread. Put the beans on the toast.')
        cls.alpha_ordering = [3, 1, 2]

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/recipelist/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('recipelist'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recipelist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipelist.html')

    def test_view_displays_all(self):
        response = self.client.get(reverse('recipelist'))
        self.assertEqual(response.status_code, 200)
        all_recipes = Recipe.objects.all()
        for r in all_recipes:
            self.assertContains(response, str(r))

    def test_view_receives_all(self):
        response = self.client.get(reverse('recipelist'))
        self.assertEqual(response.status_code, 200)
        ctx_recipes = response.context['recipes']
        all_recipes = Recipe.objects.all()
        self.assertEqual(len(all_recipes), len(ctx_recipes))
        for r in all_recipes:
            self.assertIn(r, ctx_recipes)

    def test_view_lists_alphabetical(self):
        response = self.client.get(reverse('recipelist'))
        self.assertEqual(response.status_code, 200)
        recipes = response.context['recipes']
        for r, i in zip(recipes, self.alpha_ordering):
            self.assertEqual(r, Recipe.objects.get(id=i))
