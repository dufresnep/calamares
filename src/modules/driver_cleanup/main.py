#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <http://github.com/calamares> ===
#
#   Copyright 2014-2018 KaOS (http://kaosx.us)
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.
#  MA 02110-1301, USA.

import os
import shutil
import subprocess
import re

import libcalamares


def run():
    """ Clean up unused drivers """

    print('cleaning up video drivers')

    install_path = libcalamares.globalstorage.value("rootMountPoint")

    # remove any db.lck
    db_lock = os.path.join(install_path, "var/lib/pacman/db.lck")
    if os.path.exists(db_lock):
        with misc.raised_privileges():
            os.remove(db_lock)

    searchf = "/var/log/used_gfx"
    f = open("/var/log/used_gfx", "r")
    file_c = f.read()
    
    if os.path.exists(searchf):
        if "i915" in file_c:
            libcalamares.utils.debug(file_c)
        else:
            try:
                libcalamares.utils.target_env_call(['pacman', '-R', '--noconfirm',
                                                'xf86-video-intel'])
            except Exception as e:
                pass
        if "nouveau" in file_c:
            libcalamares.utils.debug(file_c)
            sddm_conf_path = os.path.join(install_path, "etc/sddm.conf")
            text = []
            with open(sddm_conf_path, 'r') as sddm_conf:
                text = sddm_conf.readlines()
            with open(sddm_conf_path, 'w') as sddm_conf:
                for line in text:
                    if re.match('Session=plasmawayland.desktop', line):
                        line = 'Session=plasma.desktop'
                    sddm_conf.write(line)                    
        else:
            try:
                libcalamares.utils.target_env_call(['pacman', '-R', '--noconfirm',
                                                'xf86-video-nouveau'])
            except Exception as e:
                pass
        if "amdgpu" in file_c:
            libcalamares.utils.debug(file_c)
        else:
            try:
                libcalamares.utils.target_env_call(['pacman', '-R', '--noconfirm',
                                                'xf86-video-amdgpu'])
            except Exception as e:
                pass
        if "ati" in file_c or "radeon" in file_c:
            libcalamares.utils.debug(file_c)
        else:
            try:
                libcalamares.utils.target_env_call(['pacman', '-R', '--noconfirm',
                                                'xf86-video-ati'])
            except Exception as e:
                pass
        if "vmware" in file_c or "vmwgfx" in file_c:
            libcalamares.utils.debug(file_c)
        else:
            try:
                libcalamares.utils.target_env_call(['pacman', '-R', '--noconfirm',
                                                'xf86-video-vmware'])
            except Exception as e:
                pass
        f.close()
    else:
        try:
            libcalamares.utils.target_env_call(['pacman', '-R', '--noconfirm', 'xf86-video-ati',
                                            'xf86-video-vmware', 'xf86-video-amdgpu'])
        except Exception as e:
            pass

    print('video driver removal complete')

    print('cleaning up input drivers')

    xorg = open("/var/log/Xorg.0.log",  errors="surrogateescape").read()
    if 'wacom' in xorg:
        print('wacom in use')
    else:
        try:
            libcalamares.utils.target_env_call(['pacman', '-Rncs', '--noconfirm',
                                            'xf86-input-wacom'])
        except Exception as e:
            pass

    print('input driver removal complete')

    print('job_cleanup_drivers')

    return None
