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

from itertools import chain
from data_handler import Base
from re import sub, findall
from tkinter import *
from tkinter import messagebox
from webbrowser import open as open_browser
from enigma.components import alphabet, are_unique


class CopyrightNotice(Toplevel):
    """GNU GPLv3 copyright notice window"""
    def __init__(self, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        Base.__init__(self, '', 'GNU GPLv3 Copyright Notice')


        main_frame = Frame(self)
        self.scrollbar = Scrollbar(main_frame)
        self.copyright_view = Text(main_frame, width=78, height=40, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.copyright_view.yview)
        Label(main_frame, text="GNU GPLv3 - Know your rights!", font=("Arial", 12, "bold")).pack(side='top', fill='x')

        with open('LICENSE.txt', 'r') as file:
            self.copyright_view.insert(0.0, file.read())

        self.copyright_view.config(state='disabled')
        self.copyright_view.pack(side='left')
        self.scrollbar.pack(side='right', fill='both')

        main_frame.pack(side='top')

        button_frame = Frame(self)
        self.accept_button = Button(button_frame, text="I Agree", command=self.rights_accepted)
        self.accept_button.pack(side='right')

        button_frame.pack(side='bottom')

    def rights_accepted(self):

        self.destroy()


# ROOT

class Root(Tk, Base):
    """Root GUI class with enigma entry field, plugboard button, rotor button"""
    def __init__(self, data_handler, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.data_handler = data_handler
        self.data_handler.set_master(self)  # Sets up master for TkEnigma

        if not self.data_handler.rights_accepted:
            self.wait_window(CopyrightNotice())
            self.data_handler.accept_rights()

        Base.__init__(self, 'enigma.ico', self.data_handler.enigma_cfg['model'])
        self.root_menu = None

        self.option_add("*font", self.data_handler.font)

        # Settings vars ( set by default to 1,1,0,1 as an emergency measure )
        self._sound_enabled = IntVar(value=1)
        self._autorotate = IntVar(value=1)
        self._rotor_lock = IntVar(value=0)
        self._sync_scroll = IntVar(value=1)
        self._show_numbers = IntVar(value=0)
        self.__reset_setting_vars()

        self._show_numbers.trace('w', lambda *args: self.indicator_board.update_indicators())

        # Frames
        self.rotor_container = Frame(self, bd=1, relief='raised', bg=self.data_handler.bg)

        # Lid
        Button(self.rotor_container, text='\n'.join('Rotors'),
               command=self.rotor_menu).pack(side='right', pady=5, padx=(15, 4))

        # Plugboard
        if self.data_handler.enigma.has_plugboard:
            self.plugboard_frame = Frame(self)

            self.open_plugboard = Button(self.plugboard_frame, text='Plugboard',
                                         command=self.plugboard_menu)
            self.open_uhr = Button(self.plugboard_frame, text='Uhr', command=self.uhr_menu)

            # Plugboard init
            config = dict(side='left', padx=3, pady=3, fill='x', expand=True)
            self.open_plugboard.pack(**config)
            self.open_uhr.pack(**config)
            self.plugboard_frame.pack(side='bottom', fill='both')

        # Lid init
        self.rowconfigure(index=0, weight=1)

        # Container init
        self.io_board = IOBoard(self, self, self.data_handler)
        self.lightboard = Lightboard(self, self.data_handler)

        # Object not updated after reset!
        self.indicator_board = IndicatorBoard(self.rotor_container, self.data_handler)
        self.indicator_board.pack()
        self.rotor_container.pack(fill='both', padx=5, pady=5, side='top')
        self.lightboard.pack(side='top', fill='both', padx=5)
        self.io_board.pack(side='top')

        self.__make_root_menu()
        self.refresh_uhr_button()

    def __reset_setting_vars(self):
        """Resets setting variables to defaults"""
        var_config = self.data_handler.settings_vars
        self._autorotate.set(var_config['autorotate'])
        self._sound_enabled.set(var_config['sound_enabled'])
        self._sync_scroll.set(var_config['sync_scroll'])
        self._rotor_lock.set(var_config['rotor_lock'])
        self._show_numbers.set(var_config['show_numbers'])

    @property
    def rotor_lock(self):
        """Returns current rotor lock status"""
        return self._rotor_lock.get()

    @property
    def sound_enabled(self):
        """Returns current sound status"""
        return self._sound_enabled.get()

    @property
    def show_numbers(self):
        """Returns if numbers should be shown on indicators"""
        return self._show_numbers.get()

    def hard_reset(self, *event):
        """Sets all settings to default"""
        self.data_handler.switch_enigma(self.current_model.get())
        if self.data_handler.enigma.has_plugboard:
            self.data_handler.enigma.clear_plugboard()
        self.reload_plugboard_buttons()
        self.soft_reset()
        self.update_indicators()
        self.__reset_setting_vars()

    def soft_reset(self):
        """Softly resets and updates indicators"""
        self.io_board.text_input.delete('0.0', 'end')
        self.lightboard.light_up('')
        self.io_board.format_entries()
        self.io_board.last_len = 0
        self.wm_title(self.current_model.get())
        self.refresh_uhr_button()
        self.indicator_board.reload_indicators()

    def plugboard_menu(self):
        """Opens the plugboard GUI"""
        self.wait_window(PlugboardMenu(self.data_handler))
        self.refresh_uhr_button()

    def reload_plugboard_buttons(self):
        """Reloads plugboard buttons ( they will only be shown if the current
        enigma has a plugboard )"""
        self.plugboard_frame.destroy()
        if self.data_handler.enigma.has_plugboard:
            self.plugboard_frame = Frame(self)

            self.open_plugboard = Button(self.plugboard_frame, text='Plugboard',
                                         command=self.plugboard_menu)
            self.open_uhr = Button(self.plugboard_frame, text='Uhr',
                                   command=self.uhr_menu)

            # Plugboard init
            config = dict(side='left', padx=3, pady=3, fill='x', expand=True)
            self.open_plugboard.pack(**config)
            self.open_uhr.pack(**config)
            self.plugboard_frame.pack(side='bottom', fill='both')

    def refresh_uhr_button(self):
        """Refreshes uhr button ( only activated if uhr is currently
        connected to the plugboard"""
        if self.data_handler.enigma.has_plugboard:
            if self.data_handler.enigma.uhr_connected:
                self.open_uhr.config(state='active')
            else:
                self.open_uhr.config(state='disabled')

    def rotor_menu(self):
        """Opens the rotor gui and applies new values after closing"""
        self.wait_window(RotorMenu(self.data_handler))
        self.io_board.text_input.delete('0.0', 'end')
        self.io_board.format_entries()
        if len(self.indicator_board.indicators) != len(self.data_handler.enigma.rotors):
            self.indicator_board.reload_indicators()
        self.lightboard.light_up('')

    def uhr_menu(self):
        """Opens the Uhr menu ( uhr settings are adjusted there )"""
        self.wait_window(UhrMenu(self.data_handler))

    def __make_root_menu(self):
        """Creates the top bar menu with saving/loading, various settings etc."""
        root_menu = Menu(self, tearoff=0)
        settings_menu = Menu(root_menu, tearoff=0)
        root_menu.add_cascade(label='Settings', menu=settings_menu)
        root_menu.add_command(label='About', command=lambda: open_browser(
            'https://github.com/cernyd/enigma'))

        # CONFIGURATION MENU
        config_menu = Menu(settings_menu, tearoff=0)

        config_menu.add_command(label='Save Configuration',
                                command=self.save_config)
        config_menu.add_command(label='Load Configuration',
                                command=self.load_config)
        config_menu.add_command(label='Delete Configuration',
                                command=self.data_handler.remove_config)

        # SAVING AND LOADING
        settings_menu.add_cascade(label='Saving and Loading', menu=config_menu)

        settings_menu.add_separator()
        settings_menu.add_checkbutton(label='Enable sound',
                                           variable=self._sound_enabled)
        settings_menu.add_checkbutton(label='Autorotate',
                                           variable=self._autorotate)
        settings_menu.add_checkbutton(label='Rotor lock',
                                           variable=self._rotor_lock)
        settings_menu.add_checkbutton(label='Synchronised scrolling',
                                           variable=self._sync_scroll)
        settings_menu.add_checkbutton(label='Numbers on rotor indicators',
                                           variable=self._show_numbers)
        settings_menu.add_separator()

        # ENIGMA RESET AND MODEL SETTINGS
        enigma_model_menu = Menu(settings_menu, tearoff=0)

        # Current model var, must add some indication of current model into the enigma
        self.current_model = StringVar(value=self.data_handler.enigma.factory_data['model'])
        for model in self.data_handler.enigma_factory.all_models():
            enigma_model_menu.add_radiobutton(label=model, variable=self.current_model)
        self.current_model.trace('w', self.hard_reset)
        settings_menu.add_cascade(label='Enigma model', menu=enigma_model_menu)
        settings_menu.add_command(label='Reset all', command=self.hard_reset)

        self.config(menu=root_menu)

    def update_indicators(self):
        """Reloads rotor indicators"""
        self.indicator_board.update_indicators()

    @property
    def sync_scroll(self):
        """Input and output scrollbars replicate eachothers movements"""
        return self._sync_scroll.get()

    @property
    def show_numbers(self):
        """If numbers should be shown on rotor indicators"""
        return self._show_numbers.get()
    
    @property
    def autorotate(self):
        """This enables automatic rollback of rotor positions when deleting text
        from input box"""
        return self._autorotate.get()

    def save_config(self):
        """Saves all configurations to xml"""
        self.data_handler.save_config()

    def load_config(self):
        """Loads all configurations from xml"""
        data = self.data_handler.load_config()

        if data:
            enigma_cfg = data['enigma']

            plugboard_data = dict(normal_pairs=enigma_cfg.pop('normal_pairs'),
                                  uhr_pairs=enigma_cfg.pop('uhr_pairs'))

            reflector_pairs = enigma_cfg.get('reflector_pairs', [])

            position_data = dict(rotor_positions=enigma_cfg.pop('rotor_positions'),
                                 ring_settings=enigma_cfg.pop('ring_settings'))

            uhr_position = enigma_cfg.pop('uhr_position')

            self.current_model.set(enigma_cfg['model'])

            self._sound_enabled.set(data['gui']['sound_enabled'])
            self._autorotate.set(data['gui']['autorotate'])
            self._rotor_lock.set(data['gui']['rotor_lock'])
            self._sync_scroll.set(data['gui']['synchronised_scrolling'])
            self._show_numbers.set(data['gui']['show_numbers'])
            self.data_handler.switch_enigma(**enigma_cfg)
            self.data_handler.enigma.plugboard = plugboard_data
            self.data_handler.enigma.positions = position_data['rotor_positions']
            self.data_handler.enigma.ring_settings = position_data['ring_settings']
            self.data_handler.enigma.reflector_pairs = reflector_pairs
            self.data_handler.enigma.uhr_position = uhr_position

            self.soft_reset()


# PLUGBOARD MENU

class PlugboardMenu(Toplevel, Base):
    """GUI for visual plugboard pairing setup"""
    def __init__(self, data_handler, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        Base.__init__(self, 'plugboard.ico', 'Plugboard')

        self.data_handler = data_handler
        self.used = []  # All used letters
        self._uhr_mode = IntVar(0)

        labels = self.data_handler.enigma.factory_data['labels']
        layout = self.data_handler.enigma.factory_data['layout']

        # BUTTONS
        button_frame = Frame(self)
        self.apply_button = Button(button_frame, text='Apply', width=12,
                                   command=self.apply)
        self.clear_button = Button(button_frame, text='Clear all pairs',
                                   width=15, command=self.clear_all)

        # PLUG PAIRS
        rows = []
        self.plug_sockets = []

        # Frame in which all plugs are contained
        plug_socket_frame = Frame(self)

        # Creating plug objects
        for row in layout:
            new_row = Frame(plug_socket_frame)
            for item in row:
                self.plug_sockets.append(PlugSocket(self, new_row,
                                                    self.data_handler.enigma,
                                                    labels[item]))
            rows.append(new_row)

        # Packs rows vertically
        for row in rows:
            row.pack(side='top')

        # Packs item in a row
        for item in self.plug_sockets:
            item.pack(side='left')

        # Packing the whole frame
        plug_socket_frame.pack(side='top')

        # This uhr mode will be used to distinguish between choosing uhr vs
        # normal pairs > different colors.

        self.uhr_mode_button = Checkbutton(button_frame, text='Uhr pairs',
                                           variable=self._uhr_mode)
        self.uhr_mode_button.pack(side='left')

        storno_button = Button(button_frame, text='Storno', width=12,
                               command=self.destroy)

        self.apply_button.pack(side='right', padx=5, pady=5)
        self.clear_button.pack(side='right', padx=5, pady=5)
        storno_button.pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

    def refresh_apply_button(self):
        """Sets apply button to active if all conditions are met"""
        if len(self.pairs['uhr_pairs']) in (10, 0):
            self.apply_button.config(state='active')
        else:
            self.apply_button.config(state='disabled')

    @property
    def uhr_mode(self):
        """Determines if uhr pairs are currently being set or not"""
        return self._uhr_mode.get()

    @uhr_mode.setter
    def uhr_mode(self, value):
        """Sets uhr mode"""
        self._uhr_mode.set(value)

    def apply(self):
        """Applies all new pairs to the plugboard"""
        try:
            self.data_handler.enigma.plugboard = self.pairs
            self.destroy()
        except AssertionError:
            err_msg = 'Exactly 10 Uhr pairs (red pairs) must be set before applying!'
            messagebox.showerror('Invalid number of Uhr pairs', err_msg)

    def delete_used(self, letter):
        """Removes letter from used letter list"""
        self.refresh_apply_button()
        try:
            self.used.remove(letter)
        except ValueError:
            pass

    def add_used(self, letter):
        """Adds letter to used letter list"""
        self.refresh_apply_button()
        if letter not in self.used:
            self.used.append(letter)

    def clear_all(self):
        """Clears all plugboard pairs"""
        self.data_handler.enigma.clear_plugboard()
        for socket in self.plug_sockets:
            socket.unlink()

    def get_target(self, label):
        """Returns object with the target label, presumably for linking."""
        for socket in self.plug_sockets:
            if socket.label == label:
                return socket

    @property
    def pairs(self):
        """Returns all pairs"""
        pairs = {'normal_pairs': [], 'uhr_pairs': []}

        for socket in self.plug_sockets:
            pair = socket.pair['pair']

            unique = True
            for pair_type in 'normal_pairs', 'uhr_pairs':
                if pair not in pairs[pair_type] and pair[::-1] not in pairs[pair_type]:
                    continue
                unique = False
                break

            if all(pair) and unique and socket.pair['type']:
                pairs[socket.pair['type']].append(pair)

        return pairs


class PlugSocket(Frame):
    """Custom made socket class"""
    def __init__(self, master, tk_master, enigma, label, *args, **kwargs):
        Frame.__init__(self, tk_master, *args, **kwargs)

        self._label = label
        self.master = master
        self.enigma = enigma
        self.pair_obj = None
        self.pair_type = None
        self.skip_next = False
        self.nondefault_color = False

        Label(self, text=label).pack(side='top')

        self.plug_socket = PlugEntry(self, self, width=2, justify='center')

        self.plug_socket.pack(side='bottom', pady=5, padx=12)

        # Loading data ( the problem with plug color is most likely here )
        if self.label not in ''.join(self.master.used):
            for key, value in self.enigma.plugboard.items():
                for pair in value:
                    if self.label in pair:
                        self.pair_type = key
                        if key == 'uhr_pairs':
                            self.master.uhr_mode = 1
                        if pair[0] != self.label:
                            self.plug_socket.set(pair[0])
                        else:
                            self.plug_socket.set(pair[1])

                            self.master.uhr_mode = 0
                        break

    @property
    def pair(self):
        """Returns pair"""
        return {'pair': (self.label + self.get_socket()), 'type': self.pair_type}

    def link(self, target='', obj=None):
        """Links with another object of the same type"""
        pair_type = 'normal_pairs'

        if self.skip_next:
            self.skip_next = False
        else:
            if not obj:  # Link constructed locally
                if self.master.uhr_mode:
                    pair_type = 'uhr_pairs'
                    self.set_color(bg='red', fg='white')
                else:
                    self.set_color(bg='black', fg='white')
                if target:
                    obj = self.master.get_target(target)
                    if obj:
                        if self.master.uhr_mode:
                            if not obj.nondefault_color:
                                obj.set_color(bg='gray', fg='white')
                        else:
                            obj.set_color(bg='black', fg='white')
                        obj.link(obj=self)
                    else:
                        return
                else:
                    return

            self.pair_type = pair_type
            self.skip_next = True
            self.plug_socket.set(obj.label)
            self.skip_next = False
            self.pair_obj = obj
            self.master.add_used(self.label)

            if self.label in ''.join(chain(self.enigma.plugboard['uhr_pairs'])):
                color = self.enigma.uhr_letter_color(self.label)
                self.set_color(**color)

    def unlink(self, external=False):
        """Unlinks a letter pair"""
        if self.skip_next:
            self.skip_next = False
        else:
            self.master.delete_used(self.label)
            self.set_color(bg='white', fg='black')

            if self.pair_obj:
                if not external:  # Would cause a loop presumably
                    self.pair_obj.unlink(True)
                self.skip_next = True
                self.plug_socket.clear()
                self.skip_next = False
                self.pair_obj = None
                self.pair_type = None

    def set_color(self, fg='black', bg='white'):
        """Sets bg and fg color while updating the nondefault_color indicator"""
        if fg == 'black' and bg == 'white':
            self.nondefault_color = False
        else:
            self.nondefault_color = True
        self.plug_socket.config(fg=fg, bg=bg)

    @property
    def label(self):
        """Returns label of the plugsocket ( as shown in gui )"""
        return self._label[0]

    def get_socket(self):
        """Gets currently entered socket value"""
        return self.plug_socket.get()

    @property
    def local_forbidden(self):
        """Adds the label of the current plug to filtered letters"""
        if self.label not in self.master.used:
            return [self.label] + self.master.used
        else:
            return self.master.used

    def callback(self, event_type):
        """Callback from the plug_entry widget"""
        if event_type == 'WRITE':
            self.link(self.plug_socket.get())
        elif event_type == 'DELETE':
            self.unlink()


class PlugEntry(Entry):
    def __init__(self, master, tk_master, *args, **kwargs):
        # Superclass constructor call
        self.internal_tracer = StringVar()
        Entry.__init__(self, tk_master, *args, **kwargs,
                       textvariable=self.internal_tracer)

        self.internal_tracer.trace('w', self.event)
        self.master = master
        self.last_val = ''

    def event(self, *event):
        """Reports an event to its plugsocket"""
        new_val = self.validate(self.get())  # Raw new data

        if self.last_val and not new_val:
            this_action = 'DELETE'
        elif not self.last_val and new_val:
            this_action = 'WRITE'
        else:
            this_action = None

        self.set(new_val)
        self.last_val = new_val
        self.last_action = this_action

        if this_action:
            self.master.callback(this_action)

    def clear(self):
        """Clears the plugsocket"""
        self.delete('0', 'end')

    def set(self, string):
        """Sets the plugsocket"""
        self.clear()
        self.insert(0, string)

    def get(self):
        """Returns socket value"""
        return Entry.get(self).upper()

    def validate(self, raw):
        """Validates socket contents"""
        forbidden = ''.join(self.master.local_forbidden)
        raw = sub('([\s]|[%s]|[^a-zA-Z])+' % forbidden, '', raw).upper()
        return raw[0] if raw else raw


# UHR MENU

class UhrMenu(Toplevel, Base):
    """Menu for selecting Uhr position"""
    def __init__(self, data_handler, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        Base.__init__(self, 'uhr.ico', 'Uhr menu')

        self.data_handler = data_handler
        selector_frame = Frame(self)
        self.geometry('225x85')

        self.left_button = Button(selector_frame, text='<', relief='raised', command=lambda: self.rotate(-1))
        self.position_indicator = Label(selector_frame, relief='sunken', width=2, font=('', 25))
        self.right_button = Button(selector_frame, text='>', relief='raised', command=lambda: self.rotate(1))

        self.left_button.pack(side='left')
        self.position_indicator.pack(side='left', padx=10, pady=5)
        self.right_button.pack(side='left')

        selector_frame.pack(side='top')

        button_frame = Frame(self)
        Button(button_frame, text='Close', command=self.destroy).pack(side='right')
        button_frame.pack(side='bottom', padx=5, pady=5)

        self.refresh_indicator()

    def rotate(self, places=0):
        """Rotates uhr selector ( with the bakelite disk
        in the real thing... )"""
        self.data_handler.playback.play('click')
        self.data_handler.enigma.uhr_position += places
        self.refresh_indicator()

    def refresh_indicator(self):
        """Refreshes uhr indicator ( 00, 01, .... 39 )"""
        text = '{:0>2}'.format(self.data_handler.enigma.uhr_position)
        self.position_indicator.config(text=text)


# ROTOR MENU

class RotorMenu(Toplevel, Base):
    """GUI for setting rotor order, reflectors and ring settings"""
    def __init__(self, data_handler, *args, **kwargs):
        self.data_handler = data_handler
        bg = self.data_handler.bg

        Toplevel.__init__(self, bg=bg, *args, **kwargs)
        Base.__init__(self, 'rotor.ico', 'Rotor order')

        # Enigma settings buffer
        self.curr_rotors = [rotor.label for rotor in self.data_handler.enigma.rotors]
        self.curr_reflector = self.data_handler.enigma.reflector.label
        self.last_reflector = self.data_handler.enigma.reflector.label
        self.curr_ring_settings = self.data_handler.enigma.ring_settings

        self.ukw_D_pairs = []

        # Frames
        self.main_frame = Frame(self, bg=bg)
        button_frame = Frame(self, bg=bg)

        # Buttons
        self.ukw_D_setup = Button(button_frame, text='UKW-D Pairs',
                                  command=self.ukwd_menu)
        self.ukw_D_setup.pack(side='left', padx=10, pady=5)

        Button(button_frame, text='Apply', width=12, command=self.apply).pack(
            side='right', padx=10, pady=5)


        Button(button_frame, text='Storno', width=12,
               command=self.destroy).pack(side='right', padx=5, pady=5)

        button_frame.pack(side='bottom', fill='x')

        # Slots for settings
        self.reflector = ReflectorSlot(self, self.main_frame,
                                       self.data_handler.enigma.factory_data['reflectors'])
        self.reflector.pack(side='left', fill='y', padx=(10, 2), pady=5)

        self.rotors = []
        self.reload_rotor_slots()

        [rotor.pack(side='left', padx=2, pady=5, fill='y') for rotor in self.rotors]

        self.main_frame.pack(side='top', pady=(5, 0), padx=(0, 10))

        self.update_rotors()
        self.update_reflector()

    def ukwd_menu(self):
        """Opens menu where UKW-D pairs are set"""
        self.wait_window(UKWDMenu(self))

    def reload_rotor_slots(self):
        """Reloads rotor slots according to the current number of rotors"""
        for rotor in self.rotors:
            rotor.destroy()

        rotor_count = self.data_handler.enigma.rotor_count
        if self.curr_reflector == 'UKW-D' and rotor_count == 4:
            rotor_count = 3

        self.rotors = []
        for index in range(rotor_count):
            self.rotors.append(
                RotorSlot(self, self.main_frame, index, self.data_handler))

        [rotor.pack(side='left', padx=2, pady=5, fill='y') for rotor in
         self.rotors]

        self.curr_rotors = self.data_handler.enigma.factory_data['rotors'][:rotor_count]

    def apply(self):
        """Applies all settings to the global enigma instance"""
        self.data_handler.enigma.reflector = self.curr_reflector
        self.data_handler.enigma.rotors = self.curr_rotors
        self.data_handler.enigma.ring_settings = [alphabet[setting] for setting in self.curr_ring_settings]
        self.destroy()

    def update_rotors(self, *event):
        """Updates available radios for all slots"""
        try:
            for rotor in self.rotors:
                rotor.update_selected()
            for rotor in self.rotors:
                rotor.update_available()
        except AttributeError:  # If the rotor group does not exist yet
            pass

    def update_reflector(self, *event):
        """Updates current reflector choice, this triggers a rotor reload if
        UKW-D is set or unset"""
        if hasattr(self, 'reflector'):
            reflector_val = self.reflector.choice_var.get()
            if reflector_val == 'UKW-D':
                self.reload_rotor_slots()
                self.ukw_D_setup.config(state='active')
                if self.data_handler.enigma.rotor_count == 4:
                    self.reload_rotor_slots()
            elif self.last_reflector == 'UKW-D' and reflector_val != 'UKW-D':
                self.reload_rotor_slots()
                self.ukw_D_setup.config(state='disabled')
            else:
                self.ukw_D_setup.config(state='disabled')

            self.last_reflector = reflector_val


class UKWDMenu(Toplevel, Base):
    """Menu for selecting UKW-D pairs"""
    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, *args, **kwargs)
        Base.__init__(self, 'rotor.ico', 'UKW-D Settings')

        button_frame = Frame(self)
        self.master = master

        self.apply_button = Button(button_frame, text='Apply', command=self.apply)
        config = dict(side='right', padx=10, pady=5)
        self.apply_button.pack(**config)
        Button(button_frame, text='Storno', command=self.destroy).pack(**config)
        button_frame.pack(side='bottom')

        self.entry_var = StringVar()
        self.pair_entry = Entry(self, textvariable=self.entry_var, width=50)
        self.pair_entry.insert('0', self.master.data_handler.enigma.reflector_pairs)
        self.pair_entry.pack(side='top', padx=10, pady=5)
        self.entry_var.trace('w', self.refresh_apply_button)

    def apply(self):
        """Applies UKW-D pairs to UKW-D"""
        self.master.ukw_D_pairs = list(self.pair_entry.get())
        self.destroy()

    def refresh_apply_button(self, *event):
        """Enables apply button if all conditions are met"""
        validated_text = sub('[^a-zA-Z ]+', '', self.pair_entry.get()).upper()

        if validated_text != self.pair_entry.get():
            self.pair_entry.delete('0', 'end')
            self.pair_entry.insert('0', validated_text)

        text_valid = not findall('(\s[^\s]\s)|[^\s]{3,}|JY', validated_text)
        pairs_unique = are_unique(validated_text.split())
        valid_length = len(validated_text.split()) == 12

        if text_valid and pairs_unique and valid_length:
            valid = True
            for pair in validated_text.split():
                if len(pair) != 2:
                    valid = False
            if valid:
                self.apply_button.config(state='active')
            else:
                self.apply_button.config(state='disabled')
        else:
            self.apply_button.config(state='disabled')

        if not validated_text:
            self.apply_button.config(state='active')


class BaseSlot(Frame):
    """Base for RotorSlot and ReflectorSlot that are used in the ReflectorMenu"""
    def __init__(self, master, tk_master, text, *args, **kwargs):
        Frame.__init__(self, tk_master, bd=1, relief='raised', *args, **kwargs)

        Label(self, text=text, bd=1, relief='sunken').pack(side='top', padx=5,
                                                           pady=5)

        self.tk_master = tk_master
        self.master = master
        self.choice_var = StringVar()
        self.radio_group = []

    def generate_contents(self, contents):
        """Generates RadioButtons"""
        for item in contents:
            radio = Radiobutton(self, text=item, variable=self.choice_var, value=item)
            radio.pack(side='top')
            self.radio_group.append(radio)

    def update_available(self, radio_value, event=None):
        """Updates if radio buttons are enabled or disabled"""
        try:
            for radio in self.radio_group:
                if radio['value'] in radio_value:
                    if radio['value'] != self.choice_var.get():
                        radio.config(state='disabled')
                else:
                    radio.config(state='active')
        except TclError:
            pass


class RotorSlot(BaseSlot):
    """Used to select rotors in the rotor menu"""
    def __init__(self, master, tk_master, index, data_handler, *args, **kwargs):
        ring_labels = data_handler.enigma.factory_data['labels']
        rotors = data_handler.enigma.factory_data['rotors']

        labels = ['SLOW', 'MEDIUM', 'FAST']

        if data_handler.enigma.rotor_count == 4:
            labels.insert(0, 'THIN')

        text = labels[index] + ' ROTOR'

        BaseSlot.__init__(self, master, tk_master, text, *args, **kwargs)
        self.choice_var.trace('w', self.master.update_rotors)

        self.index = index
        self.labels = ring_labels

        self.generate_contents(rotors)

        # Ring setting indicator
        setting = self.master.data_handler.enigma.ring_settings[index]

        self.ring_var = StringVar(value=ring_labels[alphabet.index(setting)])

        Label(self, text='RING\nSETTING', bd=1, relief='sunken').pack(
            side='top', fill='x', padx=4)
        OptionMenu(self, self.ring_var, *ring_labels).pack(side='top')

        self.choice_var.set(self.master.data_handler.enigma.rotors[index].label)
        self.ring_var.trace('w', self.master.update_rotors)

    def update_selected(self, *event):
        """Updates currently selected values in master ( RotorMenu )"""
        self.master.curr_rotors[self.index] = self.choice_var.get()
        ring_setting = self.labels.index(self.ring_var.get())
        self.master.curr_ring_settings[self.index] = ring_setting

    def update_available(self, *event):
        """Updates what values are currently available"""
        BaseSlot.update_available(self, radio_value=self.master.curr_rotors)


class ReflectorSlot(BaseSlot):
    """Used for selecting reflectors in the RotorMenu"""
    def __init__(self, master, tk_master, reflectors, *args, **kwargs):
        BaseSlot.__init__(self, master, tk_master, 'REFLECTOR', *args, **kwargs)
        self.choice_var.trace('w', self.master.update_reflector)

        self.generate_contents(reflectors)
        radio = Radiobutton(self, text='UKW-D', variable=self.choice_var, value='UKW-D')
        radio.pack(side='bottom', pady=5)
        self.choice_var.set(self.master.data_handler.enigma.reflector.label)
        self.choice_var.trace('w', self.update_selected)

    def update_selected(self, *event):
        """Updates what values are selected in the master ( RotorMenu )"""
        self.master.curr_reflector = self.choice_var.get()


# INDICATOR BOARD( in the main gui )

class IndicatorBoard(Frame):
    """Contains all rotor indicators"""
    def __init__(self, tk_master, data_handler, *args, **kwargs):
        self.data_handler = data_handler
        bg = self.data_handler.bg
        Frame.__init__(self, tk_master, bg=bg, *args, **kwargs)

        self.indicators = []
        self.reload_indicators()

    def reload_indicators(self):
        """Reloads rotor indicators ( useful when switching rotor count )"""
        for indicator in self.indicators:
            indicator.destroy()

        self.indicators = []

        for index in range(self.data_handler.enigma.rotor_count):
            indicator = RotorIndicator(self, index, self.data_handler)
            self.indicators.append(indicator)
            indicator.pack(side='left', fill='both', pady=10)

    def update_indicators(self):
        """Update all values shown on the rotor indicators"""
        [indicator.update_indicator() for indicator in self.indicators]


class RotorIndicator(Frame):
    """Rotor indicator for indicating or rotating a rotor"""
    def __init__(self, tk_master, index, data_handler, *args, **kwargs):
        self.data_handler = data_handler
        bg = self.data_handler.bg
        Frame.__init__(self, tk_master, bg=bg, *args, **kwargs)
        self.index = index

        cfg = dict(width=1)

        Button(self, text='+', command=lambda: self.rotate(1), **cfg).pack(
            side='top')

        self.indicator = Label(self, bd=1, relief='sunken', width=2)

        Button(self, text='-', command=lambda: self.rotate(-1), **cfg).pack(
            side='bottom')

        self.indicator.pack(side='top', pady=10, padx=20)

        self.update_indicator()

    def rotate(self, places=0):
        """Rotates the rotor with the selected index backward"""
        self.data_handler.playback.play('click')
        self.data_handler.enigma.rotors[self.index].rotate(places)
        self.update_indicator()

    def update_indicator(self, *event):
        """Updates what is displayed on the indicator"""
        text = self.data_handler.enigma.positions[self.index]
        if self.data_handler.master.show_numbers:
            text = '{:0>2}'.format(alphabet.index(text)+1)
        self.indicator.config(text=text)


# IOBOARD

class IOBoard(Frame):
    """Boards where user input and output is handled"""
    def __init__(self, tk_master, master, data_handler, *args, **kwargs):
        Frame.__init__(self, tk_master, *args, *kwargs)
        self.data_handler = data_handler
        self.master = master
        self.master.bind('<Key>', self.press_event)

        # Scrollbars
        command = lambda *args: self.yview_sync(self.text_input, self.text_output, *args)
        self.input_scrollbar = Scrollbar(self, command=command)
        command = lambda *args: self.yview_sync(self.text_output, self.text_input, *args)
        self.output_scrollbar = Scrollbar(self, command=command)

        # IO init
        Label(self, text='Input').grid(row=0, column=0)

        command = lambda *args: self.yscrollcommand_sync(self.input_scrollbar, self.output_scrollbar, *args)
        self.text_input = Text(self, width=25, height=5,
                               yscrollcommand=command)

        self.text_input.is_input_widget = True

        Label(self, text='Output').grid(row=2, column=0)

        command = lambda *args: self.yscrollcommand_sync(self.output_scrollbar, self.input_scrollbar, *args)
        self.text_output = Text(self, width=25, height=5, yscrollcommand=command, state='disabled')

        self.input_scrollbar.grid(row=1, column=1, sticky='ns')
        self.output_scrollbar.grid(row=3, column=1, sticky='ns')

        # IO init
        self.text_input.grid(row=1, column=0, padx=3, pady=2)
        self.text_output.grid(row=3, column=0, padx=3, pady=2)

        self.last_len = 0  # Last input string length

    def status(self):
        """Checks for any changes in the entered text length"""
        input_length = len(self.input_box)

        if self.last_len != input_length:
            len_difference = input_length - self.last_len

            if self.last_len > input_length:
                self.last_len = input_length
                return 'shorter', len_difference
            elif self.last_len < input_length:
                self.last_len = input_length
                return 'longer', len_difference
        else:
            return False, 0

    def format_entries(self):
        """Ensures input/output fields have the same length"""
        sanitized_text = self.format_string(self.input_box)
        self.input_box = sanitized_text
        self.output_box = self.output_box[:len(sanitized_text)]

    @staticmethod
    def format_string(string):
        """Formats string to valid text ( letters only )"""
        return sub(r"[^A-Za-z]", '', string)

    def press_event(self, event=None):
        """Activates if any key is pressed, performs analysis on what happened,
        if text was correctly edited, it adds encrypted letters from the enigma
        to output box."""
        correct_widget_type = type(event.widget) == Text
        is_input_widget = hasattr(event.widget, 'is_input_widget')
        correct_widget = correct_widget_type and is_input_widget

        not_keystroke = event.state != 12 and 'Control' not in event.keysym

        # Because I can't trace it...
        if correct_widget and (not_keystroke or event.keysym in 'vVxX'):
            self.format_entries()
            length_status, length_difference = self.status()

            if length_status:
                if length_status == 'longer':
                    self.data_handler.playback.play('button_press')

                    for letter in self.input_box[-length_difference:]:
                        self.output_box += self.data_handler.enigma.button_press(letter)

                elif length_status == 'shorter' and self.master.autorotate:
                    for _ in range(abs(length_difference)):
                        self.data_handler.enigma.step_primary(-1)

            self.master.update_indicators()

            try:
                self.master.lightboard.light_up(self.output_box[-1])
            except IndexError:
                self.master.lightboard.light_up()

    def yview_sync(self, sender, receiver, *event):
        """Sets scrollbar position if the scrollbar is dragged"""
        sender.yview(*event)
        if self.master.sync_scroll:
            receiver.yview(*event)

    def yscrollcommand_sync(self, sender, receiver, *args):
        """Sets widget view position from the
        yscrollcommand parameter in Text"""
        sender.set(*args)
        if self.master.sync_scroll:
            receiver.set(*args)

    @property
    def input_box(self):
        """Gets the value of the input field"""
        return self.text_input.get('0.0', 'end').upper().replace('\n', '')

    @property
    def output_box(self):
        """Gets the value of the output field"""
        return self.text_output.get('0.0', 'end').upper().replace('\n', '')

    @input_box.setter
    def input_box(self, string):
        """Sets input field to the value of string"""
        self.text_input.delete('0.0', 'end')
        self.text_input.insert('0.0', string)

    @output_box.setter
    def output_box(self, string):
        """Sets output field to the value of string"""
        self.text_output.config(state='normal')
        self.text_output.delete('0.0', 'end')
        self.text_output.insert('0.0', string)
        self.text_output.config(state='disabled')


# LIGHTBOARD

class Lightboard(Frame):
    def __init__(self, tk_master, data_handler, *args, **kwargs):
        self.data_handler = data_handler
        bg = self.data_handler.bg
        Frame.__init__(self, tk_master, bd=1, relief='raised', bg=bg, *args, **kwargs)

        rows = []
        self.bulbs = []

        for row in self.data_handler.enigma.factory_data['layout']:
            new_row = Frame(self)
            for item in row:
                text = alphabet[item]
                self.bulbs.append(Label(new_row, text=text, font=('', 14), bg=bg, padx=2))
            rows.append(new_row)

        for row in rows:
            row.pack(side='top')

        for item in self.bulbs:
            item.pack(side='left')

        self.last_bulb = None

    def light_up(self, letter=''):
        """Makes a label glow yellow ( this represents a lightbulb on the
        actual light board )"""
        if self.last_bulb:
            self.last_bulb.config(fg='black')
        if letter:
            for bulb in self.bulbs:
                if bulb['text'] == letter:
                    bulb.config(fg='yellow')
                    self.last_bulb = bulb
                    break
