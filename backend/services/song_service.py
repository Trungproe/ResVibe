from bson import ObjectId
from datetime import datetime
from typing import List, Optional
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from random import shuffle

from models.song import SongCreate, SongUpdate, SongInDB
from database.repositories.song_repository import SongRepository
from database.repositories.artist_repository import ArtistRepository


class SongService:
    def __init__(self, song_repository: SongRepository, artist_repository: ArtistRepository):
        self.song_repository = song_repository
        self.artist_repository = artist_repository

    def _map_to_song_in_db(self, song: dict) -> SongInDB:
        artist_id = song.get("artistId")
        artist_name = ""
        if artist_id:
            artist = self.artist_repository.find_by_id(ObjectId(artist_id))
            artist_name = artist.get("name") if artist else ""

        return SongInDB(
            id=str(song.get("_id", "")),
            title=song.get("title", ""),
            artist=artist_name,
            album=song.get("album", ""),
            releaseYear=song.get("releaseYear", 0),
            duration=song.get("duration", 0),
            genre=song.get("genre", []),
            coverArt=song.get("coverArt"),
            audioUrl=song.get("audioUrl"),
            lyrics_lrc=song.get("lyrics_lrc"),
            artistId=str(artist_id) if artist_id else "",
            created_at=song.get("created_at", datetime.utcnow()),
            updated_at=song.get("updated_at", None)
        )

    @staticmethod
    def _is_url_accessible(url: str) -> bool:
        try:
            with urlopen(url, timeout=5) as response:
                return response.status == 200
        except (HTTPError, URLError):
            return False

    def get_all_songs(
        self,
        sort: Optional[str] = None,
        limit: Optional[int] = None,
        skip: Optional[int] = 0,
        query: Optional[dict] = None
    ) -> List[SongInDB]:
        songs = self.song_repository.find_all(sort=sort, limit=limit, skip=skip, query=query)
        return [self._map_to_song_in_db(song) for song in songs]

    def get_song_by_id(self, song_id: str) -> Optional[SongInDB]:
        song = self.song_repository.find_by_id(song_id)
        return self._map_to_song_in_db(song) if song else None

    def create_song(self, song_data: SongCreate) -> str:
        if not self.artist_repository.find_by_id(ObjectId(song_data.artistId)):
            raise ValueError(f"Artist with ID {song_data.artistId} does not exist")

        if song_data.audioUrl and not self._is_url_accessible(song_data.audioUrl):
            raise ValueError("Invalid or inaccessible audio URL")

        if song_data.coverArt and not self._is_url_accessible(song_data.coverArt):
            raise ValueError("Invalid or inaccessible cover art URL")

        new_song = song_data.dict(exclude_unset=True)
        new_song["artistId"] = str(new_song["artistId"])
        new_song["created_at"] = datetime.utcnow()
        new_song["updated_at"] = None

        return str(self.song_repository.insert(new_song))

    def update_song(self, song_id: str, song_data: SongUpdate) -> bool:
        update_data = song_data.dict(exclude_unset=True)

        if "artistId" in update_data:
            if not self.artist_repository.find_by_id(ObjectId(update_data["artistId"])):
                raise ValueError(f"Artist with ID {update_data['artistId']} does not exist")
            update_data["artistId"] = str(update_data["artistId"])

        if update_data.get("audioUrl") and not self._is_url_accessible(update_data["audioUrl"]):
            raise ValueError("Invalid or inaccessible audio URL")

        if update_data.get("coverArt") and not self._is_url_accessible(update_data["coverArt"]):
            raise ValueError("Invalid or inaccessible cover art URL")

        update_data["updated_at"] = datetime.utcnow()
        return self.song_repository.update(song_id, update_data)

    def delete_song(self, song_id: str) -> bool:
        return self.song_repository.delete(song_id)

    def get_random_songs(self, limit: int = 10, region: Optional[str] = None) -> List[SongInDB]:
        raw_songs = self.song_repository.get_random_songs(limit=limit * 3)

        if region:
            is_vietnamese = region.lower() == "vietnamese"
            raw_songs = [
                s for s in raw_songs
                if any("vietnamese" in g.lower() for g in s.get("genre", [])) == is_vietnamese
            ]

        shuffle(raw_songs)
        return [self._map_to_song_in_db(song) for song in raw_songs[:limit]]

    def get_songs_by_region(self, region: str, limit: int = 12) -> List[SongInDB]:
        raw_songs = self.song_repository.get_random_songs_by_region(region=region, limit=limit)
        return [self._map_to_song_in_db(song) for song in raw_songs]

    def get_random_songs_by_region(self, region: Optional[str], limit: int = 12) -> List[SongInDB]:
        raw_songs = self.song_repository.get_random_songs_by_region(region=region, limit=limit)
        return [self._map_to_song_in_db(song) for song in raw_songs]

    def get_songs_by_genre(self, genre: str, page: int = 1, limit: int = 50) -> List[SongInDB]:
        if not genre:
            raise ValueError("Genre is required")
        songs = self.song_repository.find_by_genre(genre, page, limit)
        return [self._map_to_song_in_db(song) for song in songs]
