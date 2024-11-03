from datetime import datetime

def add_timestamp(request):
    return {
        'timestamp': datetime.now().timestamp(),
    }
