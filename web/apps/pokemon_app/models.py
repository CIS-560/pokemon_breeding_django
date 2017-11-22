from django.db import models

# https://stackoverflow.com/questions/41972589/django-model-primary-key-as-a-pair


class Pokemon(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15)
    description = models.CharField(max_length=1000)
    is_evolved = models.BooleanField(default=False)


class Type(models.Model):
    type_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

# on delete cascade?


class PokeType(models.Model):
    poke_number = models.ManyToManyField(Pokemon)
    # pokemon can have up to two types
    # types can have lots of pokemon associated with them
    type_num = models.ManyToManyField(Type)

    class Meta:
        unique_together("poke_number", "type_num")


class Moves(models.Model):
    move_num = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

# has two primary keys


class LevelUpMoves(models.Model):
    # a pokemon can have many levelupmoves that it can learn
    # a levelupmove can be tied to many pokemon (some can learn same moves)
    poke_number = models.ManyToManyField(Pokemon)

    # unsure about this one, diagram says many-to-many
    # but I would assume one-to-one
    # a move has one number associated with it
    # many to many. one to one. or many to one?
    move_num = models.ManyToManyField(Moves)
    level = models.IntegerField()  # this doesn't need to be unique

    class Meta:
        unique_together("poke_number", "move_num")

# this one also has two primary keys


class EggMoves(models.Model):
    poke_number = models.ManyToManyField(Pokemon)

    # I am also not sure about this one too
    # i would assume it is one-to-one but the E/R diagram suggests many-to-many
    move_num = models.ManyToManyField(Moves)

    class Meta:
        unique_together("poke_number", "move_num")


class PokeGender(models.Model):
    # a pokemon can have many genders
    # a gender can have many pokemons associated to it
    poke_number = models.ManyToManyField(Pokemon, primary_key=True)

    GENDERS = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('X', 'Genderless'),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)


class EggGroup(models.Model):
    name = models.CharField(max_length=15, primary_key=True)
    can_breed = models.BooleanField(default=False)


class PokeEggGroup(models.Model):
    poke_number = models.ManyToManyField(Pokemon)
    name = models.ManyToManyField(EggGroup)

    class Meta:
        unique_together("poke_number", "name")


class User(models.Model):
    username = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=15)


class HistoryTrios(models.Model):
    # id field is automatically generated by django :)

    # users can make many HistoryTrios
    # but a historyTrio can only be associated with one user
    username = models.ForeignKey(User)

    # should these pokemon be many-to-many or many-to-one
    parent1 = models.ForeignKey(Pokemon)
    parent2 = models.ForeignKey(Pokemon)
    child = models.ForeignKey(Pokemon)

    # relation on these?
    parent_level_up_move = models.ForeignKey(Moves)
    child_egg_move = models.ForeignKey(Moves)
