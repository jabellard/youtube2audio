'''
from .handlers import execute_delete_expired_texts
from .handlers import execute_sync_plans

COMMANDS = {
    'DELETE_EXPIRED_TEXTS': execute_delete_expired_texts,
    'SYNC_PLANS': execute_sync_plans,
}
'''
