from rest_framework import serializers
from .models import User, Post, PieceJointe, Reaction, Commentaire, Etudiant, Enseignant, Administrateur, Classe, AnneeUniversitaire, Matiere

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('idUser', 'nom', 'prenom', 'email', 'password', 'numTel')

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('idPost', 'contenu', 'published', 'user', 'estpublie')

class PieceJointeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PieceJointe
        fields = ('idPiece', 'nomPiece', 'typePiece', 'post')

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('idReaction', 'emoji', 'user', 'post')

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = ('idComment', 'contenu', 'published', 'user', 'post')

class EtudiantSerializer(serializers.ModelSerializer):
    classe = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all())  
    class Meta:
        model = Etudiant
        fields = ('idUser', 'nom', 'prenom', 'email', 'password', 'numTel', 'specialite', 'classe')

class EnseignantSerializer(serializers.ModelSerializer):
    classes = serializers.PrimaryKeyRelatedField(queryset=Classe.objects.all(), many=True)  
    class Meta:
        model = Enseignant
        fields = ('idUser', 'nom', 'prenom', 'email', 'password', 'numTel', 'nbAnneeExp', 'classes')

class AdministrateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrateur
        fields = ('idUser', 'nom', 'prenom', 'email', 'password', 'numTel', 'role')

class ClasseSerializer(serializers.ModelSerializer):
    etudiants = EtudiantSerializer(many=True)  
    enseignants = EnseignantSerializer(many=True) 
    class Meta:
        model = Classe
        fields = ('idClasse', 'num', 'etudiants', 'enseignants')

class AnneeUniversitaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnneeUniversitaire
        fields = ('etudiant', 'classe', 'annee')

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = ('enseignant', 'classe', 'nomMatiere')
