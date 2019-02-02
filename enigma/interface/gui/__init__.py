from string import ascii_uppercase as alphabet

labels = ['A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06', 'G-07', 'H-08', 'I-09', 'J-10', 'K-11', 'L-12', 'M-13',
          'N-14', 'O-15', 'P-16', 'Q-17', 'R-18', 'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24', 'Y-25', 'Z-26']

# For the GUI plug board
layout = [[16, 22, 4, 17, 19, 25, 20, 8, 14], [0, 18, 3, 5, 6, 7, 9, 10], [15, 24, 23, 2, 21, 1, 13, 12, 11]]

# Data for enigma settings model wiki


base_dir = 'enigma/interface/gui/assets/icons/'


_enigma1 = \
"""
<h1>Enigma I</h1>
<hr>
<ul>
<li>Developed in: 1927</li>
<li>Number produced: 20 000</li>
<li>Used by: Heer, Luftwaffe, Kriegsmarine</li>
<li>Rotor count: 3</li>
<li>Features: Plugboard</li>
</ul>
<hr>
The Enigma M1 model was used primarily before the second world war
"""

_enigmam3 = \
"""
<h1>Enigma M3 (M1, M2, M3)</h1>
<hr>
<ul>
<li>Developed in: 1934</li>
<li>Number produced: 611 M1 units, 890 M2 units, 800 M3 units</li>
<li>Used by: Heer, Luftwaffe, Kriegsmarine</li>
<li>Rotor count: 3</li>
<li>Features: Plugboard</li>
</ul>
<hr>
Backward compatible with Enigma I, but featured different rotors for
every part of the army
"""

_enigmam4 = \
"""
<h1>Enigma M4</h1>
<hr>
<ul>
<li>Developed in: 1942</li>
<li>Number produced: 1500 (estimated)</li>
<li>Used by: Kriegsmarine</li>
<li>Rotor count: 4</li>
<li>Features: Plugboard, thin reflectors</li>
</ul>
<hr>
Naval version featuring 4 rotors, the last rotor is stationary.
"""

_norenigma = \
"""
<h1>Norenigma/Norway Enigma</h1>
<hr>
<ul>
<li>Developed in: -</li>
<li>Number produced: ?</li>
<li>Used by: Norwegian Police Security Service (Overvaakingspolitiet)</li>
<li>Rotor count: 3</li>
<li>Features: Plugboard</li>
</ul>
<hr>
Enigma I machines captured and used by the norwegian secret service after 1945.
Used custom rotor wiring.
"""

_enigmag = \
"""
<h1>Enigma G</h1>
<hr>
<ul>
<li>Developed in: 1931</li>
<li>Number produced: ?</li>
<li>Used by: Commercial use, Abwehr, Sicherheitsdienst</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector, cog driven rotors</li>
</ul>
<hr>
A compact Enigma model that featured a different rotor turning mechanism,
used commercially and by the police
"""

_enigmad = \
"""
<h1>Enigma D</h1>
<hr>
<ul>
<li>Developed in: 1926</li>
<li>Number produced: ?</li>
<li>Used by: Commercial use</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Commercially used Enigma model
"""

_enigmak = \
"""
<h1>Enigma K</h1>
<hr>
<ul>
<li>Developed in: 1927</li>
<li>Number produced: ?</li>
<li>Used by: Commercial use, Swiss army, Italian navy, Reichsbahn, Spanish civil war</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Improved Enigma D, 'K' probably stands for 'Komerziell'
"""

_swissk = \
"""
<h1>Swiss Enigma K</h1>
<hr>
<ul>
<li>Developed in: 1939</li>
<li>Number produced: 65 (?)</li>
<li>Used by: Swiss army</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector, modified wheel stepping, extra lamp board, power supply with transformer</li>
</ul>
<hr>
Used by the Swiss army, the extra lamp panel was used by a person who wrote down the letters.
"""

_railway = \
"""
<h1>Railway</h1>
<hr>
<ul>
<li>Developed in: 1927</li>
<li>Number produced: ?</li>
<li>Used by: Reichsbanh</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Rewired version of the Enigma K used by the german railway.
"""

_tirpitz = \
"""
<h1>Tirpitz</h1>
<hr>
<ul>
<li>Developed in: 1942</li>
<li>Number produced: ?</li>
<li>Used by: Communication between Germany and Japan</li>
<li>Rotor count: 3</li>
<li>Features: Rotatable reflector</li>
</ul>
<hr>
Rewired version of the Enigma K used by the Japanese army
"""


stylesheet = 'font-family: "Courier New", Courier, monospace'


view_data = {
    'Enigma1': {'description': _enigma1, 'img': base_dir + 'enigma1.jpg'},
    'EnigmaM3': {'description': _enigmam3, 'img': base_dir + 'enigmam3.jpg'},
    'EnigmaM4': {'description': _enigmam4, 'img': base_dir + 'enigmam4.jpg'},
    'Norenigma': {'description': _norenigma, 'img': base_dir + 'enigma1.jpg'},
    'EnigmaG': {'description': _enigmag, 'img': base_dir + '/enigmag.jpg'},
    'EnigmaD': {'description': _enigmad, 'img': base_dir + 'enigmad.jpg'},  # UKW CAN ROTATE
    'EnigmaK': {'description': _enigmak, 'img': base_dir + 'enigmak.jpg'},
    'SwissK': {'description': _swissk, 'img': base_dir + 'swissk.png'},
    'Railway': {'description': _railway, 'img': base_dir + 'enigmak.jpg'},
    'Tirpitz': {'description': _tirpitz, 'img': base_dir + 'tirpitz.jpg'}
}
