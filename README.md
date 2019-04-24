# upload-api
Example repo of REST API for resizing image files & uploading them to AWS S3.

Quick summary:
- Accepted file formats: `jpg`, `jpeg`, `gif`, `png`.
- Accepted file size: < 5 mb. (can be changed in config)
- accepted route: `/`
- GET request returns simple JSON confirming success
- POST requests allow to upload a file, which will then be resized and sent to AWS S3 storage.
- POST requests should be in `form-data` format with `file` in key and file attached to value.
- POST requests should have `Content-Type` : `multipart/form-data` in Headers
- POST requests accepts `size` param with supported values of: `medium` and `small`, which sets the size of resized file.

Broader API documentation below.

## Setup:
- Docker (version user: `Docker version 18.03.0-ce, build 0520e24302` )
- docker-compose (version used: `docker-compose version 1.20.1, build 5d8c71b2` )

  Proposed distribution: [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/)
- [ElephantSQL](https://www.elephantsql.com/) (preconfigured PostgreSQL online database - if you are using FREE version be sure to change max. size accepted in config.py, because free version has 20 mb capacity only)
- configured [AWS S3 storage](https://aws.amazon.com/s3/) bucket

## How to install? Extremely easy step-by-step guide.

1.  Set up `.env` file - you can use  `_env [pattern]` file as a pattern

2. Run `Docker Quickstart Terminal` to set up Docker automatically. 
Now you should be running on default docker-machine - to inspect IP you can use command `docker-machine ip`

3. Go into the repository directory.
(You don't have to use Docker Terminal - since you set up docker you can navigate also in Gitbash or any other console)

4. Run `docker-compose build` to build images

5. Run `docker-compose up -d` to run containers in detached mode 
(alternatively you can also combine both commands by running `docker-compose up --build -d` )

6. You should have a local instance of a server running. 
Try connecting to docker machine IP via Internet Browser and you should encounter json informing of succesful GET requests.
To make POST requests you will have to use [Postman](https://www.getpostman.com/downloads/)

7. **How to run app.py only for development purposes?** First stop running containers using `docker-compose down`. 
Then run `docker-compose run -p 8000:8000 web python app.py` - this command runs python app.py web container on port 8000.

8. **How to run tests?** Stop the container with `docker-compose down`. Then run `docker-compose run -p 8000:8000 web python tests.py`.

9. **How to log into running container?** Check running containers list using `docker ps` and then run `docker exec -it <container-nr> sh` into console. 
On Win10 you will probably need to prefix it with `winpty` resulting `winpty docker exec -it <container-nr> sh` . 
You don't have to use full number - only 4 first digits.

#### Possible errors

1. **Question:** While running `docker-compose run -p 8000:8000 web python app.py` I run into:
```
/usr/bin/env: ‘python\r’: No such file or directory
```

**Answer:** your app.py may have set DOS line endings instead of Unix line ending. 
To fix it open `app.py` in vim by running: `vim app.py`, then type `:set ff=unix` and close a file by typing `:wq`.
It should work fine now, although you may have to rebuild your container (`docker-compose down` then `docker-compose build` and finally command from question)

2. **Question:** While running `docker-compose run -p 8000:8000 web python tests.py` I run into errors with connection to DB like:
```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedTable) table "uploads" does not exist
```

**Answer:** you might have a running container with a restart option on (it is set in docker-compose.yml file).
Running container can be making requests, create tables or droping them while you are running your tests - running 2 set of tests at the same time can easily result in a conflict since both instances of tests are running on the same database.

Investigate docker containers using `docker ps`. If you find any container running `... python tests.py` execute them using 
`docker stop <cont-nr> && docker rm <cont-nr>`.

## API Documentation

#### Test GET request

Responses a simple json file assuring user that they are connected to server.

- URL

  `/`

- Method:

  `GET`

- URL Params

  None

- Headers

  None

- Body

  None

- Success Response

  - Code: 200
  - Content: `{"status": "success"}`

- Error Response

  None

#### Upload image

Accepts uploaded image file and resizes it to 400 px x 300 px (default or "medium") or 120 px x 90 px ("small") according to param or without it. 
Then uploads resized file to AWS S3 storage and sends user a json response with status, id, filename and url. 
Original file content and original filename is stored in database.

- Constrains:

  - Only accepts files smaller than 5 mb.
  - Only accepts file in formats: `jpg`, `jpeg`, `gif`, `png`.

- URL

  `/`

- Method:

  `POST`

- URL Params

  Not required:
  
  `size=medium` 
  
  OR
  
  `size=small`

- Headers

  Required:
  
  `Content-Type : multipart/form-data`

- Body
  
  form-data:
  
  `file` : value have to be upcoming file

- Success Response

  - Code: 201
  - Content: 
  ```
  {"status": "success",
  "id": 12,
  "filename": "Image_100012_15560325648157046.jpg",
  "url" : "https://s3.eu-central-1.amazonaws.com/your-bucket-name/uploads/Image_100012_1556032564817046.jpg"}`
  ```

- Error Response

  - Code: 400
  - Content: `{"status": "error: no file detected"}`

   OR
   
  - Code: 400
  - Content: `{"status": "error: empty filename detected"}`

   OR
   
  - Code: 400
  - Content: `{"status": "error: file with that extension is not allowed"}`

   OR
   
  - Code: 400
  - Content: `{"status": "error: values 'medium' and 'small' are only ones allowed for 'size' key"}`

   OR

  - Code: 422
  - Content: `{"status": "error: file is too small resize it"}`

   OR

  - Code: 422
  - Content: `{"status": "error: the file is corrupted or is not a proper image file"}`
