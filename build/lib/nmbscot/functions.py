#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""NMBS Cursor-on-Target Gateway Functions."""

import datetime

import pycot

import NMBSCoT

def nmbs_to_cot(trip: dict, stale: int = None,
                 classifier = None) -> pycot.Event:
    """
    Transforms an ADS-B Exchange Aircraft Object to a Cursor-on-Target PLI.
    """
    time = datetime.datetime.now(datetime.timezone.utc)
    stale = stale or NMBSCoT.constants.DEFAULT_STALE

    lat = trip[1]['position'][0]
    lon = trip[1]['position'][1]

    if lat is None or lon is None:
        return None

    callsign = trip[1]['trip_short_name']

    cot_type = "a-f-G-E-V-T"

    point = pycot.Point()
    point.lat = lat
    point.lon = lon
    point.ce = "9999999.0"
    point.le = "9999999.0"
    point.hae = "9999999.0"

    uid = pycot.UID()
    uid.Droid = callsign

    contact = pycot.Contact()
    contact.callsign = callsign+" "+trip[1]['trip_headsign']['nl']

    #remarks = pycot.Remarks()
    #_remarks = "Volgende halte: "


    #if bool(os.environ.get('DEBUG')):
    #    _remarks = f"{_remarks} via nmbscot"

    #remarks.value = _remarks

    detail = pycot.Detail()
    detail.uid = uid
    detail.contact = contact
    #detail.remarks = remarks

    event = pycot.Event()
    event.version = "2.0"
    event.event_type = cot_type
    event.uid = callsign
    event.time = time
    event.start = time
    event.stale = time + datetime.timedelta(seconds=stale)
    event.how = "m-g"
    event.point = point
    event.detail = detail

    return event


def hello_event():
    time = datetime.datetime.now(datetime.timezone.utc)
    name = 'nmbscot'
    callsign = 'nmbscot'

    point = pycot.Point()
    point.lat = '9999999.0'
    point.lon = '9999999.0'

    # FIXME: These values are static, should be dynamic.
    point.ce = '9999999.0'
    point.le = '9999999.0'
    point.hae = '9999999.0'

    uid = pycot.UID()
    uid.Droid = name

    contact = pycot.Contact()
    contact.callsign = callsign

    detail = pycot.Detail()
    detail.uid = uid
    detail.contact = contact

    event = pycot.Event()
    event.version = '2.0'
    event.event_type = 'a-n-G-E-S'
    event.uid = name
    event.time = time
    event.start = time
    event.stale = time + datetime.timedelta(hours=1)
    event.how = 'h-g-i-g-o'
    event.point = point
    event.detail = detail

    return event