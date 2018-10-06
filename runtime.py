#!/usr/bin/env python3
"""
Copyright (C) 2016, 2017  David Cerny

This file is part of gnunigma

Gnunigma is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from enigma.components import TestEnigma, unittest
from data_handler import DataHandler, platform
from gui import Root


data_handler = DataHandler()
root = Root(data_handler)

if platform == "Linux":
    print("Linux platform detected! Some features (like sound and icons) will be omitted due to compatibility issues...")
    try:
        import tkinter
    except Exception:
        print("Unable to import tkinter graphical library, please install using \"./install.bash\"")

# Main unittest before running, could warn about potential flaws
# If this passes, enigma should be ready for accurate simulation


if data_handler.global_cfg.data['globals']['unit_tests']['startup_test']:
    TestEnigma.model = data_handler.enigma_cfg['model']
    TestEnigma.cfg_path = ['config.yaml']
    unittest.main(exit=False, verbosity=1)


if __name__ == '__main__':
    root.mainloop()
