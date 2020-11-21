from django.db import models

class Pokemon(models.Model):
    poke_id = models.IntegerField()
    name = models.CharField(max_length = 50, unique=True )
    height = models.IntegerField()
    weight = models.IntegerField()

class Evolution(models.Model):
    poke_id = models.IntegerField()
    evolution_type = models.IntegerField()
    id_evolution = models.IntegerField()
    name = models.CharField(max_length= 50)
    
    class Meta:
        unique_together = (("poke_id", "id_evolution"),)

class Stats(models.Model):
    poke_id = models.IntegerField()
    stat_name = models.CharField(max_length = 50)
    stat_score = models.IntegerField()

    class Meta:
        unique_together = (("poke_id", "stat_name"),)