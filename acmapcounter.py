from PIL import Image, ImageChops
import sys, math, operator, functools, os

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
		self.f1 = MapSquare("f1", [409, 441])
		self.f2 = MapSquare("f2", [464, 441])
		self.f3 = MapSquare("f3", [519, 441])
		self.f4 = MapSquare("f4", [574, 441])
		self.squares = [self.f1, self.f2, self.f3, self.f4]
	
class Map(object):
	def __init__(self):
		self.c1 = MapSquare("c1", [411, 275])
		self.c2 = MapSquare("c2", [466, 275])
		self.c3 = MapSquare("c3", [520, 275])
		self.c4 = MapSquare("c4", [575, 275])
		self.c5 = MapSquare("c5", [629, 275])
		
		self.d1 = MapSquare("d1", [411, 331])
		self.d2 = MapSquare("d2", [466, 331])
		self.d3 = MapSquare("d3", [520, 331])
		self.d4 = MapSquare("d4", [575, 331])
		self.d5 = MapSquare("d5", [629, 331])
		
		self.e1 = MapSquare("e1", [411, 387])
		self.e2 = MapSquare("e2", [466, 387])
		self.e3 = MapSquare("e3", [520, 387])
		self.e4 = MapSquare("e4", [575, 387])
		self.e5 = MapSquare("e5", [629, 387])
		
		self.squares = [self.c1, self.c2, self.c3, self.c4, self.c5, self.d1, self.d2, self.d3, self.d4, self.d5, self.e1, self.e2, self.e3, self.e4, self.e5]
	

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

def main():
	fileCount = 0
	directory = "."
	if sys.argv[1]:
		directory = sys.argv[1]
	for file in os.listdir(directory):
		if file.endswith(".png"):
			fileCount += 1
			im = Image.open(directory+file)
			for building in buildings:
				lowestdiff = 100
				bestmatch = 0
				for mapsquare in building.acmap.squares:
					region = im.crop((mapsquare.coordinates[0], mapsquare.coordinates[1], mapsquare.coordinates[0]+50, mapsquare.coordinates[1]+50))
					diff = rms(region, building.img)
					if(diff < lowestdiff):
						lowestdiff = diff
						bestmatch = mapsquare
							
				bestmatch.count += 1
				building.count += 1
					
	for building in buildings:
		print(str(building.name))
		for mapsquare in building.acmap.squares:
					print("\t"+str(mapsquare.name)+":\t"+str(mapsquare.count)+"\t"+str((mapsquare.count/building.count)*100)+"%")	
	print("files: "+str(fileCount))
if __name__ == "__main__":
	main()
