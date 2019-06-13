# from PIL import Image
import numpy as np
import cv2
import argparse
# http://www.msarnoff.org/millitext/
# Black, Red, Green, Blue, White, Cyan, Yellow, Magenta
subpixels = {
	" ": "   ",
	"R": "█  ",
	"G": " █ ",
	"B": "  █",
	"W": "███",
	"C": " ██",
	"Y": "██ ",
	"M": "█ █"
}

# Pixel column for 1x5 characters
colour_encodings = {
	"0":"WMMMW",
	"1":"WGGGY",
	"2":"WRWBW",
	"3":"WBWBW",
	"4":"BBWMM",
	"5":"WBWRW",
	"6":"WMWRW",
	"7":"BBBMW",
	"8":"WMWMW",
	"9":"WBWMW",
	"A":"MMWMW",
	"B":"YMYMY",
	"C":"WRRRW",
	"D":"YMMMY",
	"E":"WRWRW",
	"F":"RRWRW",
	"G":"WMMRW",
	"H":"MMWMM",
	"I":"WGGGW",
	"J":"WBBBB",
	"K":"MMYMM",
	"L":"WRRRR",
	"M":"MMWWM",
	"N":"MMMMY",
	"O":"GMMMG",
	"P":"RRYMY",
	"Q":"CWMMG",
	"R":"MMYMY",
	"S":"YBGRC",
	"T":"GGGGW",
	"U":"WMMMM",
	"V":"BCMMM",
	"W":"MWWMM",
	"X":"MMGMM",
	"Y":"GGGMM",
	"Z":"WRGBW",
	" ":"     ",
}

# Pixel columns for 2x5 characters
colour_encodings_2 = {
	"0": ["CYMRC","RGGYR"],
	"1": ["CBBCB","R    "],
	"2": ["WRC W","Y RGR"],
	"3": ["W C W","RGRGR"],
	"4": ["  WRR","RRYRR"],
	"5": ["W WRW","RGR Y"],
	"6": ["CRWRC","RGR R"],
	"7": ["BB  W","  RGY"],
	"8": ["CRCRC","RGRGR"],
	"9": ["C CRC","RGYGR"],
	"A": ["RRWRC","GGYGR"],
	"B": ["WRWRW","RGRGR"],
	"C": ["CRRRC","Y   Y"],
	"D": ["WRRRW","RGGGR"],
	"E": ["WRWRW","Y R Y"],
	"F": ["RRWRW","  R Y"],
	"G": ["CRMRC","YGY Y"],
	"H": ["RRWRR","GGYGG"],
	"I": ["CBBBC","R   R"],
	"J": ["CR   ","RGGGG"],
	"K": ["RRWRR","GR RG"],
	"L": ["WRRRR","Y    "],
	"M": ["RRMYR","GGGYG"],
	"N": ["RRMYR","GYGGG"],
	"O": ["CRRRC","RGGGR"],
	"P": ["RRWRW","  RGR"],
	"Q": ["CRRRC","GRGGR"],
	"R": ["RRWRW","GGRGR"],
	"S": ["W CRC","RGR Y"],
	"T": ["BBBBW","    Y"],
	"U": ["CRRRR","RGGGG"],
	"V": ["BGRRR"," RGGG"],
	"W": ["RYMRR","GYGGG"],
	"X": ["RGBGR","GR RG"],
	"Y": ["BBBGR","   RG"],
	"Z": ["WGB W","Y  RY"],
	" ": ["     ","     "],
}

def subpixel_view(encoded, space=False):
	# Given an image parsed into text, print each subpixel as on or off
	for line in encoded.split("\n"):
		for char in line:
			spacer=''
			if(space):spacer=' '
			print(subpixels[char], end=spacer)
		print("")

def parse_image(filename):
	# im = Image.open(filename)
	im = cv2.imread(filename)
	# arr = np.array(im,dtype="int32")
	out = []
	for x in range(0, im.shape[0]):
		linetext=""
		for y in range(0, im.shape[1]):
			pixel=im[x, y]
			linetext=linetext + parse_pixel(pixel)
		out.append(linetext)
	# print("\n".join(out))
	return "\n".join(out)

def parse_pixel(BGR):
	r=BGR[2]
	g=BGR[1]
	b=BGR[0]
	if(r>1):r=1
	if(g>1):g=1
	if(b>1):b=1
	if(r==g and g==b):
		if(r==0):
			return " "
		else:
			return "W"
	elif(r==g and r!=0):
		return "Y"
	elif(g==b and g!=0):
		return "C"
	elif(r==b and r!=0):
		return "M"
	elif(r==0 and g==0 and b!=0):
		return "B"
	elif(r==0 and g!=0 and b==0):
		return "G"
	elif(r!=0 and g==0 and b==0):
		return "R"
	return " "

def output_image(encoded,filename="out.png"):
	arr=list((list(x) for x in encoded.split("\n")))
	imgarr = []
	for y in arr:
		line=[]
		for x in y:
			line.append(output_pixel(x))
		imgarr.append(line)
	imgarr = np.array(imgarr)
	imgarr = cv2.convertScaleAbs(imgarr)
	cv2.imwrite(filename,imgarr)
	# cv2.destroyAllWindows()

def output_pixel(char):
	# RETURNS BGR
	out=[0,0,0]
	if char==' ':
		out=[0,0,0]
	elif char=='W':
		out=[255,255,255]
	elif char=='Y':
		out=[255,255,0]
	elif char=='C':
		out=[0,255,255]
	elif char=='M':
		out=[255,0,255]
	elif char=='B':
		out=[0,0,255]
	elif char=='G':
		out=[0,255,0]
	elif char=='R':
		out=[255,0,0]
	return out[::-1]

def encode_to_colors(string, width=1):
	arr = [];
	for char in string:
		if(width==1):
			arr.append(list(colour_encodings[char.upper()]))
			arr.append(list(colour_encodings[" "]))
		if(width==2):
			arr.append(list(colour_encodings_2[char.upper()][0]))
			arr.append(list(colour_encodings_2[char.upper()][1]))
	if(width==1):del arr[-1]
	arr = np.array(arr)
	arr = np.rot90(arr)
	strout=""
	for y in arr:
		strout=strout+"".join(y)+"\n"
	# print(strout.strip())
	return strout.strip()

def main():
	parser=argparse.ArgumentParser(description='Encode or Decode millitext.')
	parser.add_argument('-i', '--image')
	parser.add_argument('-s', '--string')
	parser.add_argument('-o', '--out', '--output')
	parser.add_argument('-w', '--width', default=2, type=int)
	parser.add_argument('-e', '--encode')
	parser.add_argument('-d', '--decode')
	args = vars(parser.parse_args())
	# print(args)
	if(args["out"] and args["string"]):
		print("TEST")
		output_image(encode_to_colors(args["string"], width=args["width"]), filename=args["out"])
	elif(args["image"]):
		subpixel_view(parse_image(args["image"]))
	elif(args["encode"]):
		print(encode_to_colors(args["encode"], width=args["width"]))
	elif(args["decode"]):
		subpixel_view(args["decode"])

if __name__ == "__main__":
    main()