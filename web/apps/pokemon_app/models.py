from django.db import models
from django.conf import settings

class Type(models.Model):
    type_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

class Moves(models.Model):
    move_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

class EggGroup(models.Model):
    name = models.CharField(max_length=15, primary_key=True)
    can_breed = models.BooleanField(default=False)

class Pokemon(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=1000)
    is_evolved = models.BooleanField(default=False)
    type = models.ManyToManyField(Type)
    female_ratio = models.FloatField(default= 0) 
    male_ratio = models.FloatField(default= 0) 
    picture = models.CharField(max_length=100, default='picture')
    level_up_moves = models.ManyToManyField(Moves, through='LevelUpMove')
    egg_moves = models.ManyToManyField(Moves, related_name='%(class)s_egg_move')
    egg_groups = models.ManyToManyField(EggGroup)

class PokemonType(models.Model):
    #id auto-generated
    poke_num = models.ForeignKey(Pokemon)
    type_num = models.ForeignKey(Type)

#this is an example of an intermediate table in django, 
#it refers to the instace of specifc pokemon, levelup_move
#and it provides additional information about Level_move
class LevelUpMove(models.Model):
    pokemon = models.ForeignKey(Pokemon)
    move = models.ForeignKey(Moves)
    level = models.IntegerField()  # this doesn't need to be unique

class HistoryTrios(models.Model):
    # id field is automatically generated by django :)

    # users can make many HistoryTrios
    # but a historyTrio can only be associated with one user
    username = models.ForeignKey(settings.AUTH_USER_MODEL)

    # should these pokemon be many-to-many or many-to-one
    parent1 = models.ForeignKey(Pokemon, related_name='%(class)s_parent_1')
    parent2 = models.ForeignKey(Pokemon, related_name='%(class)s_parent_2')
    child = models.ForeignKey(Pokemon, related_name='%(class)s_child')

    # relation on these?
    parentmove = models.ForeignKey(LevelUpMove)
    childmove = models.ForeignKey(Moves) 
