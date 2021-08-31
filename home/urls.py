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
    path('donation/thanks/',views.thanks.as_view(),name="thanks"),
    path('change_donate_link/',views.edituserdonatelink,name="userdonatelink"),
    path('get_premium/',views.GetPremiumPage.as_view(),name="getpremium"),
    path('get_premium/confirm/',views.GetPremium,name="getpremiumconfirm"),
    path('get_premium/alreadyhavepremium/',views.alreadyHavePremium.as_view(),name="alreadyhavepremium"),
    path('deletelink/<int:id>/',views.deletelink,name="deletelink"),
    path('reply_to_comment/<int:id>/',views.reply_to_comment,name="reply_to_comment"),
    path('reply_to_reply/<int:id1>/<int:id2>/',views.reply_to_reply,name="reply_to_reply"),
    path('delete_comment/<int:id>/',views.delete_comment,name="delete_comment"),
    path('delete_reply/<int:id>/',views.delete_reply,name="delete_reply"),
    path('report/post/<int:id>/',views.send_report_post,name="send_report_post"),
    path('report/user/<int:id>/',views.send_report_user,name="send_report_user"),
    path('reports/',views.reports,name="reports"),
    path('reports/<int:id>/',views.report_detail,name="report"),
    path('reports/<int:id>/delete/',views.ReportDelete,name="deletereport"),
    path('reports/<int:id>/delete/post/',views.PostDeleterep,name="deletepostrep"),
    path('reports/<int:id>/delete/post/confirm/',views.PostDeleteRepConfirm,name="PostDeleteRepConfirm"),
    path('reports/<int:id>/delete/user/',views.UserDeleterep,name="deleteuserrep"),
    path('reports/<int:id>/delete/user/confirm/',views.UserDeleteRepConfirm,name="UserDeleteRepConfirm"),
    path('delete/user/<int:pk>/',views.UserDelete.as_view(),name="deleteuser"),
]
