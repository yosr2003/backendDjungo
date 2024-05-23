from http import server
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import AnneeUniversitaire, Commentaire, Enseignant, Etudiant, Matiere, PieceJointe, Post, Reaction
from .serializers import ClasseSerializer, CommentaireSerializer, PieceJointeSerializer, PostSerializer, ReactionSerializer
from .models import User
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import UserSerializer
from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Post
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Commentaire, Reaction, Post
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Reaction
import json
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from .models import User
# Liste tous les posts
def post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)

def post_list2(request):
    posts = Post.objects.all()
    serialized_posts = PostSerializer(posts, many=True).data

    # Récupérer les commentaires pour chaque post
    for post_data in serialized_posts:
        post_id = post_data['idPost']
        post_comments = CommentaireSerializer(Post.objects.get(idPost=post_id).commentaire_set.all(), many=True).data
        post_data['commentaires'] = post_comments

    # Récupérer les pièces jointes pour chaque post
    for post_data in serialized_posts:
        post_id = post_data['idPost']
        post_pieces_jointes = PieceJointeSerializer(Post.objects.get(idPost=post_id).piecejointe_set.all(), many=True).data
        post_data['pieces_jointes'] = post_pieces_jointes

    # Récupérer les réactions pour chaque post
    for post_data in serialized_posts:
        post_id = post_data['idPost']
        post_reactions = ReactionSerializer(Post.objects.get(idPost=post_id).reaction_set.all(), many=True).data
        post_data['reactions'] = post_reactions

    return JsonResponse(serialized_posts, safe=False)


# Récupère un post par son ID
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    serializer = PostSerializer(post)
    return JsonResponse(serializer.data)

# Crée un nouveau post
@csrf_exempt
def post_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    

#-------------------------------------------

@csrf_exempt
def creer_post22(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contenu = data.get('contenu')
        user_id = data.get('user')
        estpublie = data.get('estpublie')
        pieces_jointes_data = request.FILES.getlist('PieceJointe')

        user = get_object_or_404(User, idUser=user_id)
        nouveau_post = Post.objects.create(contenu=contenu, user=user, estpublie=estpublie)

        for uploaded_file in pieces_jointes_data:
            nom_piece = uploaded_file.name
            type_piece = uploaded_file.content_type
            piece_jointe = PieceJointe.objects.create(nomPiece=nom_piece, typePiece=type_piece, post=nouveau_post)

        return JsonResponse({'message': 'Post créé avec succès'}, status=201)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

#-------------------------------------------

@csrf_exempt
def creer_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        contenu = data.get('contenu')
        user_id = data.get('user')
        published=data.get('published')
        estpublie = data.get('estpublie')
        pieces_jointes_data = data.get('PieceJointe', [])
        reactions_data = data.get('Reaction', [])
        commentaires_data = data.get('Commentaire', [])

        user = get_object_or_404(User, idUser=user_id)
        nouveau_post = Post.objects.create(contenu=contenu, published=published, user=user, estpublie=estpublie)
        for piece_data in pieces_jointes_data:
            PieceJointe.objects.create(
                nomPiece=piece_data['nomPiece'], 
                typePiece=piece_data['typePiece'], 
                post=nouveau_post
            )

        for reaction_data in reactions_data:
            Reaction.objects.create(
                emoji=reaction_data['emoji'], 
                user_id=reaction_data['user'], 
                post=nouveau_post
            )

        for commentaire_data in commentaires_data:
            Commentaire.objects.create(
                contenu=commentaire_data['contenu'], 
                user_id=commentaire_data['user'], 
                post=nouveau_post
            )
    
    
        serializer = PostSerializer(nouveau_post)

        
        return JsonResponse({'message': 'Post créé avec succès', 'nouveau_post':serializer.data}, status=201)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


import os
from django.views.static import serve
@csrf_exempt
def serve_media(request, path):
    media_root = settings.MEDIA_ROOT
    media_path = os.path.join(media_root, path)
    
    if os.path.exists(media_path):
        return serve(request, path, document_root=media_root)
    else:
        raise Http404("File not found")



@csrf_exempt
def saveFile(request):
    if request.method == 'POST' and request.FILES:
        uploaded_files = request.FILES.getlist('uploadedFiles')
        post_id = request.POST.get('post_id')

        if post_id:
            try:
                post_id = int(post_id)
                piece_jointe_ids = []

                for uploaded_file in uploaded_files:
                    file_name = default_storage.save(uploaded_file.name, uploaded_file)

                    nouvelle_piece_jointe = PieceJointe.objects.create(
                        nomPiece=uploaded_file.name,
                        typePiece=uploaded_file.content_type,
                        post_id=post_id
                    )
                    piece_jointe_ids.append(nouvelle_piece_jointe.idPiece)

                return JsonResponse({'message': 'Pièces jointes ajoutées avec succès', 'piece_jointe_ids': piece_jointe_ids})
            except ValueError:
                return JsonResponse({'error': 'L\'ID du post doit être un entier valide'})
        else:
            return JsonResponse({'error': 'L\'ID du post est manquant'})
    else:
        return JsonResponse({'error': 'Aucun fichier téléchargé ou méthode de requête incorrecte'})
    



#----------------------------------------------



# Supprime un post existant
@csrf_exempt
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'DELETE':
        post.delete()
        return JsonResponse({'message': 'Post supprimé avec succès'}, status=204)

#---------------------------------------users-------------------------------------------------users-----------------------------------------------

# Liste tous les utilisateurs
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

# Récupère un utilisateur par son ID
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)

