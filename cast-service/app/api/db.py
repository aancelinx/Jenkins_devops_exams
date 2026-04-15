# Version simplifiée - pas de base de données
database = None
engine = None
metadata = None

# Mock des tables pour éviter les erreurs d'import
class MockTable:
    pass

casts = MockTable()
movies = MockTable()

def create_engine(*args, **kwargs):
    return None
