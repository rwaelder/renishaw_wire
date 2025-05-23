import sys, os, struct
import numpy as np
import pandas as pd

def wdf_deconstruct(filename, unpackFiles=False):

	try:
		fileStream = open(filename, mode='rb')

	except FileNotFoundError as error:
		raise
		sys.exit()

	blockInfo = {}
	finished = False
	while not finished:
		blockName, blockSize = get_block_ID(fileStream)
		print('%s : %i' % (blockName, blockSize))


		if blockName == 'WDF1':
			blockInfo[blockName] = read_WDF1_block(fileStream)
		elif blockName == 'DATA':
			blockInfo[blockName] = read_DATA_block(fileStream)
		elif blockName == 'XLST':
			blockInfo[blockName] = read_LST_block(fileStream)
		elif blockName == 'YLST':
			blockInfo[blockName] = read_LST_block(fileStream)
		elif blockName == 'WMAP':
			blockInfo[blockName] = read_WMAP_block(fileStream)
		elif blockName == 'TEXT':
			blockInfo[blockName] = read_TEXT_block(fileStream)
		elif blockName == 'ORGN':
			blockInfo[blockName] = read_ORGN_block(fileStream)
		elif blockName == 'WCHK':
			finished = True
		elif blockName == '':
			finished = True
		else:
			blockInfo[blockName] = read_OTHER_block(fileStream)
			# fileStream.seek(blockSize, 1) # move past current block

		# if blockSize == 0:
		# 	finished = True

	if unpackFiles:
		foldername = filename[:-4]

		try:
			os.chdir(foldername)
		except FileNotFoundError: 
			os.mkdir(foldername)
			os.chdir(foldername)
		

		with open('data.csv', 'w') as f:
			data = blockInfo['DATA']
			xlst = blockInfo['XLST']

			if len(data) == len(xlst):
				for i in range(len(data)):
					f.write('%f, %f\n' % (xlst[i], data[i]))

			else:
				pass 

		blockInfo.pop('DATA', None)
		blockInfo.pop('XLST', None)

		for block in blockInfo:
			try:
				binoutfile = block + '.bin'
				with open(binoutfile, 'wb') as f:
					f.write(blockInfo[block])

			except TypeError:
				os.remove(binoutfile)
				txtoutfile = block + '.txt'
				with open(txtoutfile, 'w') as f:
					f.write(str(blockInfo[block]))



	

def bin_read(fileStream, byteFormat, debug=False):
	if byteFormat == 'char':
		byteFormat = '<c'
		size = 1
	elif byteFormat == 'uint8':
		byteFormat = '<B'
		size = 1
	elif byteFormat == 'uint32':
		byteFormat = '<I'
		size = 4
	elif byteFormat == 'uint64':
		byteFormat = '<Q'
		size = 8
	elif byteFormat == 'float':
		byteFormat = '<f'
		size = 4
	elif byteFormat == 'double':
		byteFormat = '<d'
		size = 8
	else:
		print('Byte format not currently supported: %s' % byteFormat)
		sys.exit()

	value = struct.unpack(byteFormat, fileStream.read(size))

	if len(value) == 1:
		value = value[0]

	if debug:
		print(value)
	
	return value	

def get_block_ID(fileStream):

	try:
		blockStart = fileStream.tell()
		blockName = fileStream.read(4).decode('ascii')
		unknown = bin_read(fileStream, 'uint32')
		blockSize = bin_read(fileStream, 'uint32')
		fileStream.seek(blockStart, 0)

		return blockName, blockSize
	except:
		return '', 0

def skip_rest_of_block(fileStream, blockStart, blockSize):
	position = fileStream.tell()
	remainingBytes = (blockStart + blockSize) - position
	fileStream.seek(remainingBlocks, 1)


def read_rest_of_block(fileStream, blockStart, blockSize):
	position = fileStream.tell()
	remainingBytes = (blockStart + blockSize) - position
	remainingContents = fileStream.read(remainingBytes)

	return remainingContents

def try_rest_of_block(fileStream, byteFormat, blockStart, blockSize, debug=True):
	endPosition = blockStart + blockSize

	while fileStream.tell() < endPosition:
		attemptedTranslation = bin_read(fileStream, byteFormat)
		if debug:
			print(attemptedTranslation)

def read_WDF1_block(fileStream):
	blockStart = fileStream.tell()
	blockName = fileStream.read(4).decode('ascii')

	unknown = bin_read(fileStream, 'uint32')
	blockSize = bin_read(fileStream, 'uint32')
	unknown = bin_read(fileStream, 'uint32')

	# while fileStream.tell() < blockStart + blockSize:
	# 	unknown = bin_read(fileStream, 'char', debug=True)

	blockContents = read_rest_of_block(fileStream, blockStart, blockSize)

	return blockContents

def read_DATA_block(fileStream):
	blockStart = fileStream.tell()
	blockName = fileStream.read(4).decode('ascii')

	unknown = bin_read(fileStream, 'uint32')
	blockSize = bin_read(fileStream, 'uint32')
	unknown = bin_read(fileStream, 'uint32')

	dataStart = fileStream.tell()
	dataEnd = blockStart + blockSize
	dataSize = dataEnd - dataStart

	numPoints = dataSize // 4

	data = []
	for i in range(numPoints):

		data.append(bin_read(fileStream, 'float'))

	return data

