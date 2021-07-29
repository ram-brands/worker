# RAM Web Services

## Requirements

- [Docker](https://www.docker.com/) (needed)
- [Docker Compose](https://docs.docker.com/compose/) (needed)
- [Make](https://en.wikipedia.org/wiki/Make_(software)) (highly recommended)
- [Poetry](https://python-poetry.org/docs/) (highly recommended)

---

## Install RAM Web Services’ file-processing worker for local development

Build the images (but first make sure the Docker deamon is running):

```bash
make build
```

Start the application:

```bash
docker-compose up
```

(Then, to stop the application just type `ctrl-C`.)

Kill all processes (on another terminal, if the application is still running):

```bash
docker-compose down
```

---

## Wanna write some code? Follow these steps first

Create a development-friendly virtual environment:

```bash
make createvenv
```

If new dependencies are added, update your virtual environment and re-build the images:

```bash
make createvenv
make build
```

If you are adding any files or folders that should be considered by Docker, un-ignore them at the `.dockerignore`. Then, re-build the images:

```bash
make build
```

Format your code with [black](https://pypi.org/project/black/) and [isort](https://pypi.org/project/isort/):

```bash
make format!
```
