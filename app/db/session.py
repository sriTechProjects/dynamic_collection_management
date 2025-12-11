# app/db/session.py
import logging
import certifi
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None

    def connect(self):
        """
        Create the connection to MongoDB Atlas with SSL Certificate fix.
        """
        try:
            self.client = AsyncIOMotorClient(
                settings.MONGO_URL,
                maxPoolSize=100,
                minPoolSize=10,
                tlsCAFile=certifi.where() # Fixes the SSL Handshake error
            )
            logger.info("✅ Connected to MongoDB Atlas")
        except Exception as e:
            logger.error(f"❌ Could not connect to MongoDB: {e}")
            raise e

    def close(self):
        """Close the connection pool on shutdown."""
        if self.client:
            self.client.close()
            logger.info("Connection closed.")

    def getMasterDB(self):
        """
        Returns the Database object for Master Metadata.
        """
        return self.client[settings.MASTER_DB_NAME]
    
    def get_tenant_collection(self, collection_name: str):
        """
        Returns the Collection object for a specific tenant.
        This was missing and caused your error!
        """
        return self.client[settings.MASTER_DB_NAME][collection_name]

# Create a single instance to be imported elsewhere
db = Database()