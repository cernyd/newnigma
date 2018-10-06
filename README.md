# gnunigma
![Enigma logo](https://images.duckduckgo.com/iu/?u=https%3A%2F%2Fs-media-cache-ak0.pinimg.com%2F236x%2F59%2Ff7%2F4e%2F59f74e1fbac1f6adcf039f13feb4e67e.jpg&f=1) 

[Basic information](#basic-information) | [Compatibility](#compatibility) | [Installation](#installation) | [Requirements](#requirements) | [Platform differences](#features-missing-in-the-ubuntu-version) | [FAQ](#faq) | [License](#license)

## Basic information
* Gnunigma simulates the *enigma encryption machine*, which was used by the Germans in 20th century.
* **Language of choice** - python
* **Graphical library** - tkinter/Tkinter

## How it looks
### On Windows
* Warning! This screenshot is old and some new GUI features were added in newer versions! (as you can see on the Ubuntu screenshot)

![Gnunigma on Windows](http://i.imgur.com/DczgfHE.png)
### On Ubuntu
![Gnunigma on Ubuntu](http://i.imgur.com/2DmzAvX.png)
----
## Compatibility
* Gnunigma was tested on Windows 10 and Ubuntu (16.04, 16.10, 17.04) and should be compatible

### Installation
1. Download the source
2. If you are on Ubuntu and don't have Tkinter installed on python 3, run this command
```bash
sudo apt-get install python3-tk
```
3. Run the ```runtime.py``` file with python 3

### Requirements
1. Python version 3.5 and newer (older python 3 versions might work as well but were not tested by me!)
   * *tkinter* library is included on Windows by default but must be installed on Ubuntu

### Features missing in the Ubuntu version
1. **Sound** - gnunigma on Windows is using the *winsound* library, which is not available on linux
2. **Icons** - there were some issues with iconbitmaps on
3. **Styling** - The gui does not looks as good as on Windows (scaling, weird colors)

---
# How it works
* Gnunigma has come a long way since the start of its developement, I tried to make it as "modular" as possible, this means:
  1. Objects derived from the BaseEnigma

# Project hierarchy
* Files that require further explanations are links to sections describing them in more detail.

* **gnunigma/**
  * **enigma/**
    * [components.py](#components)
    * **historical_data.yaml** - Historical enigma data
  * **icons/** - Icons used by the Windows version
  * **sounds/** - Sounds played by the Windows version
  * **.gitignore** - Ignores .pyc and .idea folder from pycharm
  * [LICENSE.txt](#license)
  * **README.md** - This file
  * [cfg_handler.py](#cfg_handler)
  * [config.yaml](#config)
  * [data_handler.py](#data_handler)
  * [enigma_deciphered.txt](#accomplishments-of-gnunigma)
  * [gui.py](#gui)
  * [runtime.py](#runtime)

# Files
## components
 * Enigma simulation classes (enigma machines, machine parts, additional devices)
## cfg_handler
* Used for loading raw data from YAML files

## config
* Global configuration (GUI settings, enigma settings saved by the user, unit test config)

## data_handler
*  Handlers (for sound and configuration/data IO)

## gui
* All GUI classes (most of them represent a window, others some tkinter derived classes)

## runtime
* Launches the GUI version

# Accomplishments of gnunigma
* Gnunigma proved its historical accuracy by successfully deciphering original enigma messages
  * Message examples were taken from [this site](http://wiki.franklinheath.co.uk/index.php/Enigma/Sample_Messages) 
---
## Barbarossa 1941
**Reflector:** B
**Wheel order:** II IV V
**Ring positions:** 02 21 12
**Plug pairs:**	AV BS CG DL FU HZ IN KM OW RX

### PART 1, msg key - **BLA**

#### Raw decrypted message

```AUFKL X ABTEILUNG X VON X KURTINOWA X KURTINOWA X NORDWESTL X SEBEZ X SEBEZ X U AFFLIEGER STRASZERIQTUNG X DUBROWKI X DUBROWKI X OPOTSCHKA X OPOTSCHKA X UM X EINS AQT DREI NULL X UHR ANGETRETEN X ANGRIFF X INF X RGT X```
#### Adjusted for german symbols

```AUFKL ABTEILUNG VON KRUTINOWA KURTINOWA NORDWESTL SEBEZ SEBEZ U AFFLIEGER STRAßERICHTUNG DUBROWKI DUBROWKI OPOTSCHKA OPOTSCHKA OPOTSCHKA UM 18 30 UHR ANGETRETEN ANGRIFF INF RGT```

### PART 2, msg key - LSD
#### Raw decrypted message

`DREI GEHT LANGSAM ABER SIQER VOR WAERTS X EINS SIEBEN NULL SEQS X UHR X ROEM X EINS X INFRGT X DREI X AUF FLIEGER STRASZE MIT ANFANG X EINS SEQS X KM X KM X OSTW X KAMENEC X K`
#### Adjusted for german symbols

`3 GEHT LANGSAM ABER SICHER VORWÄRST 17 06 UHR RÖM 1 IFRGT 3 AUF FLIEGERSTRAßE MIT ANFANG 16 KM KM OSTW KAMENEC K`

---
## Enigma Instruction Manual, 1930, msg key - ABL
**Reflector:**	A
**Wheel order:**	II I III
**Ring positions:** 	24 13 22
**Plug pairs:**	AM FI NV PS TU WZ
#### Raw decrypted message

```FEINDLIQE INFANTERIEKOLONNE BEOBAQTET X ANFANG SEDD AUSGANG BAER WALDE X ENDE DREI KMOST WAERTS NEUSTADT```

#### Adjusted for german symbols

```FEINDLICHE INFANTERIEKOLONNE BEOBACHTET ANFANG SEDD AUSGANG BÄR WALDE ENDE 3 KMOST WÄRTS NEUSTADT```

---
## Scharnhorst (Konteradmiral Erdich Bey), 1943, msg key - UZV
**Reflector:**	B
**Wheel order:**	III VI VIII
**Ring positions:** 	01 08 13
**Plug pairs:**	AN EZ HK IJ LR MQ OT PV SW UX
#### Raw decrypted message

```STEUERE J TANA FJORD J AN STAN DORT QU AAA CCC VIER NEUN NEUN ZWO FAHRT ZWO NUL SMXX SCHARNHORST HCO```

---
# FAQ
* If you have any questions, visit the wiki first (mostly incomplete!) or PM me.

---
# License
* The project is licensed with [GNU GPLv3](https://en.wikipedia.org/wiki/GNU_General_Public_License)
![GNU GPL logo](https://cloud.githubusercontent.com/assets/18537381/26077378/236c0eec-39bc-11e7-8013-29bfbe1ab2f0.png)
