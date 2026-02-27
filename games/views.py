from django.shortcuts import render, get_object_or_404
from .models import GameChallenge
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import CompletedGame
from .safe_runner import run_user_code


def game_list(request):
    games = GameChallenge.objects.all()
    return render(request, 'games/game_list.html', {'games': games})


def game_detail(request, game_id):
    game = get_object_or_404(GameChallenge, pk=game_id)
    return render(request, 'games/game_detail.html', {'game': game})


@require_POST
@login_required
def run_game_code(request, game_id):
    code = request.POST.get('code', '')
    game = get_object_or_404(GameChallenge, pk=game_id)

    result = run_user_code(code, timeout_seconds=2)

    # اگر موفق بود، XP بده (فقط یک بار برای هر بازی)
    xp_awarded = False
    if result.success and not request.user.completed_games.filter(game=game).exists():
        CompletedGame.objects.create(user=request.user, game=game, xp_earned=game.xp_reward)
        request.user.add_xp(game.xp_reward)
        xp_awarded = True

    return JsonResponse(
        {
            'output': result.output,
            'success': result.success,
            'xp_awarded': xp_awarded,
            'xp_amount': game.xp_reward if xp_awarded else 0,
        }
    )
