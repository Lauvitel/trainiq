from fastapi import FastAPI
from routes import auth
from db.database import Base, engine

# Créer les tables si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

app = FastAPI(title="TrainIQ Auth Service")

# Inclure les routes
app.include_router(auth.router)
