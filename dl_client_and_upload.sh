#!/bin/bash
if [ $# -ne 1 ]; then
    echo "Usage: $0 <mc version>"
    exit 1
fi
scriptsdir=$(pwd)/scripts
zipfname=$(python3 -c "print('$1' + '_bundle.zip')")
echo "Downloading client and libraries to $zipfname..."
python3 $scriptsdir/dl_jar_libs.py $1
echo "Uploading $zipfname to provider..."
longurl=$(python3 $scriptsdir/upload_to_provider.py $zipfname)
shorturl=$(python3 $scriptsdir/shorten_url.py $longurl)
echo "----------------------------------------"
echo "Client and libraries downloaded to $zipfname"
echo "Client and libraries uploaded to $shorturl"
echo "Long URL: $longurl"
echo "----------------------------------------"