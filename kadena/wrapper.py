import asyncio
import json
from pathlib import Path

import httpx

from kadena.constants import ENCODINGS
from kadena.types import decode_header, WorkHeader
from kadena.utils import base64_to_dict, base64_to_int


class Kadena:
    """
    Async client for chainweb-node.

    See also:
        https://github.com/kadena-io/chainweb-node/wiki/REST-API-Examples-with-curl

    Args:
        node: host:port to connect to.
    """

    def __init__(self, node: str):
        self._base_url = f"https://{node}"
        self.node_version = None
        self._prefix = None

    async def get_info(self):
        """
        Get node network, api version and list supported chains.
        """
        resp = await self._request("/info", prefix=False)
        return resp.json()

    async def get_cut(self):
        """
        Get current cut including height, weight and chain hashes.
        """
        resp = await self._request("/cut")
        data = resp.json()
        data["weight"] = base64_to_int(data["weight"])
        return data

    async def get_peers(self):
        """
        Get list of peers known to a node in ``host:port`` format.
        """
        results = []
        async for data in self._request_pages("/cut/peer"):
            for peer in data["items"]:
                host = peer["address"]["hostname"]
                port = peer["address"]["port"]
                results.append(f"{host}:{port}")
        return results

    async def stream_header_updates(self):
        """
        Stream header updates as they happen.

        Note:
            You need to have ``headerStream: true`` in the node config for this to work.

        >>> async for header in Kadena('host:443').stream_header_updates():
        >>>     print(header)
        """
        await self._init()
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            resp = await client.get(f"{self.prefix}/header/updates", timeout=None, stream=True)
            resp.raise_for_status()
            async for message in resp.stream():
                print(message)
                pairs = [line.split(":", maxsplit=1) for line in message.decode().splitlines()]
                event = {pair[0]: pair[1] for pair in pairs if len(pair) == 2}
                if event["event"] == "BlockHeader":
                    data = json.loads(event["data"])
                    yield decode_header(data["header"])

    async def get_recent_headers(self, depth=6):
        """
        Get the most recent headers for each chain.
        """
        cut = await self.cut()
        heights = {chain: block["height"] for chain, block in cut["hashes"].items()}
        tasks = [
            self._request(f"/chain/{chain}/header", params={"minheight": height - depth, "maxheight": height})
            for chain, height in heights.items()
        ]
        responses = await asyncio.gather(*tasks)
        headers = [[decode_header(header) for header in chain_headers.json()["items"]] for chain_headers in responses]
        return dict(zip(heights, headers))

    async def stream_headers_ascending(self, chain: int, page=None):
        """
        Stream all headers of a ``chain`` starting from ``page``.

        >>> page = "excluding:sv_e1g4XA35IZic34XIn5DB14V5RvOddY8--q_zRTkw"
        >>> async for header in Kadena('host:443').stream_headers_ascending(4, page):
        >>>     print(header)
        """
        async for data in self._request_pages(f"/chain/{chain}/header", page=page):
            for header in data["items"]:
                yield decode_header(header)

    async def get_payload(self, chain, payload):
        """
        Get payload with outputs by payload hash.
        """
        resp = await self._request(f"/chain/{chain}/payload/{payload}/outputs")
        data = resp.json()
        data["minerData"] = base64_to_dict(data["minerData"])
        data["transactions"] = [
            {"transaction": base64_to_dict(transaction), "output": base64_to_dict(output)}
            for transaction, output in data["transactions"]
        ]
        for tx in data["transactions"]:
            tx["transaction"]["cmd"] = json.loads(tx["transaction"]["cmd"])
        if "coinbase" in data:
            data["coinbase"] = base64_to_dict(data["coinbase"])
        return data

    async def get_total_balance(self, account):
        """
        Get total account balance across all chains.
        """
        balances = await self.get_balances(account)
        return sum(balances.values())

    async def get_balances(self, account):
        """
        Get account balances across all chains.

        Requires ``pact`` executable in PATH.
        """
        script = f'code: (coin.get-balance "{account}") \nkeyPairs: []\n'
        balance_script = Path("get_balance.yml")
        balance_script.write_text(script)
        pact = await asyncio.create_subprocess_shell(
            f"pact -l -a {balance_script.name}", stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        out, err = await pact.communicate()
        payload = json.loads(out.decode())
        balance_script.unlink()
        cut = await self.get_cut()
        chains = sorted([chain for chain in cut["hashes"]], key=int)
        tasks = [self.get_chain_balance(chain, payload) for chain in chains]
        balances = await asyncio.gather(*tasks)
        return {chain: balance for chain, balance in zip(chains, balances)}

    async def get_chain_balance(self, chain, payload):
        resp = await self._request(f"/chain/{chain}/pact/api/v1/local", verb="post", json=payload)
        return resp.json()["result"].get("data", 0)

    async def get_work(self, mining_request: dict) -> WorkHeader:
        resp = await self._request("/mining/work", encoding="binary", json=mining_request)
        return decode_header(resp.content)

    # internal methods

    async def _init(self):
        if self._prefix is not None:
            return
        async with httpx.AsyncClient(base_url=self._base_url) as client:
            resp = await client.get("/info", verify=False)
            data = resp.json()
            self.node_version = resp.headers.get("x-chainweb-node-version")
            self._prefix = f"/chainweb/{data['nodeApiVersion']}/{data['nodeVersion']}"

    async def _request(self, method, verb="get", encoding="base64", prefix=True, **kwargs):
        await self._init()
        headers = {"content-type": "application/json", "accept": ENCODINGS[encoding]}
        async with httpx.AsyncClient(base_url=self._base_url, headers=headers) as client:
            url = f"{self._prefix}{method}" if prefix else method
            resp = await client.request(verb, url, verify=False, **kwargs)
            resp.raise_for_status()
            return resp

    async def _request_pages(self, method, page=None, **kwargs):
        while True:
            params = {"next": page} if page else None
            resp = await self._request(method, params=params, **kwargs)
            data = resp.json()
            yield data
            page = data["next"]
            if page is None:
                return
