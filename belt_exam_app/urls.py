from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register_user),
    path('login', views.login_user),
    path('success', views.success),
    path('logout', views.logout),
    path('quotes', views.main),
    path('quotes/create', views.create_quote),
    path('users/<int:user_id>', views.user_profile),
    path('quotes/<int:quote_id>', views.render_edit),
    path('quotes/process_edit/<int:quote_id>', views.process_edit),
    path('quotes/<int:quote_id>/delete',views.process_delete),
    path('quotes/<int:quote_id>/favorit', views.favorit ),
    path('quotes/<int:quote_id>/unfavorit', views.unfavorit ),
    #end of urls
]