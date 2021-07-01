"""A video player class."""

from video_library import VideoLibrary
from video_playlist import Playlist
import random


class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()

        self._map_titleToVideo = {} #A dictionary mapping a Video's alphabetically-sortable title to its non-alphabetically-sortable Video object.
        for video in self._video_library.get_all_videos():
            self._map_titleToVideo[video.title] = video
        
        self._map_idToVideo = {} #A dictionary mapping a Video's primary key to the rest of the Video object.
        self._map_idToFlag = {} #A dictionary mapping whether a Video is flagged or not. If not, it maps to False, but if it is, it maps to the reason.
        for video in self._video_library.get_all_videos():
            self._map_idToVideo[video.video_id] = video
            self._map_idToFlag[video.video_id] = False
            
        self._playing = None
        self._isPaused = False

        self._playlists = {} #{NAME_ALL_CAPS: PlaylistObject}

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos_alphabetically = list(self._map_titleToVideo.keys())
        videos_alphabetically.sort() #Sorting all the titles alphabetically.
        print("Here's a list of all available videos:")
        for title in videos_alphabetically:
            flag_or_not = self._map_idToFlag[self._map_titleToVideo[title].video_id]
            if flag_or_not == False:
                print(self._map_titleToVideo[title])
            else:
                print(self._map_titleToVideo[title], "- FLAGGED (reason:", flag_or_not + ")")


    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        if self._playing != None:
            self.stop_video()
        if video_id in list(self._map_idToVideo.keys()):
            if self._map_idToFlag[video_id] != False:
                print("Cannot play video: Video is currently flagged (reason:", self._map_idToFlag[video_id] + ")")
            else:
                self._playing = self._map_idToVideo[video_id]
                print("Playing video:", self._map_idToVideo[video_id].title)
                self._isPaused = False
        else:
            print("Cannot play video: Video does not exist")

    def stop_video(self):
        """Stops the current video."""
        if self._playing == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video:", self._playing.title)
            self._playing = None

    def play_random_video(self):
        """Plays a random video from the video library."""
        list_of_IDs = [video_id for video_id in list(self._map_idToVideo.keys()) if self._map_idToFlag[video_id] == False] #Only looks at videos that aren't flagged.
        if list_of_IDs == []:
            print("No videos available")
        else:
            random_video_id = list_of_IDs[random.randint(0, len(list_of_IDs) - 1)]
            self.play_video(random_video_id)

    def pause_video(self):
        """Pauses the current video."""
        if self._playing is None:
            print("Cannot pause video: No video is currently playing")
        elif self._isPaused:
            print("Video already paused:", self._playing.title)
        else:
            print("Pausing video:", self._playing.title)
            self._isPaused = True

    def continue_video(self):
        """Resumes playing the current video."""
        if self._playing is None:
            print("Cannot continue video: No video is currently playing")
        elif self._isPaused == False:
            print("Cannot continue video: Video is not paused")
        else:
            print("Continuing video:", self._playing.title)
            self._isPaused = False

    def show_playing(self):
        """Displays video currently playing."""
        if self._playing is None:
            print("No video is currently playing")
        else:
            paused_string = ""
            if self._isPaused:
                paused_string = " - PAUSED"
            print("Currently playing:", str(self._playing) + paused_string)
        

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in list(self._playlists.keys()):
            print("Cannot create playlist: A playlist with the same name already exists")
        else:
            self._playlists[playlist_name.upper()] = Playlist(playlist_name)
            print("Successfully created new playlist:", playlist_name)

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """
        if playlist_name.upper() in list(self._playlists.keys()):
            if video_id not in list(self._map_idToVideo.keys()):
                print("Cannot add video to", playlist_name + ": Video does not exist")
            elif self._map_idToFlag[video_id] != False:
                print("Cannot add video to", playlist_name + ": Video is currently flagged (reason:", self._map_idToFlag[video_id] + ")")
            elif self._playlists[playlist_name.upper()].has(video_id):
                print("Cannot add video to", playlist_name + ": Video already added")
            else:
                video = self._map_idToVideo[video_id]
                self._playlists[playlist_name.upper()].append(video)
                print("Added video to", playlist_name + ":", video.title)
        else:
            print("Cannot add video to", playlist_name + ": Playlist does not exist")

    def show_all_playlists(self):
        """Display all playlists."""
        if self._playlists == {}:
            print("No playlists exist yet")
        else:
            playlists_alphabetically = list(self._playlists.keys())
            playlists_alphabetically.sort() #Sorting all the titles alphabetically.
            print("Showing all playlists:")
            for name in playlists_alphabetically:
                print(self._playlists[name].name)


    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in list(self._playlists.keys()):
            print("Showing playlist:", playlist_name)
            videos = self._playlists[playlist_name.upper()].get_videos()
            if videos == []:
                print("No videos here yet")
            else:
                for video in videos:
                    flag_or_not = self._map_idToFlag[video.video_id]
                    if flag_or_not == False:
                        print(video)
                    else:
                        print(video, "- FLAGGED (reason:", flag_or_not + ")")
        else:
            print("Cannot show playlist", playlist_name + ": Playlist does not exist")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        if playlist_name.upper() in list(self._playlists.keys()):
            if video_id not in list(self._map_idToVideo.keys()):
                print("Cannot remove video from", playlist_name + ": Video does not exist")
            elif not self._playlists[playlist_name.upper()].has(video_id):
                print("Cannot remove video from", playlist_name + ": Video is not in playlist")
            else:
                playlist = self._playlists[playlist_name.upper()].get_videos()
                video = self._map_idToVideo[video_id]
                playlist.remove(video)
                self._playlists[playlist_name.upper()].set_videos(playlist)
                print("Removed video from", playlist_name + ":", video.title)
        else:
            print("Cannot remove video from", playlist_name + ": Playlist does not exist")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in list(self._playlists.keys()):
            self._playlists[playlist_name.upper()].set_videos([])
            print("Successfully removed all videos from", playlist_name)
        else:
            print("Cannot clear playlist", playlist_name + ": Playlist does not exist")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        if playlist_name.upper() in list(self._playlists.keys()):
            self._playlists.pop(playlist_name.upper())
            print("Deleted playlist:", playlist_name)
        else:
            print("Cannot delete playlist", playlist_name + ": Playlist does not exist")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        videos_alphabetically = list(self._map_titleToVideo.keys())
        videos_alphabetically.sort()
        search_results = []
        for title in videos_alphabetically:
            has_flag = self._map_idToFlag[self._map_titleToVideo[title].video_id] != False
            if (search_term.upper() in title.upper()) and (not has_flag):
                search_results.append(self._map_titleToVideo[title])
        if search_results == []:
            print("No search results for", search_term)
        else:
            print("Here are the results for", search_term + ":")
            for i in range(0, len(search_results)):
                print(str(i+1) + ")", search_results[i])
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            user_input = input("")
            if user_input in [str(x + 1) for x in range(0, len(search_results))]:
                self.play_video(search_results[int(user_input) - 1].video_id)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        workings = []
        for video in self._video_library.get_all_videos():
            if self._map_idToFlag[video.video_id] == False:
                if video_tag.lower() in [tag.lower() for tag in video.tags]:
                    workings.append(video.title)
        workings.sort()
        search_results = []
        for title in workings:
            search_results.append(self._map_titleToVideo[title])
        if search_results == []:
            print("No search results for", video_tag)
        else:
            print("Here are the results for", video_tag + ":")
            for i in range(0, len(search_results)):
                print(str(i+1) + ")", search_results[i])
            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            user_input = input("")
            if user_input in [str(x + 1) for x in range(0, len(search_results))]:
                self.play_video(search_results[int(user_input) - 1].video_id)

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        if video_id in list(self._map_idToFlag.keys()):
            if self._map_idToFlag[video_id] != False:
                print("Cannot flag video: Video is already flagged")
            else:
                self._map_idToFlag[video_id] = flag_reason
                if self._playing == self._map_idToVideo[video_id]:
                    self.stop_video()
                print("Successfully flagged video:", self._map_idToVideo[video_id].title, "(reason:", flag_reason + ")")
        else:
            print("Cannot flag video: Video does not exist")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        if video_id in list(self._map_idToFlag.keys()):
            if self._map_idToFlag[video_id] == False:
                print("Cannot remove flag from video: Video is not flagged")
            else:
                self._map_idToFlag[video_id] = False
                print("Successfully removed flag from video:", self._map_idToVideo[video_id].title)
        else:
            print("Cannot remove flag from video: Video does not exist")
