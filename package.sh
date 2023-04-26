#! /bin/bash

flet pack ./src/mask_visualizer.py --icon assets/carnival-mask.png --add-data "assets:assets"
cp -r assets ./dist/
cd ./dist
tar -czvf mask_visualizer.tar.gz ./assets ./mask_visualizer