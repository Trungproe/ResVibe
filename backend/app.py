from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

# Import các router
from routes import (
    song_routes, user_routes, playlist_routes, albums_routes,
    artist_routes, history_songs_routes, recomment_routes,
    notifications_routes
)
from routes.admin_routes.song_admin_routes import router as admin_song_router
from routes.admin_routes.admin_artist_routes import router as admin_artist_router
from routes.admin_routes.admin_album_routes import router as admin_album_router
from routes.artist_request_routes import router as artist_request_router
from routes.master_artist_routes.artist_profile_routes import router as artist_profile_router
from routes.master_artist_routes.artist_song_routes import router as artist_song_router
from routes.master_artist_routes.artist_album_routes import router as artist_album_router
from routes.search_routes import router as search_routes
from routes import recommended_routes  # import router recommended đúng

load_dotenv()

app = FastAPI()

# Mount thư mục static audio
app.mount("/audio", StaticFiles(directory="audio"), name="audio")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3002"  # Thêm dòng này
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include các router với prefix tương ứng
app.include_router(song_routes.router, prefix="/api")
app.include_router(user_routes.router, prefix="/user")
app.include_router(recomment_routes.router, prefix="/api")
app.include_router(history_songs_routes.router)
app.include_router(playlist_routes.router, prefix="/api")
app.include_router(admin_artist_router, prefix="/api")
app.include_router(albums_routes.router, prefix="/api")
app.include_router(admin_song_router, prefix="/api")
app.include_router(artist_routes.router, prefix="/api")
app.include_router(admin_album_router, prefix="/api")
app.include_router(artist_request_router)
app.include_router(search_routes, prefix="/api")
app.include_router(notifications_routes.router)
app.include_router(recommended_routes.router, prefix="/api")  # router recommended

app.include_router(artist_profile_router, prefix="/api")
app.include_router(artist_song_router, prefix="/api")
app.include_router(artist_album_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "VibeSync API is running"}
