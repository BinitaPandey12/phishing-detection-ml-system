import os

bind = "0.0.0.0:" + os.environ.get("PORT", "5000")

worker_class = "gthread"
workers = 1
threads = int(os.environ.get("WEB_CONCURRENCY_THREADS", "4"))

timeout = 180
graceful_timeout = 30
keepalive = 5

accesslog = "-"
errorlog = "-"
loglevel = "info"
