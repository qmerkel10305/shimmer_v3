#!/bin/bash

for img in ./test_images/*
do 
    echo $img
    curl -X POST 127.0.0.1:5000/shimmer/ -H 'Content-Type:multipart/form-data' -F "file=@${img}"
done