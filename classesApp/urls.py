from django.urls import path
from classesApp import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('User/', views.user_list),
    path('User/<int:pk>/', views.user_detail),
    path('Post/', views.post_list),
    path('PostsAll/', views.post_list2),
    path('Post/<int:pk>/', views.post_detail),
    path('User/Create/', views.user_create),
    path('User/Update/<int:pk>/', views.user_update),
    path('User/Delete/<int:pk>/', views.user_delete),
    path('Post/Create/', views.post_create),
    path('Post/Delete/<int:pk>/', views.post_delete),
    path('creer_post/', views.creer_post, name='creer_post'),
     path('saveFile/', views.saveFile, name='saveFile'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('posts/<int:post_id>/comments/create/', views.create_comment, name='create_comment'),
    path('posts/<int:post_id>/reactions/create/', views.create_reaction, name='create_reaction'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('reactions/<int:reaction_id>/delete/', views.delete_reaction, name='delete_reaction'),
    path('etudiant/ajouter', views.etudiant_create, name='addEtudiant'),
    path('ajouter-annee-universitaire/', views.ajouter_annee_universitaire, name='ajouter_annee_universitaire'),
    path('enseignant-create/', views.enseignant_create, name='enseignant_create'),
    path('classe-create/', views.classe_create, name='classe_create'),
    path('matiere-create/', views.matiere_create, name='matiere_create'),
    path('get-etudiants/', views.get_etudiants, name='get_etudiants'),
    path('enseignants/', views.get_enseignants_with_classes, name='enseignants_with_classes'),
    path('etudiants/<int:etudiant_id>/', views.update_etudiant, name='update_etudiant'),
    path('enseignants/<int:enseignant_id>/', views.update_enseignant, name='update_enseignant'),
    path('etudiants/<int:etudiant_id>/add_class/<int:class_id>/<str:academic_year>/', views.add_class_to_etudiant, name='add_class_to_etudiant'),
    #  path('enseignants/<int:enseignant_id>/add_class/<int:class_id>/matiere/<str:matiere_name>/',views.addClassToEnseignant ,name='add_class_to_enseignant'),


   path('media/<path:path>/', views.serve_media, name='serve_media')

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
