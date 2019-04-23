# upload-api
Example repo of REST API for resizng image files & uploading them to AWS S3.

Accepted files: `jpg`, `jpeg`, `gif`, `png`.
Size < 5 mb.
Requests accepts `size` param with supported values of: `medium` and `small`, which sets the size of resized file.

## Prerequisites:
- Docker (built using: `Docker version 18.03.0-ce, build 0520e24302` )
- docker-compose (built using: `docker-compose version 1.20.1, build 5d8c71b2` )

Proposed setup: [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_windows/)

## How to? Extremely easy step-by-step guide.

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

1. While running `docker-compose run -p 8000:8000 web python app.py` I run into:
```
/usr/bin/env: ‘python\r’: No such file or directory
```

Answer: your app.py is probably ...
