import os
from ecolyzer.repository import Repository  # TODO: why?
from ecolyzer.system import File, SourceFile
from ecolyzer.parser import StaticAnalyzer


def test_reverse_engineering():
	operations = {
		'extends.JFreeChart': True,
		'JFreeChart.JFreeChart': True,
		'JFreeChart.isCompatibleValue': True,
		'JFreeChart.getID': True,
		'JFreeChart.setID': True,
		'JFreeChart.getElementHinting': True,
		'JFreeChart.setElementHinting': True,
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
		'JFreeChart.getSubtitles': True,
		'JFreeChart.setSubtitles': True,
		'JFreeChart.getSubtitleCount': True,
		'JFreeChart.getSubtitle': True,
		'JFreeChart.addSubtitle': True,
		'JFreeChart.clearSubtitles': True,
		'JFreeChart.removeSubtitle': True,
		'JFreeChart.getPlot': True,
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
		# 'createAlignedRectangle2D': True,
		'JFreeChart.drawTitle': True,
		'JFreeChart.createBufferedImage': True,
		'JFreeChart.handleClick': True,
		'JFreeChart.addChangeListener': True,
		'JFreeChart.removeChangeListener': True,
		'JFreeChart.fireChartChanged': True,
		'JFreeChart.notifyListeners': True,
		'JFreeChart.addProgressListener': True,
		'JFreeChart.removeProgressListener': True,
		'JFreeChart.titleChanged': True,
		'JFreeChart.plotChanged': True,
		'JFreeChart.equals': True,
		# TODO: the class doen't use these methods
		# 'writeObject': True,
		# 'readObject': True,
		'JFreeChart.clone': True,
		'JFreeChart.DEFAULT_TITLE_FONT': True,
		'JFreeChart.DEFAULT_BACKGROUND_PAINT': True,
		'JFreeChart.DEFAULT_BACKGROUND_IMAGE': True,
		'JFreeChart.DEFAULT_BACKGROUND_IMAGE_ALIGNMENT': True,
		'JFreeChart.DEFAULT_BACKGROUND_IMAGE_ALPHA': True,
		'JFreeChart.KEY_SUPPRESS_SHADOW_GENERATION': True,
	}

	calls = {
		'Objects.requireNonNull': True,
		'Plot.setChart': True,
		'EventListenerList.EventListenerList': True,
		'RenderingHints.RenderingHints': True,
		'RenderingHints.KEY_ANTIALIASING': True,
		'RenderingHints.VALUE_ANTIALIAS_ON': True,
		'RenderingHints.put': True,
		'RenderingHints.KEY_STROKE_CONTROL': True,
		'RenderingHints.VALUE_STROKE_PURE': True,
		'BasicStroke.BasicStroke': True,
		'Color.BLACK': True,
		'RectangleInsets.ZERO_INSETS': True,
		'Plot.addChangeListener': True,
		'ArrayList.ArrayList': True,
		'LegendTitle.LegendTitle': True,
		'LegendTitle.setMargin': True,
		'RectangleInsets.RectangleInsets': True,
		'LegendTitle.setBackgroundPaint': True,
		'Color.WHITE': True,
		'LegendTitle.setPosition': True,
		'RectangleEdge.BOTTOM': True,
		'List.add': True,
		'LegendTitle.addChangeListener': True,
		'TextTitle.TextTitle': True,
		'TextTitle.addChangeListener': True,
		'ChartChangeEvent.ChartChangeEvent': True,
		'TextTitle.removeChangeListener': True,
		'TextTitle.setText': True,
		'List.size': True,
		'IllegalArgumentException.IllegalArgumentException': True,
		'List.get': True,
		'Title.addChangeListener': True,
		'Title.removeChangeListener': True,
		'List.clear': True,
		'List.remove': True,
		'RenderingHints.get': True,
		'RenderingHints.VALUE_ANTIALIAS_OFF': True,
		'RenderingHints.KEY_TEXT_ANTIALIASING': True,
		'RenderingHints.VALUE_TEXT_ANTIALIAS_ON': True,
		'RenderingHints.VALUE_TEXT_ANTIALIAS_OFF': True,
		'Paint.equals': True,
		'Image.equals': True,
		'ChartProgressEvent.ChartProgressEvent': True,
		'ChartProgressEventType.DRAWING_STARTED': True,
		'HashMap.HashMap': True,
		'Map.put': True,
		'Graphics2D.setRenderingHint': True,
		'ChartHints.KEY_BEGIN_ELEMENT': True,
		'ChartRenderingInfo.clear': True,
		'ChartRenderingInfo.setChartArea': True,
		'ChartRenderingInfo.getEntityCollection': True,
		'EntityCollection.add': True,
		'JFreeChartEntity.JFreeChartEntity': True,
		'Rectangle2D.clone': True,
		'Graphics2D.getClip': True,
		'Graphics2D.clip': True,
		'Graphics2D.addRenderingHints': True,
		'Graphics2D.setPaint': True,
		'Graphics2D.fill': True,
		'Graphics2D.getComposite': True,
		'Graphics2D.setComposite': True,
		'AlphaComposite.getInstance': True,
		'AlphaComposite.SRC_OVER': True,
		'Rectangle2D.Rectangle2D': True,
		'Rectangle2D.Double': True,
		'Image.getWidth': True,
		'Image.getHeight': True,
		'Align.align': True,
		'Graphics2D.drawImage': True,
		'Rectangle2D.getX': True,
		'Rectangle2D.getY': True,
		'Rectangle2D.getWidth': True,
		'Rectangle2D.getHeight': True,
		'Graphics2D.setStroke': True,
		'Graphics2D.draw': True,
		'Rectangle2D.setRect': True,
		'RectangleInsets.trim': True,
		'TextTitle.isVisible': True,
		'EntityCollection.addAll': True,
		'Title.isVisible': True,
		'ChartRenderingInfo.getPlotInfo': True,
		'Plot.draw': True,
		'Graphics2D.setClip': True,
		'ChartHints.KEY_END_ELEMENT': True,
		'Boolean.TRUE': True,
		'ChartProgressEventType.DRAWING_FINISHED': True,
		'Double.NaN': True,
		'Rectangle2D.getCenterX': True,
		'Size2D.width': True,
		'Rectangle2D.getMaxX': True,
		'IllegalStateException.IllegalStateException': True,
		'Rectangle2D.getCenterY': True,
		'Size2D.height': True,
		'Rectangle2D.getMaxY': True,
		'Title.getPosition': True,
		'RectangleConstraint.RectangleConstraint': True,
		'Range.Range': True,
		'LengthConstraintType.RANGE': True,
		'BlockParams.BlockParams': True,
		'BlockParams.setGenerateEntities': True,
		'RectangleEdge.TOP': True,
		'Title.arrange': True,
		'Title.getHorizontalAlignment': True,
		'VerticalAlignment.TOP': True,
		'Title.draw': True,
		'Math.min': True,
		'Math.max': True,
		'VerticalAlignment.BOTTOM': True,
		'RectangleEdge.RIGHT': True,
		'HorizontalAlignment.RIGHT': True,
		'Title.getVerticalAlignment': True,
		'RectangleEdge.LEFT': True,
		'HorizontalAlignment.LEFT': True,
		'RuntimeException.RuntimeException': True,
		'EntityBlockResult.getEntityCollection': True,
		'BufferedImage.TYPE_INT_ARGB': True,
		'BufferedImage.BufferedImage': True,
		'BufferedImage.createGraphics': True,
		'Graphics2D.dispose': True,
		'AffineTransform.getScaleInstance': True,
		'Graphics2D.transform': True,
		'Plot.handleClick': True,
		'EventListenerList.add': True,
		'EventListenerList.remove': True,
		'EventListenerList.getListenerList': True,
		'Object.length': True,
		'TitleChangeEvent.setChart': True,
		'PlotChangeEvent.setChart': True,
		'RenderingHints.equals': True,
		'ObjectUtils.equal': True,
		'PaintUtils.equal': True,
		'RectangleInsets.equals': True,
		'IOException.IOException': True,
		'ObjectOutputStream.defaultWriteObject': True,
		'SerialUtils.writeStroke': True,
		'SerialUtils.writePaint': True,
		'ClassNotFoundException.ClassNotFoundException': True,
		'ObjectInputStream.defaultReadObject': True,
		'SerialUtils.readStroke': True,
		'SerialUtils.readPaint': True,
		'CloneNotSupportedException.CloneNotSupportedException': True,
		'Object.clone': True,
		'RenderingHints.clone': True,
		'TextTitle.clone': True,
		'Plot.clone': True,
		'Font.Font': True,
		'Font.BOLD': True,
		'UIManager.getColor': True,
		'Align.FIT': True,
		'RenderingHints.Key': True,
		'Override.@': True,
		'implements.Drawable': True,
		'implements.TitleChangeListener': True,
		'implements.PlotChangeListener': True,
		'implements.Serializable': True,
		'implements.Cloneable': True,
	}

	associations = {
		'java/awt/AlphaComposite': True,
		'java/awt/BasicStroke': True,
		'java/awt/Color': True,
		'java/awt/Composite': True,
		'java/awt/Font': True,
		'java/awt/Graphics2D': True,
		'java/awt/Image': True,
		'java/awt/Paint': True,
		'java/awt/RenderingHints': True,
		'java/awt/Shape': True,
		'java/awt/Stroke': True,
		'java/awt/geom/AffineTransform': True,
		'java/awt/geom/Point2D': True,
		'java/awt/geom/Rectangle2D': True,
		'java/awt/image/BufferedImage': True,
		'java/io/IOException': True,
		'java/io/ObjectInputStream': True,
		'java/io/ObjectOutputStream': True,
		'java/io/Serializable': True,
		'java/util/ArrayList': True,
		'java/util/HashMap': True,
		'java/util/List': True,
		'java/util/Map': True,
		'java/util/Objects': True,
		'javax/swing/UIManager': True,
		'javax/swing/event/EventListenerList': True,
		'org/jfree/chart/block/BlockParams': True,
		'org/jfree/chart/block/EntityBlockResult': True,
		'org/jfree/chart/block/LengthConstraintType': True,
		'org/jfree/chart/block/RectangleConstraint': True,
		'org/jfree/chart/entity/EntityCollection': True,
		'org/jfree/chart/entity/JFreeChartEntity': True,
		'org/jfree/chart/event/ChartChangeEvent': True,
		'org/jfree/chart/event/ChartChangeListener': True,
		'org/jfree/chart/event/ChartProgressEvent': True,
		'org/jfree/chart/event/ChartProgressEventType': True,
		'org/jfree/chart/event/ChartProgressListener': True,
		'org/jfree/chart/event/PlotChangeEvent': True,
		'org/jfree/chart/event/PlotChangeListener': True,
		'org/jfree/chart/event/TitleChangeEvent': True,
		'org/jfree/chart/event/TitleChangeListener': True,
		'org/jfree/chart/plot/CategoryPlot': True,
		'org/jfree/chart/plot/Plot': True,
		'org/jfree/chart/plot/PlotRenderingInfo': True,
		'org/jfree/chart/plot/XYPlot': True,
		'org/jfree/chart/title/LegendTitle': True,
		'org/jfree/chart/title/TextTitle': True,
		'org/jfree/chart/title/Title': True,
		'org/jfree/chart/ui/Align': True,
		'org/jfree/chart/ui/Drawable': True,
		'org/jfree/chart/ui/HorizontalAlignment': True,
		'org/jfree/chart/ui/RectangleEdge': True,
		'org/jfree/chart/ui/RectangleInsets': True,
		'org/jfree/chart/ui/Size2D': True,
		'org/jfree/chart/ui/VerticalAlignment': True,
		'org/jfree/chart/util/ObjectUtils': True,
		'org/jfree/chart/util/PaintUtils': True,
		'org/jfree/chart/util/SerialUtils': True,
		'org/jfree/data/Range': True
	}

	javafile = os.path.join(os.path.dirname(__file__), '../data', 'JFreeChart.java')
	file = File(javafile)
	src_file = SourceFile(file)
	src = open(javafile).read()
	analyzer = StaticAnalyzer()
	code_elements = analyzer.reverse_engineering(src_file, src)

	code_elements_dict = {}
	for element in code_elements:
		code_elements_dict[element.name] = True
		# if element.type == 'call':
		# 	print(f'\'{element.name}\': True,')

	for k in operations.keys():
		assert code_elements_dict[k]

	for k in calls.keys():
		assert code_elements_dict[k]

	for k in associations.keys():
		assert code_elements_dict[k]				 

	assert len(code_elements) == 279 == len(operations) + len(calls) + len(associations)
	
	for element in code_elements:
		if element.type == 'call':
			assert calls[element.name]
			assert element.name not in operations
		elif element.type == 'operation':
			assert operations[element.name]
			assert element.name not in calls
		else:
			assert associations[element.name]


