from PIL import Image, ImageChops
import sys, math, operator, functools, os, time, shutil

import re
def sort_nicely( l ):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )


class MapSquare(object):
	
	def __init__(self, name, coordinates):
		self.name = name
		self.coordinates = coordinates
		self.count = 0

class Building(object):
	
	def __init__(self, name, img, acmap):
		self.name = name
		self.img = img
		self.acmap = acmap
		self.count = 0
		
class AMap(object):
	def __init__(self):
		self.a1 = MapSquare("a1", [409,163])
		self.a2 = MapSquare("a2", [464,163])
		self.a4 = MapSquare("a4", [573,163])
		self.a5 = MapSquare("a5", [628,163])
		self.squares = [self.a1, self.a2, self.a4, self.a5]

class FMap(object):
	def __init__(self):
		self.f1 = MapSquare("f1", [411, 442])
		self.f2 = MapSquare("f2", [466, 442])
		self.f3 = MapSquare("f3", [520, 442])
		self.f4 = MapSquare("f4", [575, 442])
		self.squares = [self.f1, self.f2, self.f3, self.f4]
	
class Map(object):
	def __init__(self):
		self.c1 = MapSquare("c1", [411, 275])
		self.c2 = MapSquare("c2", [466, 275])
		self.c3 = MapSquare("c3", [520, 275])
		self.c4 = MapSquare("c4", [575, 275])
		self.c5 = MapSquare("c5", [630, 275])
		
		self.d1 = MapSquare("d1", [411, 331])
		self.d2 = MapSquare("d2", [466, 331])
		self.d3 = MapSquare("d3", [520, 331])
		self.d4 = MapSquare("d4", [575, 331])
		self.d5 = MapSquare("d5", [630, 331])
		
		self.e1 = MapSquare("e1", [411, 387])
		self.e2 = MapSquare("e2", [466, 387])
		self.e3 = MapSquare("e3", [520, 387])
		self.e4 = MapSquare("e4", [575, 387])
		self.e5 = MapSquare("e5", [630, 387])
		
		self.squares = [self.c1, self.c2, self.c3, self.c4, self.c5, self.d1, self.d2, self.d3, self.d4, self.d5, self.e1, self.e2, self.e3, self.e4, self.e5]
		
class HouseMap(object):
	def __init__(self):
		self.b1 = MapSquare("b1", [411, 220])
		self.b2 = MapSquare("b2", [466, 220])
		self.b3 = MapSquare("b3", [520, 220])
		self.b4 = MapSquare("b4", [575, 220])
		self.b5 = MapSquare("b5", [630, 220])
		
		self.c1 = MapSquare("c1", [411, 275])
		self.c2 = MapSquare("c2", [466, 275])
		self.c3 = MapSquare("c3", [520, 275])
		self.c4 = MapSquare("c4", [575, 275])
		self.c5 = MapSquare("c5", [630, 275])
		
		self.d1 = MapSquare("d1", [411, 331])
		self.d2 = MapSquare("d2", [466, 331])
		self.d3 = MapSquare("d3", [520, 331])
		self.d4 = MapSquare("d4", [575, 331])
		self.d5 = MapSquare("d5", [630, 331])
		
		self.e1 = MapSquare("e1", [411, 387])
		self.e2 = MapSquare("e2", [466, 387])
		self.e3 = MapSquare("e3", [520, 387])
		self.e4 = MapSquare("e4", [575, 387])
		self.e5 = MapSquare("e5", [630, 387])
		
		self.f1 = MapSquare("f1", [411, 442])
		self.f2 = MapSquare("f2", [466, 442])
		self.f3 = MapSquare("f3", [520, 442])
		self.f4 = MapSquare("f4", [575, 442])
		self.f5 = MapSquare("f5", [630, 442])
		
		self.squares = [self.b1, self.b2, self.b3, self.b4, self.b5, self.c1, self.c2, self.c3, self.c4, self.c5, self.d1, self.d2, self.d3, self.d4, self.d5, self.e1, self.e2, self.e3, self.e4, self.e5, self.f1, self.f2, self.f3, self.f4, self.f5]

def rms(img1, img2):
	h = ImageChops.difference(img1, img2).histogram()
	return math.sqrt(functools.reduce(operator.add, map(lambda h, i: h*(i**2), h, range(256)))/(float(img1.size[0]) * img1.size[1]))
	
shop = Building("shop", Image.open("shop.png"), AMap())
dump = Building("dump", Image.open("dump.png"), AMap())
postoffice = Building("post office", Image.open("postoffice.png"), AMap())
tailor = Building("tailor", Image.open("tailor.png"), FMap())
policestation = Building("police station", Image.open("policestation.png"), Map())
fountain = Building("fountain", Image.open("fountain.png"), Map())
museum = Building("museum", Image.open("museum.png"), Map())
buildings = [shop, dump, postoffice, tailor, policestation, fountain, museum]

cliff = Image.open("cliff.png")
cliffSquares = [MapSquare("b1", [409, 249]), MapSquare("c1", [409, 305]), MapSquare("d1", [409, 361]), MapSquare("e1", [409, 417])]

houseMap = HouseMap()

