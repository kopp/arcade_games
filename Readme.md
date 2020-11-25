# Arcade Games

Some simple games written with
[Python Arcade](https://arcade.academy/).


# License

The code in this repository is MIT licensed, see
[LICENSE](LICENSE).

The games base on other games that are also MIT licensed by

    Copyright (c) 2020 Paul Vincent Craven


# Known Issues

On Linux you might get a crash when drawing a text with a core dump from
`munmap_chunk`.
To fix this, run
(see [here](https://github.com/python-pillow/Pillow/issues/4225#issuecomment-605769767)):

    pip uninstall PilloW
    pip install --compile --install-option=-O1 PilloW