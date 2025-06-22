## About The Project
My fastapi case project for allowing users to upload their pdf's and chat with llm's about their pdf context also includes IAM related flows like authentication authorization jwts etc. 

## Install:

Create virtualenv with python 3.11 
```bash
$ virtualenv -p python3.11 venv
$ source venv/bin/activate
```

Install requirements for project
```bash
$ pip install -r requirements.txt
```

Run project
```bash
$ python main.py --config=local
```

Run project with migration on startup
```bash
$ python main.py --config=local --migrate=true
```

Run project via docker
```bash
--in app folder
$ docker build -t [image_name] .
$ docker run -i -t [image_name] /bin/bash
do not forget the change host to --> host.docker.internal
```


## Requirements:
- MongoDB [ File Storage ]
- PostgreSQL [ IAM Database ]


## Environment Variables:
defaults set under local configuration
- HOST
- PORT
- MONGO_CONNECTION_STRING
- MONGO_DATABASE_NAME
- POSTGRES_CONNECTION_STRING
- WORKER_COUNT
- REFRESH_TOKEN_TTL
- ACCESS_TOKEN_TTL
- GEMINI_API_KEY
- GEMINI_BASE_URL
- GEMINI_MODEL