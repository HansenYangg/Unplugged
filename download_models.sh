#!/bin/bash

echo "Downloading model zip from Google Drive..."
gdown --id 1FgEcP_JHechbtrS_pd_4XDkdToWsMeqO --output models.zip

echo "Unzipping..."
unzip models.zip
rm models.zip

echo "Done!"
