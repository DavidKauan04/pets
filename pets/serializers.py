from rest_framework import serializers
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from pets.models import GenderPets, Pet
from groups.models import Group
from traits.models import Trait

class PetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(choices=GenderPets.choices, default=GenderPets.DEFAULT)

    group = GroupSerializer()
    traits = TraitSerializer(many=True)

    def create(self, validated_data: dict):
        group_data  = validated_data.pop("group")
        traits_data = validated_data.pop("traits")
        
        group, boolean = Group.objects.get_or_create(**group_data)
        pet = Pet.objects.create(**validated_data, group=group)

        for trait in traits_data:
            x, boolean = Trait.objects.get_or_create(**trait)
            x.pet.add(pet)     

        return pet

    def update(self, inst: Pet, validated_data: dict):
        group_data  = validated_data.pop("group", None)
        traits_data = validated_data.pop("traits", None)

        if group_data:
            group, boolean = Group.objects.get_or_create(**group_data)
            inst.group = group

        if traits_data:
            trait_list = []
            for trait in traits_data:
                x, boolean = Trait.objects.get_or_create(**trait)
                trait_list.append(x)
            inst.traits.set(trait_list)

        for key, value in validated_data.items():
            setattr(inst, key, value)
        
        inst.save()

        return inst
