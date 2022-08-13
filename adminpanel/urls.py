from . import views
from django.urls import path


urlpatterns = [
   path('',views.adminpanel,name='adminpanel'),
   path('admin_login/',views.admin_login,name="admin_login"),
   
   path('user_accounts_table/<int:id>/',views.user_accounts_table,name="user_accounts_table"),
  
   path('ban_user/<int:id>/',views.ban_user,name="ban_user"),
   path('unban_user/<int:id>/',views.unban_user,name='unban_user'),

   path('cart_table/<int:id>/',views.cart_table,name="cart_table"),
   

   path('category_table/<int:id>/',views.category_table,name="category_table"),
   path('add_category/',views.add_category,name="add_category"),
   path('edit_category/<int:id>/',views.edit_category,name="edit_category"),
   path('delete_category/<int:id>/',views.delete_category,name="delete_category"),

   path('store_table/<int:id>/',views.store_table,name="store_table"),
   path('add_product/',views.add_product,name="add_product"),
   path('add_variation/',views.add_variation,name="add_variation"),
   path('edit_variation/<int:id>/',views.edit_variation,name='edit_variation'),
   path('delete_variaton/<int:id>/',views.delete_variaton,name="delete_variaton"),
   path('edit_product/<int:id>/',views.edit_product,name="edit_product"),
   path('delete_product/<int:id>/',views.delete_product,name="delete_product"),

   path('order_table/<int:id>/',views.order_table,name="order_table"),
   path('order_accepted/<int:order_id>',views.order_accepted,name="order_accepted"),
   path('order_completed/<int:order_id>',views.order_completed,name="order_completed"),
   path('order_cancelled/<int:order_id>',views.order_cancelled,name="order_cancelled"),

    path('psearch/',views.psearch,name='psearch'),


   
   
]
