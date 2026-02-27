from django.db import models

class GameChallenge(models.Model):
    title = models.CharField(max_length=200, verbose_name="نام بازی")
    description = models.TextField(verbose_name="توضیح کوتاه")
    xp_reward = models.PositiveIntegerField(default=50, verbose_name="امتیاز جایزه")

    def __str__(self):
        return self.title
    
    
class CompletedGame(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='completed_games')
    game = models.ForeignKey(GameChallenge, on_delete=models.CASCADE)
    xp_earned = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return f"{self.user.username} - {self.game.title}"