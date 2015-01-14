## INSTAGRAM DOWNLOADER

Use it to download images of a user.


### How to use it

To get started with little to no configuration, run the script like this 

``` 
  $ python downloader.py username
```

replace username with the persons username/handle. Script will assume you want to download all the images of the following user.

Alternatively to fine tune what you want to download use the following command

```
  $ python downloader.py username [--save-only] [[all] [recent]]
```

* `username all` - will download all the images
* `username recent` - will download _only_ recent images
* `username --save-only [...]` - will _only_ save and _not_ download images

To change default settings open __settings.conf__ and choose as you like.

### TODO
1. Improve downloading module. Multithreading can be used.
1. Save the urls to a file to batch download with likes of IDM
1. Let people download tags 
1. Do something about captions too
