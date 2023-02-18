from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from apps.users import models


class UserAPI(ModelViewSet):

    serializer_class = UserSerializer
    queryset = models.User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        if pk == 'me':
            if not request.user.is_anonymous:
                user = models.User.objects.get(pk=request.user.id)
                return Response(self.serializer_class(user, context={'request': request}).data)
            else:
                return Response(
                    {'message': 'unauthenticated_user'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        return super().retrieve(request, *args, **kwargs)

