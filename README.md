# Fake News Detector

This fake news detector was developed for BYU's Big Data capstone, 2019-2020. The intent is to provide an extension for the Google Chrome browser that will allow users to access a model trained on fake news datasites to get a probability that the news site they're on is fake. The extension and model are both works in progress at the current time.

## Server

### Anaconda
In order to install and run the server, you'll need to have Anaconda installed and added to your path. Run this command in your terminal:

```bash
conda --version
```

If you get an error, you may need to look up how to install Anaconda and add it to your path.

### Setting Up a Conda Environment
A Conda environment will install all the dependencies you'll need to run the server. I've included the environment in a `.yml` file. To create this environement locally, navigate to the `server` directory and run the Conda command to create an environment.

```bash
cd server/
conda env create -f environment.yml
```

It may take several minutes to install all the dependencies in the environment. Once installation completes, activate your environment by running

```bash
conda activate fake-news-server
```

### Flask
Flask is a framework for running simple Python servers. For more information about Flask, see [here](https://flask.palletsprojects.com/en/1.1.x/).

The Chrome extension expects the server to be running at `localhost:3000`. To start the server there, run the following commands from the `server` directory:

```bash
export FLASK_APP=app.py
flask run -h localhost -p 3000
```

It may take a little while for the server to start.

*Edit: I still got some errors trying to install this on another machine after following all the steps. You may just have to `pip install` the necessary packages yourself. If you try to start the server and it doesn't work, just install the package it says it doesn't have. It's not too many. I had to manually install `flask_cors`, `tldextract`, `editdistance`, and `pytorch`.*

## Chrome Extension
In order to install dependencies locally, you'll need to have NPM installed and added to your path. You can check by running

```bash
npm --version
```

To install dependencies, navigate to the `chrome-extension` directory and run

```bash
npm install
```

It may take a few minutes to install dependencies. After dependencies are installed, build the app by running

```bash
npm run build
```

This compiles `App.svelte` into raw JavaScript that can be easily run as a web app.

### Bonus: Why Svelte?
Svelte is quite new as frontend frameworks come; it was only released last year (2019). My original plan was to use React to develop this, a frontend framework with which I have much more experience and which is more widely used in the industry today. However, React doesn't play well as a Chrome extension, since it depends on inline `<script>` tags to run, which Chrome extensions block by default. I chose to use Svelte, which a coworker introduced to me recently, because it's just so darn simple and easy to write in. I'm hoping it'll catch on in a big way in the next few years. For more info on Svelte, see the demo video [here](https://www.youtube.com/watch?v=AdNJ3fydeao) and the documentation [here](https://svelte.dev/).

## Installing in Chrome
In Google Chrome, navigate to `chrome://extensions`. In the top right, you should see a little switch that says "Developer mode". Turn that on, and then click the button on the top left that says "Load unpacked". Select the `public` folder in this project; that's where our assets and build are found. This should load the extension and you should see it in the top right of browser.
