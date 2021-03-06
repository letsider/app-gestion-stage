# -*- coding: utf-8 -*-

#from django.core.management import setup_environ
#from gestionStage import settings
#setup_environ(settings)
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestionStage.settings")
from django.forms import ModelForm
from entreprise.models import Entreprise
from stage.models import Personne, PersonneExterieure, PersonneInterne, Diplome, Promotion, Etudiant, Enseignant, Stage, Logiciel, OffreStage
from planning.models import Salle, Soutenance
from pprint import pprint

import json



#charger les permissions
from django.contrib.auth.models import Permission, User, Group
from django.contrib.contenttypes.models import ContentType



personne_interne_content_type = ContentType.objects.get_for_model(PersonneInterne)
# perms= json.load(open("json/permissions.json"))
# PERMS = {}

# for p in perms:
# 	perm=Permission.objects.create(
# 		codename=p["codename"],
# 		name=p["name"],
# 		content_type=personne_interne_content_type
# 	)
# 	perm.save()
# 	PERMS[p["codename"]] = perm
# 	print(perm)

#charger les groupes
groups=json.load(open("json/groups.json"))
GROUPS={}
for g in groups:
	group=Group.objects.create(name=g["name"])
	group.save()
	for p in g["permissions"]:
		perm = Permission.objects.get(codename=p)
		group.permissions.add(perm)
	group.save()
	GROUPS[g["name"]]=group


#charger les utilisateurs
users=json.load(open("json/users.json"))
USERS={}
for u in users:
	user=User.objects.create_user(
		username=u["username"],
		password='',
		first_name=u["first_name"],
		last_name=u["last_name"],
		email=u["email"]
	)
	user.set_password(u["password"])
	user.save()

	for g in u["groups"]:
		user.groups.add(GROUPS[g])
	user.save()
	USERS[u["username"]]=user






entreprise = json.load(open("json/entreprise.json")) 				#encoding='utf-8'
logiciels = json.load(open("json/logiciels.json"))	 	#encoding='utf-8'
stage = json.load(open("json/stage.json")) 				#encoding='utf-8'
enseignants = json.load(open("json/enseignants.json")) 	#encoding='utf-8'
etudiants = json.load(open("json/etudiants.json")) 		#encoding='utf-8'
personnesExt = json.load(open("json/personnes_exterieures.json")) 	#encoding='utf-8'
promotions = json.load(open("json/promotions.json")) 	#encoding='utf-8'
diplomes = json.load(open("json/diplomes.json")) 		#encoding='utf-8'
offreStage = json.load(open("json/offrestage.json")) 				#encoding='utf-8'
soutenances = json.load(open("json/soutenances.json")) 				#encoding='utf-8'
salles = json.load(open("json/salles.json")) 				#encoding='utf-8'

for d in diplomes:
	diplome=Diplome(
		nom=d["nom"],
		specialite=d["specialite"]
	)
	diplome.save()


for p in promotions:
	promo=Promotion(
		diplome=Diplome.objects.get(pk=p["diplome"]),
		intitule=p["intitule"],
		annee=p["annee"]
	)
	promo.save()
	
for e in entreprise:
	Entreprise(
		idEntreprise=e["idEntreprise"],
		nom=e["nom"],
		adresse=e["adresse"],
		codePostal=e["codePostal"],
		ville=e["ville"],
		pays=e["pays"],
		telephone=e["telephone"],
		fax=e["fax"]
	).save()

for l in logiciels:
	Logiciel(
		nomLog=l["nomLog"],
		theme=l["theme"],
		description=l["description"]
	).save()

for e in enseignants:
	Enseignant(
		idEnseignant=e["idEnseignant"],
		nom=e["nom"],
		prenom=e["prenom"],
		username=User.objects.get(username=e["username"]),
		emailPerso=e["emailPerso"],
		civilite=e["civilite"],
		telephone=e["telephone"],
		emailEns=e["emailEns"],
		departement=e["departement"]
	).save()

for e in etudiants:
	Etudiant(
		numEtu=e["numEtu"], #PRIMARY KEY
		nom=e["nom"],
		prenom=e["prenom"],
		username=User.objects.get(username=e["username"]),
		emailPerso=e["emailPerso"],
		civilite=e["civilite"],
		telephone=e["telephone"],
		dateNaissance=e["dateNaissance"],
		emailEtu=e["emailEtu"],
		adresse= e["adresse"],
		cp=e["cp"],
		ville=e["ville"],
		promotion=Promotion.objects.get(pk=e["promotion"])
	).save()

for p in personnesExt:
	PersonneExterieure(
		idPersonneExt=p["idPersonneExt"],
		nom=p["nom"],
		prenom=p["prenom"],
		emailPerso=p["emailPerso"],
		civilite=p["civilite"],
		telephone=p["telephone"],
		emailPro=p["emailPro"],
		entreprise=Entreprise.objects.get(pk=p["entreprise"])
	).save()


for o in offreStage:	
	OffreStage(
		intitule=o["intitule"],
		sujet=o["sujet"],
		entreprise=Entreprise.objects.get(pk=o["entreprise"]),
		possibiliteEmbauche=o["possibiliteEmbauche"],
		valideOffreStage=o["valideOffreStage"]
	).save()


for s in stage:	
	Stage(
		etudiant=Etudiant.objects.get(pk=s["etudiant"]),
		intitule=s["intitule"],
		sujet=s["sujet"],
		dateDebut=s["dateDebut"],
		dateFin=s["dateFin"],
		entreprise=Entreprise.objects.get(pk=s["entreprise"]),
		persConvention=PersonneExterieure.objects.get(pk=s["persConvention"]),
		maitreStage=PersonneExterieure.objects.get(pk=s["maitreStage"]),
		enseignantTuteur=Enseignant.objects.get(pk=s["enseignantTuteur"]),
		valideStage=s["valideStage"],
		possibiliteEmbauche=s["possibiliteEmbauche"],
		valideOffreStage=s["valideOffreStage"]
	).save()

for s in salles:
	Salle(
		num = s['num']
	).save()

for s in soutenances:
	Soutenance(
		stage = Stage.objects.get(pk=s['stage']),
		datePassage = s['datePassage'],
		dateFinPrevu = s['dateFinPrevu'],
		salle = Salle.objects.get(pk=s['salle'])
	).save()