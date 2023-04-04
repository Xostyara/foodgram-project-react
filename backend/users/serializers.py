from djoser.serializers import UserCreateSerializer,UserSerializer
from rest_framework import serializers, validators

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer
from .models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta): 
        model = CustomUser 
        fields = [ 
            'email', 'id', 'username', 'first_name', 'last_name', 'password' 
        ]

class CustomUserSerializer(UserSerializer):
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=CustomUser.objects.all()
        )]
    )

    class Meta:
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        ]
        model = CustomUser


class FollowSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    username = serializers.CharField(
        required=True,
        validators=[validators.UniqueValidator(
            queryset=CustomUser.objects.all()
        )]
    )

    class Meta:
        model = CustomUser
        fields = [
            'email', 'id', 'username', 'first_name', 'last_name',
            'recipes', 'recipes_count', 'is_subscribed'
        ]

    def get_recipes_count(self, data):
        return Recipe.objects.filter(author=data).count()

    def get_recipes(self, data):
        recipes_limit = self.context.get('request').GET.get('recipes_limit')
        recipes = (
            data.recipes.all()[:int(recipes_limit)]
            if recipes_limit else data.recipes
        )
        serializer = serializers.ListSerializer(child=RecipeSerializer())
        return serializer.to_representation(recipes)
