from django.conf import settings

def school_name(request):
    return {'school_name': settings.SCHOOL_NAME}