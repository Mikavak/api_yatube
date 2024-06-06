from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter

from .views import GroupList, LightCommentViewSet, PostList

router_v1 = SimpleRouter()
router_v1.register('posts', PostList)
router_v1.register('groups', GroupList)
router_v1.register(
    r'posts/(?P<post_id>[\d]+)/comments', LightCommentViewSet,
    basename='comments')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('api-token-auth/', views.obtain_auth_token)
]
