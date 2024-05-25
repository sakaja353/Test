from django.db import models

# Create your models here.
class Recipe(models.Model):
    '''Model representing a recipe.'''

    # CA377 STUDENTS: DO NOT ALTER THIS METHOD
    def get_absolute_url(self):
        '''Returns the URL for a specific Recipe instance.'''
        return reverse('recipedetails', args=[str(self.id)])

class Ingredient(models.Model):
    '''Model representing an ingredient.'''

    # CA377 STUDENTS: DO NOT ALTER THIS METHOD
    def get_absolute_url(self):
        '''Returns the URL for a specific Ingredient instance.'''
        return reverse('ingredientdetails', args=[str(self.id)])

class RecipeIngredient(models.Model):
    '''Model representing a recipe ingredient.'''
    pass
