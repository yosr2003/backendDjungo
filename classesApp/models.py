from django.db import models

class User(models.Model):
    idUser = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    numTel = models.DecimalField(max_digits=15, decimal_places=0)

class Post(models.Model):
    idPost = models.AutoField(primary_key=True)
    contenu = models.CharField(max_length=255)
    published = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estpublie = models.BooleanField(default=False) 


class PieceJointe(models.Model):
    idPiece = models.AutoField(primary_key=True)
    nomPiece = models.CharField(max_length=100)
    typePiece = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Reaction(models.Model):
    idReaction = models.AutoField(primary_key=True)
    emoji = models.ImageField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Commentaire(models.Model):
    idComment = models.AutoField(primary_key=True)
    contenu = models.CharField(max_length=255)
    published = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

class Etudiant(User):
    specialite = models.CharField(max_length=255)
    classes = models.ManyToManyField('Classe', through='AnneeUniversitaire', related_name='etudiants')

class Enseignant(User):
    nbAnneeExp = models.IntegerField()
    classes = models.ManyToManyField('Classe', through='Matiere', related_name='enseignants')

class Administrateur(User):
    role = models.CharField(max_length=500)

class Classe(models.Model):
    idClasse = models.AutoField(primary_key=True)
    num = models.IntegerField()
    

class AnneeUniversitaire(models.Model):
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    annee = models.CharField(max_length=10)  

class Matiere(models.Model):
    enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, related_name='matieres_enseignees')
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    nomMatiere = models.CharField(max_length=100)
















