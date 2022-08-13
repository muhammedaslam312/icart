from multiprocessing.spawn import import_main_path
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout, name='logout'),
    path('register/',views.user_register,name='signup'),
    
    
    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetpassword_validate/<uidb64>/<token>', views.resetpassword_validate, name="resetpassword_validate"),
    path('resetPassword/', views.resetPassword, name="resetPassword"),

    #dashboard
    path('user_profile/',views.user_profile,name='user_profile'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_track/<int:order_id>/', views.order_track, name='order_track'),
]
