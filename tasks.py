from invoke import task, Collection

@task
def update_progress(ctx, message):
    print(message)

@task
def commit(ctx, message="init"):
    ctx.run("git add .")
    ctx.run(f"git commit -m \"{message}\"")

@task
def quit(ctx):
    print("Copyright © 2024 Charudatta")

@task
def test(ctx):
    ctx.run("python -m unittest discover -s tests")

@task
def train(ctx):
    with ctx.prefix('conda activate w'):
        ctx.run("python src/main.py")

@task
def run(ctx):
    ctx.run("ollama run gemma:2b &", pty=True)
    with ctx.prefix('conda activate w'):
        ctx.run("python src/ai_write_blog_post_v4.py")

@task
def list_scoop_installed_apps(ctx):
    with open("scoop_list.txt", "w") as file:
        ctx.run("scoop list", out_stream=file)

@task(default=True)
def default(ctx):
    # Get a list of tasks
    tasks = sorted(ns.tasks.keys())
    # Display tasks and prompt user
    for i, task_name in enumerate(tasks, 1):
        print(f"{i}: {task_name}")
    choice = int(input("Enter the number of your choice: "))
    ctx.run(f"invoke {tasks[choice - 1]}")

# Create a collection of tasks
ns = Collection(update_progress, commit, quit, run_backup, list_pipx_installed_packages, list_scoop_installed_apps, default)
