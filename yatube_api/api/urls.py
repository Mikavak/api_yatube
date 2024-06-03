from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from .views import PostList, GroupList, comments, one_comment
from django.urls import path, include


router = SimpleRouter()
router.register('posts', PostList)
router.register('groups', GroupList)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('posts/<int:post_id>/comments/', comments),
    path('posts/<int:post_id>/comments/<int:comment_id>/', one_comment)
]
