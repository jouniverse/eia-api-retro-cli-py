# EIA API App

## Overview

The EIA API App is a Python library that provides access to the Energy Information Administration (EIA) API<sup>1</sup>. You need to have an API key to use the EIA API.

## Description

This project is a Python application that allows you to interact with the EIA API. It provides a command-line interface for exploring and querying energy data.

> Imagine that you are a high-powered analyst in an even more high-powered financial institution, and I am sure that you are one. Your ego is the size of Manhattan, but alas, your skillset is not quite in the metaverse yet. Don’t panic! This app is for you. It transports you into a bygone era of analytics, maybe seventies, or perhaps eighties. So, just lay back and let the terminal take you into a trip to the energy information administration’s database, in old school style, the best style there is.

![EIA API MENU](./app/imgs/menu.jpg)

## Installation

Install all the required packages:

```bash
pip install -r requirements.txt
```

Add your API key to the `api_key.py` file.

## Usage

Run the app:

```bash
python app/eia_app.py
```

A walkthrough of the app is available [here](https://youtu.be/LLWuH_CcbYE).

## Disclaimer

This project is not affiliated with the Energy Information Administration (EIA) and is not endorsed by EIA.

According to EIA:

> The information submitted by reporting entities is preliminary data and is made available "as-is" by EIA. Neither EIA nor reporting entities are responsible for reliance on the data for any specific use.<sup>2</sup>

The same applies to my analysis of the data. Caveat lector.

## License

All Rights Reserved

Copyright (c) 2024 jouniverse

<sup>1</sup> [The EIA API is a free and open-source API that provides access to energy data from the U.S. Energy Information Administration (EIA)](https://www.eia.gov/opendata/index.php)

<sup>2</sup> [Hourly Electric Grid Monitor](https://www.eia.gov/electricity/gridmonitor/dashboard/electric_overview/US48/US48)