# Crée un nouvel utilisateur
@csrf_exempt
def user_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

# Met à jour un utilisateur existant
@csrf_exempt
def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'PUT':
        data = json.loads(request.body)
        serializer = UserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
# Supprime un utilisateur existant
@csrf_exempt
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'DELETE':
        user.delete()
        return JsonResponse({'message': 'Utilisateur supprimé avec succès'}, status=204)


#----------------------------------------------------------------------------------------

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Commentaire

@csrf_exempt
def get_comment_by_id(request, comment_id):
    if request.method == 'GET':
        # Récupérer le commentaire par son ID
        commentaire = get_object_or_404(Commentaire, idComment=comment_id)

        # Serializer le commentaire
        serialized_comment = {
            'idComment': commentaire.idComment,
            'contenu': commentaire.contenu,
            'published': commentaire.published,
            'user': commentaire.user.idUser,  # Vous pouvez ajouter d'autres détails de l'utilisateur si nécessaire
            'post': commentaire.post.idPost  # Vous pouvez ajouter d'autres détails du post si nécessaire
        }

        return JsonResponse(serialized_comment, status=200)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
#-----------------------------------------------------------------------------------


@csrf_exempt
def delete_post(request, post_id):
    if request.method == 'DELETE':
        post = get_object_or_404(Post, pk=post_id)
        post.commentaire_set.all().delete()
        post.reaction_set.all().delete()
        post.piecejointe_set.all().delete()
        post.delete()
        return JsonResponse({'message': 'Post and associated data deleted successfully'}, status=204)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Commentaire, Reaction, Post

# Création d'un commentaire pour un post existant
@csrf_exempt
def create_comment(request, post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        contenu = data.get('contenu')
        user_id = data.get('user')

        # Récupérer le post associé
        post = get_object_or_404(Post, idPost=post_id)

        # Récupérer l'utilisateur
        user = get_object_or_404(User, idUser=user_id)

        # Créer le commentaire
        commentaire = Commentaire.objects.create(
            contenu=contenu,
            user=user,
            post=post
        )

        return JsonResponse({'message': 'Commentaire créé avec succès'}, status=201)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)



@csrf_exempt
def create_reaction(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            emoji = data.get('emoji')
            user_id = data.get('user')

            # Vérifier si l'utilisateur et le post existent
            user = get_object_or_404(User, pk=user_id)
            post = get_object_or_404(Post, pk=post_id)

            # Créer la réaction
            reaction = Reaction.objects.create(
                emoji=emoji,
                user=user,
                post=post
            )

            return JsonResponse({'message': 'Réaction créée avec succès'}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Données JSON invalides'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'error': 'L\'utilisateur spécifié n\'existe pas'}, status=404)
        except Post.DoesNotExist:
            return JsonResponse({'error': 'Le post spécifié n\'existe pas'}, status=404)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


