from fabric import task


@task
def develop(ctx):
    ctx.run("[ -d env ] || python3 -m venv env", replace_env=False)
    ctx.run("./env/bin/pip install -U pip")
    ctx.run("./env/bin/pip install -e .")
