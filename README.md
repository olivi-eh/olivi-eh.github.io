# Personal website

This repository contains my personal website, which is hosted on [olivi-eh.dev](https://olivi-eh.dev/).

## How to run

The following command will generate the HTML files from MD input:

```sh
./make.sh
```

And then you can use a simple Python server to serve the assets:

```sh
python3 -m http.server -d out/ 8080
```
