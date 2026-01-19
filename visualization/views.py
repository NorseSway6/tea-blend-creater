import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from io import BytesIO
import base64
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from accounts.models import UserBlendInteraction, UserProfile
from main_functionality.models import Blend, Subtaste
from django.http import HttpResponse

matplotlib.use('Agg')

@login_required
def taste_radar_chart(request):
    user = request.user

    user_interactions = UserBlendInteraction.objects.filter(user=user)

    blend_ids = user_interactions.values_list('blend_id', flat=True).distinct()
    
    if not blend_ids:
        return render(request, 'radar_chart.html', {
            'has_data': False,
            'user': user,
        })

    user_blends = Blend.objects.filter(id__in=blend_ids)

    stats = {}
    for blend in user_blends:
        if blend.subtaste:
            subtaste_name = blend.subtaste.name
            stats[subtaste_name] = stats.get(subtaste_name, 0) + 1

    if not stats:
        return render(request, 'radar_chart.html', {
            'has_data': False,
            'user': user,
        })
    
    if len(stats) < 3:
        categories = list(stats.keys())
        values = list(stats.values())
    else:
        categories = list(stats.keys())
        values = list(stats.values())
    
    max_value = max(values) if values and max(values) > 0 else 1
    normalized_values = [v / max_value * 100 for v in values]
    
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    
    N = len(categories)
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    values_plot = normalized_values + normalized_values[:1]
    
    ax.plot(angles, values_plot, 'o-', linewidth=2, color='#2e7d32', markersize=8)

    ax.fill(angles, values_plot, alpha=0.1, color='#2e7d32')
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 110)
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=9)
    
    ax.set_title(f'Вкусовой профиль {user.username}', fontsize=16, fontweight='bold', pad=20)
    
    created_count = user_interactions.filter(created_by_user=True).count()
    saved_count = user_interactions.filter(saved=True).count()
    rated_count = user_interactions.filter(rating__isnull=False).count()
    
    legend_text = f"Создано: {created_count}, Сохранено: {saved_count}, Оценено: {rated_count}"
    ax.text(0.5, -0.15, legend_text, transform=ax.transAxes, 
            ha='center', fontsize=10, style='italic', color='gray')
    
    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    taste_data = []
    for i, (category, value) in enumerate(stats.items()):
        percentage = normalized_values[i] if i < len(normalized_values) else 0
        taste_data.append({
            'name': category,
            'count': value,
            'percentage': percentage,
        })
    
    taste_data.sort(key=lambda x: x['count'], reverse=True)
    
    return render(request, 'radar_chart.html', {
        'has_data': True,
        'chart_image': image_base64,
        'taste_data': taste_data,
        'user': user,
        'total_interactions': user_interactions.count(),
        'total_tastes': len(stats),
        'created_count': created_count,
        'saved_count': saved_count,
        'rated_count': rated_count,
    })


@login_required
def all_tastes_radar(request):
    blends_with_taste = Blend.objects.filter(subtaste__isnull=False)
    
    if not blends_with_taste.exists():
        return render(request, 'all_tastes.html', {
            'has_data': False,
        })
    
    stats = {}
    for blend in blends_with_taste:
        if blend.subtaste:
            taste_name = blend.subtaste.name
            stats[taste_name] = stats.get(taste_name, 0) + 1
    
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    
    top_stats = dict(sorted_stats[:10])
    
    categories = list(top_stats.keys())
    values = list(top_stats.values())

    max_value = max(values) if values else 1
    normalized_values = [v / max_value * 100 for v in values]

    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))

    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    values_plot = normalized_values + normalized_values[:1]

    ax.plot(angles, values_plot, 'o-', linewidth=2, color='#1976d2', markersize=8)
    ax.fill(angles, values_plot, alpha=0.1, color='#1976d2')
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 110)
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5, alpha=0.7)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'], fontsize=9)

    ax.set_title('Популярность вкусов (топ-10)', fontsize=16, fontweight='bold', pad=20)

    buffer = BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    plt.close()
    
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    taste_data = []
    for taste_name, count in sorted_stats:
        taste_data.append({
            'name': taste_name,
            'count': count,
        })
    
    return render(request, 'all_tastes.html', {
        'has_data': True,
        'chart_image': image_base64,
        'taste_data': taste_data,
        'top_tastes': taste_data[:10],
        'total_blends': blends_with_taste.count(),
        'total_tastes': len(stats),
    })