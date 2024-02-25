from . import views
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Описание для API части",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.new_all, name='new_all'),
    path('new_page/<int:pk>/', views.new_page, name='new_page'),
    path('new_find/<str:tag>/', views.new_find, name='new_find'),
    path('statistic_page/', views.statistic_page, name='statistic_page'),
    path('submit_like/', views.submit_like, name='submit_like'),
    path('submit_dislike/', views.submit_dislike, name='submit_dislike'),
    path('api/get_new/<int:pk>/', views.get_new, name='get_new'),
    path('api/create_new/', views.create_new, name='create_new'),
    path('api/delete_new/<int:pk>', views.delete_new, name='delete_new'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]