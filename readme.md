# pykadena

python tools and goodies for kadena.

## installation

no package available yet, install manually with poetry.

## chainweb api client

```python
from kadena import Kadena

kadena = Kadena('host:443')

await kadena.get_cut()
await kadena.get_peers()
await kadena.get_info()
await kadena.get_recent_headers(6)
await kadena.get_work(request)
await kadena.get_payload(chain, payload)
await kadena.get_balances(account)

async for header in kadena.stream_header_updates():
    print(header)  # requires `headerStream: true`

async for header in kadena.stream_headers_ascending(4, page):
    print(header)
```
