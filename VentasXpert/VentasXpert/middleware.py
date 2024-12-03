from datetime import timedelta
from django.utils.timezone import now
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages  # Para mostrar mensajes al usuario
from django.urls import reverse  # Para generar la URL del login


class SessionTimeoutMiddleware:
    """
    Middleware para cerrar la sesión del usuario si está inactivo por demasiado tiempo.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Solo verifica usuarios autenticados
        if request.user.is_authenticated:
            # Obtén la última actividad del usuario desde la sesión
            last_activity = request.session.get('last_activity')

            # Si hay un registro previo, conviértelo de cadena a objeto datetime
            if last_activity:
                from django.utils.dateparse import parse_datetime
                last_activity = parse_datetime(last_activity)

            # Si no hay registro previo de actividad, inicializa con la hora actual
            if last_activity:
                # Calcula si ha pasado el tiempo máximo permitido
                session_expiry_time = now() - timedelta(seconds=900)  # 1 minuto de inactividad
                if last_activity < session_expiry_time:
                    # La sesión expiró: cerrar sesión y redirigir al login con un mensaje
                    logout(request)
                    messages.info(request, "Tu sesión ha expirado por inactividad.")  # Mensaje para el usuario
                    return redirect(reverse('login'))  # Redirige al login después del logout

            # Si no expiró, actualiza la última actividad como cadena serializable
            request.session['last_activity'] = now().isoformat()

        # Continuar con el procesamiento de la solicitud
        response = self.get_response(request)
        return response