def test_number_of_calls():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'JFreeChart.java')
	file = File(javafile)
	src_file = SourceFile(file)
	src = open(javafile).read()
	analyzer = StaticAnalyzer()
	assert analyzer.number_of_calls(src_file, src, 'Title.getHorizontalAlignment') == 2
	assert analyzer.number_of_calls(src_file, src, 'Rectangle2D.getX') == 7
	assert analyzer.number_of_calls(src_file, src, 'Objects.requireNonNull') == 12


def test_class_modifiers():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'InternalClasses.java')
	file = File(javafile)
	src_file = SourceFile(file)
	src = open(javafile).read()
	analyzer = StaticAnalyzer()
	code_elements = analyzer.reverse_engineering(src_file, src)
	assert len(code_elements) == 4
	assert code_elements[0].name == 'extends.ClassA'
	assert code_elements[1].name == 'ClassA.ClassA'
	assert code_elements[2].name == 'extends.ClassB'
	assert code_elements[3].name == 'ClassB.ClassB'


def test_lexer_exception():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'HelloWorld.java')
	file = File(javafile)
	src_file = SourceFile(file)
	src = open(javafile).read()
	analyzer = StaticAnalyzer()
	code_elements = analyzer.reverse_engineering(src_file, src)	
	assert not code_elements


