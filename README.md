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

```
git clone git@github.com:zakharb/aireading.git
cd aireading
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

Edit Dockerfile and spicify server IP address

Build image
```
docker build --network host -t syslogen .
```

Run image
```
docker run syslogen
```
## :red_square: Versioning

Using [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/zakharb/syslogen/tags). 

## :red_square: Authors

* **Zakhar Bengart** - *Initial work* - [Ze](https://github.com/zakharb)

See also the list of [contributors](https://github.com/zakharb/syslogen/contributors) who participated in this project.

## :red_square: License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation - see the [LICENSE](LICENSE) file for details

