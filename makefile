do_all:
		make -j 4 packages redis celery_beat celery_worker bot
packages:	
		pip3 install -r requirements.txt
redis:
		redis-server
celery_beat:
			celery -A periodic beat
celery_worker:
			celery -A periodic worker
bot:
	python bot.py