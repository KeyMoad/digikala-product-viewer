#!/usr/bin/env bash

#set -e

# Variables
ARGLEN=$#
REPOSITORY_NAME="digikala-product-viewer"
SERVICE_NAME=$REPOSITORY_NAME
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME.service"W
P_PATH="/opt/$REPOSITORY_NAME"
RESOLVER_CONF_FILE=/etc/resolv.conf
COUNTRY_CODE=$(curl -SskL ifconfig.io/country_code)


if [ $COUNTRY_CODE == "IR" ]; then
    PIP="pip install --trusted-host https://mirrors.aliyun.com -i https://mirrors.aliyun.com/pypi/simple/ --quiet"
else
    PIP="pip install --quiet"
fi

function uninstall() {
    # Stop and disable service and reload daemon
    systemctl stop $SERVICE_NAME >/dev/null 2>&1
    systemctl disable $SERVICE_NAME >/dev/null 2>&1
    systemctl daemon-reload >/dev/null 2>&1

    # Remove files
    rm -rf $P_PATH $SERVICE_PATH;
}

function install() {
    if [ -x $P_PATH ]; then
        uninstall;
    fi

    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
    echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" | tee /etc/apt/sources.list.d/google-chrome.list
    apt update -y
    apt upgrade -y
    apt install -y python3.11-full python3-pip git vim tmux wget apt-transport-https software-properties-common google-chrome-stable

    sed -i 's|yourapppath|'$P_PATH'|g' $P_PATH/service/start.sh $P_PATH/service/$SERVICE_NAME.service
    sed -i 's|servicename|'$SERVICE_NAME'|g' $P_PATH/service/stop.sh $P_PATH/service/$SERVICE_NAME.service

    # Install python venv
    python3.11 -m $PIP virtualenv >/dev/null 2>&1
    python3.11 -m venv $P_PATH/.venv >/dev/null 2>&1

    # Insatll requirements on venv
    . $P_PATH/.venv/bin/activate > /dev/null
    $P_PATH/.venv/bin/python3 -m $PIP -U pip > /dev/null
    $P_PATH/.venv/bin/python3 -m $PIP -r $P_PATH/installer/requirements.txt > /dev/null

    # Install service
    mv $P_PATH/service/$SERVICE_NAME.service $SERVICE_PATH >/dev/null 2>&1
    systemctl daemon-reload && systemctl enable $SERVICE_NAME >/dev/null 2>&1 && systemctl start $SERVICE_NAME > /dev/null
}

function help() {
    echo -e "use this script with options:\ninstall\nuninstall\nhelp for this"
}


if [ $ARGLEN -eq 0 ]; then
    help;
elif [ $ARGLEN -eq 1 ]; then
    if [ $1 == "uninstall" ]; then
        uninstall;
    elif [ $1 == "help" ]; then
        help;
    elif [ $1 == "install" ];then
        install;
    else
        echo "unknown argument: $1"
        help;
    fi
else
    echo "unknown argument: $1"
    help;
fi
