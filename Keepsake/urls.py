from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.Homepage, name='Homepage'),

    path('Login/', views.Login, name='Login'),
    path('Login/LoginSubmit/', views.LoginSubmit, name='LoginSubmit'),
    path('Login/Register/', views.Register, name='Register'),
    path('Login/Logout/', views.Logout, name='Logout'),
    path('Login/UpdateProfile/', views.UpdateProfile, name='UpdateProfile'),
    path('Login/DeleteProfile/', views.DeleteProfile, name='DeleteProfile'),


    path('Catalogue/',views.Catalogue, name='Catalogue'),
    path('Catalogue/Birthday/',views.Birthday, name = 'Birthday'),
    path('Catalogue/Anniversary/',views.Anniversary, name = 'Anniversary'),
    path('Catalogue/Graduation/',views.Graduation, name = 'Graduation'),

    path('AllOrder/',views.AllOrder, name = 'AllOrder'),
    path('Update_Order/<str:Product_Name>/', views.Update_Order, name='Update_Order'),
    path('Delete_Order/<int:order_id>/', views.Delete_Order, name='Delete_Order'),

    path('reviews/', views.review_list, name='review_list'),
    path('reviews/create/', views.create_review, name='create_review'),
    path('reviews/update/<int:review_id>/', views.update_review, name='update_review'),
    path('reviews/delete/<int:review_id>/', views.delete_review, name='delete_review'),

]