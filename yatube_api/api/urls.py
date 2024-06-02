from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from .views import PostList
from django.urls import path, include


router = SimpleRouter()
router.register('posts', PostList)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
]
