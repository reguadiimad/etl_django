from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from ..models.inscription import Inscription


class InscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscription
        fields = '__all__'
    def validate(self, attrs):
        # Prevent duplicate registrations by student name + school year
        nom = attrs.get('eleve_nom')
        prenom = attrs.get('eleve_prenom')
        school_year = attrs.get('school_year')
        if Inscription.objects.filter(
            eleve_nom__iexact=nom,
            eleve_prenom__iexact=prenom,
            school_year=school_year
        ).exists():
            raise serializers.ValidationError(
               f"L'élève que vous avez saisi est déjà inscrit pour l'année scolaire {school_year}. "
                "Vous pouvez modifier son inscription, enregistrer un autre enfant, ou fermer."
            )
        return attrs

    def to_internal_value(self, data):
        flat = {}

        # Date & School Year
        flat['date'] = data.get('date')
        flat['school_year'] = data.get('school_year')
        flat['confirmed']       = data.get('confirmed')
        flat['confirmed_by']    = data.get('confirmed_by')

        # Responsable
        responsable = data.get('responsable', {})
        flat['responsable_nom']       = responsable.get('nom')
        flat['responsable_prenom']    = responsable.get('prenom')
        flat['responsable_lien']      = responsable.get('lien')
        flat['responsable_email']     = responsable.get('email')
        flat['responsable_telephone'] = responsable.get('telephone')

        # Élève
        eleve = data.get('eleve', {})
        flat['eleve_nom']    = eleve.get('nom')
        flat['eleve_prenom'] = eleve.get('prenom')

        # Date de naissance: build YYYY-MM-DD from parts
        naissance = eleve.get('dateNaissance', {})
        if naissance:
            try:
                year  = int(naissance.get('annee'))
                month = int(naissance.get('mois'))
                day   = int(naissance.get('jour'))
                flat['eleve_date_naissance'] = f"{year}-{month:02d}-{day:02d}"
            except (TypeError, ValueError, KeyError):
                self.fail('invalid_dateNaissance')

        # Other fields
        flat['niveau_scolaire'] = eleve.get('niveauScolaire')
        flat['classe']          = eleve.get('classe')
        flat['institut']        = eleve.get('institut')
        flat['province']        = eleve.get('province')
       

        return super().to_internal_value(flat)

    def create(self, validated_data):
        # Save the record
        instance = super().create(validated_data)
        # Send confirmation email
        self.send_confirmation_email(instance)
        return instance

    def send_confirmation_email(self, inscription):
        to_email = inscription.responsable_email
        subject = "Confirmation de préinscription – Écoles La Tour Eiffel"
        message = (
            f"Bonjour {inscription.responsable_prenom} {inscription.responsable_nom},\n\n"
            f"Nous avons bien reçu la préinscription de votre enfant "
            f"{inscription.eleve_prenom} {inscription.eleve_nom} "
            f"pour l'année scolaire {inscription.school_year}.\n\n"
            f"Notre équipe des Écoles La Tour Eiffel traitera la demande "
            f"et vous contactera dans les plus brefs délais.\n\n"
            f"Merci pour votre confiance.\n\n"
            f"— Écoles La Tour Eiffel"
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )

    def to_representation(self, instance):
        # Format output JSON into nested structure
        return {
            "id": instance.id,
            "date": instance.date,
            "school_year": instance.school_year,
            "confirmed": instance.confirmed,
            "confirmed_by": instance.confirmed_by,
            "responsable": {
                "nom": instance.responsable_nom,
                "prenom": instance.responsable_prenom,
                "lien": instance.responsable_lien,
                "email": instance.responsable_email,
                "telephone": instance.responsable_telephone
            },
            "eleve": {
                "nom": instance.eleve_nom,
                "prenom": instance.eleve_prenom,
                "dateNaissance": {
                    "annee": instance.eleve_date_naissance.year,
                    "mois": instance.eleve_date_naissance.month,
                    "jour": instance.eleve_date_naissance.day
                },
                "niveauScolaire": instance.niveau_scolaire,
                "classe": instance.classe,
                "institut": instance.institut,
                "province": instance.province,
                
            }
        }
 