# PitStop

----

[![Pylint Check](https://github.com/Nepitwin/PitStop/actions/workflows/pylint.yml/badge.svg?branch=main&style=flat)](https://github.com/Nepitwin/PitStop/actions/workflows/pylint.yml)
[![Pytest Check](https://github.com/Nepitwin/PitStop/actions/workflows/pytest.yml/badge.svg?branch=main&style=flat)](https://github.com/Nepitwin/PitStop/actions/workflows/pytest.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/nepitwin/pitstop?style=flat)](https://hub.docker.com/r/nepitwin/pitstop)
[![Latest Release](https://img.shields.io/github/v/tag/Nepitwin/PitStop?label=latest%20release&style=flat)](https://github.com/Nepitwin/PitStop/releases)

----

![PitStop](logo.jpg "PitStop")

PitStop is a Python project that uses the `fastf1` library to retrieve additional Formula 1 race information.

- [Example Hosting](https://racing.cloudnepi.de)

## Environment

.env file is required to build docker-compose file.

Required arguments are:

  * DEBUG - Host application in debug mode (1) or not (0)
  * DJANGO_SECRET_KEY - Your django application secret key
  * DJANGO_LOGLEVEL - Your django application log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  * DJANGO_ALLOWED_HOSTS - Allowed host as array for example '["localhost", "127.0.0.1"]'

Example .env file:

```
DJANGO_SECRET_KEY=django-insecure-t_tgg3h%zr(&z7mtzn^00#m8(ex#dt0+x=12s0g4#)sz-c)ws9
DEBUG=True
DJANGO_LOGLEVEL=info
DJANGO_ALLOWED_HOSTS='["localhost", "127.0.0.1"]'
```

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for more details.
