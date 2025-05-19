# Movie Discovery Service

This microservice provides two endpoints: `trending-movies` and `movie-recommendations`, over a ZeroMQ REP socket. Once defined, this communication contract must not change, as clients rely on its stability.


## Connection:
Protocol: ZeroMQ REP socket
Bind Address: `tcp://0.0.0.0:${ZMQ_PORT}` (default port: `5555`)

Clients MUST connect via a REQ socket to the same address.

## HOW TO REQUEST DATA:

Requests to this service are JSON objects sent with `socket.send_json(...)`

Here is a general look at the format:
```
{
  "endpoint": "<endpoint-name>",
  "params": { /* endpoint-specific parameters */ }
}
```

### For the `trending-movies` endpoint, here are the parameters:

**sort_by**,            Type: string,          Required?: yes

**genres**,            Type: integer[],        Required?: yes

**time_range**,        Type: string,          Required?: yes

**start_year**,         Type: int,            Required?: no

**end_year**,           Type: int,            Required?: no

**page**,              Type: int,           Required?: no


*The use of start_year and end_year are only needed when the user sets the time_range to "custom".*

### Example Request:

```
request = {
    "endpoint": "trending-movies",
    "params": {
        "sort_by":    "popularity",
        "genres":     [28, 12],       # Action (28) and Adventure (12)
        "time_range": "month",
        "page":       2
    }
}
socket.send_json(request)
```


### For the `movie-recommendations` endpoint, here are the parameters:

**movie_id**,            Type: int,          Required?: yes

**page**,            Type: int,        Required?: no


### Example Request:
```
request = {
    "endpoint": "movie-recommendations",
    "params": {
        "movie_id": 550,  # e.g. Fight Club
        "page":     1
    }
}
socket.send_json(request)
```


## HOW TO RECIEVE DATA:

Responses from this service are JSON objects received via `socket.recv_json().`


### Here is the basic response format:

```
{
  "status": "ok" | "error",
  "data"?: { /* TMDB response object when status is "ok" */ },
  "message"?: "<error details>"  // present when status is "error"  
}
```


When `"status": "ok"`, the full TMDB payload is provided under `"data"`

When `"status": "error"`, the `"message"` describes what went wrong.


### Examples:

`trending-movies`:

```
reply = socket.recv_json()
if reply["status"] == "ok":
    trending_data = reply["data"]
    # trending_data is TMDB’s JSON (with keys: page, results, total_pages, total_results)
else:
    raise RuntimeError(f"Service error: {reply['message']}")
```

`movie-recommendations`:

```
reply = socket.recv_json()
if reply["status"] == "ok":
    recs = reply["data"]
    # recs is TMDB’s JSON (with keys: page, results, total_pages, total_results)
else:
    raise RuntimeError(f"Service error: {reply['message']}")
```

## UML Sequence Diagram
![image](https://github.com/user-attachments/assets/905c83fd-89a9-45d8-92f0-ff92d44d700d)






