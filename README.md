# buildwheel.py
A Python script for building and uploading package wheels to PyPI using the ActiveState platform.

## Installation
Clone this repository to your local machine

```
$ git clone https://github.com/your-username/your-repo-name.git
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

## License
This script is licensed under the MIT License. See the LICENSE file for more details.