def _get_code_elements(filepath):
	file = File(filepath)
	src_file = SourceFile(file)
	src = open(filepath).read()
	analyzer = StaticAnalyzer()
	code_elements = analyzer.reverse_engineering(src_file, src)	
	# for ce in code_elements:
	# 	print(f'\'{ce.name}\': True,')
	# print('--')
	return code_elements


def test_code_elements_checker():
	central_class_filepath = os.path.join(os.path.dirname(__file__),
			'../data/seco/centralsoft/src/central_a', 'CentralSoftware.java')	
	central_interface_filepath = os.path.join(os.path.dirname(__file__), 
			'../data/seco/centralsoft/src/central_a', 'CentralInterface.java')	
	dep1_extends_filepath = os.path.join(os.path.dirname(__file__), 
			'../data/seco/dependentalpha/src/package_a', 'DependentExtends.java')	
	dep1_implements_filepath = os.path.join(os.path.dirname(__file__), 
			'../data/seco/dependentalpha/src/package_a', 'DependentImplements.java')	
	dep1_factory_filepath = os.path.join(os.path.dirname(__file__), 
			'../data/seco/dependentalpha/src/package_a', 'DependentCentralFactory.java')	
	dep1_app_filepath = os.path.join(os.path.dirname(__file__), 
			'../data/seco/dependentalpha/src/package_a', 'DependentApp.java')	
	
	central_code_elements = _get_code_elements(central_class_filepath)
	central_expected = {
		'extends.CentralSoftware': True,
		'CentralSoftware.CentralSoftware': True,
		'CentralSoftware.getVar': True,
		'CentralSoftware.getVarCopy': True,
		'CentralSoftware.getVarRef': True,
		'CentralSoftware.setVar': True,
	}

	for ce in central_code_elements:
		assert central_expected[ce.name]

	central_inter_code_elements = _get_code_elements(central_interface_filepath)
	central_inter_expected = {
		'implements.CentralInterface': True,
		'CentralInterface.centralInterfaceMethod': True,
	}

	for ce in central_inter_code_elements:
		assert central_inter_expected[ce.name]

	dep1_code_elements = _get_code_elements(dep1_extends_filepath)
	dep1_expected = {
		'extends.DependentSoftware': True,
		'DependentSoftware.DependentSoftware': True,
		'DependentSoftware.getVar': True,
		'CentralSoftware.CentralSoftware': True,
		'CentralSoftware.getVar': True,
		'extends.CentralSoftware': True,
		'package_a/CentralSoftware': True,
	}

	for ce in dep1_code_elements:
		assert dep1_expected[ce.name]

	dep1_impl_code_elements = _get_code_elements(dep1_implements_filepath)
	dep1_impl_expected = {
		'extends.DependentSoftware': True,
		'DependentSoftware.DependentSoftware': True,
		'CentralSoftware.getVar': True,
		'CentralFactory.createCentralSoftware': True,
		'implements.CentralInterface': True,
		'package_a/CentralInterface': True,
	}

	for ce in dep1_impl_code_elements:
		assert dep1_impl_expected[ce.name]	

	dep1_fac_code_elements = _get_code_elements(dep1_factory_filepath)
	dep1_fac_expected = {
		'extends.DependentCentralFactory': True,
		'DependentCentralFactory.createCentralSoftware': True,
		'DependentCentralFactory.DependentCentralFactory': True,
		'CentralSoftware.CentralSoftware': True,
		'package_a/CentralSoftware': True,
	}

	for ce in dep1_fac_code_elements:
		assert dep1_fac_expected[ce.name]

	dep1_app_code_elements = _get_code_elements(dep1_app_filepath)
	dep1_app_expected = {
		'DependentCentralFactory.createCentralSoftware': True,
		'CentralSoftware.getVar': True,
		'CentralSoftware.CentralSoftware': True,
		'CentralSoftware.getVarCopy': True,
		'DependentApp.getVarByCentral': True,
		'CentralSoftware.getVarRef': True,
		'package_a/CentralSoftware': True,
	}

	for ce in dep1_app_code_elements:
		assert dep1_app_expected[ce.name]	
