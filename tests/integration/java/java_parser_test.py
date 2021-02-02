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
		'FileSerializer.pp': True,
		'FileSerializer.df': True,
		'FileSerializer.FileSerializer': True,
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
		#print(f'\'{op["name"]}\': True,')

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
		'JFreeChart.serialVersionUID': True,
		'JFreeChart.INFO': True,
		'JFreeChart.DEFAULT_TITLE_FONT': True,
		'JFreeChart.DEFAULT_BACKGROUND_PAINT': True,
		'JFreeChart.DEFAULT_BACKGROUND_IMAGE': True,
		'JFreeChart.DEFAULT_BACKGROUND_IMAGE_ALIGNMENT': True,
		'JFreeChart.DEFAULT_BACKGROUND_IMAGE_ALPHA': True,
		'JFreeChart.KEY_SUPPRESS_SHADOW_GENERATION': True,
		'JFreeChart.isCompatibleValue': True,
		'JFreeChart.renderingHints': True,
		'JFreeChart.borderVisible': True,
		'JFreeChart.borderStroke': True,
		'JFreeChart.borderPaint': True,
		'JFreeChart.padding': True,
		'JFreeChart.title': True,
		'JFreeChart.subtitles': True,
		'JFreeChart.plot': True,
		'JFreeChart.backgroundPaint': True,
		'JFreeChart.backgroundImage': True,
		'JFreeChart.backgroundImageAlignment': True,
		'JFreeChart.backgroundImageAlpha': True,
		'JFreeChart.changeListeners': True,
		'JFreeChart.progressListeners': True,
		'JFreeChart.notify': True,
		'JFreeChart.JFreeChart': True,
		'JFreeChart.JFreeChart': True,
		'JFreeChart.JFreeChart': True,
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
		'JFreeChart.setTitle': True,
		'JFreeChart.addLegend': True,
		'JFreeChart.getLegend': True,
		'JFreeChart.getLegend': True,
		'JFreeChart.removeLegend': True,
		'JFreeChart.getSubtitles': True,
		'JFreeChart.setSubtitles': True,
		'JFreeChart.getSubtitleCount': True,
		'JFreeChart.getSubtitle': True,
		'JFreeChart.addSubtitle': True,
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
		'JFreeChart.draw': True,
		'JFreeChart.draw': True,
		'JFreeChart.createAlignedRectangle2D': True,
		'JFreeChart.drawTitle': True,
		'JFreeChart.createBufferedImage': True,
		'JFreeChart.createBufferedImage': True,
		'JFreeChart.createBufferedImage': True,
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

	assert len(operations) == 95 == len(src_operations) + 12 

	for op in operations:
		assert src_operations[op['name']]		
		#print(f'\'{op["name"]}\': True,')

	operations = classes[1]['operations']	
	src_operations = {
		'extends.JFreeChartInfo': True,
		'JFreeChartInfo.JFreeChartInfo': True,
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
		'DataFormatter.formatData': {'caller': 'df'},
		'FileSerializer.getPropertiesList': {'caller': ''},
		'PostProcessor.postProcess': {'caller': 'pp'},
		'FileOutputStream.FileOutputStream': {'caller': 'new'},
		'FileOutputStream.write': {'caller': 'fileout'},
		'FileOutputStream.close': {'caller': 'fileout'},
		'RuntimeException.RuntimeException': {'caller': 'new'},
		'HashMap.HashMap': {'caller': 'new'},
		'Object.getClass': {'caller': 'obj'},
		'Class.getMethods': {'caller': 'clas'},
		'FileSerializer.isAllowedGetter': {'caller': ''},
		'Method.invoke': {'caller': 'm'},
		'Method.getName': {'caller': 'm'},
		'String.substring': {'caller': 'getterName'},
		'String.substring': {'caller': 'getterName'},
		'FileSerializer.formatValue': {'caller': ''},
		'Map.put': {'caller': 'props'},
		'RuntimeException.RuntimeException': {'caller': 'new'},
		'InstantiationException.InstantiationException': {'caller': 'throws'},
		'IllegalAccessException.IllegalAccessException': {'caller': 'throws'},
		'Method.getAnnotations': {'caller': 'm'},
		'Annotation.annotationType': {'caller': 'an'},
		'Class.isAnnotationPresent': {'caller': 'anType'},
		'Class.getAnnotation': {'caller': 'anType'},
		'FormatterImplementation.value': {'caller': 'fi'},
		'Class.newInstance': {'caller': 'c'},
		'ValueFormatter.readAnnotation': {'caller': 'vf'},
		'ValueFormatter.formatValue': {'caller': 'vf'},
		'Method.getName': {'caller': 'm'},
		'Method.getParameterTypes': {'caller': 'm'},
		'Method.getReturnType': {'caller': 'm'},
		'Method.getName': {'caller': 'm'},
		'Method.isAnnotationPresent': {'caller': 'm'},
		'Override.@': {'caller': '@'},
		'Override.@': {'caller': '@'},
		'implements.Serializer': {'caller': 'implements'},
		# 'toLowerCase': True, # method chaining doesn't work
		# 'startsWith': True, # method chaining doesn't work
		# 'equals': True, # method chaining doesn't work
	}

	for call in calls:
		assert src_calls[call['ref']]
		assert src_calls[call['ref']]['caller'] is not None
		# print(f'\'{call["ref"]}\': {{\'caller\': \'{call["caller"]}\'}},')

	assert len(calls) == 36 == len(src_calls) + 5  # repeated calls	


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
		# print('\'' + assoc + '\': ' + 'True,')