def main():
	startTime = time.time()
	fileCount = 0
	twoLayers = 0
	threeLayers = 0
	directory = "./"
	skip = 0
	most = 0
	current = 0
	possiblyDecentMaps = 0
	printStats = True
	if len(sys.argv) > 1:
		directory = sys.argv[1]
	if len(sys.argv) > 2:
		skip = int(sys.argv[2])
	if len(sys.argv) > 3:
		printStats = sys.argv[3]
	
	if printStats == 0 or printStats == "0" or printStats == "false":
		printStats = False
		
	files = os.listdir(directory)
	sort_nicely(files)
	for file in files:
		if file.endswith(".png"):
			fileCount += 1
			if fileCount <= skip:
				continue
			im = Image.open(directory+file)
			layers = 1
			shop = 0
			post = 0
			fountain = 0
			housesOkay = True
			for building in buildings:
				lowestdiff = 100
				bestmatch = 0
				for mapsquare in building.acmap.squares:
					region = im.crop((mapsquare.coordinates[0], mapsquare.coordinates[1], mapsquare.coordinates[0]+50, mapsquare.coordinates[1]+50))
					diff = rms(region, building.img)
					if diff < lowestdiff:
						lowestdiff = diff
						bestmatch = mapsquare
							
				bestmatch.count += 1
				building.count += 1
				if building.name == "shop":
					shop = bestmatch
				elif building.name == "post office":
					post = bestmatch
				elif building.name == "fountain":
					fountain = bestmatch
				if  bestmatch.name == "c2" or bestmatch.name == "c3" or bestmatch.name == "c4":
					print(str(file))
			
			for square in cliffSquares:
				region = im.crop((square.coordinates[0], square.coordinates[1], square.coordinates[0]+12, square.coordinates[1]+16))
				diff = rms(region, cliff)
				if diff < 20:
					layers += 1
					
			if layers == 2:
				twoLayers += 1
			elif layers == 3:
				threeLayers += 1
				
			c1 = False
			c5 = False
			col1 = False
			col5 = False
			belowShop = False
			ramp = ["z9","z9","z9","z9"]
			rampFound = 0

			for square in houseMap.squares:
				region = im.crop((square.coordinates[0], square.coordinates[1], square.coordinates[0]+50, square.coordinates[1]+50))
				colors = region.getcolors(maxcolors=1000)
				
				for color in colors:
					#blue house = (90, 90, 225, 255)	purple house = (145, 70, 205, 255)	yellow house = (170, 115, 20, 255)
					if color[1] == (90, 90, 225, 255) or color[1] == (145, 70, 205, 255) or color[1] == (170, 115, 20, 255):
						if "e" in square.name or "f" in square.name:
							housesOkay = False
						elif square.name == "d1" or square.name == "d5":
							housesOkay = False
						elif "1" in square.name:
							col1 = True
						elif "5" in square.name:
							col5 = True
						if square.name == "c1":
							c1 = True
						elif square.name == "c5":
							c5 = True
						elif (shop.name == "a2" and square.name == "b2") or (shop.name == "a4" and square.name == "b4"):
							belowShop = True
						if (square.name == "c1" or square.name == "d1") and fountain.name == "d5":
							housesOkay = False
						elif (square.name == "c5" or square.name == "d5") and fountain.name == "d1":
							housesOkay = False
					#ramp
					if color[1] == (66, 189, 66, 255):
						ramp[rampFound] = square.name
						rampFound += 1


			if c1 and c5:
				housesOkay = False
			elif belowShop == False:
				housesOkay = False
			elif col1 and col5 and "e" in fountain.name:
				housesOkay = False

			OK = False
			if housesOkay and ("e" in fountain.name) or ("d" in fountain.name):
				for i in range (0, 3):
					if ramp[i][1:2] == chr(ord(fountain.name[1:2])) or (abs(ord(ramp[i][1:2]) - ord(fountain.name[1:2])) == 1 and ramp[i][0:1] !=  fountain.name[0:1]):
						OK = True
				if not OK:
					housesOkay = False

			if (housesOkay and ((shop.name == "a2" and post.name == "a4") or (shop.name == "a4" and post.name == "a2")) and not (fountain.name == "e1" or fountain.name == "e5" or (layers == 3 and "e" in fountain.name))):
				if not os.path.exists(directory+"maybe/"):
					os.makedirs(directory+"maybe/")
				shutil.copy(directory+file, directory+"maybe/"+file)
				possiblyDecentMaps += 1
				current = 0
			else:
				current += 1
				if current > most:
					most = current
	
	if printStats:				
		print("two layers:\t"+str(twoLayers)+"\t"+str((twoLayers/(fileCount-skip))*100)+"%")
		print("three layers:\t"+str(threeLayers)+"\t"+str((threeLayers/(fileCount-skip))*100)+"%")
		
		for building in buildings:
			print(str("\n"+building.name))
			for mapsquare in building.acmap.squares:
						print("\t"+str(mapsquare.name)+":\t"+str(mapsquare.count)+"\t"+str((mapsquare.count/building.count)*100)+"%")	
	print("\nmaps: "+str((fileCount-skip)))
	print("possibly decent maps: "+str(possiblyDecentMaps))
	print("Longest bad streak: " +str(most))
	print("elapsed time: "+str(time.time()-startTime)+" seconds")
	
	
	
if __name__ == "__main__":
	main()
