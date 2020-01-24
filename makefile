do_all:
		make -j 2 celery_beat celery_worker 
#redis:
#		redis-server
celery_beat:
			celery -A periodic beat -l info --pidfile=/tmp/celeryd.pid
celery_worker:
			celery -A periodic worker 
#bot:
	#python bot.py