from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomPasswordReset

urlpatterns = [path('', views.index, name='home'),
               path('details/<int:pk>/', views.recipe_view, name='recipe_details'),
               path('create/', views.create_view, name='recipe_create'),
               path('edit/<int:pk>/', views.edit_view, name='recipe_edit'),
               path('delete/<int:pk>', views.delete_view, name='recipe_delete'),

               path('notifications/<int:post_pk>/<int:notification_pk>', views.recipe_view_for_notification, name='from_notification'),

               path('login/', views.MyLogin.as_view(), name='login'),
               path('logout/', views.LogoutView.as_view(), name='logout'),
               path('register/', views.register_user, name='register'),

               path('myrecipes/', views.my_recipes, name='my_recipes'),
               path('search/',views.search_results, name='search_bar'),
               path('recipes/<str:type>', views.get_by_type, name='get_by_type'),

               path('profile/', views.user_profile, name='profile'),
               path('profile_edit/', views.edit_profile, name='profile_edit'),

               path('add_comment/<int:pk>', views.add_comment, name='comment_create'),
               path('edit_comment/<int:pk>', views.edit_comment, name='comment_edit'),
               path('delete_comment/<int:pk>', views.delete_comment, name='comment_delete'),

               path('password_reset',
                    auth_views.PasswordResetView.as_view(template_name='Base/password_reset.html',
                                                         form_class=CustomPasswordReset),
                    name='password_reset'),
               path('password_reset_done',
                    auth_views.PasswordResetDoneView.as_view(template_name='Base/password_reset_done.html'),
                    name='password_reset_done'),
               path('reset/<uidb64>/<token>/',
                    auth_views.PasswordResetConfirmView.as_view(template_name='Base/password_reset_confirm.html'),
                    name='password_reset_confirm'),
               path('reset_password_complete',
                    auth_views.PasswordResetCompleteView.as_view(template_name='Base/password_reset_complete.html'),
                    name='password_reset_complete')

               ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)