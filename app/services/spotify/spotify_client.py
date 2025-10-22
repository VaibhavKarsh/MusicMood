"""
Spotify API Client
Handles authentication, rate limiting, and API interactions with Spotify
"""

import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx

from app.config.settings import settings

logger = logging.getLogger(__name__)


class SpotifyClient:
    """
    Spotify API Client with OAuth2 authentication and rate limiting

    Features:
    - Client credentials OAuth2 flow
    - Automatic token refresh
    - Rate limit tracking
    - Retry logic with exponential backoff
    - Comprehensive error handling
    """

    # Spotify API endpoints
    TOKEN_URL = "https://accounts.spotify.com/api/token"
    API_BASE_URL = "https://api.spotify.com/v1"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        timeout: int = 30,
    ):
        """
        Initialize Spotify client (lazy loading - no API calls on init)

        Args:
            client_id: Spotify client ID (defaults to settings)
            client_secret: Spotify client secret (defaults to settings)
            timeout: Request timeout in seconds
        """
        self.client_id = client_id or settings.SPOTIFY_CLIENT_ID
        self.client_secret = client_secret or settings.SPOTIFY_CLIENT_SECRET
        self.timeout = timeout

        # Authentication state
        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None

        # Rate limiting state
        self._rate_limit_remaining: Optional[int] = None
        self._rate_limit_reset_at: Optional[datetime] = None

        # HTTP client
        self._http_client: Optional[httpx.Client] = None

        logger.info("SpotifyClient initialized (lazy loading enabled)")

    @property
    def http_client(self) -> httpx.Client:
        """Get or create HTTP client"""
        if self._http_client is None:
            self._http_client = httpx.Client(timeout=self.timeout)
        return self._http_client

    def _get_auth_header(self) -> str:
        """
        Get Basic authentication header for token requests

        Returns:
            Base64 encoded 'client_id:client_secret'
        """
        import base64

        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_bytes = auth_str.encode("utf-8")
        auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")
        return f"Basic {auth_b64}"

    def _is_token_expired(self) -> bool:
        """Check if access token is expired or about to expire (within 5 minutes)"""
        if self._token_expires_at is None:
            return True
        # Refresh 5 minutes before actual expiration
        return datetime.now() >= (self._token_expires_at - timedelta(minutes=5))

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        Get access token using OAuth2 client credentials flow

        Args:
            force_refresh: Force token refresh even if not expired

        Returns:
            Valid access token

        Raises:
            Exception: If authentication fails
        """
        # Return cached token if still valid
        if not force_refresh and self._access_token and not self._is_token_expired():
            logger.debug("Using cached access token")
            return self._access_token

        logger.info("Requesting new access token from Spotify")

        try:
            response = self.http_client.post(
                self.TOKEN_URL,
                headers={
                    "Authorization": self._get_auth_header(),
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                data={"grant_type": "client_credentials"},
            )
            response.raise_for_status()

            token_data = response.json()
            self._access_token = token_data["access_token"]
            expires_in = token_data.get("expires_in", 3600)  # Default 1 hour
            self._token_expires_at = datetime.now() + timedelta(seconds=expires_in)

            logger.info(f"Access token obtained successfully (expires in {expires_in}s)")
            return self._access_token

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                logger.error("Authentication failed: Invalid client credentials")
                raise Exception("Invalid Spotify client credentials")
            elif e.response.status_code == 400:
                logger.error(f"Bad request: {e.response.text}")
                raise Exception(f"Bad request to Spotify API: {e.response.text}")
            else:
                logger.error(f"HTTP error during authentication: {e}")
                raise
        except Exception as e:
            logger.error(f"Error getting access token: {e}")
            raise

    def _update_rate_limit_info(self, headers: Dict[str, str]) -> None:
        """
        Extract and update rate limit information from response headers

        Args:
            headers: Response headers dictionary
        """
        # Spotify uses X-RateLimit-* headers
        if "X-RateLimit-Remaining" in headers:
            self._rate_limit_remaining = int(headers["X-RateLimit-Remaining"])

        if "X-RateLimit-Reset" in headers:
            reset_timestamp = int(headers["X-RateLimit-Reset"])
            self._rate_limit_reset_at = datetime.fromtimestamp(reset_timestamp)

        if self._rate_limit_remaining is not None:
            logger.debug(f"Rate limit: {self._rate_limit_remaining} requests remaining")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        max_retries: int = 3,
    ) -> Dict[str, Any]:
        """
        Make authenticated request to Spotify API with retry logic

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (e.g., '/search')
            params: Query parameters
            json_data: JSON body data
            max_retries: Maximum number of retries for 5xx errors

        Returns:
            JSON response data

        Raises:
            Exception: If request fails after all retries
        """
        # Ensure we have a valid token
        token = self.get_access_token()
        url = f"{self.API_BASE_URL}{endpoint}"

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        retry_count = 0
        backoff_seconds = 1

        while retry_count <= max_retries:
            try:
                logger.debug(f"{method} {endpoint} (attempt {retry_count + 1}/{max_retries + 1})")

                response = self.http_client.request(
                    method=method, url=url, headers=headers, params=params, json=json_data
                )

                # Update rate limit info
                self._update_rate_limit_info(response.headers)

                # Handle different status codes
                if response.status_code == 200 or response.status_code == 201:
                    return response.json()

                elif response.status_code == 204:
                    # No content (successful DELETE, etc.)
                    return {}

                elif response.status_code == 401:
                    # Token expired, retry with new token
                    logger.warning("Token expired, refreshing...")
                    token = self.get_access_token(force_refresh=True)
                    headers["Authorization"] = f"Bearer {token}"
                    continue

                elif response.status_code == 429:
                    # Rate limited
                    retry_after = int(response.headers.get("Retry-After", 60))
                    logger.warning(f"Rate limited, waiting {retry_after} seconds")
                    time.sleep(retry_after)
                    continue

                elif 500 <= response.status_code < 600:
                    # Server error - retry with exponential backoff
                    if retry_count < max_retries:
                        logger.warning(
                            f"Server error {response.status_code}, retrying in {backoff_seconds}s"
                        )
                        time.sleep(backoff_seconds)
                        backoff_seconds *= 2  # Exponential backoff
                        retry_count += 1
                        continue
                    else:
                        raise Exception(
                            f"Server error after {max_retries} retries: {response.status_code}"
                        )

                elif response.status_code == 404:
                    logger.error(f"Resource not found: {endpoint}")
                    raise Exception(f"Resource not found: {endpoint}")

                elif response.status_code == 400:
                    error_msg = response.json().get("error", {}).get("message", response.text)
                    logger.error(f"Bad request: {error_msg}")
                    raise Exception(f"Bad request: {error_msg}")

                else:
                    # Other errors
                    logger.error(f"Unexpected status code: {response.status_code}")
                    raise Exception(
                        f"Unexpected status code: {response.status_code} - {response.text}"
                    )

            except httpx.TimeoutException:
                if retry_count < max_retries:
                    logger.warning(f"Request timeout, retrying in {backoff_seconds}s")
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2
                    retry_count += 1
                    continue
                else:
                    raise Exception(f"Request timeout after {max_retries} retries")

            except httpx.ConnectError as e:
                logger.error(f"Connection error: {e}")
                raise Exception(f"Failed to connect to Spotify API: {e}")

            except Exception as e:
                logger.error(f"Request failed: {e}")
                raise

        raise Exception("Max retries exceeded")

    # ==================== API Methods ====================

    def search(
        self, query: str, search_type: str = "track", limit: int = 50, market: str = "US"
    ) -> Dict[str, Any]:
        """
        Search Spotify catalog

        Args:
            query: Search query string
            search_type: Type to search for (track, artist, album, playlist)
            limit: Number of results (max 50 per request)
            market: Market/country code (e.g., 'US')

        Returns:
            Search results dictionary
        """
        params = {
            "q": query,
            "type": search_type,
            "limit": min(limit, 50),  # Spotify max is 50
            "market": market,
        }

        logger.info(f"Searching Spotify: '{query}' (type={search_type}, limit={limit})")
        return self._make_request("GET", "/search", params=params)

    def get_track(self, track_id: str, market: str = "US") -> Dict[str, Any]:
        """
        Get track details

        Args:
            track_id: Spotify track ID
            market: Market/country code

        Returns:
            Track details dictionary
        """
        params = {"market": market}
        return self._make_request("GET", f"/tracks/{track_id}", params=params)

    def get_tracks(self, track_ids: List[str], market: str = "US") -> Dict[str, Any]:
        """
        Get multiple tracks (up to 50 at once)

        Args:
            track_ids: List of Spotify track IDs (max 50)
            market: Market/country code

        Returns:
            Tracks dictionary with 'tracks' array
        """
        params = {"ids": ",".join(track_ids[:50]), "market": market}  # Max 50
        return self._make_request("GET", "/tracks", params=params)

    def get_audio_features(self, track_ids: List[str]) -> Dict[str, Any]:
        """
        Get audio features for multiple tracks (up to 100 at once)

        Args:
            track_ids: List of Spotify track IDs (max 100)

        Returns:
            Audio features dictionary with 'audio_features' array
        """
        params = {"ids": ",".join(track_ids[:100])}  # Max 100
        return self._make_request("GET", "/audio-features", params=params)

    def get_recommendations(
        self,
        seed_tracks: Optional[List[str]] = None,
        seed_artists: Optional[List[str]] = None,
        seed_genres: Optional[List[str]] = None,
        limit: int = 20,
        target_valence: Optional[float] = None,
        target_energy: Optional[float] = None,
        target_danceability: Optional[float] = None,
        target_tempo: Optional[int] = None,
        market: str = "US",
    ) -> Dict[str, Any]:
        """
        Get track recommendations based on seeds and target audio features

        Args:
            seed_tracks: List of track IDs for seeds (max 5 total seeds)
            seed_artists: List of artist IDs for seeds
            seed_genres: List of genre strings for seeds
            limit: Number of recommendations (max 100)
            target_valence: Target valence (0.0 to 1.0, happiness)
            target_energy: Target energy (0.0 to 1.0)
            target_danceability: Target danceability (0.0 to 1.0)
            target_tempo: Target tempo in BPM
            market: Market/country code

        Returns:
            Recommendations dictionary with 'tracks' array
        """
        params = {"limit": min(limit, 100), "market": market}

        # Add seeds (max 5 total)
        if seed_tracks:
            params["seed_tracks"] = ",".join(seed_tracks[:5])
        if seed_artists:
            params["seed_artists"] = ",".join(seed_artists[:5])
        if seed_genres:
            params["seed_genres"] = ",".join(seed_genres[:5])

        # Add target audio features
        if target_valence is not None:
            params["target_valence"] = target_valence
        if target_energy is not None:
            params["target_energy"] = target_energy
        if target_danceability is not None:
            params["target_danceability"] = target_danceability
        if target_tempo is not None:
            params["target_tempo"] = target_tempo

        logger.info(f"Getting recommendations with {len(params)} parameters")
        return self._make_request("GET", "/recommendations", params=params)

    def get_available_genre_seeds(self) -> List[str]:
        """
        Get list of available genre seeds for recommendations

        Returns:
            List of genre strings
        """
        result = self._make_request("GET", "/recommendations/available-genre-seeds")
        return result.get("genres", [])

    def get_audio_features(self, track_id: str) -> Optional[Dict[str, Any]]:
        """
        Get audio features for a single track

        Args:
            track_id: Spotify track ID

        Returns:
            Dictionary with audio features or None if not found
        """
        try:
            logger.info(f"Getting audio features for track: {track_id}")
            return self._make_request("GET", f"/audio-features/{track_id}")
        except Exception as e:
            logger.error(f"Failed to get audio features for {track_id}: {e}")
            return None

    def get_audio_features_batch(self, track_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get audio features for multiple tracks (batch operation)

        Spotify limits batch requests to 100 tracks.
        This method handles batching automatically for larger lists.

        Args:
            track_ids: List of Spotify track IDs (can be > 100)

        Returns:
            Dictionary mapping track_id to audio features
            Features include:
            - energy (0-1): Intensity and activity
            - danceability (0-1): How suitable for dancing
            - valence (0-1): Musical positiveness
            - tempo (BPM): Beats per minute
            - acousticness (0-1): Confidence track is acoustic
            - instrumentalness (0-1): Predicts if track has no vocals
            - liveness (0-1): Presence of audience
            - speechiness (0-1): Presence of spoken words
            - loudness (dB): Overall loudness
            - key: Pitch class (0-11)
            - mode: Major (1) or minor (0)
            - time_signature: Estimated time signature
        """
        if not track_ids:
            logger.warning("get_audio_features_batch called with empty track list")
            return {}

        all_features = {}
        batch_size = 100  # Spotify API limit

        # Process in batches of 100
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i : i + batch_size]
            batch_num = (i // batch_size) + 1
            total_batches = (len(track_ids) + batch_size - 1) // batch_size

            logger.info(f"Processing batch {batch_num}/{total_batches}: {len(batch)} tracks")

            try:
                # Make batch API call
                params = {"ids": ",".join(batch)}
                result = self._make_request("GET", "/audio-features", params=params)

                # Parse results
                audio_features_list = result.get("audio_features", [])

                for features in audio_features_list:
                    if features and features.get("id"):
                        track_id = features["id"]
                        all_features[track_id] = features
                        logger.debug(
                            f"Got features for track {track_id}: energy={features.get('energy')}, valence={features.get('valence')}"
                        )
                    else:
                        logger.warning("Received null audio features in batch response")

                logger.info(
                    f"Batch {batch_num}: Retrieved features for {len(audio_features_list)} tracks"
                )

            except Exception as e:
                logger.error(f"Failed to get audio features for batch {batch_num}: {e}")
                # Continue with next batch instead of failing completely
                continue

        logger.info(f"Total audio features retrieved: {len(all_features)}/{len(track_ids)}")
        return all_features

    def close(self) -> None:
        """Close HTTP client connection"""
        if self._http_client:
            self._http_client.close()
            self._http_client = None
            logger.info("SpotifyClient HTTP connection closed")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connections"""
        self.close()

    def get_client_info(self) -> Dict[str, Any]:
        """
        Get client status information (for debugging)

        Returns:
            Dictionary with client status
        """
        return {
            "authenticated": self._access_token is not None,
            "token_expires_at": (
                self._token_expires_at.isoformat() if self._token_expires_at else None
            ),
            "token_expired": self._is_token_expired(),
            "rate_limit_remaining": self._rate_limit_remaining,
            "rate_limit_reset_at": (
                self._rate_limit_reset_at.isoformat() if self._rate_limit_reset_at else None
            ),
        }
