from django.test import TestCase
from missions.models import Mission, Target
from cats.models import Cat
from missions.services import (
    complete_target,
    delete_mission_if_no_cat,
    mark_mission_completed_if_all_targets_done,
)


class MissionServicesTest(TestCase):
    def setUp(self):
        self.mission = Mission.objects.create()
        self.target1 = Target.objects.create(
            mission=self.mission, title="T1", country="US"
        )
        self.target2 = Target.objects.create(
            mission=self.mission, title="T2", country="UK"
        )

    def test_complete_target(self):
        target = complete_target(self.mission.id, self.target1.id)
        self.assertTrue(target.is_completed)

    def test_delete_mission_if_no_cat(self):
        result = delete_mission_if_no_cat(self.mission)
        self.assertTrue(result)
        self.assertEqual(Mission.objects.count(), 0)

    def test_delete_mission_with_cat_returns_false(self):
        cat = Cat.objects.create(
            name="Agent", years_of_experience=1, breed="Siberian", salary=1000
        )
        self.mission.cat = cat
        self.mission.save()

        result = delete_mission_if_no_cat(self.mission)

        self.assertFalse(result)
        self.assertEqual(Mission.objects.count(), 1)

    def test_mark_mission_completed_if_all_targets_done(self):
        complete_target(self.mission.id, self.target1.id)
        complete_target(self.mission.id, self.target2.id)
        result = mark_mission_completed_if_all_targets_done(self.mission)
        self.assertTrue(result)
        self.mission.refresh_from_db()
        self.assertTrue(self.mission.is_completed)
