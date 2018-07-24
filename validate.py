from PIL import Image
import argparse

parse = argparse.ArgumentParser()
parse.add_argument("-d", "--directory", required=True, help="path to directory file.")
parse.add_argument("-f", "--file", required=True, help="path to master file.")
parse.add_argument("-c", "--compile", action="store_true", help="fix master file to correct for errors.")
args = vars(parse.parse_args())

hit_w, hit_h = 0, 0
fixed_file = open("fixed-file.txt", "w") if args["compile"] else None

with open(args["directory"] + "/" + args["file"], "r") as file:
	empty = file.readline()
	for line in file:
		split_line = line.split(" ")
		im = Image.open(args["directory"] + "/" + split_line[0])
		width, height = im.size
		if (int(split_line[2]) + int(split_line[4])) >= width:
			print(str(split_line[0]) + ": width specified for bounding box too large.")
			hit_w += 1
			if args["compile"]:
				split_line[4] = int(split_line[4])
				split_line[4] -= (int(split_line[2]) + int(split_line[4])) - width + 1
		if (int(split_line[3]) + int(split_line[5])) > height:
			print(str(split_line[0]) + ": height specific for bounding box too large.")
			hit_h += 1
			if args["compile"]:
				split_line[5] = int(split_line[5])
				split_line[5] -= (int(split_line[3]) + int(split_line[5])) - width + 1
		if args["compile"]:
			fixed_file.write(str(split_line[0]) + " " + str(split_line[1]) + " " + str(split_line[2]) + " " + str(split_line[3]) + " " + str(
				split_line[4]) + " " + str(split_line[5]))
if args["compile"]:
	fixed_file.close()
print("Width hits: " + str(hit_w) + ", Height hits: " + str(hit_h))