def test_extract_inner_class_creator():  # TODO: review inner class declarations and how they work
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'InspectInvitationsPage.java')
	src = open(javafile).read()
	parser = JavaParser()
	parser.parser(src)
	class_operations = parser.extract_operations()
	calls = parser.extract_calls()		

	expected_operations = {
		'InspectInvitationsPage.extends.InspectInvitationsPage': True,
		'InspectInvitationsPage.InspectInvitationsPage.getTable': True,
		'InspectInvitationsPage.InspectInvitationsPage.getFooter': True,
		'InspectInvitationsPage.InspectInvitationsPage.getStatusAndMemo': True,
		'InspectInvitationsPage.InspectInvitationsPage.getMessageWhere': True,
		'InspectInvitationsPage.InspectInvitationsPage.clickMessageHistory': True,
		'InspectInvitationsPage.InspectInvitationsPage.getMessage': True,
		'InspectInvitationsPage.InspectInvitationsPage.notSpam': True,
		'InspectInvitationsPage.InspectInvitationsPage.cancel': True,
		'InspectInvitationsPage.InspectInvitationsPage.getStatusAndMemo': True,
		'InspectInvitationsPage.InspectInvitationsPage.clickMessageHistory': True,
		'InspectInvitationsPage.InspectInvitationsPage.getMessageWhere': True,
		'InspectInvitationsPage.InspectInvitationsPage.getMessage': True,
		'InspectInvitationsPage.InspectInvitationsPage.clickMessageHistory': True,
		'InspectInvitationsPage.InspectInvitationsPage.cancel': True,
		'InspectInvitationsPage.InspectInvitationsPage.notSpam': True,
		'InspectInvitationsPage.InspectInvitationsPage.getMessageWhere': True,
		'InspectInvitationsPage.InspectInvitationsPage.getMessage': True,
		'InspectInvitationsPage.InspectInvitationsPage.clickMessageHistory': True,
		'InspectInvitationsPage.InspectInvitationsPage.cancel': True,
		'InspectInvitationsPage.InspectInvitationsPage.notSpam': True,
		'InspectInvitationsPage.InspectInvitationsPage.InspectInvitationsPage': True,
		'InspectInvitationsPage.InspectInvitationsPage.footer': True,
		'InspectInvitationsPage.InspectInvitationsPage.tableWebEl': True,
		'InspectInvitationsPage.InspectInvitationsPage.preview': True,
		'InspectInvitationsPage.InspectInvitationsPage.notSpamButton': True,
		'InspectInvitationsPage.InspectInvitationsPage.cancelButton': True,
	}

	expected_calls = {
		'new.TableElement.TableElement': True,
		'.InspectInvitationsPage.getDriver': True,
		'elements.List.size': True,
		'elements.List.get': True,
		'new.ArrayList.ArrayList': True,
		'.InspectInvitationsPage.getTable': True,
		'cell.WebElement.getText': True,
		'.InspectInvitationsPage.getDriver': True,
		'link.WebElement.click': True,
		'columnEntries.List.add': True,
		'cell.WebElement.getText': True,
		'new.WebDriverException.WebDriverException': True,
		'columnEntries.List.toString': True,
		'.InspectInvitationsPage.getTable': True,
		'new.TableElement.TableElement': True,
		'.InspectInvitationsPage.getDriver': True,
		'super.InspectInvitationsPage.getMessageWhere': True,
		'new.OneMessage.OneMessage': True,
		'super.InspectInvitationsPage.getMessageWhere': True,
		'new.OneMessage.OneMessage': True,
		'new.InvitationMessageDisplayElement.InvitationMessageDisplayElement': True,
		'super.AsAdmin.clickMessageHistory': True,
		'new.WebDriverException.WebDriverException': True,
		'notSpamButton.WebElement.click': True,
		'new.InvitationActionConfirmationElement.InvitationActionConfirmationElement': True,
		'confirm.InvitationActionConfirmationElement.getLabel': True,
		'new.WebDriverException.WebDriverException': True,
		'confirm.InvitationActionConfirmationElement.getLabel': True,
		'confirm.InvitationActionConfirmationElement.setMemo': True,
		'confirm.InvitationActionConfirmationElement.confirm': True,
		'new.InvitationMessageDisplayElement.InvitationMessageDisplayElement': True,
		'super.AsUser.clickMessageHistory': True,
		'cancelButton.WebElement.click': True,
		'new.InvitationActionConfirmationElement.InvitationActionConfirmationElement': True,
		'new.WebDriverException.WebDriverException': True,
		'new.InvitationFooterElement.InvitationFooterElement': True,
		'@.FindBy.@': True,
		'@.Override.@': True,
		'@.FindBy.@': True,
		'@.FindBy.@': True,
		'@.Override.@': True,
		'@.Override.@': True,
		'@.Override.@': True,
		'@.Override.@': True,
		'@.FindBy.@': True,
		'@.Override.@': True,
		'@.FindBy.@': True,
		'@.Override.@': True,
		'@.Override.@': True,
		'@.Override.@': True,
		'@.Override.@': True,
		'extends.extends.BasePage': True,
		'extends.extends.InspectInvitationsPage': True,
		'extends.extends.InspectInvitationsPage': True,
		'extends.extends.AsAdmin': True,
		'implements.implements.InspectInvitationsPage': True,
		'extends.extends.AsUser': True,
		'implements.implements.InspectInvitationsPage': True,
	}

	for clas in class_operations:
		for op in clas['operations']:
			# print(f'\'{clas["name"]}.{op["name"]}\': True,')
			assert expected_operations[f'{clas["name"]}.{op["name"]}']

	for call in calls:
		# print(f'\'{call["caller"]}.{call["ref"]}\': True,')
		assert expected_calls[f'{call["caller"]}.{call["ref"]}']


