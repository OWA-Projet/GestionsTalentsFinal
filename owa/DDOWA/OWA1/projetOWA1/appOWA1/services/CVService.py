import os
from pathlib import Path
import re, string
from typing import Any, Dict
from django.conf import settings
from ..models import CV, Utilisateur,CV_Offre,OffresEmploi
import pdfplumber

from django.utils import timezone

# ML imports
from joblib import load

# Chargement du modèle ML (au premier appel, une seule fois)
class CVService:
    BASE_DIR = Path(__file__).resolve().parent
    _bundle = None

    @classmethod
    def load_bundle(cls):
        if cls._bundle is None:
            cls._bundle = load(cls.BASE_DIR / "ml_models" / "cv_classifier_bundle_3.joblib")
        return cls._bundle

    @classmethod
    def vectorizer(cls):
        return cls.load_bundle()["vectorizer"]

    @classmethod
    def classifier(cls):
        return cls.load_bundle()["model"]

    @classmethod
    def label_encoder(cls):
        return cls.load_bundle()["label_encoder"]

    @staticmethod
    def nettoyer_texte(texte):
        texte = texte.lower()
        texte = re.sub(r"\d+", "", texte)
        texte = texte.translate(str.maketrans("", "", string.punctuation))
        return re.sub(r"\s+", " ", texte).strip()

    @classmethod
    def predict_one(cls, texte_brut):
        txt_clean = cls.nettoyer_texte(texte_brut)
        X = cls.vectorizer().transform([txt_clean])
        proba = cls.classifier().predict_proba(X)[0]
        classes = cls.classifier().classes_
        labels = cls.label_encoder().inverse_transform(classes)
        pairs = sorted(zip(labels, proba), key=lambda t: t[1], reverse=True)
        return [{"label": l, "probability": float(round(p, 4))} for l, p in pairs]

    @classmethod
    def predict_batch(cls, queryset):
        results = []
        for obj in queryset:
            
            preds = cls.predict_one(obj.texte_brut)
            results.append({"id": obj.id, "result": preds})
        return results

    @staticmethod
    def extract_text_pdf(pdf_file):
        pdf_file.seek(0)
        with pdfplumber.open(pdf_file) as pdf:
            return "\n\n".join((p.extract_text() or "") for p in pdf.pages)

    """Opérations CRUD encapsulées pour la logique métier."""

    @staticmethod
    # extrait de CVService.list_for_user
    @staticmethod
    def list_for_user(user: Utilisateur):
        is_rh = user.roles.filter(name="RH").exists()
        return CV.objects.all() if is_rh else CV.objects.filter(owner=user)
    
    @staticmethod
    def list_for_user(user: Utilisateur):
        if user.roles.filter(name="RH").exists() and user.entreprise is not None:
            return CV.objects.filter(offres__entreprise=user.entreprise).distinct()
        else:
            return CV.objects.filter(owner=user)



    @staticmethod
    def create(owner: Utilisateur, validated_data: Dict[str, Any]) -> CV:
        offres = validated_data.pop('offres', None)
        validated_data.pop('owner', None)  # <--- Ajoute cette ligne !!
        cv = CV.objects.create(owner=owner, **validated_data)

        if offres is not None:
            if isinstance(offres, (list, tuple)):
                for offre in offres:
                    # Peut être un objet ou un ID
                    if isinstance(offre, OffresEmploi):
                        CV_Offre.objects.create(cv=cv, offre=offre)
                    else:
                        offre_obj = OffresEmploi.objects.get(pk=offre)
                        CV_Offre.objects.create(cv=cv, offre=offre_obj)
            else:
                # cas d'un seul objet ou id
                if isinstance(offres, OffresEmploi):
                    CV_Offre.objects.create(cv=cv, offre=offres)
                else:
                    offre_obj = OffresEmploi.objects.get(pk=offres)
                    CV_Offre.objects.create(cv=cv, offre=offre_obj,selected=False)
        return cv

    @staticmethod
    def update(cv: CV, validated_data: Dict[str, Any]) -> CV:
        offres = validated_data.pop('offres', None)
        for attr, value in validated_data.items():
            setattr(cv, attr, value)
        cv.save()
        if offres is not None:
            cv.offres.set(offres)
        return cv


    @staticmethod
    def delete(cv: CV):
        cv.delete()

    @staticmethod
    def get_all_CVs():
        return CV.objects.all()

    @staticmethod
    def cvs_for_offre(offre_id):
        """Retourne tous les CVs qui ont postulé pour une offre donnée."""
        return CV.objects.filter(offres__id=offre_id)