"""
Supabase client configuration
Supports both real Supabase and mock client for local testing
"""

try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

from functools import lru_cache
from app.config import get_settings

settings = get_settings()

if not SUPABASE_AVAILABLE:
    # Mock implementation for local testing
    class MockSupabaseClient:
        def __init__(self, url, key):
            self.url = url
            self.key = key
            self.auth = MockAuth()
            self.storage = MockStorage()

    class MockAuth:
        def get_user(self, token):
            return MockUserResponse()
        def sign_out(self):
            pass

    class MockUserResponse:
        def __init__(self):
            import uuid
            from datetime import datetime
            self.user = type('User', (), {
                'id': str(uuid.uuid4()),
                'email': 'local@testing.com',
                'user_metadata': {'name': 'Local User', 'role': 'admin'},
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            })()

    class MockStorage:
        def from_(self, bucket):
            return MockBucket()

    class MockBucket:
        def upload(self, path, file, file_options=None):
            return {'path': path}
        def get_public_url(self, path):
            return f'http://localhost:8000/files/{path}'
        def remove(self, paths):
            return True

    def create_client(url, key):
        return MockSupabaseClient(url, key)


@lru_cache()
def get_supabase_client():
    """Get Supabase client with anon key"""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)


@lru_cache()
def get_supabase_admin_client():
    """Get Supabase client with service role key (admin access)"""
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
