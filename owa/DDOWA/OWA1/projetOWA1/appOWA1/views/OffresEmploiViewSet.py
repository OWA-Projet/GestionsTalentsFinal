# views/OffresEmploiViewSet.py
from django.forms import ValidationError
from ..services.permissions import permissions
from ..services.permissions import HasUserRole
from rest_framework import viewsets, status
from rest_framework.response import Response
from ..serializers.OffresEmploiSerializer import OffresEmploiSerializer
from ..services.ServiceOffresEmploi import ServiceOffresEmploi
import google.generativeai as genai
import openai
from ..models import Metier,OffresEmploi,CV_classe,CV,CV_Offre
from rest_framework.decorators import action
from django.core.mail import send_mail
from rest_framework import status
import json

openai.api_key = "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"  # Ta clé OpenAI

class OffresEmploiViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated, HasUserRole.with_roles('RH')]
    queryset = OffresEmploi.objects.all()
    serializer_class = OffresEmploiSerializer

    def list(self, request):
        try:
            user = request.user
            id_entreprise = getattr(user, 'entreprise_id', None)
            emplois = ServiceOffresEmploi.list_all(id_entreprise=id_entreprise)
            serializer = OffresEmploiSerializer(emplois, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la récupération des offres : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request, pk=None):
        try:
            emploi = ServiceOffresEmploi.retrieve(pk)
            if not emploi:
                return Response({"detail": "Offre introuvable."}, status=status.HTTP_404_NOT_FOUND)
            serializer = OffresEmploiSerializer(emploi)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {"detail": f"Erreur lors de la récupération de l'offre : {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    def get_metier_with_openai(offer_data):
        try:
            metiers = Metier.objects.all()
            liste_metiers = [m.nom for m in metiers]
            prompt = (
                f"À partir de ces données d'offre d'emploi :\n"
                f"{offer_data}\n"
                f"Quel est le métier le plus adapté parmi cette liste : {', '.join(liste_metiers)} ? "
                f"Réponds uniquement par le métier exact de la liste."
            )
            response = openai.ChatCompletion.create(
                model="gpt-4.1",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0
            )
            metier = response['choices'][0]['message']['content'].strip()
            return metier
        except Exception as e:
            raise Exception(f"Erreur OpenAI : {e}")

    def create(self, request):
        serializer = OffresEmploiSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data.copy()
            if 'image' in request.FILES:
                validated_data['image'] = request.FILES['image']
            try:
                validated_data['metier_propose'] = OffresEmploiViewSet.get_metier_with_openai(validated_data)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            emploi = ServiceOffresEmploi.create(validated_data)
            return Response(OffresEmploiSerializer(emploi).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la création de l'offre : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        emploi = ServiceOffresEmploi.retrieve(pk)
        if not emploi:
            return Response({"detail": "Offre introuvable."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OffresEmploiSerializer(emploi, data=request.data, partial=False)
        try:
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data.copy()
            if 'image' in request.FILES:
                validated_data['image'] = request.FILES['image']
            try:
                validated_data['metier_propose'] = OffresEmploiViewSet.get_metier_with_openai(validated_data)
            except Exception as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            updated_emploi = ServiceOffresEmploi.update(emploi, validated_data)
            return Response(OffresEmploiSerializer(updated_emploi).data)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la mise à jour de l'offre : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        emploi = ServiceOffresEmploi.retrieve(pk)
        if not emploi:
            return Response({"detail": "Offre introuvable."}, status=status.HTTP_404_NOT_FOUND)
        serializer = OffresEmploiSerializer(emploi, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data.copy()
            if 'image' in request.FILES:
                validated_data['image'] = request.FILES['image']
            updated_emploi = ServiceOffresEmploi.update(emploi, validated_data)
            return Response(OffresEmploiSerializer(updated_emploi).data)
        except ValidationError as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la mise à jour partielle de l'offre : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        emploi = ServiceOffresEmploi.retrieve(pk)
        if not emploi:
            return Response({"detail": "Offre introuvable."}, status=status.HTTP_404_NOT_FOUND)
        try:
            ServiceOffresEmploi.delete(emploi)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la suppression de l'offre : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='cvs-classification')
    def cvs_classification(self, request, pk=None):
        try:
            offre = self.get_object()
            cvs = CV.objects.filter(offres=offre)
            cv_classes = CV_classe.objects.filter(cv__in=cvs)
            metier_propose = getattr(offre.metier_propose, 'nom', str(offre.metier_propose))
            results = []
            for cv_class in cv_classes:
                metier_score = None
                for m in cv_class.metiers:
                    if m['label'] == metier_propose:
                        metier_score = m['probability']
                        break
                results.append({
                    "cv_id": cv_class.cv.id,
                    "nom": getattr(cv_class.cv.owner, "nom", ""),
                    "prenom": getattr(cv_class.cv.owner, "prenom", ""),
                    "score_metier_propose": metier_score,
                    "metier_propose": metier_propose
                })
            return Response(results)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la classification des CVs : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='send-tests')
    def send_tests(self, request, pk=None):
        try:
            cv_offre_ids = request.data.get("cv_offre_ids", [])
            if not isinstance(cv_offre_ids, list) or not cv_offre_ids:
                return Response({"detail": "cv_offre_ids must be a non-empty list"}, status=400)

            for cv_offre_id in cv_offre_ids:
                try:
                    cv_offre = CV_Offre.objects.get(cv_id=cv_offre_id, offre_id=pk)
                except CV_Offre.DoesNotExist:
                    continue

                cv_offre.selected = True
                cv_offre.save()

                owner = cv_offre.cv.owner
                send_mail(
                    subject="Test à passer - Confirmation",
                    message=f"Bonjour {owner.prenom},\n\nVous avez été sélectionné pour passer un test.\nConnectez-vous à votre espace candidat.",
                    from_email="noreply@tondomaine.com",
                    recipient_list=[owner.email],
                    fail_silently=True,
                )

            return Response({"success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Erreur lors de l'envoi des tests : {e}"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='offres-selectionnees')
    def offres_selectionnees(self, request):
        try:
                user = request.user
                cv_offres = CV_Offre.objects.filter(cv__owner=user, selected=True).select_related('offre')
                results = []
                for cv_offre in cv_offres:
                    results.append({
                        "cv_offre_id": cv_offre.id,
                        "offre": OffresEmploiSerializer(cv_offre.offre).data,
                        "score": cv_offre.score,
                        "selected": cv_offre.selected,
                        "date": cv_offre.date,
                    })
                return Response(results)
        except Exception as e:
                return Response(
                    {"detail": f"Erreur lors de la récupération des offres sélectionnées : {e}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=True, methods=['get'], url_path='generate-qcm')
    def generate_qcm(self, request, pk=None):
        try:
            offre = OffresEmploi.objects.get(pk=pk)
        except OffresEmploi.DoesNotExist:
            return Response({"detail": "Offre introuvable"}, status=status.HTTP_404_NOT_FOUND)
        
        metier = offre.metier_propose
        prompt = (
            f"Tu es un expert RH. Génère-moi 10 questions QCM techniques sur le métier '{metier}'. "
            f"Pour chaque question, propose 4 réponses dont une seule correcte. "
            f"Réponds STRICTEMENT avec un tableau JSON (aucun mot avant ou après), exemple :\n"
            '[{"question": "...", "choices": ["...", "...", "...", "..."], "answer": "..."}, ...]'
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=900,
                temperature=0.6,
            )
            import json
            content = response.choices[0].message["content"]
            # Extrait ce qui ressemble à un tableau JSON
            start = content.find('[')
            end = content.rfind(']')
            json_str = content[start:end+1]
            try:
                questions = json.loads(json_str)
            except json.JSONDecodeError as e:
                # En DEV, utile de voir le JSON problématique (ne mets pas output_complet en prod)
                return Response(
                    {
                        "detail": f"Erreur lors du parsing JSON : {e}",
                        "json_recu": json_str,
                        "output_complet": content
                    },
                    status=500
                )
            # Ajoute les ids pour Angular
            for i, q in enumerate(questions):
                q['id'] = i+1
            return Response({"questions": questions}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"Erreur lors de la génération du QCM : {e}"}, status=500)

                    

    @action(detail=True, methods=['post'], url_path='store-score')
    def store_score(self, request, pk=None):
    
        user = request.user
        score = request.data.get('score')
        cv_offre_id = request.data.get('cv_offre_id')
        if not cv_offre_id:
            return Response({"detail": "cv_offre_id requis"}, status=400)
        try:
            cv_offre = CV_Offre.objects.get(id=cv_offre_id, offre_id=pk, cv__owner=user)
            cv_offre.score = score
            cv_offre.save()
            return Response({"success": True, "score": score}, status=200)
        except CV_Offre.DoesNotExist:
            return Response({"detail": "Candidature (CV_Offre) introuvable"}, status=404)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
        