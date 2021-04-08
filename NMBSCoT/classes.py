#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""NMBS Cursor-on-Target Class Definitions."""

from pprint import pprint

import aiohttp
import asyncio

import pytak


class NMBSWorker(pytak.MessageWorker):

    """Reads ADS-B Exchange Data, renders to CoT, and puts on queue."""

    def __init__(self, event_queue: asyncio.Queue, url: str, api_key: str,
                 cot_stale: int = None, poll_interval: int = None):
        super().__init__(event_queue)
        self.url = url
        self.cot_stale = cot_stale
        self.poll_interval: int = int(poll_interval or
                                      NMBSCot.DEFAULT_POLL_INTERVAL)
        self.api_key: str = api_key
        self.cot_renderer = NMBSCot.nmbs_to_cot

    async def handle_message(self, trips: list) -> None:
        if not trips:
            self._logger.warning("Empty trips list")
            return False

        _lac = len(trips)
        _acn = 1
        for trip in trips:
            event = NMBSCot.nmbs_to_cot(
                trip,
                stale=self.cot_stale
            )
            if not event:
                self._logger.debug(f"Empty CoT Event for trip={trip}")
                _acn += 1
                continue

            self._logger.debug(
                "Handling %s/%s trip: %s ",
                _acn,
                _lac,
                trip.get("trip_short_name"),
            )
            await self._put_event_queue(event)
            _acn += 1

    async def _get_nmbs_feed(self):
        async with aiohttp.ClientSession() as session:
            ws = await  session.ws_connect(self.url)
            while True:
                msg = await ws.receive()

                if msg.type == aiohttp.MsgType.text:
                    if msg.data == 'close':
                        await ws.close()
                        break
                    else:
                        json_resp = msg.json()
                        trips = json_resp[1]['trips']
                        pprint(trips)
                        self._logger.debug("Retrieved %s trips", len(trips))
                        await self.handle_message(trips)

                elif msg.type == aiohttp.MsgType.closed:
                    break
                elif msg.type == aiohttp.MsgType.error:
                    break

    async def run(self):
        """Runs this Thread, Reads from Pollers."""
        self._logger.info(
            "Running NMBSWorker with URL '%s'", self.url.geturl())

        while 1:
            await self._get_nmbs_feed()
            await asyncio.sleep(self.poll_interval)
