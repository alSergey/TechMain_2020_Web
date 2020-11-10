from app.models import Tag, Profile


def popular_tags_users(request):
    return {
        'best_tags': Tag.objects.popular_tags(),
        'best_users': Profile.objects.popular_users(),

    }
