#!/usr/bin/env python3

from enigma.components import EnigmaFactory
import platform
platform = platform.system()
if platform == "Windows":
    from winsound import PlaySound, SND_ASYNC
from cfg_handler import Config
from glob import glob
from os import path
from tkinter import messagebox


# MISC

class Base:
    """Base initiation class for Tk and TopLevel derivatives"""
    def __init__(self, icon: str, wm_title: str):
        self.attributes("-alpha", 0.0)
        self.after(0, self.attributes, "-alpha", 1.0)
        self.resizable(False, False)
        if platform == "Windows":
            self.iconbitmap(path.join('icons', icon))
        self.wm_title(wm_title)
        self.grab_set()


class Playback:
    """Module for playing sounds from the sounds folder"""
    def __init__(self, master_instance):
        self.platform = platform
        self.sounds = list(
            map(lambda snd: snd[7:], glob(path.join('sounds', '*.wav'))))
        self.master_instance = master_instance

    def play(self, sound_name):
        """Plays a sound based on the entered sound name"""
        sound_name += '.wav'

        if sound_name in self.sounds and self.master_instance.sound_enabled:
            if self.platform == "Windows":
                PlaySound(path.join('sounds', sound_name), SND_ASYNC)


class DataHandler:
    """Holds all up to date data and distributes it accross the whole program"""
    def __init__(self, master=None):
        self.global_cfg = Config('config.yaml', 'unordered')
        self.master = master
        self.enigma_factory = EnigmaFactory(['enigma', 'historical_data.yaml'])
        self.enigma = None
        self.playback = Playback(master)
        self.switch_enigma()

    def switch_enigma(self, model='Enigma1', **config):
        """Switches current enigma model"""
        if self.master:
            self.enigma = self.enigma_factory.produce_enigma(model, **config,
                                                             master=self.master)
        else:
            self.enigma = self.enigma_factory.produce_enigma(model, **config)

    def set_master(self, master):
        """Sets datahandler gui tkinter master"""
        self.master = master
        self.playback.master_instance = master
        self.switch_enigma()

    @property
    def font(self):
        """Returns font from config"""
        font = self.global_cfg.data['globals']['font']
        return font['style'], font['size']

    @property
    def bg(self):
        """Returns background color from config"""
        return self.global_cfg.data['globals']['bg']['color']

    @property
    def enigma_cfg(self):
        """Returns default enigma settings"""
        return self.global_cfg.data['globals']['enigma_defaults']

    @property
    def settings_vars(self):
        """Returns setting variables for gui"""
        return self.global_cfg.data['globals']['setting_vars']

    @property
    def rights_accepted(self):
        return self.global_cfg.data['globals']['rights_accepted']

    def accept_rights(self):
        self.global_cfg.data['globals']['rights_accepted'] = True
        self.global_cfg.write()

    def save_config(self):
        """Saves all important configuration to the global_cfg file"""
        data = dict(gui=dict(sound_enabled=str(self.master.sound_enabled),
                    autorotate=str(self.master.autorotate),
                    rotor_lock=str(self.master.rotor_lock),
                    synchronised_scrolling=str(self.master.sync_scroll),
                    show_numbers=str(self.master.show_numbers)),
                    enigma=dict(self.enigma.dump_config()))

        self.global_cfg.data['saved'].clear()
        self.global_cfg.data['saved']['gui'] = dict(**data['gui'])
        self.global_cfg.data['saved']['enigma'] = dict(**data['enigma'])

        self.global_cfg.write()

    def load_config(self):
        """Returns data for configuration loading"""
        data = None
        try:
            data = dict(enigma=self.global_cfg.data['saved']['enigma'],
                        gui=self.global_cfg.data['saved']['gui'])
        except AssertionError:
            messagebox.showerror('Configuration loading error',
                                 'No configuration available')
        finally:
            return data

    def remove_config(self):
        """Clears configuration data"""
        self.global_cfg.data['saved'] = {}
        self.global_cfg.data['globals']['rights_accepted'] = False
        self.global_cfg.write()
