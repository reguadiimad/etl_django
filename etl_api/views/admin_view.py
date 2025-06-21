from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from ..models.admin import Admin,NewsLetterEmails
from ..serializers.admin_serializers import AdminSerializer, NewsLetterEmailsSerializer

import string


class AdminListCreateView(APIView):
    def get(self, request):
        admins = Admin.objects.all()
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminDeleteView(APIView):
    def delete(self, request, pk, format=None):
        admin = Admin.objects.filter(pk=pk).first()
        if admin:
            admin.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            admin = Admin.objects.get(email=email)
        except Admin.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, admin.password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(admin)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "admin": {
                "admin_id": admin.admin_id,
                "prenom": admin.prenom,
                "nom": admin.nom,
                "email": admin.email,
                "role": admin.role,
                "telephone": admin.telephone,
                "adresse": admin.adresse,
                "birthday": admin.birthday,
                "isSuperAdmin": admin.isSuperAdmin,
                "picture": admin.picture,
                "must_change_password": admin.must_change_password,
                "civilite": admin.civilite,
            }
        })


class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email', '').strip()

        try:
            admin = Admin.objects.get(email=email)
        except Admin.DoesNotExist:
            return Response({"detail": "Aucun compte trouvé avec cet email."}, status=status.HTTP_404_NOT_FOUND)

        temp_password = get_random_string(length=8, allowed_chars=string.ascii_letters + string.digits)
        
        # Save password
        admin.password = temp_password
        admin.must_change_password = True
        admin.save()

        # TEMPORARY: Debug print
        print("TEMP PASSWORD:", temp_password)

        subject = "Réinitialisation de votre mot de passe"
        message = f"""
Bonjour {admin.prenom},

Voici votre nouveau mot de passe temporaire : {temp_password}

Veuillez vous connecter et le changer immédiatement pour plus de sécurité.

Merci,
Équipe Support
        """
        send_mail(subject, message, None, [email])

        return Response({"detail": "Un nouveau mot de passe a été envoyé par email."}, status=status.HTTP_200_OK)


class AdminUpdateView(generics.UpdateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'admin_id'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def change_password(request, admin_id):
    admin = get_object_or_404(Admin, admin_id=admin_id)
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')

    if not current_password or not new_password:
        return Response(
            {"detail": "Both current_password and new_password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    if not check_password(current_password, admin.password):
        return Response(
            {"detail": "Mot de passe actuel incorrect."},
            status=status.HTTP_400_BAD_REQUEST
        )

    admin.password = new_password
    admin.must_change_password = False
    admin.save(update_fields=['password', 'must_change_password'])

    return Response({"detail": "Mot de passe mis à jour avec succès."}, status=status.HTTP_200_OK)




class NewsLetterEmailsListCreateAPIView(generics.ListCreateAPIView):
    queryset = NewsLetterEmails.objects.all()
    serializer_class = NewsLetterEmailsSerializer