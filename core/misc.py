from datetime import datetime

STABLE_QUEUE = []
STABLE_XL_QUEUE = []
DALLE_QUEUE = []
VS_QUEUE = []
SM_QUEUE = []
SA_QUEUE = []

def curTime() -> str:
    now = datetime.now()
    return str(now.strftime("%I:%M:%S %p"))

