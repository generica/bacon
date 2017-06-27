#!/usr/bin/env python
# coding: utf-8

'''
BACON
Copyright (C) 2017 Brett Pemberton

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Bacon module for package operations

Accepts a change structure for a change on a package
'''

import logging
import dbus

LOGGER = logging.getLogger("bacon")

def service_is_running(service):
    ''' See if a service is running or not '''

    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

    if not service.endswith(".service"):
        service += ".service"

    joblist = manager.ListUnits()

    for job in joblist:
        name = job[0]
        active = job[3]
        if name == service:
            if active == 'active':
                return True
            return False

    LOGGER.error("Service %s not found", service)
    return False


def perform_change(service, ensure):
    ''' Perform the change on the resource '''

    sysbus = dbus.SystemBus()
    systemd1 = sysbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
    manager = dbus.Interface(systemd1, 'org.freedesktop.systemd1.Manager')

    if not service.endswith(".service"):
        service += ".service"

    if ensure == 'running':
        manager.StartUnit(service, 'fail')
    elif ensure == 'stopped':
        manager.StopUnit(service)
    elif ensure == 'reload':
        manager.Reload(service)

    return None
