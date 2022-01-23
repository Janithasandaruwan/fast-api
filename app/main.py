from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import Settings
from fastapi.middleware.cors import CORSMiddleware

# Create engine
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#***********************************************************************************************************************

#Save post data in memory/ database
my_post = [{"id": 1, "title": "Sri Lanka", "content": "This is the content of the post1"},
           {"id": 2, "title": "America", "content": "This is the content of the post2"},
           {"id": 3, "title": "India", "content": "This is the content of the post3"}]

#Find post details by id
def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#Home page
@app.get("/")
def root():
    return {"message": "This is your home page!"}

