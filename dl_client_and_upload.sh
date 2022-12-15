#!/bin/bash
version=$1
fname="$(python3 scripts/download_jar.py $version)"
echo "Downloaded $fname, starting upload"
cdn_url="$(python3 scripts/upload_to_provider.py $fname)"
echo "Uploaded to $cdn_url"