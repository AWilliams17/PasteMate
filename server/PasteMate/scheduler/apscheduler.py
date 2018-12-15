from apscheduler.schedulers.background import BackgroundScheduler as _BaseAPScheduler


class APScheduler(_BaseAPScheduler):
    """ Subclass of APScheduler which uses application context for adding jobs. """
    app = None

    def __init__(self, app, gconfig={}, **options):
        self.app = app
        super().__init__(gconfig=gconfig, options=options)

    def add_job(self, func, **kwargs):
        with self.app.app_context():
            super().add_job(func, **kwargs)

    @classmethod
    def generate_config(cls, app):
        """ APScheduler's add_jobstore method leads to a massive headache, so I'm doing to do it this way. """
        return {
            'apscheduler.jobstores.default': {
                'type': 'sqlalchemy',
                'url': app.config['SQLALCHEMY_DATABASE_URI']
            },
            'apscheduler.executors.default': {
                'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
                'max_workers': '20'
            },
            'apscheduler.executors.processpool': {
                'type': 'processpool',
                'max_workers': '5'
            },
            'apscheduler.job_defaults.coalesce': 'false',
            'apscheduler.job_defaults.max_instances': '3',
            'apscheduler.timezone': 'UTC',
        }
