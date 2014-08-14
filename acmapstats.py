from PIL import Image, ImageChops
import sys, math, operator, functools, os, time, shutil

import re
def sort_nicely( l ):
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )

yA = 165
yB = 220
yC = 275
yD = 331
yE = 387
yF = 442

x1 = 411
x2 = 466
x3 = 521
x4 = 575
x5 = 630


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
		self.a1 = MapSquare("a1", [x1, yA])
		self.a2 = MapSquare("a2", [x2, yA])
		self.a4 = MapSquare("a4", [x4, yA])
		self.a5 = MapSquare("a5", [x5, yA])
		self.squares = [self.a1, self.a2, self.a4, self.a5]

class FMap(object):
	def __init__(self):
		self.f1 = MapSquare("f1", [x1, yF])
		self.f2 = MapSquare("f2", [x2, yF])
		self.f3 = MapSquare("f3", [x3, yF])
		self.f4 = MapSquare("f4", [x4, yF])
		self.squares = [self.f1, self.f2, self.f3, self.f4]
	
class Map(object):
	def __init__(self):
		self.c1 = MapSquare("c1", [x1, yC])
		self.c2 = MapSquare("c2", [x2, yC])
		self.c3 = MapSquare("c3", [x3, yC])
		self.c4 = MapSquare("c4", [x4, yC])
		self.c5 = MapSquare("c5", [x5, yC])
		
		self.d1 = MapSquare("d1", [x1, yD])
		self.d2 = MapSquare("d2", [x2, yD])
		self.d3 = MapSquare("d3", [x3, yD])
		self.d4 = MapSquare("d4", [x4, yD])
		self.d5 = MapSquare("d5", [x5, yD])
		
		self.e1 = MapSquare("e1", [x1, yE])
		self.e2 = MapSquare("e2", [x2, yE])
		self.e3 = MapSquare("e3", [x3, yE])
		self.e4 = MapSquare("e4", [x4, yE])
		self.e5 = MapSquare("e5", [x5, yE])
		
		self.squares = [self.c1, self.c2, self.c3, self.c4, self.c5, self.d1, self.d2, self.d3, self.d4, self.d5, self.e1, self.e2, self.e3, self.e4, self.e5]
		
