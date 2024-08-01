from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from src.db import Base
from src.db import engine
from src.routers.routers_command import router as router_command
from src.routers.routers_residents import router as router_resident
from src.routers.routers_blogs import router as router_article
from src.routers.routers_tariffs import router as router_tariff
from src.routers.routers_space import router as router_space
from src.routers.routers_faq import router as router_faq
from src.routers.router_translation import router as router_translation
from src.routers.routers_cards_blog import router as router_cards_blog
from src.routers.routers_user import router as router_user


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Collabrium")

app.include_router(router=router_command)
app.include_router(router=router_resident)
app.include_router(router=router_article)
app.include_router(router=router_tariff)
app.include_router(router=router_space)
app.include_router(router=router_faq)
app.include_router(router=router_translation)
app.include_router(router=router_cards_blog)
app.include_router(router=router_user)




app.mount("/static", StaticFiles(directory="static"), name="static")