from abc import ABC, abstractmethod

class MusicContent(ABC):
    def __init__(self):
        self._track_list = []
        
    def add_track(self, track):
        self._track_list.append(track)

    def get_track_list(self):
        return self._track_list


class Band:
    def __init__(self, name, genre):
        self._name = name
        self._genre = genre
        self._albums = []

    def add_album(self, album):
        self._albums.append(album)

    def get_name(self):
        return self._name

    def get_genre(self):
        return self._genre

    def get_albums(self):
        return self._albums

    def str(self):
        return f"{self._name} ({self._genre})"


class Track:
    def __init__(self, name, length, band):
        self._name = name
        self._length = length
        self._band = band

    def get_name(self):
        return self._name

    def get_length(self):
        return self._length

    def get_band(self):
        return self._band

    def __str__(self):
        return f"{self._name} by {self._band.get_name()} ({self._length} min)"

    @staticmethod
    def search_track_by_name(track_name, albums):
        found_tracks = []
        for album in albums:
            for track in album.get_track_list():
                if track.get_name() == track_name:
                    found_tracks.append(track)
        return found_tracks


class Album(MusicContent):
    def __init__(self, title, release_year, band):
        super().__init__()
        self._title = title
        self._release_year = release_year
        self._band = band
        self._ratings = []
        self._track_order = {}

    def add_track(self, track):
        current_position = len(self.get_track_list()) + 1 
        super().add_track(track)
        self._track_order[track.get_name()] = current_position

    def get_title(self):
        return self._title

    def get_release_year(self):
        return self._release_year
    
    def get_band(self):
        return self._band

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self._ratings.append(rating)
        else:
            raise ValueError("Rating must be between 1 and 5")

    def calculate_average_rating(self):
        if len(self._ratings) == 0:
            return 0
        return sum(self._ratings) / len(self._ratings)


class Playlist(MusicContent):
    def __init__(self, playlist_title):
        super().__init__()
        self._playlist_title = playlist_title
        self._tags = []
        self._comments = []
        self._likes = set()

    def get_playlist_title(self):
        return self._playlist_title

    def set_playlist_title(self, new_title):
        self._playlist_title = new_title

    def remove_track(self, track):
        if track in self._track_list:
            self._track_list.remove(track)
        else:
            raise ValueError("Track not found in playlist")

    @staticmethod
    def merge_playlists(playlist1, playlist2, new_title):
        merged_playlist = Playlist(new_title)
        track_names = {track.get_name() for track in playlist1.get_track_list()}

        for track in playlist1.get_track_list():
            merged_playlist.add_track(track)

        for track in playlist2.get_track_list():
            if track.get_name() not in track_names:
                merged_playlist.add_track(track)

        return merged_playlist

    def add_tag(self, tag):
        self._tags.append(tag)

    def get_tags(self):
        return self._tags

    def add_comment(self, user, comment):
        self._comments.append((user.get_username(), comment))

    def get_comments(self):
        return self._comments

    def add_like(self, user):
        self._likes.add(user.get_username())

    def get_like_count(self):
        return len(self._likes)

    def get_interactions(self):
        return {
            "comments": self.get_comments(),
            "likes": self.get_like_count()
        }

class UserContent:
    def __init__(self):
        self._user_comments = []
        self._likes = set()

    def add_comment(self, user, comment):
        self._user_comments.append((user.get_username(), comment))

    def add_like(self, user):
        self._likes.add(user.get_username())

    def get_interactions(self):
        return {
            'likes': len(self._likes),
            'comments': self._user_comments
        }


class Playlist(MusicContent):
    def __init__(self, playlist_title):
        super().__init__()
        self._playlist_title = playlist_title

    def get_playlist_title(self):
        return self._playlist_title

    def set_playlist_title(self, new_title):
        self._playlist_title = new_title

    def add_track(self, track):
        super().add_track(track)

    def remove_track(self, track):
        if track in self._track_list:
            self._track_list.remove(track)
        else:
            raise ValueError("Track not found in playlist")
        
    @staticmethod
    def merge_playlists(playlist1, playlist2, new_title):
        merged_playlist = CustomPlaylist(new_title)
        track_names = {track.get_name() for track in playlist1.get_track_list()}

        for track in playlist1.get_track_list():
            merged_playlist.add_track(track)

        for track in playlist2.get_track_list():
            if track.get_name() not in track_names:
                merged_playlist.add_track(track)
                track_names.add(track.get_name())

        return merged_playlist


