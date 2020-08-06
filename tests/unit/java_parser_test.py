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
	annotations = parser.extract_operations()
	assert len(annotations) == 1
	assert annotations[0]['name'] == 'ProcessorPerMethod'
	assert 'public' in annotations[0]['modifiers']

	calls = parser.extract_calls()
	assert len(calls) == 3
	assert calls[0] == 'Retention'
	assert calls[1] == 'AnnotationReadingConfig'
	assert calls[2] == 'SearchOnEnclosingElements'
