# Audiobook Tracker

An API to store your notes when you are hearing your favourites audiobooks. <br />
Also, you will be able to receive the bestsellers books from New York Times and see the most scored posts about books in Reddit.

---
## Run
* Create an .env file, and insert a NYT_KEY for using the management command get_bestsellers.
```bash 
$ docker-compose up
```
---
## Managements Commands
Two management commands are provided.<br />
* get_bestsellers will return the bestseller books from New York Times, setting the NYT_KEY environment variable.<br />

* get_books_posts will return the top posts from a book subreddit.
```bash 
$ make get_bestsellers
$ make get_books_posts
```
* If you do not want to create the required API key to receive books,<br />
you can use the following command:
```bash
$ make restore_db
```
---
## Endpoints
For API documentation please go to http://127.0.0.1:8000/api/docs <br />
The APIs are protected, for consuming them, you can follow the next steps:
* Send a post request to the endpoint /api/user/create.
* Send a post request ti the endpoint /api/user/token.
* Add an authorization header: -H 'Authorization: token 5b516cd8c4322ea9df068700726ea7bf6d70294b'


## Tests
```bash
$ make test
```

## TODO
The management command get_books_posts could not be fully tested. <br/>
Receiving too many requests response from Reddit.
