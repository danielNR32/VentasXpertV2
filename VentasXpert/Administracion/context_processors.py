from datetime import datetime
from Usuarios_permisos.models import Categoria

def categorias_context(request):
    return {'categorias': Categoria.objects.all()}

def add_timestamp(request):
    return {
        'timestamp': datetime.now().timestamp(),
    }
