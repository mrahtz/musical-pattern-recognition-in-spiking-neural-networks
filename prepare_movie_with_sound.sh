#!/bin/bash

# exit if any single command fails
set -o errexit

VARS_FILE=$1
AUDIO_FILE=$2
VIDEO_FILE=$(sed 's/.pickle/.video.mp4/g' <<< "$VARS_FILE")
OUTPUT_FILE=$(sed 's/.pickle/.mp4/g' <<< "$VARS_FILE")

./write_movie.py "$VARS_FILE"
ffmpeg -y \
    -i "$VIDEO_FILE" -i "$AUDIO_FILE" \
    -vcodec h264 -shortest "$OUTPUT_FILE"
