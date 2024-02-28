from . import views
from django.urls import path

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('search/', views.search_results, name='search-results'), 
    path('family/', views.FamilyView.as_view(), name='family'), 
    path('pastimes/', views.PastimesView.as_view(), name='pastimes'),
    path('career/', views.CareerView.as_view(), name='career'),
    path('wall_of_complaints/', views.WallOfComplaintsView.as_view(), name='wall_of_complaints'),
    path('post/new/', views.create_post, name='create_post'),
    path('edit/<int:pk>', views.PostUpdateView.as_view(), name='post-edit'),
    path('signup/', views.signup, name='signup'),
    path('terms/', views.terms_and_conditions, name='terms'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('<slug:slug>/add_comment/', views.add_comment, name='add_comment'),
    path('edit-comment/<int:pk>/', views.CommentUpdateView.as_view(), name='edit-comment'),
    path('delete-post/<slug:slug>/', views.PostDeleteView.as_view(), name='delete-post'),
    path('delete-comment/<int:pk>/', views.CommentDeleteView.as_view(), name='delete-comment'),
    path('send_report_email/<slug:post_slug>/', views.send_report_email, name='send_report_email_post'),
    path('send_report_email/comment/<int:comment_id>/', views.send_report_email, name='send_report_email_comment'),
]