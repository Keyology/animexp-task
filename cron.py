from crontab import CronTab


cron = CronTab(user=True)
job = cron.new(command='python task.py', comment='task')
job.dow.on('FRI')
cron.write()
job.enable()