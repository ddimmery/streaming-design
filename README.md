# streaming-design
 
To get a working server, take the following steps:

## Clone this repository
```
git clone git@github.com:ddimmery/streaming-design.git
```

## Install Heroku CLI
[Read the Heroku documentation for full details](https://devcenter.heroku.com/articles/heroku-cli). On a Mac, if you have Homebrew installed, run the command
```
brew tap heroku/brew && brew install heroku
```

## Enable Heroku beta version

Currently, to work with manifests in Heroku, it's [necessary to use the beta version](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml#creating-your-app-from-setup).

```
heroku update beta
heroku plugins:install @heroku-cli/plugin-manifest
heroku create <YOUR APP NAME> --manifest
```

## Make any changes for your application

In particular, it will be necessary to update the `covariates.yml` definition to spell out how covariates should be encoded.

Commit your changes and push the code to Heroku.

```
git add .
git commit -m "An informative commit message!"
git push heroku main
```