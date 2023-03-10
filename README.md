<p align="center">
  <img src="https://user-images.githubusercontent.com/101948294/224011944-f5d171ef-9c38-4031-ba0a-a76d04900c09.png" alt="Angry Birds Font" />
</p>

<p align="center">

  <a href="https://git.io/typing-svg">
    <img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&weight=600&pause=1000&color=E11E7B&center=true&width=435&lines=Read+fast+with+AI+power.;Learn for fun!" alt="Typing SVG" />
  </a>

</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0-blue" height="20"/>
  <img src="https://img.shields.io/badge/python-3.11-blue" height="20"/>
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/101948294/224011809-81c79668-eb40-4e7e-b61d-0f99cafd67cb.gif" alt="animated" />
</p>


## :red_square: Getting Started

[AIreading](https://github.com/zakharb/aireading) is the simple tool to work with text using OpenAI like ChatGPT. It helps to find vocabulary in the text, generate short description and main idea for text and suggest to you similar stories.  

Online [demo site](https://github.com/zakharb/aireading) where you can try it!

### Requirements

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

### Install and run

Clone the project

```sh
git clone git@github.com:zakharb/aireading.git
cd aireading
```

Create API key on [OpenAI site](https://platform.openai.com/account/api-keys)

Write created API key to `OPENAI_API_KEY` variable into `docker-compose.yml` file  
```
services:
  aireading:
    build: ./aireading
    command: uvicorn app.main:app --host 0.0.0.0 --port 8080 --forwarded-allow-ips=* --proxy-headers
    volumes:
      - ./aireading/:/app/
    environment:
      - OPENAI_API_KEY=sk-asjhdAWEhw781h2ih2UIHADG@G3792q1u23hiUWHAUWEhiq  
```
Start docker-compose

```
docker-compose up -d --build
```
Open site [locally](http://localhost:8080) by address 
```
http://localhost:8080
```

## :red_square: Deployment to Deta

Deployment is described in this [gudie](https://deta.space/docs/en/basics/cli)

Install Deta Space CLI
```sh
curl -fsSL https://get.deta.dev/space-cli.sh | sh
```
Generate an access token on [Space dashboard](https://deta.space/)

Login to Deta Space
```sh
space login
```

Go to folder and create project
```sh
cd aireading
space new
```

Push the project
```sh
space push
```

## :red_square: Versioning

Using [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/zakharb/syslogen/tags). 

## :red_square: Authors

* **Zakhar Bengart** - *Initial work* - [Ze](https://github.com/zakharb)

See also the list of [contributors](https://github.com/zakharb/syslogen/contributors) who participated in this project.

## :red_square: License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation - see the [LICENSE](LICENSE) file for details

