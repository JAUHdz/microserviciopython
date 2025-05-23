from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


SQLALCHEMY_DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_LlSOxqCg5PMIKPX6JPu@mysql-19a77c38-uttt-944e.j.aivencloud.com:12364/logistica"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Al final del archivo database.py
if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        print("✅ Conexión a la base de datos exitosa.")
    except Exception as e:
        print("❌ Error al conectar a la base de datos:")
        print(e)