class CustomPlaylist(Playlist):
    def __init__(self, playlist_title):
        super().__init__(playlist_title)
        self._tags = []
        self._comments = []
        self._likes = set()

    def add_tag(self, tag):
        self._tags.append(tag)

    def get_tags(self):
        return self._tags

    def add_comment(self, user, comment):
        self._comments.append((user.get_username(), comment))

    def get_comments(self):
        return self._comments

    def add_like(self, user):
        self._likes.add(user.get_username())

    def get_like_count(self):
        return len(self._likes)

    def get_interactions(self):
        return {
            "comments": self.get_comments(),
            "likes": self.get_like_count()
        }
    

class User:
    def __init__(self, username):
        self._username = username
        self._ratings = []

    def rate_album(self, album, rating):
        album.add_rating(rating)
        self._ratings.append((album.get_title(), rating))

    def get_username(self):
        return self._username

    def create_playlist(self, playlist_title):
        return CustomPlaylist(playlist_title)


class MusicService:
    def __init__(self):
        self._albums = []
        self._users = []
        self._playlists = {}

    def add_album(self, album):
        self._albums.append(album)

    def get_album_by_title(self, title):
        for album in self._albums:
            if album.get_title() == title:
                return album
        return None

    def add_user(self, user):
        self._users.append(user)

    def add_playlist(self, playlist):
        self._playlists[playlist.get_playlist_title()] = playlist

    def get_top_albums(self):
        return sorted(self._albums, key=lambda a: a.calculate_average_rating(), reverse=True)


music_service = MusicService()

band1 = Band("Iron Maiden", "Heavy Metal")
band2 = Band("Lady Gaga", "Pop")
band3 = Band("Dio", "Heavy Metal")

track1 = Track("The Trooper", 4.11, band1)
track2 = Track("Fear of the Dark", 7.16, band1)
track3 = Track("Bad Romance", 4.54, band2)
track4 = Track("Poker Face", 3.57, band2)
track5 = Track("Holy Diver", 5.54, band3)
track6 = Track("Rainbow in the Dark", 4.16, band3)

album1 = Album("The Trooper", 1983, band1)
album2 = Album("Fear of the Dark", 1992, band1)
album3 = Album("The Fame Monster", 2009, band2)
album4 = Album("Holy Diver", 1983, band3)

album1.add_track(track1)
album2.add_track(track2)
album3.add_track(track3)
album3.add_track(track4)
album4.add_track(track5)
album4.add_track(track6)

music_service.add_album(album1)
music_service.add_album(album2)
music_service.add_album(album3)
music_service.add_album(album4)

print("Searching for tracks named 'Holy Diver':")
found_tracks = Track.search_track_by_name("Holy Diver", [album1, album2, album3, album4])
for track in found_tracks:
    print(track)

user1 = User("MegaHacker")
user2 = User("MusicFan")

music_service.add_user(user1)
music_service.add_user(user2)

user1.rate_album(album1, 5)
user2.rate_album(album2, 5)
user1.rate_album(album3, 4)
user2.rate_album(album4, 5)

retrieved_album = music_service.get_album_by_title("The Trooper")
print(f"Retrieved Album: {retrieved_album.get_title()} by {retrieved_album.get_band().get_name()}")

custom_playlist = user1.create_playlist("My Favorite Tracks")
custom_playlist.add_track(track1)
custom_playlist.add_track(track5)

custom_playlist.add_tag("Epic Metal")
custom_playlist.add_comment(user1, "Great playlist!")
custom_playlist.add_like(user1)
custom_playlist.add_comment(user2, "Love this!")
custom_playlist.add_like(user2)

print(f"Playlist Title: {custom_playlist.get_playlist_title()}")
print("Tracks in Playlist:")
for track in custom_playlist.get_track_list():
    print(f"{track.get_name()} by {track.get_band().get_name()} ({track.get_length()} min)")
print("Tags:", custom_playlist.get_tags())
print("Interactions:", custom_playlist.get_interactions())

print(f"{album1.get_title()} Rating: {album1.calculate_average_rating()}")
print(f"{album2.get_title()} Rating: {album2.calculate_average_rating()}")

playlist1 = Playlist("Chill Vibes")
playlist1.add_track(track1)
playlist1.add_track(track3)

playlist2 = Playlist("Metal Storm")
playlist2.add_track(track2)
playlist2.add_track(track5)

print("\nMerging playlists:")
merged_playlist = Playlist.merge_playlists(playlist1, playlist2, "Merged Playlist")
print(f"Merged Playlist Title: {merged_playlist.get_playlist_title()}")
print("Tracks in Merged Playlist:")
for track in merged_playlist.get_track_list():
    print(f"{track.get_name()} by {track.get_band().get_name()} ({track.get_length()} min)")

merged_playlist.add_tag("Merged Collection")
print("Tags in Merged Playlist:", merged_playlist.get_tags())

print("\nTop Albums:")
for album in music_service.get_top_albums():
    print(f"{album.get_title()}: {album.calculate_average_rating()}")
