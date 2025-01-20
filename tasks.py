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
def run_backup(ctx):
    script_path = Path("Generate-SystemReports.ps1")
    if script_path.is_file():
        ctx.run(f"pwsh.exe -NoLogo -Command .\\{script_path.name}")
        ctx.run("pwsh.exe -NoLogo -Command Generate-SystemReports")
    else:
        print(f"Script {script_path} not found")

@task
def list_pipx_installed_packages(ctx):
    update_progress(ctx, "Listing Pipx installed packages...")
    with open("pipx_list.txt", "w") as file:
        ctx.run("pipx list", out_stream=file)

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
