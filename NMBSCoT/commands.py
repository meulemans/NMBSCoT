#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""NMBS Cursor-on-Target Gateway Commands."""

import argparse
import asyncio
import os
import sys
import urllib

import pytak

import NMBSCoT

# Python 3.6 support:
if sys.version_info[:2] >= (3, 7):
    from asyncio import get_running_loop
else:
    from asyncio import _get_running_loop as get_running_loop




async def main(opts):
    loop = asyncio.get_running_loop()
    tx_queue: asyncio.Queue = asyncio.Queue()
    rx_queue: asyncio.Queue = asyncio.Queue()
    cot_url: urllib.parse.ParseResult = urllib.parse.urlparse(opts.cot_url)

    # Create our CoT Event Queue Worker
    reader, writer = await pytak.protocol_factory(cot_url)
    write_worker = pytak.EventTransmitter(tx_queue, writer)
    read_worker = pytak.EventReceiver(rx_queue, reader)

    nmbs_url: urllib.parse.ParseResult = urllib.parse.urlparse(opts.nmbs_url)

    message_worker = NMBSCoT.NMBSWorker(
        event_queue=tx_queue,
        url=nmbs_url,
        api_key=opts.api_key,
        poll_interval=opts.poll_interval,
        cot_stale=opts.cot_stale
    )

    await tx_queue.put(NMBSCoT.hello_event())

    done, pending = await asyncio.wait(
        set([message_worker.run(), read_worker.run(), write_worker.run()]),
        return_when=asyncio.FIRST_COMPLETED)

    for task in done:
        print(f"Task completed: {task}")


def cli():
    """Command Line interface for NMBS Cursor-on-Target Gateway."""

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-U', '--cot_url', help='URL to CoT Destination.',
        required=True
    )
    parser.add_argument(
        '-K', '--fts_token', help='FreeTAKServer REST API Token.'
    )
    parser.add_argument(
        '-S', '--cot_stale', help='CoT Stale period, in seconds',
    )

    parser.add_argument(
        '-N', '--nmbs_url', help='NMBS URL.',
        required=True
    )
    opts = parser.parse_args()

    if sys.version_info[:2] >= (3, 7):
        asyncio.run(main(opts), debug=bool(os.environ.get('DEBUG')))
    else:
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(main(opts))
        finally:
            loop.close()


if __name__ == '__main__':
    cli()