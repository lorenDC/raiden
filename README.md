# AMANDA in Gauge
[![Gauge Badge](https://gauge.org/Gauge_Badge.svg)](https://gauge.org)

## Usage with Docker

Prerequisites:
1. Docker is running.

```shell
docker build . -t 887374955478.dkr.ecr.ap-southeast-1.amazonaws.com/gauge/raiden:prodregistry060623
docker run --rm --name container_gauge -v $(pwd):/workspace/gauge-amanda -w="/workspace/gauge-amanda" image_gauge gauge run --env "test_kong_api, test_db" --verbose specs
```

## Usage without Docker
```shell
gauge run --env "test_kong_api, test_db" --verbose specs
open reports/html-report/index.html
```

## Usage with API requests running behind BURP proxy
```shell
gauge run --env "test_kong_api, test_db, proxy_burp" --verbose specs
open reports/html-report/index.html
```

## Usage with API requests running behind ZAP proxy'C:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon
```shell
gauge run --env "test_kong_api, test_db, proxy_zap" --verbose specs
open reports/html-report/index.html
```

## Installation (without using Docker)

Guidelines:
* Upgrade any of the following if current version is less than latest version. Else, skip the step.
* Ensure each step finishes its execution without error.
* Proceed through each step while inside project's root directory unless otherwise specified.

### MacOS

1. Clone the project.
2. Go inside this project's root directory. Executing the following command: 
    ```shell
    pwd
    ```
    should yield:
    ```shell
    <some_dir_path>/gauge-amanda
    ```
3. Install Command Line Tools.
    ```shell
    xcode-select --install
    ```
4. Install Homebrew.
    ```shell
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    ```
5. Install Gauge.
    ```shell
    brew install gauge
    ```
6. Install pyenv.
    ```shell
    brew install pyenv
    ```
7. Install zlib.
    ```shell
    brew install zlib
    ```
8. Export the following to your `~/.zshrc` or `~/.bashrc`.
    ```shell
    # For compilers to find zlib you may need to set:
    export LDFLAGS="${LDFLAGS} -L/usr/local/opt/zlib/lib"
    export CPPFLAGS="${CPPFLAGS} -I/usr/local/opt/zlib/include"
    # For pkg-config to find zlib you may need to set:
    export PKG_CONFIG_PATH="${PKG_CONFIG_PATH} /usr/local/opt/zlib/lib/pkgconfig"
    eval "$(pyenv init --path)"
    ```
9. Install the latest Python version (3.9.4) in via `pyenv`.
    ```shell
    pyenv install 3.9.4
    pyenv local 3.9.4
    python --version
    ```
10. Create a virtual environment named `env`.
    ```shell
    python3 -m venv env
    ```
11. Activate your vitrual environment through the following command.
    ```shell
    source env/bin/activate
    ```
12. Install gauge-amanda's Python package dependencies.
    ```shell
    pip install -r requirements.txt
    ```
13. Download the cx_Oracle binary installer.
    ```shell
    curl -O https://download.oracle.com/otn_software/mac/instantclient/198000/instantclient-basic-macos.x64-19.8.0.0.0dbru.dmg
    ```
14. Mount the dmg file.
    ```shell
    hdiutil mount instantclient-basic-macos.x64-19.8.0.0.0dbru.dmg
    ```
15. Install cx_Oracle binaries.
    ```shell
    /Volumes/instantclient-basic-macos.x64-19.8.0.0.0dbru/install_ic.sh
    ```
16. Unmount the dmg file.
    ```shell
    hdiutil unmount /Volumes/instantclient-basic-macos.x64-19.8.0.0.0dbru
    ```
17. Delete the dmg file.
    ```shell
    rm -f instantclient-basic-macos.x64-19.8.0.0.0dbru.dmg
    ```
18. Move the installed binaries from Downloads to this project directory's `lib` directory.
    ```shell
    mv ~/Downloads/instantclient_19_8 lib/instantclient_19_8
    ```
19. To run gauge-amanda tests and see its report, see `Usage without Docker` above.

### Windows

1. Clone the project.
2. Download and install the [latest Python stable release](https://www.python.org/downloads/windows/).
3. Download and install the [latest Gauge stable release](https://docs.gauge.org/getting_started/installing-gauge.html?os=windows&language=python&ide=vscode#install-using-windows-installer).
4. Go inside this project's root directory. Executing the following command: 
    ```powershell
    pwd
    ```
    should yield:
    ```powershell
    <some_dir_path>\gauge-amanda
    ```
5. Create a virtual environment named `env`.
    ```powershell
    python3 -m venv env
    ```
6. Activate your vitrual environment through the following command.
    ```powershell
    env\Scripts\activate
    ```
7. Install gauge-amanda's Python package dependencies.
    ```powershell
    pip install -r requirements.txt
    ```
8. Download the [cx_Oracle Basic package](https://www.oracle.com/ph/database/technologies/instant-client/winx64-64-downloads.html).
9. Unzip the `instantclient-basic-windows.x64-x.x.x.x.xdbru.zip`.
10. Move the instantclient_x_x to this project directory's `lib` directory.
11. To run gauge-amanda tests and see its report, see `Usage without Docker` above.

## IF ERROR ENCOUNTERED in WINDOWS
1. about_Execution_Policies / FullyQualifiedErrorId : UnauthorizedAccess | https:/go.microsoft.com/fwlink/?LinkID=135170
    a. Open PowerShell as ADMIN
    b. ```Set-ExecutionPolicy -ExecutionPolicy RemoteSigned```
    
## Modifying Spreadsheet DDT
Go to and export the spreadsheet in CSV format:
https://voyagerinnovation.sharepoint.com/:x:/r/sites/AcquiringQEs950/Shared%20Documents/General/Test%20Cases/BOSE/Gauge%20Data/ProvisioningData.xlsx?d=wc28ab9cb3c7440918de72b9945df6eca&csf=1&web=1&e=HtNRaI
