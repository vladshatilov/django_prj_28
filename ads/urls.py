from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ads import views
from ads.views import CategoryListView, Ad, CategoryDetail, AdDetail, CategoryUpdate, CategoryDelete, AdsUpdate, \
    AdsDelete, AdsImageView, UserListView, UserDetailView, UserDelete, UserUpdate
from main_avito import settings

urlpatterns = [
                  path('', views.get),
                  path('cat/', CategoryListView.as_view()),
                  path('ad/', Ad.as_view()),
                  path('cat/<int:pk>/', CategoryDetail.as_view()),
                  path('cat/<int:pk>/update/', CategoryUpdate.as_view()),
                  path('cat/<int:pk>/delete/', CategoryDelete.as_view()),
                  path('ad/<int:pk>/', AdDetail.as_view()),
                  path('ad/<int:pk>/upload_image/', AdsImageView.as_view()),
                  path('ad/<int:pk>/update/', AdsUpdate.as_view()),
                  path('ad/<int:pk>/delete/', AdsDelete.as_view()),
                  path('user/', UserListView.as_view()),
                  path('user/<int:pk>/', UserDetailView.as_view()),
                  path('user/<int:pk>/update/', UserUpdate.as_view()),
                  path('user/<int:pk>/delete/', UserDelete.as_view()),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


