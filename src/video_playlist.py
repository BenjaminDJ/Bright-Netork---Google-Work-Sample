"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""
    def __init__(self, name):
        self._name = name
        self._playlist = []

    @property
    def name(self) -> str:
        """Returns the name of the playlist."""
        return self._name
    
    def get_videos(self):
        return self._playlist
    
    def set_videos(self, different_playlist):
        self._playlist = different_playlist

    def append(self, video):
        """Appends a video to the playlist."""
        self._playlist.append(video)

    def has(self, video_id):
        """Returns whether or not the playlist has a video with this id."""
        for video in self._playlist:
            if video.video_id == video_id:
                return True
        return False
