# Meetings

[![REST API Build](https://github.com/tomasanchez/grupo-3-tacs/actions/workflows/rest.yml/badge.svg)](https://github.com/tomasanchez/grupo-3-tacs/actions/workflows/rest.yml)
[![REST Image Build](https://github.com/tomasanchez/grupo-3-tacs/actions/workflows/rest-image.yml/badge.svg)](https://github.com/tomasanchez/grupo-3-tacs/actions/workflows/rest-image.yml)

Meetings is an application developed by `Group-3` during the course 
Advanced Technologies in Software Construction, as was taught during first semester of 2023.

## Table of Contents

<!-- TOC -->
* [Meetings](#meetings)
  * [Table of Contents](#table-of-contents)
  * [Requirements](#requirements)
  * [Team](#team)
  * [Continuous Integration](#continuous-integration)
  * [Development Environment](#development-environment)
    * [Back-End](#back-end)
    * [Front-End](#front-end)
  * [Running Local](#running-local)
  * [License](#license)
<!-- TOC -->

## Requirements

Available on [docs](https://docs.google.com/document/d/e/2PACX-1vSOjnpw4O-XEjpcK3Yei_FUmBoAQNMwre7mpq81ub2Xqbzy_TRupGIqjIURd4RijgiE7s0fAOlR1DR2/pub)

## Team

| Name                           | File      | e-Mail                       |
|--------------------------------|-----------|------------------------------|
| Alvarez, Leandro               | 146.887-0 | lean.alvarez@live.com.ar     |
| Sanchez, Tomas                 | 166.043-3 | tosacnehz@frba.utn.edu.ar    |
| Torregrosa, Florencia          | 163.519-0 | ftorregrossa@frba.utn.edu.ar |      
| Olmedo Paco, Jhon Daniel       | 152.222-0 | jhonpaco@frba.utn.edu.ar     |
| Yogui Arakaki, Matias Ezequiel | 167.264-2 | myogui@frba.utn.edu.ar       |
| Grosclaude, Julian             | 171.656-6 | jgrosclaude@frba.utn.edu.ar  |



## Continuous Integration

This project uses `GitHub Actions`.

Read more about in the [documentation site](https://docs.github.com/en/actions)

## Development Environment

It is recommended to use [IntelliJ](https://www.jetbrains.com/idea/download/).

1. Clone the repository

Via HTTPS

```bash
git clone https://github.com/tomasanchez/grupo-3-tacs.git
```

or SSH
```bash
git clone git@github.com:tomasanchez/grupo-3-tacs.git
```

2. Install Docker

Read the official website about [Docker](https://docs.docker.com/get-docker/)


### Back-End

For more information about technologies used, how to set up development environment, running local,
read the [`README`](./rest/README.md) file on `rest` package.

### Front-End

See [`README`](./web/README.md) file on `web` package.

## Running Local

1. Run docker-compose

```bash
docker-compose up
```

## License

All material is provided under an MIT License unless otherwise specified.
MIT License: https://mit-license.org/ or see the [`LICENSE`](./LICENSE) file.

