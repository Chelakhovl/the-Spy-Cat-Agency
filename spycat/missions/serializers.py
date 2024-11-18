from rest_framework import serializers
from .models import Mission, Target

class TargetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Target model.
    Handles validation to ensure that completed targets cannot be modified.
    """

    class Meta:
        model = Target
        fields = '__all__'
        read_only_fields = ('mission',)

    def validate(self, data):
        """
        Validates that a completed target cannot be modified.
        """
        if self.instance and self.instance.is_completed:
            raise serializers.ValidationError("Completed targets cannot be modified.")
        return data


class MissionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Mission model.
    Validates the number of targets and prevents updates for missions with an assigned spy cat.
    """
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = '__all__'

    def validate_targets(self, value):
        """
        Validates that a mission must have between 1 and 3 targets.
        """
        if len(value) < 1 or len(value) > 3:
            raise serializers.ValidationError("A mission must have between 1 and 3 targets.")
        return value

    def validate(self, data):
        """
        Validates that a mission cannot be updated if it has an assigned spy cat.
        """
        if self.instance and self.instance.cat:
            raise serializers.ValidationError("Cannot modify a mission assigned to a spy cat.")
        return data

    def create(self, validated_data):
        """
        Creates a new mission along with its associated targets.
        """
        targets_data = validated_data.pop('targets', [])
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance, validated_data):
        """
        Updates an existing mission and its associated targets.
        """
        targets_data = validated_data.pop('targets', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        existing_targets = {target.id: target for target in instance.targets.all()}
        for target_data in targets_data:
            target_id = target_data.get('id')
            if target_id and target_id in existing_targets:
                target = existing_targets.pop(target_id)
                for attr, value in target_data.items():
                    setattr(target, attr, value)
                target.save()
            else:
                Target.objects.create(mission=instance, **target_data)

        for target in existing_targets.values():
            target.delete()

        return instance
