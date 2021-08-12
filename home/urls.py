from django.contrib import admin
from django.urls import path
from . import views

app_name= 'home'

urlpatterns = [
    path('',views.HomePageView,name="home"),
    path('subscriptions/',views.SubscriptionListView.as_view(),name="subscriptions"),
    path('subscribers/',views.SubscribersListView.as_view(),name="subscribers"),
    path('users/',views.UsersListView.as_view(),name="users"),
    path('user/<int:id>/',views.UserDetailView,name="user"),
    path('unsubscribe/<int:id>/',views.unsubscribe,name="unsubscribe"),
    path('subscribe/<int:id1>/',views.subscribe,name="subscribe"),
    path('post/<int:id>/',views.PostDetailView,name="post"),
    path('post/create/',views.PostCreateView.as_view(),name="postcreateview"),
    path('post/create/success/',views.createpost,name="createpost"),
    path('post/delete/<int:pk>/', views.PostDelete.as_view(),name="DeletePost"),
    path('user_settings/',views.UserSettings.as_view(),name="settings"),
    path('change_username/',views.editusername,name="editusername"),
    path('change_ava/',views.edituserava,name="edituserava"),
    path('change_password/',views.edituserpassword,name="edituserpassword"),
    path('create_comment/<int:id>/',views.createcomment,name="createcomment"),
    path('editpost/<int:id>/',views.PostEdit,name="postedit"),
    path('editpost/<int:id>/confirm/',views.PostEditConfirm,name="posteditconfirm"),
    path('deleteimage/<int:id>/',views.deleteimage,name="deleteimage"),
    path('deletevideo/<int:id>/',views.deletevideo,name="deletevideo"),
    path('donation/form/',views.DonationPage.as_view(),name="donate"),
    path('donation/confirm/',views.Donate,name="donateconfirm"),

]
