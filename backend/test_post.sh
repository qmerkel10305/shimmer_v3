#!/bin/bash

for img in ./test_images/*
do 
    #for testing metadata send (adds complexity because curl doesn't accept dictionaries)
    # echo $img
    # if [ "$img" = './test_images/test_IMG.png' ]; then
    #     echo "-----------Test Metadata----------------"
    #     curl -X POST 127.0.0.1:5000/shimmer/ -H 'Content-Type:multipart/form-data' -F "file=@${img}" -F "metadata={\"test_key\":\"test_value\"}"
    # else
    #     echo "****************************"
    #     curl -X POST 127.0.0.1:5000/shimmer/ -H 'Content-Type:multipart/form-data' -F "file=@${img}"
    # fi
    curl -X POST 127.0.0.1:5000/shimmer/ -H 'Content-Type:multipart/form-data' -F "file=@${img}"
done