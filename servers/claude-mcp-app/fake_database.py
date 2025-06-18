# fake_database.py
class Database:
    """A mock database class for demonstration purposes."""
    
    @classmethod
    async def connect(cls):
        """Simulates connecting to a database."""
        print("Database connected")
        return cls()
    
    async def disconnect(self):
        """Simulates disconnecting from a database."""
        print("Database disconnected")
    
    def query(self):
        """Simulates a database query."""
        return "Query result from mock database"
