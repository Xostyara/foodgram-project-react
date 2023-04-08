import traceback

from django.db import IntegrityError
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from users.models import CustomUser

from .models import (FavoriteRecipe, Ingredient, IngredientsRecipe, Recipe,
                     ShoppingCart, Tag, TagsRecipe)


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField( 
        source='ingredient.id' 
    ) 

    name = serializers.ReadOnlyField( 
        source='ingredient.name' 
    ) 

    measurement_unit = serializers.ReadOnlyField( 
        source='ingredient.measurement_unit' 
    )  

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    slug = serializers.SlugField()

    class Meta:
        model = Tag
        fields = '__all__'
        lookup_field = 'slug'


class RecipeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        required=True,
    )
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientsRecipeSerializer(
        many=True, source='recipe_ingredients'
    )
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    text = serializers.CharField()
    cooking_time = serializers.IntegerField(max_value=32767, min_value=1)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        exclude = ('pub_date',)

    # def get_status_func(self, data):
    #     request = self.context.get('request')
    #     if request is None or request.user.is_anonymous:
    #         return False
    #     try:
    #         user = self.context.get('request').user
    #     except:
    #         user = self.context.get('user')
    #     callname_function = format(traceback.extract_stack()[-2][2])
    #     if callname_function == 'get_is_favorited':
    #         init_queryset = FavoriteRecipe.objects.filter(recipe=data.id, user=user)
    #     elif callname_function == 'get_is_in_shopping_cart':
    #         init_queryset = ShoppingCart.objects.filter(recipe=data, user=user)
    #     if init_queryset.exists():
    #         return True
    #     return False

    def get_is_favorited(self, obj): 
        user = self.context.get('request').user 
        if user.is_anonymous: 
            return False 

        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists() 

    def get_is_in_shopping_cart(self, obj): 
        user = self.context.get('request').user 
        if user.is_anonymous: 
            return False 

        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()  
    
    def create_ingredients(self, ingredients, recipe): 
        obj = [ 
            IngredientsRecipe( 
                recipe=recipe, 
                ingredient_id=ingredient.get('id'), 
                amount=ingredient.get('amount') 
            ) 
            for ingredient in ingredients 
        ] 

        IngredientsRecipe.objects.bulk_create(obj)

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(image=image, **validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        instance.tags.clear()
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(recipe=instance,
                                        ingredients=ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        response = super(RecipeSerializer, self).to_representation(instance)
        if instance.image:
            response['image'] = instance.image.url
        return response


class FavoritedSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True, source='recipe.id',
    )
    cooking_time = serializers.CharField(
        read_only=True, source='recipe.cooking_time',
    )
    image = serializers.CharField(
        read_only=True, source='recipe.image',
    )
    name = serializers.CharField(
        read_only=True, source='recipe.name',
    )

    def validate(self, data):
        recipe = data['recipe']
        user = data['user']
        if user == recipe.author:
            raise serializers.ValidationError('You are the author!')
        if (FavoriteRecipe.objects.filter(recipe=recipe, user=user).exists()):
            raise serializers.ValidationError('You have already subscribed!')
        return data

    def create(self, validated_data):
        favorite = FavoriteRecipe.objects.create(**validated_data)
        favorite.save()
        return favorite

    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'cooking_time', 'name', 'image')


class ShoppingCartSerializer(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
        source='recipe.id',
    )
    cooking_time = serializers.CharField(
        read_only=True,
        source='recipe.cooking_time',
    )
    image = serializers.CharField(
        read_only=True,
        source='recipe.image',
    )
    name = serializers.CharField(
        read_only=True,
        source='recipe.name',
    )

    class Meta:
        model = ShoppingCart
        fields = ('id', 'cooking_time', 'name', 'image')
