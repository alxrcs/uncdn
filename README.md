# Mini-scrapy: Just another Python scraper

This is a small scraper I built for finding, downloading, and replacing external assets in open source projects. It might be useful if you're trying to deploy an open-source project on a local network (without Internet access).

I built this one specifically for use with [FreeCodeCamp](https://github.com/FreeCodeCamp/FreeCodeCamp), but it should be useful for similar projects as well.

## Requirements

Just make sure you have Python and `wget` installed.

## Usage

Copy this script into your project, and run:

```
./scrapy.py scrape
``` 

This will build the external assets list (by default `links.txt`). Check which ones you want to download, delete the ones you don't, and download them by running:

```
./scrapy.py download
```

Lastly, running:

```
./scrapy.py internalize
``` 

will switch the external urls for local ones. 

Make sure to move the assets on the `external` folder to a publicly available location on your server. This, of course, depends on your server configuration.
