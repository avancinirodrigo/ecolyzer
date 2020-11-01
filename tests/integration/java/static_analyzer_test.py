import os
from ecolyzer.repository import Repository #TODO: why?
from ecolyzer.system import File, SourceFile
from ecolyzer.parser import StaticAnalyzer

def test_reverse_engineering():
	operations = {
		'extends.JFreeChart': True,
		'JFreeChart': True,
		'isCompatibleValue': True,
		'getID': True,
		'setID': True,
		'getElementHinting': True,
		'setElementHinting': True,
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
		'getSubtitles': True,
		'setSubtitles': True,
		'getSubtitleCount': True,
		'getSubtitle': True,
		'addSubtitle': True,
		'clearSubtitles': True,
		'removeSubtitle': True,
		'getPlot': True,
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
		# 'createAlignedRectangle2D': True,
		'drawTitle': True,
		'createBufferedImage': True,
		'handleClick': True,
		'addChangeListener': True,
		'removeChangeListener': True,
		'fireChartChanged': True,
		'notifyListeners': True,
		'addProgressListener': True,
		'removeProgressListener': True,
		'titleChanged': True,
		'plotChanged': True,
		'equals': True,
		#TODO: the class doen't use these methods
		# 'writeObject': True,
		# 'readObject': True,
		'clone': True
	}

	calls = {
		'getColor': True,
		'requireNonNull': True,
		'setChart': True,
		'put': True,
		'setMargin': True,
		'setPosition': True,
		'add': True,
		'setText': True,
		'size': True,
		'get': True,
		'clear': True,
		'remove': True,
		'setRenderingHint': True,
		'setChartArea': True,
		'getEntityCollection': True,
		'getClip': True,
		'clip': True,
		'addRenderingHints': True,
		'setPaint': True,
		'fill': True,
		'getComposite': True,
		'setComposite': True,
		'getInstance': True,
		'getWidth': True,
		'getHeight': True,
		'align': True,
		'drawImage': True,
		'getX': True,
		'getY': True,
		'setStroke': True,
		'setRect': True,
		'trim': True,
		'isVisible': True,
		'addAll': True,
		'getPlotInfo': True,
		'setClip': True,
		'getCenterX': True,
		'getMaxX': True,
		'getCenterY': True,
		'getMaxY': True,
		'getPosition': True,
		'setGenerateEntities': True,
		'arrange': True,
		'getHorizontalAlignment': True,
		'min': True,
		'max': True,
		'getVerticalAlignment': True,
		'createGraphics': True,
		'dispose': True,
		'getScaleInstance': True,
		'transform': True,
		'getListenerList': True,
		'equal': True,
		'defaultWriteObject': True,
		'writeStroke': True,
		'writePaint': True,
		'defaultReadObject': True,
		'readStroke': True,
		'readPaint': True,
		'Override': True, #TODO: Annotation
		'implements.Drawable': True,
		'implements.TitleChangeListener': True,
		'implements.PlotChangeListener': True,
		'implements.Serializable': True,
		'implements.Cloneable': True
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

	for k in operations.keys():
		assert code_elements_dict[k]

	for k in calls.keys():
		assert code_elements_dict[k]	

	for k in associations.keys():
		assert code_elements_dict[k]				 

	#assert len(code_elements) == 176 == len(operations) + len(calls) + len(associations)
	
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
	assert analyzer.number_of_calls(src_file, src, 'getHorizontalAlignment') == 2
	assert analyzer.number_of_calls(src_file, src, 'getX') == 7
	assert analyzer.number_of_calls(src_file, src, 'requireNonNull') == 12

def test_class_modifiers():
	javafile = os.path.join(os.path.dirname(__file__), '../data', 'InternalClasses.java')
	file = File(javafile)
	src_file = SourceFile(file)
	src = open(javafile).read()
	analyzer = StaticAnalyzer()
	code_elements = analyzer.reverse_engineering(src_file, src)
	assert len(code_elements) == 4
	assert code_elements[0].name == 'extends.ClassA'
	assert code_elements[1].name == 'ClassA'
	assert code_elements[2].name == 'extends.ClassB'
	assert code_elements[3].name == 'ClassB'