# Supprimer un commentaire existant par son ID
@csrf_exempt
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        comment = get_object_or_404(Commentaire, pk=comment_id)
        comment.delete()
        return JsonResponse({'message': 'Commentaire supprimé avec succès'}, status=204)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)

# Supprimer une réaction existante par son ID
@csrf_exempt
def delete_reaction(request, reaction_id):
    if request.method == 'DELETE':
        reaction = get_object_or_404(Reaction, pk=reaction_id)
        reaction.delete()
        return JsonResponse({'message': 'Réaction supprimée avec succès'}, status=204)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    





from django.http import JsonResponse
from .models import Etudiant, Classe
from .serializers import EtudiantSerializer

@csrf_exempt
def etudiant_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Extract relevant data from the request
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        password = data.get('password')
        numTel = data.get('numTel')
        specialite = data.get('specialite')
        classes_data = data.get('classe', []) 
        
        # Create Etudiant instance
        etudiant = Etudiant.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            password=password,
            numTel=numTel,
            specialite=specialite
        )

        # Create or get Classe instances and associate them with the etudiant
        for classe_data in classes_data:
            num = classe_data.get('num')
            classe, created = Classe.objects.get_or_create(num=num)
            etudiant.classes.add(classe)

        serializer = EtudiantSerializer(etudiant)
        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Etudiant, Classe, AnneeUniversitaire

