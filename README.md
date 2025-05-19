Movie Discovery Service

This microservice provides two endpoints: trending-movies and movie-recommendations, over a ZeroMQ REP socket. Once defined, this communication contract must not change, as clients rely on its stability.


Connection:
Protocol: ZeroMQ REP socket
Bind Address: tcp://0.0.0.0:${ZMQ_PORT} (default port: 5555)

Clients MUST connect via a REQ socket to the same address.

HOW TO REQUEST DATA:
Requests to this service are JSON objects sent with socket.send_json(...)

Here is a general look at the format:
{
  "endpoint": "<endpoint-name>",
  "params": { /* endpoint-specific parameters */ }
}

For the trending-movies endpoint, here are the parameters:

**sort_by**            Type: string          Required?: yes

**genres**            Type: integer[]        Required?:yes

**time_range**        Type: string          Required?:yes

**start_year**         Type: int            Required?:no

**end_year**           Type: int            Required?:no

**page**              Type: int           Required?: no



