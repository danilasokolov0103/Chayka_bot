do_all:
		make -j 4  redis celery_beat celery_worker bot
redis:
		redis-server
celery_beat:
			celery -A periodic beat
celery_worker:
			celery -A periodic worker
bot:
	python bot.py