# buildwheel.py
A Python script for building and uploading package wheels to PyPI using the ActiveState platform.

```
## Warning: This script is intended as a demonstration only. It utilizes API calls and other functionality
## that is unstable and in development. Things could change in the future so you probably shouldn't rely
## on any particular API call.
```

## Installation
Clone this repository to your local machine

```
$ git clone https://github.com/ActiveState/buildwheels.git
```

## Install the required packages using the state tool

If you don't have the state tool installed, you can install it for free from ActiveState. The state tool is a universal package manager that enables you to easily manage and maintain your runtime environments.

### Windows

Download and run the [state tool installer](https://state-tool.s3.amazonaws.com/remote-installer/windows-amd64/state-remote-installer.exe).

### Linux and macOS

Open your command prompt and execute the following command:

```
sh <(curl -q https://platform.activestate.com/dl/cli/install.sh)`
```

Once installed it is recommended that you close your command prompt and start a new one to ensure your environment is properly updated.

### Activating the runtime environment

The simplest way to download, install and utilize the fully prepared runtime environment is to simply run the following command in your terminal:

```
$ state activate
```

This will download, install and put you into a virtual shell using a runtime environment tailored to this application.

## Usage
The script takes in the following arguments:

`org_name`: The name of the organization on ActiveState.  
`project_name`: The name of the project on ActiveState.  
`package_name`: The name of the package to build and upload.  
`version`: The version of the package to build and upload.  
`platforms`: The platforms on which to build the package. Valid platforms are `windows`, `linux`, and `mac`. Short forms `win`, `lin`, and `mac` are also supported.  
`--publish`: Automatically publish the wheel to PyPI. Requires PYPI_USER and PYPI_PASS to be set. Defaults to `false`.  

```
$ export PYPI_USER=<your-username>
$ export PYPI_PASS=<your-password>
$ python buildwheel.py org_name project_name package_name version platforms
```

For example, to build and upload a package named "mypackage" version 1.0.0 for Windows and Linux platforms to PyPI, you would run the following command:

```
$ export PYPI_USER=<your-username>
$ export PYPI_PASS=<your-password>
$ python buildwheel.py acme myproject mypackage 1.0.0 win,lin
```

## Using a .env file
To make it easier to use the script, you can create a `.env` file in the root directory of the project and store your `PYPI_USER` and `PYPI_PASS` credentials there. To do this, create a new file named `.env` and add the following lines:

```
PYPI_USER=<your-username>
PYPI_PASS=<your-password>
```
Make sure to replace <your-username> and <your-password> with your actual PyPI credentials. Then, when you run the script, it will automatically load these variables from the `.env` file. This way, you don't have to export the variables each time you run the script. Note that you should never commit your `.env` file to a public repository as it contains sensitive information.

## Using as a GitHub Action
You can use this script as a GitHub action in your workflows to automatically build wheels. You need to configure a few secrets on your repo first:

`ACTIVESTATE_API_KEY` : Set this to your API key for the platform.
`PYPI_USER` : Set this to your PyPI username or `__token__` to use an API key.
`PYPI_PASS` : Set this to your PyPI API key or password.

### Inputs
The action takes all the same arguments as the script. They are all named the same: `org_name`, `project_name`, `package_name`, `version`, `platforms` and `publish`. See the *Usage* section for more details.

### Acquiring an ActiveState API KEY
You need an account on the ActiveState Platform to generate an API key. Head to [https://platform.activestate.com](https://platform.activestate.com) to sign up. Once you have the state tool installed, run:

```
$ state auth
```
...and authenticate with your account credentials. Then, run:

```
$ state export new-api-key
```
Copy your API key and use it to populate the ACTIVESTATE_API_KEY environment variable in your GitHub repo.

### Publishing to PYPI
If you want to publish to PyPI direct from GitHub actions, you can simply set the `publish` input to `true` and the script will use your `PYPI_USER` and `PYPI_PASS` secrets to upload your wheel to PyPI.

Alternatively, you can also use another action like [https://github.com/pypa/gh-action-pypi-publish](https://github.com/pypa/gh-action-pypi-publish) to publish the wheels to PyPI. This action will publish the output as artifacts that can then be uploaded using a different action.

## License
This script is licensed under the MIT License. See the LICENSE file for more details.
