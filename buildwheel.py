import subprocess
import time
import json
import requests
import yaml
import os
import click
import re

from dotenv import load_dotenv
load_dotenv()

# Constants
yamlfile = "activestate.yaml"
build_url = "https://platform.activestate.com/sv/head-chef/v2/builds"
platforms_codes = {'win': 'Windows@10.0.17134.1', 'windows': 'Windows@10.0.17134.1', 'lin': 'Linux@4.18.0', 'linux': 'Linux@4.18.0', 'mac': 'Darwin@19.0.0', 'macos': 'Darwin@19.0.0'}
pypi_user = os.environ.get("PYPI_USER")
pypi_pass = os.environ.get("PYPI_PASS")

def parse_platforms(platforms):
    valid_platforms = {"windows", "linux", "mac"}
    short_forms = {"win": "windows", "lin": "linux", "mac": "mac"}
    platform_list = platforms.split(",")
    for i, platform in enumerate(platform_list):
        platform = platform.strip().lower()
        if platform in short_forms:
            platform = short_forms[platform]
        if platform not in valid_platforms:
            raise click.BadParameter(f"Invalid platform: {platform}. Valid options are {', '.join(valid_platforms)}.")
        platform_list[i] = platform
    return platform_list

def validate_version(version):
    pattern = re.compile(r"^\d+(\.\d+){1,2}$")
    if not pattern.match(version):
        raise click.BadParameter(f"Invalid version number: {version}. Example of valid version: '1.2.3'")

def append_version_number(s):
    parts = s.split('-')
    version_number = parts[1]
    parts[1] = version_number + '-4'
    return '-'.join(parts)

def GenerateWheel(project, rootname, platforms,lang,id,pkg):
    print("Creating Project Folder...")
    if not os.path.exists(project):
        print(f"Creating folder {project}.")
        os.makedirs(project)

    print("Clearing out any existing config files...")

    if os.path.exists(os.path.join(project,yamlfile)):
        os.remove(os.path.join(project,yamlfile))

    print("Creating Project...")
    stdout = subprocess.run(['state', 'init', id, lang, "-n"], check=True, capture_output=True, text=True).stdout

    print("Pushing Project to Platform...")

    stdout = subprocess.run(['state', 'push', "-n"], check=True, capture_output=True, text=True).stdout

    for p in platforms:
        print(f"Adding {p}...")
        stdout = subprocess.run(['state', 'platforms', 'add', platforms_codes[p.lower()], "-n"], check=True, capture_output=True, text=True).stdout

    print("Syncing changes with platform...")

    stdout = subprocess.run(['state', 'pull', "-n"], check=True, capture_output=True, text=True).stdout

    print("Adding Package to Project...")

    stdout = subprocess.run(['state', 'install', pkg, "-n"], check=True, capture_output=True, text=True).stdout

    print("Pushing Project to Platform...")

    stdout = subprocess.run(['state', 'push', "-n"], check=True, capture_output=True, text=True).stdout

    commit_id = ""
    print("Gathering Commit ID...")

    ## Open the new YAML file and get the latest commit now that it's installed
    with open(yamlfile, "r") as stream:
        try:
            yfile = yaml.safe_load(stream)
            commit_id = yfile['project'][-36:]
        except yaml.YAMLError as exc:
            print(exc)

    print("Exporting Recipe...")

    stdout = subprocess.run(['state', 'export', 'recipe', "-n"], check=True, capture_output=True, text=True).stdout

    recipe = json.loads(stdout)

    print("Generating Wheels...")

    r = requests.post(build_url, json={"recipe_id": recipe['recipe_id']})

    jsr = r.json()

    bpid = jsr['build_plan_id']

    ready =  False

    status_url = build_url +"/" + bpid

    while(not ready):
        r = requests.get(status_url)
        jsr = r.json()
        if jsr["build_state"] == "build_succeeded":
            ready = True
            break
        print("Waiting for wheels to build...")
        time.sleep(5)

    gql_url = "https://platform.activestate.com/sv/mediator/api"
    query = f"""
            {{
            builds(commit_id:"{commit_id}"){{
                ...on Builds{{
                builds{{
                    ...on BuildSuccess {{
                    platform_id
                    artifacts {{
                        name
                        mime_type
                        uri
                    }}
                    }}
                }}            
                }}
            }}
            }}
    """

    print("Gathering Artifacts...")

    # TODO: Add auth to cover private projects? 
    variables = {'commit': commit_id}
    r = requests.post(gql_url, json={'query': query , 'variables': variables})

    builds = r.json()

    print("Downloading Artifacts...")

    print("Creating Artifact Dist Folder...")
    if not os.path.exists("dist"):
        os.makedirs("dist")

    print("Downloading wheels...")
    for b in builds['data']['builds']['builds']:
        for a in b['artifacts']:
            if a['mime_type'] == 'application/x-python-wheel+zip':
                url = a['uri']
                fname = url[url.rfind('/')+1:]
                if rootname in fname:
                    print(fname)
                    r = requests.get(a['uri'], stream=True)
                    with open(os.path.join("dist",append_version_number(fname)),'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024): 
                            if chunk:
                                f.write(chunk)

    print("Uploading wheel(s) to PyPI...")
    stdout = subprocess.run(["twine", "upload", "-r","testpypi","dist/*","-u",f"{pypi_user}","-p",f"{pypi_pass}","--non-interactive"], check=True, capture_output=True, text=True).stdout

    os.chdir("..")

    print("Done!")

@click.command()
@click.argument("org_name", type=str, required=True)
@click.argument("project_name", type=str, required=True)
@click.argument("package_name", type=str, required=True)
@click.argument("version", type=str, required=True)
@click.argument("platforms", type=str, required=True)
def main(org_name, project_name, package_name, version, platforms):
    platforms = parse_platforms(platforms)
    validate_version(version)

    ts = time.strftime('%H%M%S')
    id = f"{org_name}/{project_name+ts}"

    lang = f"python3@3.10.8"

    pkg = "@".join([package_name,version])

    rootname = package_name.replace("-","_")

    GenerateWheel(project_name+ts,rootname,platforms,lang,id,pkg)

if __name__ == "__main__":
    main()