def test_extract_public_static_constants(): 
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'Align.java')
	src = open(javafile).read()
	parser = JavaParser()
	parser.parser(src)
	class_operations = parser.extract_operations()
	expected_operations = {
		'Align.Align.CENTER': True,
		'Align.Align.TOP': True,
		'Align.Align.BOTTOM': True,
		'Align.Align.LEFT': True,
		'Align.Align.RIGHT': True,
		'Align.Align.TOP_LEFT': True,
		'Align.Align.TOP_RIGHT': True,
		'Align.Align.BOTTOM_LEFT': True,
		'Align.Align.BOTTOM_RIGHT': True,
		'Align.Align.FIT_HORIZONTAL': True,
		'Align.Align.FIT_VERTICAL': True,
		'Align.Align.FIT': True,
		'Align.Align.NORTH': True,
		'Align.Align.SOUTH': True,
		'Align.Align.WEST': True,
		'Align.Align.EAST': True,
		'Align.Align.NORTH_WEST': True,
		'Align.Align.NORTH_EAST': True,
		'Align.Align.SOUTH_WEST': True,
		'Align.Align.SOUTH_EAST': True,
		'Align.Align.Align': True,
		'Align.Align.align': True,
	}
	for clas in class_operations:
		for op in clas['operations']:
			# print(f'\'{clas["name"]}.{op["name"]}\': True,')	
			assert expected_operations[f'{clas["name"]}.{op["name"]}']
