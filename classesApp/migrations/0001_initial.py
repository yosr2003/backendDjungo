# Generated by Django 5.0.6 on 2024-05-10 14:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('idUser', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=50)),
                ('prenom', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('numTel', models.DecimalField(decimal_places=0, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('idClasse', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Administrateur',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='classesApp.user')),
                ('role', models.CharField(max_length=500)),
            ],
            bases=('classesApp.user',),
        ),
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='classesApp.user')),
                ('nbAnneeExp', models.IntegerField()),
            ],
            bases=('classesApp.user',),
        ),
        migrations.CreateModel(
            name='AnneeUniversitaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.CharField(max_length=10)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.classe')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('idPost', models.AutoField(primary_key=True, serialize=False)),
                ('contenu', models.CharField(max_length=255)),
                ('published', models.DateField(auto_now_add=True)),
                ('estpublie', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='PieceJointe',
            fields=[
                ('idPiece', models.AutoField(primary_key=True, serialize=False)),
                ('nomPiece', models.CharField(max_length=100)),
                ('typePiece', models.CharField(max_length=100)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.post')),
            ],
        ),
        migrations.CreateModel(
            name='Commentaire',
            fields=[
                ('idComment', models.AutoField(primary_key=True, serialize=False)),
                ('contenu', models.CharField(max_length=255)),
                ('published', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.user')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.post')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('idReaction', models.AutoField(primary_key=True, serialize=False)),
                ('emoji', models.ImageField(upload_to='')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.user')),
            ],
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomMatiere', models.CharField(max_length=100)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.classe')),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matieres_enseignees', to='classesApp.enseignant')),
            ],
        ),
        migrations.AddField(
            model_name='enseignant',
            name='classes',
            field=models.ManyToManyField(related_name='enseignants', through='classesApp.Matiere', to='classesApp.classe'),
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='classesApp.user')),
                ('specialite', models.CharField(max_length=255)),
                ('classes', models.ManyToManyField(related_name='etudiants', through='classesApp.AnneeUniversitaire', to='classesApp.classe')),
            ],
            bases=('classesApp.user',),
        ),
        migrations.AddField(
            model_name='anneeuniversitaire',
            name='etudiant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classesApp.etudiant'),
        ),
    ]
