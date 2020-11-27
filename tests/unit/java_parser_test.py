from ecolyzer.parser import JavaParser


def test_annotations():
	src = """
		package net.sf.esfinge.metadata.annotation.container;

		import java.lang.annotation.Annotation;
		import java.lang.annotation.Retention;
		import java.lang.annotation.RetentionPolicy;

		import net.sf.esfinge.metadata.annotation.finder.SearchOnEnclosingElements;
		import net.sf.esfinge.metadata.container.reading.MethodProcessorsReadingProcessor;

		@Retention(RetentionPolicy.RUNTIME)
		@AnnotationReadingConfig(MethodProcessorsReadingProcessor.class)
		@SearchOnEnclosingElements

		public @interface ProcessorPerMethod {
			Class<? extends Annotation> configAnnotation();
			ProcessorType type() default ProcessorType.READER_ADDS_METADATA;

		}
	"""

	parser = JavaParser()
	parser.parser(src)
	annotations = parser.extract_operations()[0]['operations']
	assert len(annotations) == 1
	assert annotations[0]['name'] == 'ProcessorPerMethod'
	assert 'public' in annotations[0]['modifiers']

	calls = parser.extract_calls()
	assert len(calls) == 3
	assert calls[0]['ref'] == 'Retention'
	assert calls[1]['ref'] == 'AnnotationReadingConfig'
	assert calls[2]['ref'] == 'SearchOnEnclosingElements'

def test_parse_cast():
	src = """
		public class EyeCandySixtiesChartTheme extends GenericChartTheme {

			@Override
			protected JFreeChart createCandlestickChart() throws JRException
			{
				JFreeChart jfreeChart = super.createCandlestickChart();
				XYPlot xyPlot = (XYPlot) jfreeChart.getPlot();
				CandlestickRenderer renderer = (CandlestickRenderer)xyPlot.getRenderer();  
				DefaultHighLowDataset dataset = (DefaultHighLowDataset)xyPlot.getDataset();  
				if (dataset != null)
				{
					for (int i = 0; i < dataset.getSeriesCount(); i++)
					{
						renderer.setSeriesFillPaint(i, ChartThemesConstants.EYE_CANDY_SIXTIES_COLORS.get(i));
						renderer.setSeriesPaint(i, Color.DARK_GRAY);
					}
				}
				return jfreeChart;
			}
		}
	"""

	parser = JavaParser()
	parser.parser(src)
	calls = parser.extract_calls()
	calls_map = {}
	for call in calls:
		calls_map[call['ref']] = True		
	assert calls_map['XYPlot.getRenderer']
	assert calls_map['XYPlot.getDataset']
