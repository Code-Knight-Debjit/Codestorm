from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('shops_detail/', views.shops_detail, name='shops_detail'),
    path('shop/', views.shop, name='shop'),
    path('add_product/', views.shop, name='add_product'),
    path('upload_csv/', views.upload_review_csv, name='upload_review_csv'),
    path('report/', views.upload_review_csv, name='report'),

]
