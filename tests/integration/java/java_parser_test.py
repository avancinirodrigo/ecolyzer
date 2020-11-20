from ecolyzer.parser import JavaParser
import os

def test_extract_operations():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'FileSerializer.java')
	src = open(javafile).read()
	parser = JavaParser()
	parser.parser(src)
	operations = parser.extract_operations()[0]['operations']

	src_operations = {
		'extends.FileSerializer': True,	
		'FileSerializer': True,
		'FileSerializer.getPostProcessor': True,
		'FileSerializer.setPostProcessor': True,
		'FileSerializer.generateFile': True,
		'FileSerializer.getPropertiesList': True,
		'FileSerializer.formatValue': True,
		'FileSerializer.isAllowedGetter': True,
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
		'extends.JFreeChart': True,
		'JFreeChart': True,
		'JFreeChart.isCompatibleValue': True,
		'JFreeChart.getRenderingHints': True,
		'JFreeChart.setRenderingHints': True,
		'JFreeChart.isBorderVisible': True,
		'JFreeChart.setBorderVisible': True,
		'JFreeChart.getBorderStroke': True,
		'JFreeChart.setBorderStroke': True,
		'JFreeChart.getBorderPaint': True,
		'JFreeChart.setBorderPaint': True,
		'JFreeChart.getPadding': True,
		'JFreeChart.setPadding': True,
		'JFreeChart.getTitle': True,
		'JFreeChart.setTitle': True,
		'JFreeChart.addLegend': True,
		'JFreeChart.getLegend': True,
		'JFreeChart.removeLegend': True,
		'JFreeChart.setSubtitles': True,
		'JFreeChart.getSubtitles': True,
		'JFreeChart.getSubtitleCount': True,
		'JFreeChart.getSubtitle': True,
		'JFreeChart.addSubtitle': True,
		'JFreeChart.clearSubtitles': True,
		'JFreeChart.removeSubtitle': True,
		'JFreeChart.getPlot': True,
		'JFreeChart.getCategoryPlot': True,
		'JFreeChart.getXYPlot': True,
		'JFreeChart.getAntiAlias': True,
		'JFreeChart.setAntiAlias': True,
		'JFreeChart.getTextAntiAlias': True,
		'JFreeChart.setTextAntiAlias': True,
		'JFreeChart.getBackgroundPaint': True,
		'JFreeChart.setBackgroundPaint': True,
		'JFreeChart.getBackgroundImage': True,
		'JFreeChart.setBackgroundImage': True,
		'JFreeChart.getBackgroundImageAlignment': True,
		'JFreeChart.setBackgroundImageAlignment': True,
		'JFreeChart.getBackgroundImageAlpha': True,
		'JFreeChart.setBackgroundImageAlpha': True,
		'JFreeChart.isNotify': True,
		'JFreeChart.setNotify': True,
		'JFreeChart.draw': True,
		'JFreeChart.createAlignedRectangle2D': True,
		'JFreeChart.drawTitle': True,
		'JFreeChart.createBufferedImage': True,
		'JFreeChart.handleClick': True,
		'JFreeChart.addChangeListener': True,
		'JFreeChart.removeChangeListener': True,
		'JFreeChart.fireChartChanged': True,
		'JFreeChart.notifyListeners': True,
		'JFreeChart.addProgressListener': True,
		'JFreeChart.removeProgressListener': True,
		'JFreeChart.notifyListeners': True,
		'JFreeChart.titleChanged': True,
		'JFreeChart.plotChanged': True,
		'JFreeChart.equals': True,
		'JFreeChart.writeObject': True,
		'JFreeChart.readObject': True,
		'JFreeChart.main': True,
		'JFreeChart.clone': True,
	}

	assert len(operations) == 72 == len(src_operations) + 12 

	for op in operations:
		assert src_operations[op['name']]		
		#print(f'\'{op["name"]}\': True,')

	operations = classes[1]['operations']	
	src_operations = {
		'extends.JFreeChartInfo': True,
		'JFreeChartInfo': True,
		'JFreeChartInfo.getLogo': True
	}
	
	assert len(operations) == 3 == len(src_operations)

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
		'DataFormatter.formatData': True,
		'FileSerializer.getPropertiesList': True,
		'PostProcessor.postProcess': True,
		'FileOutputStream.write': True,
		'FileOutputStream.close': True,
		'HashMap': True,		
		'Object.getClass': True,
		'Class.getMethods': True,
		'FileSerializer.isAllowedGetter': True,
		'Method.invoke': True,
		'Method.getName': True,
		'Method.getName': True,
		'Method.getName': True,
		'String.substring': True,
		'String.substring': True,
		#'toLowerCase': True, # method chaining doesn't work
		'ValueFormatter.formatValue': True,
		'FileSerializer.formatValue': True,
		'Map.put': True,
		'Method.getAnnotations': True,
		'Annotation.annotationType': True,
		'Class.isAnnotationPresent': True,
		'Class.getAnnotation': True,
		'FormatterImplementation.value': True,
		'Class.newInstance': True,
		'ValueFormatter.readAnnotation': True,
		#'startsWith': True, # method chaining doesn't work
		'Method.getParameterTypes': True,
		'Method.getReturnType': True,
		'Method.isAnnotationPresent': True,
		# 'equals': True, # method chaining doesn't work
		'Override': True, #TODO: Annotation call
		'Override': True,
		'implements.Serializer': True,
		'FileOutputStream': True,
		'RuntimeException': True,
		'RuntimeException': True,
		'InstantiationException': True,
		'IllegalAccessException': True,
	}

	for call in calls:
		assert src_calls[call]
		# print(f'\'{call}\': True,')

	assert len(calls) == 36 == len(src_calls) + 5 # 5 repeated calls	

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