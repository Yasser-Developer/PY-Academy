from django.contrib import admin
from .models import GameChallenge

@admin.register(GameChallenge)
class GameChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'xp_reward')