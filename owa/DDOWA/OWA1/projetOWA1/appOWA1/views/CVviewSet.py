from rest_framework import viewsets, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.decorators import action

from ..models import Utilisateur, CV, CV_classe
from ..serializers.CvSerializer import CVSerializer
from ..services.CVService import CVService
from ..services.permissions import HasUserRole

class CVViewSet(mixins.CreateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                viewsets.GenericViewSet):

    serializer_class   = CVSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        HasUserRole.with_roles("RH")
    ]

    def get_serializer(self, *args, **kwargs):
        # Toujours passer le context pour afficher les URLs correctes dans le serializer
        kwargs.setdefault('context', self.get_serializer_context())
        return super().get_serializer(*args, **kwargs)

    def _queryset_for(self, user):
        return CVService.list_for_user(user)

    def list(self, request):
        qs = self._queryset_for(request.user)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            cv = self._queryset_for(request.user).get(pk=pk)
        except CV.DoesNotExist:
            return Response({"detail": "CV introuvable."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur inattendue : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(cv)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data.copy()
        pdf  = request.FILES.get("fichier")
        fichier_file = request.FILES.get("fichier")
        offres_ids = request.data.getlist("offres") if hasattr(request.data, "getlist") else request.data.get("offres", None)

        # Gestion owner
        try:
            owner_field = data.pop("owner")
            if isinstance(owner_field, Utilisateur):
                owner = owner_field
            else:
                owner = Utilisateur.objects.get(pk=int(owner_field))
        except (ValueError, Utilisateur.DoesNotExist):
            return Response({"detail": "Utilisateur introuvable."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Erreur sur l'identification du propriétaire : {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # Permissions
        is_rh = request.user.roles.filter(name="RH").exists()
        if owner.id != request.user.id and not is_rh:
            return Response({"detail": "Tu ne peux créer un CV que pour toi-même."}, status=status.HTTP_403_FORBIDDEN)

        # Extraction du texte PDF si besoin
        if pdf and not pdf.name.lower().endswith(".pdf"):
            return Response({"detail": "Le fichier doit être un PDF."}, status=status.HTTP_400_BAD_REQUEST)
        if pdf:
            try:
                data["texte_brut"] = CVService.extract_text_pdf(pdf)
            except Exception as e:
                return Response({"detail": f"Erreur d'extraction du texte PDF : {e}"}, status=status.HTTP_400_BAD_REQUEST)

        if fichier_file:
            data["fichier"] = fichier_file

        if offres_ids:
            try:
                if isinstance(offres_ids, str):
                    offres_ids = [int(x) for x in offres_ids.split(',') if x]
                elif isinstance(offres_ids, list):
                    offres_ids = [int(x) for x in offres_ids if x]
                data["offres"] = offres_ids
            except Exception:
                return Response({"detail": "Paramètre 'offres' mal formaté."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cv = CVService.create(owner=owner, validated_data=data)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la création du CV : {e}"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(cv)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, partial=False):
        try:
            cv = self._queryset_for(request.user).get(pk=pk)
        except CV.DoesNotExist:
            return Response({"detail": "CV introuvable."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"Erreur inattendue : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(cv, data=request.data, partial=partial)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data.copy()
        fichier_file = request.FILES.get("fichier")
        offres_ids = request.data.getlist("offres") if hasattr(request.data, "getlist") else request.data.get("offres", None)

        if fichier_file:
            data["fichier"] = fichier_file
        if offres_ids is not None:
            try:
                if isinstance(offres_ids, str):
                    offres_ids = [int(x) for x in offres_ids.split(',') if x]
                elif isinstance(offres_ids, list):
                    offres_ids = [int(x) for x in offres_ids if x]
                data["offres"] = offres_ids
            except Exception:
                return Response({"detail": "Paramètre 'offres' mal formaté."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            CVService.update(cv, data)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la mise à jour du CV : {e}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(cv).data)

    def partial_update(self, request, pk=None):
        return self.update(request, pk, partial=True)

    def destroy(self, request, pk=None):
        try:
            cv = self._queryset_for(request.user).get(pk=pk)
        except CV.DoesNotExist:
            return Response({"detail": "CV introuvable."}, status=status.HTTP_404_NOT_FOUND)
        try:
            CVService.delete(cv)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la suppression du CV : {e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    # ───────── Classification ───────── #

    @action(detail=True, methods=["post"])
    def classify(self, request, pk=None):
        try:
            cv = self._queryset_for(request.user).get(pk=pk)
        except CV.DoesNotExist:
            return Response({"detail": "CV introuvable."}, status=status.HTTP_404_NOT_FOUND)
        try:
            preds = CVService.predict_one(cv.texte_brut)
            CV_classe.objects.create(cv=cv, metiers=preds)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la classification : {e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(preds, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def classify_batch(self, request):
        ids = request.data.get("ids", [])
        if not ids or not isinstance(ids, list):
            return Response({"detail": "La liste d'ids est requise."}, status=status.HTTP_400_BAD_REQUEST)
        cvs = CV.objects.filter(id__in=ids)
        if not cvs.exists():
            return Response({"detail": "Aucun CV trouvé pour les ids fournis."}, status=status.HTTP_404_NOT_FOUND)
        try:
            res = CVService.predict_batch(cvs)
            by_id = {cv.id: cv for cv in cvs}
            for r in res:
                CV_classe.objects.filter(cv=by_id[r["id"]]).delete()
                CV_classe.objects.create(cv=by_id[r["id"]], metiers=r["result"])
        except Exception as e:
            return Response({"detail": f"Erreur lors de la classification batch : {e}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(res, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], url_path="cvs")
    def list_cvs_for_offre(self, request, pk=None):
        try:
            cvs = CVService.cvs_for_offre(pk)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la récupération des CVs pour l'offre : {e}"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CVSerializer(cvs, many=True)
        return Response(serializer.data)
