from .models import Cat


def update_cat_salary(cat: Cat, new_salary: float) -> Cat:
    """
    Updates the salary of a spy cat and saves it to the database.
    """
    cat.salary = new_salary
    cat.save()
    return cat
