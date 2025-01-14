from enum import Enum

class RecipeCategory(Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DESSERT = "dessert"
    DRINK = "drink"
    OTHER = "other"

    @classmethod
    def choices(cls):
        return [(category.value, category.name.title()) for category in cls]
