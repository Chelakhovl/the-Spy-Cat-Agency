from django.db import models

class Cats(models.Model):
    """
    Represents a spy cat in the system.
    Attributes:
        name (str): The name of the spy cat.
        years_of_experience (int): The number of years the cat has been a spy.
        breed (str): The breed of the spy cat.
        salary (decimal): The salary of the spy cat.
    """
    name = models.CharField(max_length=100, help_text="The name of the spy cat.")
    years_of_experience = models.IntegerField(help_text="The number of years the cat has been a spy.")
    breed = models.CharField(max_length=100, help_text="The breed of the spy cat.")
    salary = models.DecimalField(max_digits=10, decimal_places=2, help_text="The salary of the spy cat.")

    def __str__(self):
        return self.name