def read_LST_block(fileStream):
	blockStart = fileStream.tell()
	blockName = fileStream.read(4).decode('ascii')

	unknown = bin_read(fileStream, 'uint32')
	blockSize = bin_read(fileStream, 'uint32')
	unknown = bin_read(fileStream, 'uint32')
	unknown = bin_read(fileStream, 'uint32')
	unknown = bin_read(fileStream, 'uint32')

	dataStart = fileStream.tell()
	dataEnd = blockStart + blockSize
	dataSize = dataEnd - dataStart

	numPoints = dataSize // 4

	data = []
	for i in range(numPoints):

		data.append(bin_read(fileStream, 'float'))

	return data

def read_WMAP_block(fileStream):
	blockStart = fileStream.tell()
	blockName = fileStream.read(4).decode('ascii')

	unknown1 = bin_read(fileStream, 'uint32')
	blockSize = bin_read(fileStream, 'uint32')
	unknown2 = bin_read(fileStream, 'uint32')
	unknown3 = bin_read(fileStream, 'uint32')
	unknown4 = bin_read(fileStream, 'uint32')

	xStart = bin_read(fileStream, 'float')
	yStart = bin_read(fileStream, 'float')

	unknown5 = bin_read(fileStream, 'float')

	xPad = bin_read(fileStream, 'float')
	yPad = bin_read(fileStream, 'float')

	unknown6 = bin_read(fileStream, 'float')

	height = bin_read(fileStream, 'uint32')
	width = bin_read(fileStream, 'uint32')

	unknown7 = bin_read(fileStream, 'uint32')
	unknown8 = bin_read(fileStream, 'uint32')

	mapInfo = {}
	mapInfo['xStart'] = xStart
	mapInfo['yStart'] = yStart
	mapInfo['xPad'] = xPad
	mapInfo['yPad'] = yPad
	mapInfo['height'] = height
	mapInfo['width'] = width

	return mapInfo

def read_TEXT_block(fileStream):
	blockStart = fileStream.tell()
	blockName = fileStream.read(4).decode('ascii')

	unknown = bin_read(fileStream, 'uint32')
	blockSize = bin_read(fileStream, 'uint32')
	unknown = bin_read(fileStream, 'uint32')

	dataStart = fileStream.tell()
	dataEnd = blockStart + blockSize
	dataSize = dataEnd - dataStart
	text = fileStream.read(dataSize).decode('ascii')

	return text

def read_ORGN_block(fileStream, debug=True):
	blockStart = fileStream.tell()
	blockName = fileStream.read(4).decode('ascii')
	unknown = bin_read(fileStream, 'uint32')
	blockSize = bin_read(fileStream, 'uint32')
	dataStart = fileStream.tell()

	try_rest_of_block(fileStream, 'float', blockStart, blockSize, debug=debug)



def read_OTHER_block(fileStream):
	blockStart = fileStream.tell()
	blockName = fileStream.read(4).decode('ascii')

	unknown = bin_read(fileStream, 'uint32')
	blockSize = bin_read(fileStream, 'uint32')
	unknown = bin_read(fileStream, 'uint32')

	remainingContents = read_rest_of_block(fileStream, blockStart, blockSize)

	return remainingContents


def wire_read(filename, as_numpy=False, as_pandas=False, map_data=False, verbose=False):
	assert as_numpy != as_pandas or as_numpy == as_pandas == False, 'cannot return multiple types'
	assert map_data == False, 'maps currently not supported. sorry'

	try:
		fileStream = open(filename, mode='rb')

	except FileNotFoundError as error:
		raise
		sys.exit()

	blockInfo = {}
	finished = False
	while not finished:
		blockName, blockSize = get_block_ID(fileStream)
		if verbose:
			print('%s : %i' % (blockName, blockSize))


		if blockName == 'WDF1':
			blockInfo[blockName] = read_WDF1_block(fileStream)
		elif blockName == 'DATA':
			blockInfo[blockName] = read_DATA_block(fileStream)
		elif blockName == 'XLST':
			blockInfo[blockName] = read_LST_block(fileStream)
		elif blockName == 'YLST':
			blockInfo[blockName] = read_LST_block(fileStream)
		elif blockName == 'WMAP':
			blockInfo[blockName] = read_WMAP_block(fileStream)
		elif blockName == 'TEXT':
			blockInfo[blockName] = read_TEXT_block(fileStream)
		elif blockName == 'ORGN':
			blockInfo[blockName] = read_ORGN_block(fileStream, debug=False)
		elif blockName == 'WCHK':
			finished = True
		elif blockName == '':
			finished = True
		else:
			blockInfo[blockName] = read_OTHER_block(fileStream)
			# fileStream.seek(blockSize, 1) # move past current block

		# if blockSize == 0:
		# 	finished = True

	blockInfo['XLST'].reverse()
	blockInfo['DATA'].reverse()

	if as_numpy:
		return np.asarray(blockInfo['XLST']), np.asarray(blockInfo['DATA'])
	elif as_pandas:
		frame = pd.DataFrame()
		frame['XLST'] = blockInfo['XLST']
		frame['DATA'] = blockInfo['DATA']
		return frame
	else:
		return blockInfo['XLST'], blockInfo['DATA']	

if __name__ == '__main__':
	try:
		filename = sys.argv[1]
	except:
		filename = input('Specify WDF file: ').rstrip()
		if '.wdf' not in filename:
			filename += '.wdf'

	wdf_deconstruct(filename, unpackFiles=True)
