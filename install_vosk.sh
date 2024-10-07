#!/bin/bash

function printHelp () {
    echo "install_vosk.sh [ Vosk model id ]"
    echo ""
    echo "Offline Assistant - Vosk Installer"
    echo " running this program with no arguments will"
    echo " show this message. Please provide an ID to"
    echo " start a download."
    echo ""
    echo "Vosk Model IDs :"
    echo " 0 - English US Small"
    echo " 1 - English US med, lgraph"
    echo " 2 - English Full Size"
    echo " 3 - English Gigsspeech"
    echo ""
}

URL_BASE="https://alphacephei.com/vosk/models/"

if [ $1 == 0 ] || [ -z "$1" ]; then
    FILENAME="vosk-model-small-en-us-0.15.zip"
elif [ $1 == 1 ]; then
    FILENAME="vosk-model-en-us-0.22-lgraph.zip"
elif [ $1 == 2 ]; then
    FILENAME="vosk-model-en-us-0.22.zip"
elif [ $1 == 3 ]; then
    FILENAME="vosk-model-en-us-0.42-gigaspeech.zip"
else
    $(printHelp)
fi

URL=${URL_BASE}${FILENAME}
echo "Downloading : ${URL}"
wget $URL

if [ -e ${FILENAME} ]; then
    unzip ./${FILENAME}
else
    echo "Failed to download!"
    exit 1
fi

