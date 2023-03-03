from django.shortcuts import render

# Create your views here.
from django.forms.models import model_to_dict
from rest_framework.views import APIView, Request, Response, status
from .models import Pet
from .serializers import PetSerializer
from django.shortcuts import get_object_or_404

class PetView(APIView):
    def get(self, req: Request):
        pets = Pet.objects.all()
        serializer = PetSerializer(pets, many=True)

        return Response(serializer.data)

    def post(self, req: Request):
        serializer = PetSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class PetDetailView(APIView):
    def get(self, req: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(pet)

        return Response(serializer.data)

    def patch(self, req: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)

        serializer = PetSerializer(pet, data=req.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, req: Request, pet_id: int):
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)