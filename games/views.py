from django.shortcuts import render, get_object_or_404
from .models import GameChallenge
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import sys
from io import StringIO


def game_list(request):
    games = GameChallenge.objects.all()
    return render(request, 'games/game_list.html', {'games': games})


def game_detail(request, game_id):
    game = get_object_or_404(GameChallenge, pk=game_id)
    return render(request, 'games/game_detail.html', {'game': game})


@require_POST
def run_game_code(request, game_id):
    code = request.POST.get('code', '')
    game = get_object_or_404(GameChallenge, pk=game_id)

    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()

    try:
        exec(code)
        output = redirected_output.getvalue()
        success = True
    except Exception as e:
        output = str(e)
        success = False
    finally:
        sys.stdout = old_stdout

    # اگر موفق بود، XP بده (فقط یک بار برای هر بازی)
    if success and not request.user.completed_games.filter(game=game).exists():
        from .models import CompletedGame  # بعداً مدل رو اضافه می‌کنیم
        CompletedGame.objects.create(user=request.user, game=game, xp_earned=game.xp_reward)
        request.user.xp += game.xp_reward
        request.user.save()

    return JsonResponse({'output': output, 'success': success})