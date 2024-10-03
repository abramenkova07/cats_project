from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from cats.models import Breed, Cat, Score


class BreedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Breed
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class CatSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    breed = serializers.SlugRelatedField(
        queryset=Breed.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Cat
        fields = (
            'name', 'color', 'age',
            'description', 'owner', 'breed', 'id'
        )
        read_only_fields = ('owner',)
        validators = [
            UniqueTogetherValidator(
                queryset=Cat.objects.all(),
                fields=('name', 'owner')
            )
        ]


class ScoreSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault(),
        source='owner'
    )

    class Meta:
        model = Score
        fields = ('user', 'score', 'cat', 'id')
        validators = [
            UniqueTogetherValidator(
                queryset=Score.objects.all(),
                fields=('cat', 'user')
            )
        ]

    def validate(self, data):
        request = self.context['request']
        if request.method == 'POST':
            if Cat.objects.filter(id=data.get('cat').id, owner=request.user):
                raise ValidationError('Нельзя поставить оценку своему котику.')
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context['request']
        serializer = CatSerializer(
            instance.cat,
            context={'request': request}
        )
        representation['cat'] = serializer.data
        return representation
