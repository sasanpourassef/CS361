import os
import zmq
import requests
from datetime import datetime, timedelta

# Load TMDB API key from environment
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
if not TMDB_API_KEY:
    raise EnvironmentError("Please set the TMDB_API_KEY environment variable")

# ZeroMQ server settings
ZMQ_PORT = os.getenv('ZMQ_PORT', '5555')

# TMDB endpoints
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Allowed parameters
SORT_OPTIONS = {
    'popularity': 'popularity.desc',
    'revenue': 'revenue.desc',
    'rating': 'vote_average.desc'
}
TIME_RANGES = {'week', 'month', 'year', 'custom'}


def fetch_trending_movies(params):
    # Validate required params
    sort_by = params['sort_by']
    genres = params['genres']  # list of genre IDs
    time_range = params['time_range']
    page = params.get('page', 1)

    if sort_by not in SORT_OPTIONS:
        raise ValueError(f"Invalid sort_by: {sort_by}")
    if time_range not in TIME_RANGES:
        raise ValueError(f"Invalid time_range: {time_range}")

    # Build discover/movie query
    query = {
        'api_key': TMDB_API_KEY,
        'sort_by': SORT_OPTIONS[sort_by],
        'page': page,
        'with_genres': ','.join(map(str, genres)) if genres else ''
    }

    # Handle time filtering
    today = datetime.utcnow()
    if time_range == 'week':
        start = today - timedelta(weeks=1)
        query['release_date.gte'] = start.strftime('%Y-%m-%d')
        query['release_date.lte'] = today.strftime('%Y-%m-%d')
    elif time_range == 'month':
        start = today - timedelta(days=30)
        query['release_date.gte'] = start.strftime('%Y-%m-%d')
        query['release_date.lte'] = today.strftime('%Y-%m-%d')
    elif time_range == 'year':
        start = today - timedelta(days=365)
        query['release_date.gte'] = start.strftime('%Y-%m-%d')
        query['release_date.lte'] = today.strftime('%Y-%m-%d')
    else:  # custom
        start_year = params.get('start_year')
        end_year = params.get('end_year')
        if not start_year or not end_year:
            raise ValueError("start_year and end_year are required for custom time_range")
        query['release_date.gte'] = f"{start_year}-01-01"
        query['release_date.lte'] = f"{end_year}-12-31"

    url = f"{TMDB_BASE_URL}/discover/movie"
    resp = requests.get(url, params=query)
    resp.raise_for_status()
    return resp.json()


def fetch_movie_recommendations(params):
    movie_id = params['movie_id']
    page = params.get('page', 1)
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    query = {'api_key': TMDB_API_KEY, 'page': page}
    resp = requests.get(url, params=query)
    resp.raise_for_status()
    return resp.json()


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{ZMQ_PORT}")
    print(f"Movie discovery service listening on port {ZMQ_PORT}...")

    while True:
        try:
            request = socket.recv_json()
            endpoint = request.get('endpoint')
            params = request.get('params', {})

            if endpoint == 'trending-movies':
                result = fetch_trending_movies(params)
            elif endpoint == 'movie-recommendations':
                result = fetch_movie_recommendations(params)
            else:
                result = {'error': f"Unknown endpoint: {endpoint}"}

            socket.send_json({'status': 'ok', 'data': result})

        except Exception as e:
            # Send back error message
            socket.send_json({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    main()
