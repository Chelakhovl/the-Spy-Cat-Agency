from rest_framework import serializers
from .models import Mission, Target


class TargetSerializer(serializers.ModelSerializer):
    """Serializer for the Target model. Prevents editing completed targets."""

    class Meta:
        model = Target
        fields = ["id", "title", "country", "notes", "is_completed", "mission"]
        read_only_fields = ("mission",)

    def validate(self, data):
        if self.instance and self.instance.is_completed:
            raise serializers.ValidationError("Completed targets cannot be modified.")
        return data


class MissionSerializer(serializers.ModelSerializer):
    """Serializer for the Mission model with nested targets."""

    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ["id", "cat", "is_completed", "created_at", "targets"]
        read_only_fields = ("created_at",)

    def validate_targets(self, value):
        """Ensure mission has between 1 and 3 targets on creation."""
        if self.instance is None and not (1 <= len(value) <= 3):
            raise serializers.ValidationError(
                "A mission must have between 1 and 3 targets."
            )
        return value

    def validate(self, data):
        """Prevent updates if mission is assigned to a cat, except completion."""
        if self.instance and self.instance.cat:
            if "is_completed" in data and len(data.keys()) == 1:
                return data
            raise serializers.ValidationError(
                "Cannot modify a mission assigned to a spy cat."
            )
        return data

    def create(self, validated_data):
        """Create mission with nested targets."""
        targets_data = validated_data.pop("targets", [])
        mission = Mission.objects.create(**validated_data)
        Target.objects.bulk_create([Target(mission=mission, **t) for t in targets_data])
        return mission

    def update(self, instance, validated_data):
        """Update mission and nested targets if provided."""
        targets_data = validated_data.pop("targets", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if targets_data is not None:
            self._update_targets(instance, targets_data)

        return instance

    def _update_targets(self, mission, targets_data):
        """Handle target updates and prevent unwanted deletions."""
        existing_targets = {t.id: t for t in mission.targets.all()}
        for data in targets_data:
            target_id = data.get("id")
            if target_id and target_id in existing_targets:
                target = existing_targets[target_id]
                for attr, value in data.items():
                    setattr(target, attr, value)
                target.save()
            else:
                Target.objects.create(mission=mission, **data)
