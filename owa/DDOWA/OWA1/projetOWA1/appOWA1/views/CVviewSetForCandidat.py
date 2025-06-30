from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from ..models import CV, CV_classe
from ..services.permissions import HasUserRole
from ..serializers.CvSerializer import CVSerializer
from ..services.CVService import CVService

class CVviewSetForCandidat(viewsets.ModelViewSet):

    serializer_class = CVSerializer
    permission_classes = [permissions.IsAuthenticated, HasUserRole.with_roles('CANDIDAT')]

    def get_queryset(self):
        # Un candidat ne voit QUE ses propres CVs
        return CV.objects.filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data.copy()
        data.pop('owner', None)
        
        pdf = request.FILES.get("fichier")
        if pdf and not pdf.name.lower().endswith(".pdf"):
            return Response({"detail": "Le fichier doit être un PDF."}, status=status.HTTP_400_BAD_REQUEST)
        if pdf:
            try:
                data["texte_brut"] = CVService.extract_text_pdf(pdf)
            except Exception as e:
                return Response({"detail": f"Erreur d'extraction du texte PDF : {e}"}, status=status.HTTP_400_BAD_REQUEST)

        owner = request.user  # Ou selon ta logique
        try:
            cv = CVService.create(owner, data)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la création du CV : {e}"}, status=status.HTTP_400_BAD_REQUEST)

        out_serializer = self.get_serializer(cv)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        try:
            serializer.save(owner=self.request.user)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la mise à jour du CV : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="classify")
    def classify(self, request, pk=None):
        """
        POST /cvs/{id}/classify/
        Renvoie la liste des (label, probability) et enregistre le résultat.
        """
        try:
            cv = self.get_object()
        except CV.DoesNotExist:
            return Response({"detail": "CV introuvable."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur inattendue : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            predictions = CVService.predict_one(cv.texte_brut)
            CV_classe.objects.create(cv=cv, metiers=predictions)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la classification du CV : {e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(predictions, status=status.HTTP_200_OK)
