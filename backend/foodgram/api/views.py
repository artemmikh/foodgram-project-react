from rest_framework import viewsets
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from djoser import views as djoser_views

from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    CustomUserSerializer
)
from food.models import (
    Tag,
    Ingredient,
    User
)


class CustomUserViewSet(DjoserUserViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CustomUserSerializer
    queryset = User.objects.all()


# class CustomUserViewSetMe(djoser_views.UserViewSet):
#     serializer_class = CustomUserSerializer
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data[0] if serializer.data else None)

class CustomUserViewSetMe(DjoserUserViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserSerializer

    @action(detail=False, methods=['get'])
    def me(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    """ViewSet для сериализатора CategorySerializer."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
