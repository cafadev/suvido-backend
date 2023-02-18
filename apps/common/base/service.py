from django.db.models import Model

class BaseService:

    model = Model

    @classmethod
    def get_active_records(_class, *args, **kwargs):
        return _class.model.objects.filter(is_active=True, **kwargs)
