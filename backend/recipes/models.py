from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    name = models.CharField(
        max_length=10,
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега',
        unique=True
    )
    slug = models.SlugField(
        max_length=10,
        unique=True
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название игредиента')
    measurement_unit = models.CharField(max_length=10, verbose_name='Единицы измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):

    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name='Картинка рецепта',
        help_text='Картинка рецепта',
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='recipes',
        verbose_name='Автор рецепта', help_text='Автор рецепта',
    )
    text = models.TextField(
        help_text='Текстовое описание рецепта', verbose_name='recipe text',
    )
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientsRecipe',
        related_name='recipes',
        verbose_name='Список ингредиентов',
        help_text='Список ингредиентов',
    )
    tags = models.ManyToManyField(
        Tag, through='TagsRecipe',
        related_name='recipes',
        help_text='Выберите тэг',
    )
    cooking_time = models.PositiveSmallIntegerField(
        help_text='Время приготовления, мин',
        validators=[MinValueValidator(
            1, 'Время приготовления не может быть меньше 1 мин'
        )],
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ("-pub_date",)

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredients'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=( 
            MinValueValidator( 
                1, message='Минимальное количество ингридиентов 1'
            ),
        ),
        help_text='Количество ингредиента',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe'
            )
        ]


class TagsRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='favorite_recipes'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        blank=False, null=False,
        related_name='favorite_recipes'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )

    class Meta:
        verbose_name = 'Shopping cart'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_recipe_cart'
            )
        ]


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        help_text='Подписчик на автора рецепта'
    )
    author = models.ForeignKey(
        CustomUser, null=True,
        on_delete=models.CASCADE,
        related_name='followed',
        verbose_name='Автор',
        help_text='Автор рецепта'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['author', 'user'],
            name='unique_object'
        )]
        verbose_name = 'Подписка' 
        verbose_name_plural = 'Подписки'
 