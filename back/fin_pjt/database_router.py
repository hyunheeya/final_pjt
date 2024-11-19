class DatabaseRouter:
    def db_for_read(self, model, **hints):
        """읽기 작업을 위한 데이터베이스 지정"""
        if model._meta.db_table == 'deposit_table':
            return 'default'  # Deposit은 첫 번째 DB 사용
        elif model._meta.db_table == 'savings_table':
            return 'secondary'  # Savings는 두 번째 DB 사용
        return None

    def db_for_write(self, model, **hints):
        """쓰기 작업을 위한 데이터베이스 지정"""
        if model._meta.db_table == 'deposit_table':
            return 'default'
        elif model._meta.db_table == 'savings_table':
            return 'secondary'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """두 데이터베이스 간의 관계 허용 여부"""
        db_list = ('default', 'secondary')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """마이그레이션 허용 여부 설정 (여기선 사용하지 않음)"""
        return False
