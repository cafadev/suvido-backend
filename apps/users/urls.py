from rest_framework.routers import SimpleRouter

from django.urls import path

from . import apis

router = SimpleRouter()
router.register('', apis.UserAPI)

urlpatterns = router.urls + [
    path('me/', apis.UserAPI.as_view({'get': 'retrieve'})),
]

