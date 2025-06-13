from invoke import task


@task
def mig(c):
    c.run("python manage.py makemigrations")


@task
def upg(c):
    c.run("python manage.py migrate")


@task
def admin(c):
    c.run("python manage.py createsuperuser")


@task
def apps(c):
    c.run("python manage.py startapp apps")


@task
def celery(c):
    c.run("celery -A RestAPI worker --pool=solo -l info")


@task
def flower(c):
    c.run("celery -A RestAPI flower")


@task
def beat(c):
    c.run("celery -A RestAPI beat -l info -S django")


@task
def push(c):
    c.run(' @read -p "Commit izohini kiriting: " m; \
            git add .; \
            git commit -m "$$m"; \
            git push')
