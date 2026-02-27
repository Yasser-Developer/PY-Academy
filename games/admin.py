from django.contrib import admin
from .models import GameChallenge

@admin.register(GameChallenge)
class GameChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'xp_reward', 'difficulty', 'is_active')
    list_filter = ('difficulty', 'is_active')
    search_fields = ('title', 'description', 'instructions', 'hints')