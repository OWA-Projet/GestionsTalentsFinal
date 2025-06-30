# services/ServicePostuler.py (ou dans ton CVService.py)
from ..models import CV, OffresEmploi

class ServicePostuler:

    @staticmethod
    def postuler(utilisateur, offre_id, cv_id):
        """
        Lie le CV du candidat à l'offre d'emploi (postuler).
        - utilisateur : Utilisateur (candidat connecté)
        - offre_id    : ID de l'offre d'emploi
        - cv_id       : ID du CV choisi pour postuler
        """
        # Vérifier que le CV appartient bien à l'utilisateur
        try:
            cv = CV.objects.get(id=cv_id, owner=utilisateur)
        except CV.DoesNotExist:
            raise ValueError("CV introuvable ou non autorisé.")

        try:
            offre = OffresEmploi.objects.get(id=offre_id)
        except OffresEmploi.DoesNotExist:
            raise ValueError("Offre d'emploi introuvable.")

        # Ajouter l'offre à la liste des offres du CV si ce n'est pas déjà fait
        if not cv.offres.filter(id=offre_id).exists():
            cv.offres.add(offre)
            cv.save()
            return True  # Succès
        else:
            return False  # Déjà postulé
