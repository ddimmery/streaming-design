# streaming-design
 
To get a working server deployed via Heroku, take the following steps:

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

## Update survey design with AJAX snippet

TBD

## How to modify the setup

There are a few plac

## Development

For local development, (after cloning this repo) you'll want to first create a `.env` file in the base directory. Mine looks like the following:

```
MODE='dev'
FLASK_APP='design_app'
FLASK_ENV='env_design_${MODE}'
DESIGN_NAME=bwd
PROCESSOR_NAME=config
DATABASE_URL='postgresql://design:design@db:5432/design_db'
```

If you don't want to bother with PostgreSQL, you can replace the URL with `sqlite:///test.db` to just use SQLite for testing.

Commit to the git repository as usual and test locally by building the docker container:

```
docker-compose -f docker-compose.yml up --build
```

When you are satisfied with your changes, test in Heroku by creating an app and pushing:

```
heroku create streaming-design --manifest
```

As you make changes, update the code on Heroku by committing and then pushing with:
```
git push heroku main
```

If you make changes to the setup section in `heroku.yml`, note that you will need to re-provision the app in order for the changes to manifest, i.e.:
```
heroku apps:destroy

heroku create <YOUR APP NAME> --manifest
```