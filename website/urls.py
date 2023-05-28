from django.urls import path

from . import views,my_profile
from .includes import Action,search,user_auth,user_account


urlpatterns = [  
    path('account/login',my_profile.Login,name='ClientLogin'),
    path('account/logout',my_profile.logout,name='ClientLogout'),
    path('account/profile',my_profile.profile,name='Profile'),


    path('', views.index, name='website.index'),
    path('contact-us/', views.Contactus, name='Contactus'),
    path('rate/<int:p_id>', views.RateProduct, name='RateProduct'),

    path('product-view/<str:product_name>', views.SingleProductView, name='SingleProductViews'),
    path('product-quick-view/<str:product_name>', views.SingleProductQuickViews, name='SingleProductQuickViews'),

    path('blog-details/<int:id>', views.BlogDetail, name='BlogDetail'),
    # # ishere field 1 =>wishlist |||| 0 => cart ||| 2=> order
    path('wish-list/', views.WishList, name='WishList'),
    path('wish-list/<int:p_id>', views.WishList, name='WishList'),
    path('wish-delete/<int:p_id>/<int:pk>/<str:next>', views.WishListDelete, name='WishListDelete'),
    path('cart/', views.Cart, name='Cart'),
    path('cart/<int:p_id>/<int:c_id>', views.Cart, name='Cart'),
    path('cartQuantityUpdate', views.cartQuantityUpdate, name="cartQuantityUpdate"), #ajax
    path('checkout/', views.CheckOut, name='CheckOut'),
    # # path('checkout/<int:id>', views.CheckOut, name='CheckOut'), #not importent before userlogin

    # #user account
    path('profile', user_account.index, name="UserProfile"),
    path('logout', user_account.Logout, name="Logout"),
    path('profile/<int:order_id>', user_account.index, name="UserProfile"),
    path('setting', user_account.setting, name="UserSetting"),
    path('setting/<int:id>', user_account.setting, name="UserSetting"),
    path('change-password', user_account.ChangePassword, name="ChangePassword"),
    path('change-password/<int:id>', user_account.ChangePassword, name="ChangePassword"),
    path('view-order/<int:p_id>', user_account.ViewOrder, name="ViewOrder"),

    path('search',search.ProductSearch,name="ProductSearch"),
    path('custom-product',views.Custom,name="Custom"),

    path('login', user_auth.Login, name='user_login'),
    path('register', user_auth.SignUp, name='user_register'),
    path('register/<int:id>', user_auth.SignUp, name='user_register'),
    path('user-logout',user_auth.Logout,name='user_logout'),

    
    path('menu/<str:category_name>', views.Category, name='Category'),
    path('<str:menu>', views.Menu, name='Menu'),#127.0.0.1:8000/dhanusha here is only one slug.slug name is dhanusha . which is menu
    path('<str:menu>/<str:submenu>', views.SubMenu, name='Submenu'),#127.0.0.1:8000/dhanusha/janakpur . here is two slug . main slug(menu) is dhanusha. and second slug(submenu) is janakpur.


]