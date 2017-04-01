# A collection of my Windows 10 profile using zsh on Windows Subsystem for Linux (WSL)
All code is in src dir.
Right now this doesn't do a good job of separating my profile from generically useful things (e.g. zsh-windows-tools). I'll get better about this!

## Things it does today
- Solarized tmux with fluffmods (screen keybind for prefix key and so on)
- zsh with completion options partial to Windows (case insensitivity for filenames) and laziness
- Utilities to determine your home directory in Windows ($winhome) as well as yanking any other desired global environment variable in the laziest way possible.
- Utilities to create aliases for various Windows-y things that have extensions but dropping the extensions because fuck that's really annoying, yeah?
- Installation script (install.py) that will be reasonably polite with sensible defaults.

## Things it will do in the future
- Automatically synchronize changes from either your desired git repository / cloud storage directory of choice (maybe both, idk) -- this is so I can lazily sync changes across machines
- More dotfiles of interest
- Additional WSL enhancements as I can think of them!
