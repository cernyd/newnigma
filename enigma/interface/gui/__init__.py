
labels = ['A-01', 'B-02', 'C-03', 'D-04', 'E-05', 'F-06', 'G-07', 'H-08', 'I-09', 'J-10', 'K-11', 'L-12', 'M-13',
          'N-14', 'O-15', 'P-16', 'Q-17', 'R-18', 'S-19', 'T-20', 'U-21', 'V-22', 'W-23', 'X-24', 'Y-25', 'Z-26']

# For the GUI plug board
layout = [[16, 22, 4, 17, 19, 25, 20, 8, 14], [0, 18, 3, 5, 6, 7, 9, 10], [15, 24, 23, 2, 21, 1, 13, 12, 11]]

# Data for enigma settings model wiki


base_dir = 'enigma/interface/gui/assets/icons/'


view_data = {
    'Enigma1': {'description': "The Enigma M1 model was used primarily before the second world war", 'img': base_dir + 'enigma1.jpg'},
    'EnigmaM3': {'description': "temp", 'img': base_dir + 'enigmam3.jpg'},
    'EnigmaM4': {'description': "Naval version featuring 4 rotors, the last rotor is stationary", 'img': base_dir + 'enigmam4.jpg'},
    'Norenigma': {'description': "Enigma 1 with modified wiring, used by the Norway secret service", 'img': base_dir + 'enigma1.jpg'},
    'EnigmaG': {'description': "temp", 'img': base_dir + '/enigmag.jpg'},
    'EnigmaD': {'description': "Features a rotatable reflector, https://www.cryptomuseum.com/crypto/enigma/d/index.htm", 'img': base_dir + 'enigmad.jpg'},  # UKW CAN ROTATE
    'EnigmaK': {'description': "temp", 'img': base_dir + 'enigmak.jpg'},
    'SwissK': {'description': "Used by the Swiss army, originally with conventional Enigma D wiring, but was frequently rewired during the war", 'img': base_dir + 'swissk.png'},
    'Railway': {'description': "Rewired version of the Enigma K used by the german railway", 'img': base_dir + 'enigmak.jpg'},
    'Tirpitz': {'description': "temp", 'img': base_dir + 'enigmak.jpg'}
}
