# Twitter Clone
> Twitter Clone with most of Twitter's core features.
> [Live demo](#live-demo)

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Live demo](#live-demo)
* [API](#api)

## General info
This project is my clone of Twitter written from the scratch by myself.
It has most of core Twitter functions such as:
* Tweets
* Retweets
* Tweets' likes
* Comments
* Bookmarks
* Tweet editing and deleting feature
* Account display name changing

For the simplicity's sake everybody can see every Tweet and interact with it.

App screenshots can be found after scrolling on the [Login Page](https://wp-twitter-clone.herokuapp.com/login)
	
## Technologies
Project has been created using:
* Django - version: 3.2
* Django Crispy Forms - version: 1.12
* Django REST framework - version: 3.12
* Whitenoise - version: 5.3
	
## Setup
To run this project locally, download the code from repo and run it with:

```
$ cd twitter-clone-master
$ python manage.py runserver
```
## Live demo
You can try the project out [here](https://wp-twitter-clone.herokuapp.com).

(Due to Heroku depolyment it can take a moment for the page to load)

## API
App has it's API available at `[twitter-clone url]/api/v1` ([Live demo API base](https://wp-twitter-clone.herokuapp.com/api/v1))

Accessible endpoints:
* `/posts` - Get all posts
* `/posts/[POST ID]` - Get specific post info
* `/authors` - Get all authors
* `/authors/[AUTHOR ID]` - Get specific author's info and tweets