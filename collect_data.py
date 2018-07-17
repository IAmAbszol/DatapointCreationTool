from __future__ import division

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import argparse
from pykeyboard import PyKeyboard
import pyscreenshot as ImageGrab

# base - refers to template ( tupple )
# desired - refers to resolutions list ( tupple ) 
# coordinates - refers to the base coordinates to be assessed ( tupple )
# returns newly scaled coordinates ( list )
def rescale(base, desired, coordinates):
	scale_w = base[0] / desired[0]
	scale_h = base[1] / desired[1]
	# need to learn more of the one liner loops - alternate w and h
	return [ int(coordinates[0] / scale_w), int(coordinates[1] / scale_h), int(coordinates[2] / scale_w), int(coordinates[3] / scale_h) ] 	

def change_resolution(image, resolution):
	return image.resize(resolution)	

def write_to_file(file, name, coordinates):
	file.write(str(name) + " 1 " + str(coordinates[0]) + " " + str(coordinates[1]) + " " + str(abs(coordinates[0] - coordinates[2])) + " " + str(abs(coordinates[1] - coordinates[3])) + "\n")

sub_control = 5
global_image = 0
resolutions = [ (584, 480), (640, 480), (1280, 720), (1600, 900), (1920, 1080) ]
#resolutions = [ (584, 480), (640, 480), (1280, 720), (1600, 900), (1920, 1080), (640, 360), (960, 540), (160, 120), (240, 160), (320, 240), (400, 240), (480, 320), (768, 480), (854, 480), (800, 600), (960, 640) ]

# collect xml and storage directory
parse = argparse.ArgumentParser()
parse.add_argument("-x", "--xml", required=True, help="path to xml file.")
parse.add_argument("-d", "--directory", required=True, help="directory to store spliced image files.")
args = vars(parse.parse_args())

main_region = []
sub_region = []

tree = ET.parse(args["xml"])
root = tree.getroot()
template_resolution = (int(root.find("size")[0].text), int(root.find("size")[1].text))
for member in root.findall("object"):
	if member[0].text == "boundingBox":
		value = (int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text))
		main_region.append(value)
	if member[0].text == "falconBox":
		value = (int(member[4][0].text), int(member[4][1].text), int(member[4][2].text), int(member[4][3].text))
		sub_region.append(value)
# combine the cooresponding main region to its subregion
regions = zip(main_region, sub_region)

if not os.path.exists(args["directory"]):
	os.makedirs(args["directory"])
else:
	for the_file in os.listdir(args["directory"]):
		file_path = os.path.join(args["directory"], the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)

file = open(args["directory"] + "/master.txt", "w")

while True:
	# add timer delay
	main_image = ImageGrab.grab(bbox=(0,0,template_resolution[0], template_resolution[1]))
	for res in resolutions:
		im = main_image
		im = change_resolution(im, res)
		for x in range(len(regions)):
			main_region_coordinates = rescale(template_resolution, res, regions[x][0])
			#sub_region_coordinates = rescale(template_resolution, res, regions[x][1])
			sub_region_coordinates = rescale(template_resolution, res, regions[x][1])
			print(str(rescale(template_resolution, res, main_region_coordinates)) + " resolution: " + str(res))
			# follows xmin, ymin, xmax, ymax structure
			increment_calculation = [ (main_region_coordinates[0] - sub_region_coordinates[0]), (main_region_coordinates[1] - sub_region_coordinates[1]), (main_region_coordinates[2] - sub_region_coordinates[2]), (main_region_coordinates[3] - sub_region_coordinates[3]) ] 
			for main_sub_regions in range(1, sub_control, 1):
				distance = [ (increment_calculation[0] / main_sub_regions), (increment_calculation[1] / main_sub_regions), (increment_calculation[2] / main_sub_regions), (increment_calculation[3] / main_sub_regions) ]
				# now bridge these directions off the icon subregion
				created_main = [ sub_region_coordinates[0] + distance[0], sub_region_coordinates[1] + distance[1], sub_region_coordinates[2] + distance[2], sub_region_coordinates[3] + distance[3] ]
				# created main compared to sub_region_coordinates will yield the icons image relative to the bounding image.
				cropped_im = im.crop(box=(int(created_main[0]), int(created_main[1]), int(created_main[2]), int(created_main[3])))
				#im = ImageGrab.grab(bbox=(int(created_main[0]), int(created_main[1]), int(created_main[2]), int(created_main[3])))
				cropped_im.save(args["directory"] + "/" + str(global_image) + ".png")
				# calculate icons position relative to the picture itself aka bounding box created
				adjusted_sub = [ int(abs(created_main[0] - sub_region_coordinates[0])), int(abs(created_main[1] - sub_region_coordinates[1])), int(abs(created_main[0] - sub_region_coordinates[2])), int(abs(created_main[1] - sub_region_coordinates[3])) ]
				print(str(global_image) + ".png - " + str(main_sub_regions) + ": " + str(adjusted_sub[0]) + ", " + str(adjusted_sub[1]) + ", " + str(adjusted_sub[2]) + ", and " + str(adjusted_sub[3])) 
				write_to_file(file, str(global_image) + ".png", adjusted_sub)
				global_image += 1
	break	
