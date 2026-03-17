from django.urls import path, include

urlpatterns = [
    path('auth/', include('users.urls')),
    path('', include('ideas.urls')),
    path('', include('votes.urls')),
]
