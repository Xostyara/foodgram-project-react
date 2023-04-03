from .views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer

from .models import CustomUser, Follow
from .serializers import CustomUserSerializer, UserSubscribeSerializer

User = CustomUser()


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action(
        detail=True,
        methods=['GET',],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)
        if user == author:
            return Response(
                {'errors': 'Вы не можете подписаться на самого себя!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Follow.objects.filter(user=user, author=author).exists(): 
            return Response( 
                {'errors': 'Вы уже подписаны'}, 
                status=status.HTTP_400_BAD_REQUEST 
            )

        if request.method == 'GET':
            subscribed = (Follow.objects.filter(
                author=author, user=user).exists()
            )
            if subscribed is True:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            follow = Follow.objects.create(user=user, author=author) 
            serializer = FollowSerializer( 
            follow, context={'request': request} 
            ) 

            return Response(serializer.data, status=status.HTTP_201_CREATED) 

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @action(
        detail=True,
        methods=['DELETE',],
        permission_classes=[IsAuthenticated]
    )
    def unsubscribe(self, request, id):
        user = request.user 
        author = get_object_or_404(CustomUser, id=id) 

        if request.method == 'DELETE':
            Follow.objects.filter(
                user=user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        current_user = request.user
        followed_list = CustomUser.objects.filter(followed__user=current_user)
        paginator = PageNumberPagination()
        paginator.page_size_query_param = 'limit'
        authors = paginator.paginate_queryset(
            followed_list,
            request=request
        )
        serializer = ListSerializer(
            child=UserSubscribeSerializer(),
            context=self.get_serializer_context()
        )
        return paginator.get_paginated_response(
            serializer.to_representation(authors)
        )
