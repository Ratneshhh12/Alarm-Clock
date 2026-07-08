import asyncio
import asyncpg
from app.config import settings

async def create_database_if_not_exists():
    # Parse the DATABASE_URL to get credentials, host, and port
    # Standard format: postgresql+asyncpg://user:pass@host:port/dbname
    db_url = settings.DATABASE_URL
    if "+asyncpg" in db_url:
        connection_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    else:
        connection_url = db_url

    # Split connection URL to connect to the default 'postgres' database first
    base_url, db_name = connection_url.rsplit("/", 1)
    postgres_default_url = f"{base_url}/postgres"

    print(f"Connecting to default database to verify/create '{db_name}'...")
    try:
        # Connect to 'postgres' default database
        conn = await asyncpg.connect(postgres_default_url)
    except Exception as e:
        print(f"Failed to connect to PostgreSQL: {e}")
        print("\nPlease make sure PostgreSQL is running, and that the credentials (username/password) in the .env file match your local PostgreSQL server.")
        return False

    try:
        # Check if database already exists
        exists = await conn.fetchval(
            "SELECT 1 FROM pg_database WHERE datname = $1", db_name
        )
        if not exists:
            # CREATE DATABASE cannot be run in a transaction block
            # asyncpg connection by default is not in a transaction unless specified,
            # but we can execute it directly.
            await conn.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists.")
        await conn.close()
        return True
    except Exception as e:
        print(f"Error checking or creating database: {e}")
        await conn.close()
        return False

if __name__ == "__main__":
    asyncio.run(create_database_if_not_exists())
