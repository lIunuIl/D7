from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, ProfileUserUpdate


urlpatterns = [

    path('', PostList.as_view(), name='news'),
    path('<int:pk>', PostDetail.as_view(), name='news_detail'),
    path('create/', PostCreate.as_view(), name='news_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('search/', PostSearch.as_view(), name='news_search'),
    path('profile/<int:pk>/update', ProfileUserUpdate.as_view(), name='profile_user_update'),
]