class HouseMap(object):
	def __init__(self):
		self.b1 = MapSquare("b1", [x1, yB])
		self.b2 = MapSquare("b2", [x2, yB])
		self.b3 = MapSquare("b3", [x3, yB])
		self.b4 = MapSquare("b4", [x4, yB])
		self.b5 = MapSquare("b5", [x5, yB])
		
		self.c1 = MapSquare("c1", [x1, yC])
		self.c2 = MapSquare("c2", [x2, yC])
		self.c3 = MapSquare("c3", [x3, yC])
		self.c4 = MapSquare("c4", [x4, yC])
		self.c5 = MapSquare("c5", [x5, yC])
		
		self.d1 = MapSquare("d1", [x1, yD])
		self.d2 = MapSquare("d2", [x2, yD])
		self.d3 = MapSquare("d3", [x3, yD])
		self.d4 = MapSquare("d4", [x4, yD])
		self.d5 = MapSquare("d5", [x5, yD])
		
		self.e1 = MapSquare("e1", [x1, yE])
		self.e2 = MapSquare("e2", [x2, yE])
		self.e3 = MapSquare("e3", [x3, yE])
		self.e4 = MapSquare("e4", [x4, yE])
		self.e5 = MapSquare("e5", [x5, yE])
		
		self.f1 = MapSquare("f1", [x1, yF])
		self.f2 = MapSquare("f2", [x2, yF])
		self.f3 = MapSquare("f3", [x3, yF])
		self.f4 = MapSquare("f4", [x4, yF])
		self.f5 = MapSquare("f5", [x5, yF])
		
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
cliffSquares = [MapSquare("b1", [x1, 249]), MapSquare("c1", [x1, 305]), MapSquare("d1", [x1, 361]), MapSquare("e1", [x1, 417])]

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
			yOffset = 0
			im = Image.open(directory+file)
			region = im.crop((330, 140, 331, 141))
			colors = region.getcolors(1)
			if colors is None or colors[0][1] != (255, 255, 85, 255): #make sure it's a screenshot of the map
				region = im.crop((330, 175, 331, 176))
				colors = region.getcolors(1)
				if colors is None or colors[0][1] != (255, 255, 85, 255): #check another spot in case the map is offset and it happens to hit one of the lines.
					print(str(file) + " No map found.")
					continue
			
			#try to look to see where the map is in case it's higher or lower than expected
			region = im.crop((400, 146, 401, 147))
			colors = region.getcolors(1)
			if colors[0][1] !=	(187, 115, 60, 255) and colors[0][1] != (186, 114, 60, 255) and colors[0][1] != (202, 123, 60, 255):
				region = im.crop((400, 144, 401, 145))
				colors = region.getcolors(1)
				if colors[0][1] ==  (187, 115, 60, 255) or colors[0][1] == (186, 114, 60, 255) or colors[0][1] == (202, 123, 60, 255):
					yOffset = -2
				else:
					for y in range(0, 256):
						region = im.crop((400, y, 401, y+1))
						colors = region.getcolors(1)
						if colors[0][1] == (187, 115, 60, 255) or colors[0][1] == (186, 114, 60, 255) or colors[0][1] == (202, 123, 60, 255) or colors[0][1] == (194, 136, 64, 255):
							yOffset = y-146
							break
				
			layers = 1
			shop = 0
			post = 0
			fountain = 0
			housesOkay = True
			for building in buildings:
				lowestdiff = 100
				bestmatch = 0
				for mapsquare in building.acmap.squares:
					region = im.crop((mapsquare.coordinates[0], mapsquare.coordinates[1]+yOffset, mapsquare.coordinates[0]+48, mapsquare.coordinates[1]+48+yOffset))
					diff = rms(region, building.img)
					#print(str(file)+" "+building.name+" "+mapsquare.name+" "+str(diff))
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
					print(str(file) + " " + building.name + " " + bestmatch.name)
			
			for square in cliffSquares:
				region = im.crop((square.coordinates[0], square.coordinates[1]+yOffset, square.coordinates[0]+8, square.coordinates[1]+16+yOffset))
				diff = rms(region, cliff)
				if diff < 20:
					layers += 1
					
			if layers == 2:
				twoLayers += 1
			elif layers == 3:
				threeLayers += 1
				
			cliffs = []
			houses = []
			columns = []
			rows = []
			ramps = []
			purpleHouses = []

			houses.append(fountain.name)
			columns.append(fountain.name[1:2])
			rows.append(fountain.name[0:1])

			for square in houseMap.squares:
				region = im.crop((square.coordinates[0], square.coordinates[1]+yOffset, square.coordinates[0]+50, square.coordinates[1]+50+yOffset))
				colors = region.getcolors(maxcolors=1000)
				for color in colors:
					#blue house = (90, 90, 225, 255)	purple house = (145, 70, 205, 255)	yellow house = (170, 115, 20, 255)
					if color[1] == (90, 90, 225, 255) or color[1] == (145, 70, 205, 255) or color[1] == (170, 115, 20, 255):
						houses.append(square.name)
						columns.append(square.name[1:2])
						rows.append(square.name[0:1])
					if color[1] == (145, 70, 205, 255):
						purpleHouses.append(square.name)

					#ramp
					if color[1] == (66, 189, 66, 255) and color[0] > 10:
							ramps.append(square.name)
					# ledge
					if color[1] == (146, 146, 146, 255) or color[1] == (148, 148, 148, 255):
						cliffs.append(square.name)

			if not ((shop.name == "a2" and post.name == "a4") or (shop.name == "a4" and post.name == "a2")):
				housesOkay = False
			elif "f" in rows:
				housesOkay = False
			elif ("e" in rows and ("1" in columns or "5" in columns)):
				housesOkay = False
			elif "1" in columns and "5" in columns:
				housesOkay = False
			elif "e1" in houses or "e5" in houses or rows.count("e") > 1:
				housesOkay = False
			elif ("1" in columns or "5" in columns or "3" in columns) and ("e4" in houses and "e2" in houses):
				housesOkay = False
			elif ("d1" in houses or "e2" in houses) and ("4" in columns or shop.name == "a4"):
				housesOkay = False
			elif ("d5" in houses or "e4" in houses) and ("2" in columns or shop.name == "a2"):
				housesOkay = False
			elif ("d2" in houses and "5" in columns) or ("d4" in houses and "1" in columns):
				housesOkay = False
			elif (shop.name == "a2" and "b2" not in houses) or (shop.name == "a4" and "b4" not in houses):
				housesOkay = False
			elif ("e" in rows and (("4" in columns and "1" in columns) or ("5" in columns and "2" in columns))):
				housesOkay = False
			elif ("e" in rows) and ((shop.name == "a2" and "4" in columns) or (shop.name == "a4" and "2" in columns)):
				housesOkay = False
			elif shop.name == "a2" and (columns.count("5") > (1 + houses.count("b5"))) and fountain.name != "c5":
				housesOkay = False
			elif shop.name == "a4" and (columns.count("1") > (1 + houses.count("b1"))) and fountain.name != "c1":
				housesOkay = False
			elif "c5" in purpleHouses and not ("c5" in ramps or "b5" in ramps) and columns.count("5") > 1:
				housesOkay = False
			elif "c1" in purpleHouses and not ("c1" in ramps or "b1" in ramps) and columns.count("1") > 1:
				housesOkay = False

			#check for ramps to get to fountain
			OK = False
			OK2 = False
			if housesOkay:
				for ramp in ramps:
					if ("1" not in fountain.name and "5" not in fountain.name) and (("1" in columns and "5" in columns) or ("e" in fountain.name) or (("d" in fountain.name or "3" in fountain.name) and (("2" in columns and "5" in columns) or ("1" in columns and "4" in columns)))):
						if (ord(ramp[1:2]) == ord(fountain.name[1:2])) and ord(ramp[0:1]) <  ord(fountain.name[0:1]):
							OK = True
					else:
						if (abs(ord(ramp[1:2]) - ord(fountain.name[1:2])) <= 1 and ord(ramp[0:1]) <  ord(fountain.name[0:1])):
							OK = True
					if columns.count("2") > 1 and "5" in columns and ("d" in fountain.name or fountain.name == "c5"):
						if (ord(ramp[1:2]) == ord(fountain.name[1:2])) and ord(ramp[0:1]) <  ord(fountain.name[0:1]):
							OK2 = True
					elif columns.count("4") > 1 and "1" in columns and ("d" in fountain.name or fountain.name == "c1"):
						if (ord(ramp[1:2]) == ord(fountain.name[1:2])) and ord(ramp[0:1]) <  ord(fountain.name[0:1]):
							OK2 = True
					else:
						OK2 = True
				if not (OK and OK2):
					housesOkay = False

			#check for ramps to get to houses in d3. d2/d4 houses will always hit this condition.
			if housesOkay:
				for house in purpleHouses:
					OK = False
					OK2 = False
					#ord(ramp[0:1]) <=  ord(house[0:1]) can pick up ramp to third layer for 3 layer towns, but fuck it
					for ramp in ramps:
						if ("1" not in house and "5" not in house) and (("1" in columns and "5" in columns) or ("e" in house) or ("3" in fountain.name and (("2" in columns and "5" in columns) or ("1" in columns and "4" in columns)))):
							if (ord(ramp[1:2]) == ord(house[1:2])) and ord(ramp[0:1]) <=  ord(house[0:1]):
								OK = True
						else:
							if (abs(ord(ramp[1:2]) - ord(house[1:2])) <= 1 and ord(ramp[0:1]) <=  ord(house[0:1])):
								OK = True
						if columns.count("2") > 1 and "5" in columns and ("d" in house or house == "c5"):
							if (ord(ramp[1:2]) == ord(house[1:2])) and ord(ramp[0:1]) <=  ord(house[0:1]):
								OK2 = True
						elif columns.count("4") > 1 and "1" in columns and ("d" in house or house == "c1"):
							if (ord(ramp[1:2]) == ord(house[1:2])) and ord(ramp[0:1]) <=  ord(house[0:1]):
								OK2 = True
						else:
							OK2 = True
					if not (OK and OK2):
						housesOkay = False


			if housesOkay:
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
