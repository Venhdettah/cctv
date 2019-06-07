# cctv

cctv source code

## installation

perform the following actions to begin developing for the cctv application:

```
pipenv run pip install pip==18.0  # make sure pipenv installs a working pip version
pipenv install --dev  # install the normal and dev packages
```

## pygame 2 installation (broken)

don't install pygame 2 (yet) install pygame==1.9.6 (already selected in Pipfile).
pygame 2 isn't installable yet without many dependency issues

~~the pygame 2 installation can fail with a message like:~~

```
Installing pygame...
Collecting pygame
  Using cached https://files.pythonhosted.org/packages/fa/0a/04cb5ead3a144cdf7f9b1403feba377a65eac977ca59f36de96c5e0be02a/pygame-2.0.0.dev1.tar.gz
    Complete output from command python setup.py egg_info:


    WARNING, No "Setup" File Exists, Running "buildconfig/config.py"
    Using UNIX configuration...

    /bin/sh: 1: sdl-config: not found
    /bin/sh: 1: sdl-config: not found
    /bin/sh: 1: sdl-config: not found

    Hunting dependencies...
    WARNING: "sdl-config" failed!
    Unable to run "sdl-config". Please make sure a development version of SDL is installed.

    ----------------------------------------

Error:  An error occurred while installing pygame!
```

~~in that case, the following package (sdl 2 development package) should be installed: `libsdl2-dev`, this can be done with the following command:~~

```
sudo apt install libsdl2-dev
```

~~if this error occured during the `pipenv install --dev` command, repeat it to successfully install pygame.~~
