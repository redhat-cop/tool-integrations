from flask import Flask, request
import sys
import threading
import datetime
import logging


class WebHook:
    class __WebHook:
        def __init__(self, port):
            self.app = Flask(__name__)
            self.port = port
            cli = sys.modules['flask.cli']
            cli.show_server_banner = lambda *x: None
            self.app.logger.disabled = True
            log = logging.getLogger('werkzeug')
            log.disabled = True

        def __str__(self):
            return repr(self)

        def add(self, name, route, job):
            self.app.add_url_rule(route, route, self.__wrap_job(name, job), methods=["GET", "POST"])

        def __wrap_job(self, name, job):
            def wrapped_job():
                print(f"Webhook handler is executing task {name} at {datetime.datetime.now()}")
                try:
                    if hasattr(request, "json") and request.json:
                        value = job(context=dict(request.json))
                    else:
                        value = job(context=dict(request.values))
                    if isinstance(value, str) or isinstance(value, tuple):
                        return value
                    else:
                        return "OK"
                except Exception as e:
                    print(f"Error processing webhook trigger: {e}")
                    return "There was an error processing the request. Please see server logs for details.", 500
            return wrapped_job

        def listener(self):
            self.app.run(port=self.port, host="0.0.0.0", debug=False, use_reloader=False)

        def listen(self):
            listener = threading.Thread(name='Webhook Listener', target=self.listener)
            listener.setDaemon(True)
            listener.start()

    instance = None

    def __init__(self, port=5000):
        if not WebHook.instance:
            WebHook.instance = WebHook.__WebHook(port)
        else:
            WebHook.instance.port = port

    def __getattr__(self, name):
        return getattr(self.instance, name)

