<h1 align="center">Python Terminal Chat Demo</h1>

<p align="center">
  Cliente de chat en terminal implementado en Python para comparar una arquitectura cliente-servidor con una arquitectura basada en microservicios.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python 3.x">
  <img src="https://img.shields.io/badge/CLI-Chat-4D4D4D?style=for-the-badge&logo=gnometerminal&logoColor=white" alt="CLI Chat">
  <img src="https://img.shields.io/badge/Architecture-Demo-2EA44F?style=for-the-badge" alt="Architecture Demo">
  <br>
  <a href="https://github.com/h4cktor">
    <img src="https://img.shields.io/badge/GitHub-h4cktor-181717?style=for-the-badge&logo=github" alt="Perfil de GitHub de h4cktor">
  </a>
</p>

<p align="center">
  <a href="#descripción">Descripción</a> ·
  <a href="#arquitecturas">Arquitecturas</a> ·
  <a href="#ejecución">Ejecución</a> ·
  <a href="#estructura">Estructura</a>
</p>

---

## Descripción

Este repositorio contiene dos demos de una aplicación de chat en terminal. Ambas comparten una interfaz de línea de comandos similar, pero están organizadas para probar dos enfoques arquitectónicos diferentes.

La idea principal es facilitar la comparación entre una comunicación directa cliente-servidor y una versión orientada a microservicios.

## Arquitecturas

| Demo | Carpeta | Descripción |
| --- | --- | --- |
| Cliente-servidor | `arq-cli-serv` | Cliente de terminal que se conecta a un servidor indicando su IP. |
| Microservicios | `arq-microservices` | Cliente de terminal preparado para interactuar con una arquitectura distribuida. |

## Requisitos

- Python 3 instalado.
- En **Windows**, instalar `curses`:

```sh
pip install windows-curses
```

## Inicio rápido

Clona el repositorio y entra en la carpeta del proyecto:

```sh
git clone https://github.com/h4cktor/lrrss-p1-3-demo.git
cd lrrss-p1-3-demo
```

## Ejecución

### 1. Arquitectura cliente-servidor

Ejecuta el cliente indicando el nombre de usuario y la IP del servidor:

```sh
cd arq-cli-serv
python3 client.py --user <nombre_de_usuario> -i <ip_del_servidor>
```

Ejemplo:

```sh
python3 client.py --user h4cktor -i 127.0.0.1
```

### 2. Arquitectura de microservicios

Ejecuta el cliente desde la carpeta de microservicios:

```sh
cd arq-microservices
python3 client.py --user <nombre_de_usuario>
```

Ejemplo:

```sh
python3 client.py --user h4cktor
```

## Ayuda

Puedes usar el parámetro `-h` para consultar todas las opciones disponibles:

```sh
python3 client.py -h
```

## Estructura

```text
.
├── arq-cli-serv
│   ├── client.py
│   ├── client_app/
│   └── utils/
├── arq-microservices
│   ├── client.py
│   ├── client_app/
│   └── utils/
└── README.md
```

## Autor

Desarrollado por [@h4cktor](https://github.com/h4cktor).
