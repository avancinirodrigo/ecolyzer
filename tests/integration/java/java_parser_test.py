from ecolyzer.parser import JavaParser
import os

def test_extract_operations():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'FileSerializer.java')
	src = open(javafile).read()
	parser = JavaParser()
	parser.parser(src)
	operations = parser.extract_operations()[0]['operations']

	src_operations = {
		'FileSerializer': True,
		'getPostProcessor': True,
		'setPostProcessor': True,
		'generateFile': True,
		'getPropertiesList': True,
		'formatValue': True,
		'isAllowedGetter': True,
	}

	assert len(operations) == len(src_operations)

	for op in operations:
		assert src_operations[op['name']]

def test_internal_class_operations():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'JFreeChartJFreeChartInfo.java')
	src = open(javafile).read()
	parser = JavaParser()
	parser.parser(src)
	classes = parser.extract_operations()

	assert len(classes) == 2

	operations = classes[0]['operations']
	src_operations = {
		'JFreeChart': True,
		'isCompatibleValue': True,
		'getRenderingHints': True,
		'setRenderingHints': True,
		'isBorderVisible': True,
		'setBorderVisible': True,
		'getBorderStroke': True,
		'setBorderStroke': True,
		'getBorderPaint': True,
		'setBorderPaint': True,
		'getPadding': True,
		'setPadding': True,
		'getTitle': True,
		'setTitle': True,
		'addLegend': True,
		'getLegend': True,
		'removeLegend': True,
		'setSubtitles': True,
		'getSubtitles': True,
		'getSubtitleCount': True,
		'getSubtitle': True,
		'addSubtitle': True,
		'clearSubtitles': True,
		'removeSubtitle': True,
		'getPlot': True,
		'getCategoryPlot': True,
		'getXYPlot': True,
		'getAntiAlias': True,
		'setAntiAlias': True,
		'getTextAntiAlias': True,
		'setTextAntiAlias': True,
		'getBackgroundPaint': True,
		'setBackgroundPaint': True,
		'getBackgroundImage': True,
		'setBackgroundImage': True,
		'getBackgroundImageAlignment': True,
		'setBackgroundImageAlignment': True,
		'getBackgroundImageAlpha': True,
		'setBackgroundImageAlpha': True,
		'isNotify': True,
		'setNotify': True,
		'draw': True,
		'createAlignedRectangle2D': True,
		'drawTitle': True,
		'createBufferedImage': True,
		'handleClick': True,
		'addChangeListener': True,
		'removeChangeListener': True,
		'fireChartChanged': True,
		'notifyListeners': True,
		'addProgressListener': True,
		'removeProgressListener': True,
		'notifyListeners': True,
		'titleChanged': True,
		'plotChanged': True,
		'equals': True,
		'writeObject': True,
		'readObject': True,
		'main': True,
		'clone': True,
	}

	assert len(operations) == 71 == len(src_operations) + 12 

	for op in operations:
		assert src_operations[op['name']]		
		#print(f'\'{op["name"]}\': True,')

	operations = classes[1]['operations']	
	src_operations = {
		'JFreeChartInfo': True,
		'getLogo': True
	}
	
	assert len(operations) == 2 == len(src_operations)

	for op in operations:
		assert src_operations[op['name']]		
		# print(f'\'{op["name"]}\': True,')	

def test_extract_calls():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'FileSerializer.java')
	src = open(javafile).read()
	parser = JavaParser()
	parser.parser(src)
	calls = parser.extract_calls()

	src_calls = {
		'formatData': True,
		'getPropertiesList': True,
		'postProcess': True,
		'write': True,
		'close': True,
		'getClass': True,
		'getMethods': True,
		'isAllowedGetter': True,
		'invoke': True,
		'getName': True,
		'substring': True,
		'toLowerCase': True,
		'formatValue': True,
		'put': True,
		'getAnnotations': True,
		'annotationType': True,
		'isAnnotationPresent': True,
		'getAnnotation': True,
		'value': True,
		'newInstance': True,
		'readAnnotation': True,
		'startsWith': True,
		'getParameterTypes': True,
		'getReturnType': True,
		'equals': True,
		'Override': True #TODO: Annotation call
	}

	assert len(calls) == len(src_calls) + 6 # six repeated

	for call in calls:
		assert src_calls[call]

def test_extract_associations():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'FileSerializer.java')
	src = open(javafile).read()
	parser = JavaParser()
	parser.parser(src)
	assocs = parser.extract_associations()

	src_assocs = {
		'java/io/FileOutputStream': True,
		'java/lang/annotation/Annotation': True,
		'java/lang/reflect/InvocationTargetException': True,
		'java/lang/reflect/Method': True,
		'java/util/HashMap': True,
		'java/util/Map': True
	}

	assert len(src_assocs) == len(assocs)

	for assoc in assocs:
		assert src_assocs[assoc]		
		#print('\'' + assoc + '\': ' + 'True,')