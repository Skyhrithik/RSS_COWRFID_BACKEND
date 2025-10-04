import json, time
from queue import Queue, Empty
from threading import Lock
from django.http import StreamingHttpResponse

HEARTBEAT_SECONDS = 10

class _Broadcaster:
    def __init__(self):
        self._clients = []
        self._lock = Lock()

    def subscribe(self) -> Queue:
        q = Queue()
        with self._lock:
            self._clients.append(q)
        return q

    def unsubscribe(self, q: Queue):
        with self._lock:
            if q in self._clients:
                self._clients.remove(q)

    def publish(self, message: dict):
        with self._lock:
            for q in list(self._clients):
                q.put(message)

broadcaster = _Broadcaster()

def _event_stream():
    q = broadcaster.subscribe()
    try:
        yield ": connected\n\n"
        last = time.time()
        while True:
            try:
                data = q.get(timeout=1)
                yield f"data: {json.dumps(data)}\n\n"
                last = time.time()
            except Empty:
                now = time.time()
                if now - last >= HEARTBEAT_SECONDS:
                    yield f": ping {int(now)}\n\n"
                    last = now
    finally:
        broadcaster.unsubscribe(q)

def stream_scans(request):
    resp = StreamingHttpResponse(_event_stream(), content_type='text/event-stream')
    resp['Cache-Control'] = 'no-cache'
    resp['X-Accel-Buffering'] = 'no'
    resp['Access-Control-Allow-Origin'] = '*'          # dev-friendly; lock down in prod
    resp['Access-Control-Allow-Credentials'] = 'false'
    return resp
