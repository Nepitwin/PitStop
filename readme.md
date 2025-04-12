# PitStop

![PitStop](logo.jpg "PitStop")

PitStop is a Python project that uses the `fastf1` library to retrieve additional Formula 1 race informations.

## Planned Features

- Calendar implementation to receive events in a specific timezone

## Project Structure

```
PitStop
├── cache                 # Cache directory
├── requirements.txt      # Dependencies
├── src
│   └── main.py           # Main script
└── readme.md             # Project description
```

## Environment

.env file is requrired to build docker-compose file.

Required arguments are:

  * DEBUG - Host application in debug mode (1) or not (0)
  * DJANGO_SECRET_KEY - Your django application secret key
  * DJANGO_LOGLEVEL - Your django application log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  * DJANGO_ALLOWED_HOSTS - Allowed host as array for example ["127.0.0.1"]

## License

This project is licensed under the Apache License 2.0. See the `LICENSE` file for more details.
