# UnCDN: Remove those hardcoded cdn references from your source code. 

This is a small scraper I built for finding, downloading, and replacing external assets in open source projects. It might be useful if you're trying to deploy an open-source project on a local network (without Internet access).

I built this one specifically for use with [FreeCodeCamp](https://github.com/FreeCodeCamp/FreeCodeCamp), but it should be useful for similar projects as well.

## Requirements

Just make sure you have Python and `wget` installed.

## Usage

Copy this script into your project, and run:

```
./uncdn.py scrape
``` 

This will build the external assets list (by default `links.txt`). Check which ones you want to download, delete the ones you don't, and download them by running:

```
./uncdn.py download
```

Lastly, running:

```
./uncdn.py internalize
``` 

will switch the external urls for local ones. 

Make sure to move the assets downloaded to the `external` folder to a publicly available location on your server. This, of course, depends on your server configuration.

Feel free to change in the code the regex used to "detect" external assets.

