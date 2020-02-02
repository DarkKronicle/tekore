from typing import Union

from tekore.client.process import single, model_list, single_or_dict
from tekore.client.base import SpotifyBase, send_and_process
from tekore.serialise import ModelList
from tekore.model import (
    SimplePlaylistPaging,
    FullPlaylist,
    Image,
    PlaylistTrackPaging
)


class SpotifyPlaylistView(SpotifyBase):
    @send_and_process(single(SimplePlaylistPaging))
    def followed_playlists(
            self,
            limit: int = 20,
            offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of the playlists owned or followed by the current user.

        Requires the playlist-read-private scope to return private playlists.
        Requires the playlist-read-collaborative scope
        to return collaborative playlists.

        Parameters
        ----------
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimplePlaylistPaging
            paging object containing simplified playlists
        """
        return self._get('me/playlists', limit=limit, offset=offset)

    @send_and_process(single(SimplePlaylistPaging))
    def playlists(
            self,
            user_id: str,
            limit: int = 20,
            offset: int = 0
    ) -> SimplePlaylistPaging:
        """
        Get a list of the playlists owned or followed by a user.

        Requires the playlist-read-private scope to return private playlists.
        Requires the playlist-read-collaborative scope to return collaborative
        playlists. Collaborative playlists are only returned for current user.

        Parameters
        ----------
        user_id
            user ID
        limit
            the number of items to return (1..50)
        offset
            the index of the first item to return

        Returns
        -------
        SimplePlaylistPaging
            paging object containing simplified playlists
        """
        return self._get(
            f'users/{user_id}/playlists',
            limit=limit,
            offset=offset
        )

    @send_and_process(single_or_dict(FullPlaylist))
    def playlist(
            self,
            playlist_id: str,
            fields: str = None,
            market: str = None
    ) -> Union[FullPlaylist, dict]:
        """
        Get playlist of a user.

        Parameters
        ----------
        playlist_id
            playlist ID
        fields
            which fields to return
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        FullPlaylist
            playlist object
        """
        return self._get(
            'playlists/' + playlist_id,
            fields=fields,
            market=market
        )

    @send_and_process(model_list(Image))
    def playlist_cover_image(self, playlist_id: str) -> ModelList:
        """
        Get cover image of a playlist. Note: returns a list of images.

        Parameters
        ----------
        playlist_id
            playlist ID

        Returns
        -------
        ModelList
            list of cover images
        """
        return self._get(f'playlists/{playlist_id}/images')

    @send_and_process(single_or_dict(PlaylistTrackPaging))
    def playlist_tracks(
            self,
            playlist_id: str,
            fields: str = None,
            market: str = None,
            limit: int = 100,
            offset: int = 0
    ) -> Union[PlaylistTrackPaging, dict]:
        """
        Get full details of the tracks of a playlist owned by a user.

        Note that if `fields` is specified,
        a raw dictionary is returned instead of a dataclass model.

        Parameters
        ----------
        playlist_id
            playlist ID
        fields
            filters for the query as a comma-separated list,
            see Web API documentation for more details
        limit
            the number of items to return (1..100)
        offset
            the index of the first item to return
        market
            an ISO 3166-1 alpha-2 country code or 'from_token'

        Returns
        -------
        Union[PlaylistTrackPaging, object]
            paging object containing playlist tracks,
            or raw object if fields was specified
        """
        return self._get(
            f'playlists/{playlist_id}/tracks',
            limit=limit,
            offset=offset,
            fields=fields,
            market=market
        )
