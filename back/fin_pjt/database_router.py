class DatabaseRouter:
    def db_for_read(self, model, **hints):
        """읽기 작업에 사용할 데이터베이스 결정"""
        if model._meta.app_label == 'recommend':
            return 'secondary'  # 예금 및 적금 데이터는 secondary DB
        return 'default'  # 기본 데이터는 default DB

    def db_for_write(self, model, **hints):
        """쓰기 작업에 사용할 데이터베이스 결정"""
        if model._meta.app_label == 'recommend':
            return 'secondary'
        return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """마이그레이션 대상 데이터베이스 결정"""
        if app_label == 'recommend':
            # 예금 및 적금 데이터는 secondary DB에만 적용
            return db == 'secondary'
        else:
            # 유저 데이터는 default DB에만 적용
            return db == 'default'
