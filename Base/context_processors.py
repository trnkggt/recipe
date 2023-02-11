from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user.profile, is_read=False).order_by('-timestamp')
    else:
        notifications = {}
    return {'notifications':notifications}