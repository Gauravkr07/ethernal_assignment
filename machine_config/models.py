from django.db import models

class Machine(models.Model):
    name = models.CharField(max_length=255, unique=True)
    feedrate = models.FloatField()
    max_acceleration = models.FloatField()
    max_velocity = models.FloatField()
    acceleration = models.FloatField()
    angular_units = models.FloatField()
    velocity = models.FloatField()

class MachineData(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    actual_position_x = models.FloatField()
    actual_position_y = models.FloatField()
    actual_position_z = models.FloatField()
    actual_position_a = models.FloatField()
    actual_position_c = models.FloatField()
    distance_to_go_x = models.FloatField()
    distance_to_go_y = models.FloatField()
    distance_to_go_z = models.FloatField()
    distance_to_go_a = models.FloatField()
    distance_to_go_c = models.FloatField()
    homed_x = models.BooleanField()
    homed_y = models.BooleanField()
    homed_z = models.BooleanField()
    homed_a = models.BooleanField()
    homed_c = models.BooleanField()
    tool_offset_x = models.FloatField()
    tool_offset_y = models.FloatField()
    tool_offset_z = models.FloatField()
    tool_offset_a = models.FloatField()
    tool_offset_c = models.FloatField()

    class Meta:
        unique_together = ('machine', 'timestamp')
