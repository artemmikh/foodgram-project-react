from rest_framework import mixins, viewsets


class CreateListUpdateDestroy(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """Класс представления, обеспечивающий создание, просмотр списка,
    обновление и удаление объектов."""

    pass
