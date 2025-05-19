import zmq
import json


#GENRE ID's 
# 28=Action, 12=Adventure, 16=Animation, 35=Comedy, 80=Crime, 99=Documentary, 18=Drama, 10751=Family, 14=Fantasy, 36=History,
# 27=Horror, 10402=Music, 9648=Mystery, 10749=Romance, 878=Sci-Fiction, 10770=TV-Movie, 53=Thriller, 10752=War, 37=Western


# Properly Print JSON items in terminal
def print_nicely(data, title=None):
    """
    Pretty-print a Python object as JSON.
    """
    if title:
        print(f"\n=== {title} ===\n")
    print(json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True))

def main():
    # ZeroMQ setup
    ctx  = zmq.Context()
    sock = ctx.socket(zmq.REQ)
    sock.connect("tcp://localhost:5555")

    # Fetch trending movies
    trending_request = {
        "endpoint": "trending-movies",
        "params": {
            "sort_by":    "popularity",   # popularity | revenue | rating
            "genres":     [12],         # empty => all genres; or a list of genre IDs
            "time_range": "year",     # week | month | year | custom
            # if custom is chosen input start_year and end_year:
            # "start_year": ,
            # "end_year": ,
            "page":       1           # optional, defaults to 1
        }
    }
    sock.send_json(trending_request)
    trending_response = sock.recv_json()
    print_nicely(trending_response, title="Trending Movies Response")

    # Fetch movie recommendations
    rec_request = {
        "endpoint": "movie-recommendations",
        "params": {
            "movie_id": 550,  # Fight Club
            "page":     1     # optional
        }
    }
    sock.send_json(rec_request)
    rec_response = sock.recv_json()
    print_nicely(rec_response, title="Movie Recommendations Response")

if __name__ == "__main__":
    main()