@csrf_exempt
def ajouter_annee_universitaire(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        etudiant_id = data.get('etudiant')
        classe_id = data.get('classe')
        annee = data.get('annee')

        # Vérifier si les informations nécessaires sont présentes
        if not etudiant_id or not classe_id or not annee:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            etudiant = Etudiant.objects.get(pk=etudiant_id)
            classe = Classe.objects.get(pk=classe_id)
        except Etudiant.DoesNotExist:
            return JsonResponse({'error': f'Etudiant with id {etudiant_id} does not exist'}, status=400)
        except Classe.DoesNotExist:
            return JsonResponse({'error': f'Classe with id {classe_id} does not exist'}, status=400)

        # Créer l'instance d'AnneeUniversitaire
        annee_universitaire = AnneeUniversitaire.objects.create(
            etudiant=etudiant,
            classe=classe,
            annee=annee
        )

        return JsonResponse({
            'id': annee_universitaire.id,
            'etudiant_id': etudiant_id,
            'classe_id': classe_id,
            'annee': annee
        }, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Enseignant, Classe, Matiere
from .serializers import EnseignantSerializer

@csrf_exempt
def enseignant_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Extract relevant data from the request
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        password = data.get('password')
        numTel = data.get('numTel')
        nbAnneeExp = data.get('nbAnneeExp')
        classes_data = data.get('classes', [])

        # Create Enseignant instance
        enseignant = Enseignant.objects.create(
            nom=nom,
            prenom=prenom,
            email=email,
            password=password,
            numTel=numTel,
            nbAnneeExp=nbAnneeExp
        )

        # Create or get Classe instances and associate them with the enseignant
        for classe_data in classes_data:
            num = classe_data.get('num')
            nomMatiere = classe_data.get('nomMatiere')
            classe, created = Classe.objects.get_or_create(num=num)
            Matiere.objects.create(enseignant=enseignant, classe=classe, nomMatiere=nomMatiere)

        serializer = EnseignantSerializer(enseignant)
        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Etudiant, Classe, AnneeUniversitaire, Enseignant, Matiere
from .serializers import ClasseSerializer

@csrf_exempt
def classe_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Extract relevant data from the request
        num = data.get('num')
        etudiants_data = data.get('etudiants', [])
        enseignants_data = data.get('enseignants', [])

        # Create Classe instance
        classe = Classe.objects.create(num=num)

        # Associate Etudiants with the Classe via AnneeUniversitaire
        for etudiant_data in etudiants_data:
            etudiant_id = etudiant_data.get('id')
            try:
                etudiant = Etudiant.objects.get(pk=etudiant_id)
                AnneeUniversitaire.objects.create(etudiant=etudiant, classe=classe)
            except Etudiant.DoesNotExist:
                return JsonResponse({'error': f'Etudiant with id {etudiant_id} does not exist'}, status=400)

        # Associate Enseignants with the Classe via Matiere
        for enseignant_data in enseignants_data:
            enseignant_id = enseignant_data.get('id')
            nom_matiere = enseignant_data.get('nomMatiere')
            try:
                enseignant = Enseignant.objects.get(pk=enseignant_id)
                Matiere.objects.create(enseignant=enseignant, classe=classe, nomMatiere=nom_matiere)
            except Enseignant.DoesNotExist:
                return JsonResponse({'error': f'Enseignant with id {enseignant_id} does not exist'}, status=400)

        serializer = ClasseSerializer(classe)
        return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Enseignant, Classe, Matiere

@csrf_exempt
def matiere_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Extract relevant data from the request
        enseignant_id = data.get('enseignant')
        classe_id = data.get('classe')
        nom_matiere = data.get('nomMatiere')

        # Vérifier si les informations nécessaires sont présentes
        if not enseignant_id or not classe_id or not nom_matiere:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            enseignant = Enseignant.objects.get(pk=enseignant_id)
            classe = Classe.objects.get(pk=classe_id)
        except Enseignant.DoesNotExist:
            return JsonResponse({'error': f'Enseignant with id {enseignant_id} does not exist'}, status=400)
        except Classe.DoesNotExist:
            return JsonResponse({'error': f'Classe with id {classe_id} does not exist'}, status=400)

        # Créer l'instance de Matiere
        matiere = Matiere.objects.create(
            enseignant=enseignant,
            classe=classe,
            nomMatiere=nom_matiere
        )

        return JsonResponse({
            'id': matiere.id,
            'enseignant_id': enseignant_id,
            'classe_id': classe_id,
            'nomMatiere': nom_matiere
        }, status=201)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.http import JsonResponse
from .models import Etudiant, AnneeUniversitaire

def get_etudiants(request):
    if request.method == 'GET':
        etudiants_with_annees_universitaires = []

        # Récupérer tous les étudiants
        etudiants = Etudiant.objects.all()

        # Pour chaque étudiant, récupérer ses années universitaires avec leurs attributs
        for etudiant in etudiants:
            etudiant_data = {
                'id': etudiant.idUser,
                'nom': etudiant.nom,
                'prenom': etudiant.prenom,
                'email': etudiant.email,
                'numTel': etudiant.numTel,
                'specialite': etudiant.specialite,
                'annees_universitaires': []
            }

            # Récupérer les années universitaires associées à l'étudiant avec leurs attributs
            annees_universitaires = AnneeUniversitaire.objects.filter(etudiant=etudiant)
            for annee_universitaire in annees_universitaires:
                annee_universitaire_data = {
                    'classe': {
                        'id': annee_universitaire.classe.idClasse,
                        'num': annee_universitaire.classe.num,
                        # Ajoutez d'autres attributs de la classe ici si nécessaire
                    },
                    'annee': annee_universitaire.annee
                }
                etudiant_data['annees_universitaires'].append(annee_universitaire_data)

            etudiants_with_annees_universitaires.append(etudiant_data)

        return JsonResponse(etudiants_with_annees_universitaires, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

from django.http import JsonResponse
from .models import Enseignant, Matiere, Classe

def get_enseignants_with_classes(request):
    if request.method == 'GET':
        enseignants_with_classes = []

        # Récupérer tous les enseignants
        enseignants = Enseignant.objects.all()

        # Pour chaque enseignant, récupérer ses matières avec les classes associées et leurs attributs
        for enseignant in enseignants:
            enseignant_data = {
                'id': enseignant.idUser,
                'nom': enseignant.nom,
                'prenom': enseignant.prenom,
                'email': enseignant.email,
                'numTel': enseignant.numTel,
                'nbAnneeExp': enseignant.nbAnneeExp,
                'matieres': []
            }

            # Récupérer les matières enseignées par l'enseignant avec les classes associées et leurs attributs
            matieres = Matiere.objects.filter(enseignant=enseignant)
            for matiere in matieres:
                classe_data = {
                    'id': matiere.classe.idClasse,
                    'num': matiere.classe.num,
                    # Ajoutez d'autres attributs de la classe ici
                }
                matiere_data = {
                    'nomMatiere': matiere.nomMatiere,
                    'classe': classe_data
                }
                enseignant_data['matieres'].append(matiere_data)

            enseignants_with_classes.append(enseignant_data)

        return JsonResponse(enseignants_with_classes, safe=False)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)


import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Etudiant, AnneeUniversitaire

@csrf_exempt
def update_etudiant(request, etudiant_id):
    if request.method == 'PUT':
        # Récupérer l'étudiant à mettre à jour
        etudiant = Etudiant.objects.get(pk=etudiant_id)

        # Extraire les données JSON de la requête
        data = json.loads(request.body)

        # Mettre à jour les attributs de l'étudiant
        etudiant.nom = data.get('nom', etudiant.nom)
        etudiant.prenom = data.get('prenom', etudiant.prenom)
        etudiant.email = data.get('email', etudiant.email)
        etudiant.numTel = data.get('numTel', etudiant.numTel)
        etudiant.specialite = data.get('specialite', etudiant.specialite)

        # Sauvegarder les modifications
        etudiant.save()

        # Construire la réponse JSON
        response_data = {
            'message': 'Etudiant mis à jour avec succès',
            'etudiant': {
                'id': etudiant.idUser,
                'nom': etudiant.nom,
                'prenom': etudiant.prenom,
                'email': etudiant.email,
                'numTel': etudiant.numTel,
                'specialite': etudiant.specialite,
            }
        }

        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Enseignant

@csrf_exempt
def update_enseignant(request, enseignant_id):
    if request.method == 'PUT':
        # Récupérer l'enseignant à mettre à jour
        enseignant = Enseignant.objects.get(pk=enseignant_id)

        # Extraire les données JSON de la requête
        data = json.loads(request.body)

        # Mettre à jour les attributs de l'enseignant
        enseignant.nom = data.get('nom', enseignant.nom)
        enseignant.prenom = data.get('prenom', enseignant.prenom)
        enseignant.email = data.get('email', enseignant.email)
        enseignant.numTel = data.get('numTel', enseignant.numTel)
        enseignant.nbAnneeExp = data.get('nbAnneeExp', enseignant.nbAnneeExp)

        # Sauvegarder les modifications
        enseignant.save()

        # Construire la réponse JSON
        response_data = {
            'message': 'Enseignant mis à jour avec succès',
            'enseignant': {
                'id': enseignant.idUser,
                'nom': enseignant.nom,
                'prenom': enseignant.prenom,
                'email': enseignant.email,
                'numTel': enseignant.numTel,
                'nbAnneeExp': enseignant.nbAnneeExp,
            }
        }

        return JsonResponse(response_data, status=200)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Etudiant, Classe, AnneeUniversitaire

@csrf_exempt
def add_class_to_etudiant(request, etudiant_id, class_id, academic_year):
    if request.method == 'PUT':
        try:
            etudiant = Etudiant.objects.get(pk=etudiant_id)
            classe = Classe.objects.get(pk=class_id)
            if classe in etudiant.classes.all():
                return JsonResponse({'error': 'Class already associated with the student'}, status=400)

            annee_universitaire, created = AnneeUniversitaire.objects.get_or_create(etudiant=etudiant, classe=classe, annee=academic_year)
            etudiant.classes.add(classe)

            response_data = {
                'message': 'Class added to student successfully',
                'etudiant': {
                    'id': etudiant.idUser,
                    'nom': etudiant.nom,
                    'prenom': etudiant.prenom,
                    'email': etudiant.email,
                    'numTel': etudiant.numTel,
                    'specialite': etudiant.specialite,
                    'classes': [{'id': classe.idClasse, 'num': classe.num}],
                    'academic_year': academic_year,
                }
            }

            return JsonResponse(response_data, status=200)
        except Etudiant.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
        except Classe.DoesNotExist:
            return JsonResponse({'error': 'Class not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    



#-------------------------------------faux c'est à rectifier --------------------------------
# @csrf_exempt
# def addClassToEnseignant(cls, enseignant_id, classe_id, nom_matiere):
#         try:
#             enseignant = cls.objects.get(pk=enseignant_id)
#             classe = Classe.objects.get(pk=classe_id)

#             matiere = Matiere.objects.create(enseignant=enseignant, classe=classe, nomMatiere=nom_matiere)
#             enseignant.classes.add(classe)

#             return matiere
#         except cls.DoesNotExist:
#             raise ValueError("Enseignant not found")
#         except Classe.DoesNotExist:
#             raise ValueError("Classe not found")





