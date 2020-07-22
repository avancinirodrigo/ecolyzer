import os
from ecolyzer.repository import (RepositoryMiner, Repository, CommitInfo, 
								Commit, Author, Person, Modification,
								GitPython)
from ecolyzer.system import System, File, SourceFile, Operation, Call, Association
from ecolyzer.dataaccess import SQLAlchemyORM
	
def test_get_commit():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_java_get_commit'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	repo = Repository('repo/jfreechart')
	sys = System('terrame', repo)
	miner = RepositoryMiner(repo, sys)
	git = GitPython(repo.path)
	first_hash = next(iter(git.commit_hashs_reverse(1)))
	commit_info = miner.get_commit_info(first_hash)

	assert commit_info.msg == 'Branch for 1.0.x (starts with version 1.0.6).'
	assert commit_info.date.strftime('%Y-%m-%d %H:%M:%S') == '2007-06-29 13:35:09'
	assert commit_info.hash == '6f8f85d378dbb27da3855892a1cee294e7154a3d'
	assert commit_info.author_name == 'David Gilbert'
	assert commit_info.author_email == 'jfree@users.noreply.github.com'
	assert len(commit_info.modifications) == 999
	assert commit_info.modifications[0].filename == 'ChangeLog'
	assert commit_info.modifications[0].old_path == None
	assert commit_info.modifications[0].new_path == 'ChangeLog'
	assert commit_info.modifications[0].added == 5759
	assert commit_info.modifications[0].removed == 0
	assert commit_info.modifications[0].status == 'ADD'

	author = Author(Person(commit_info.author_name, commit_info.author_email))
	commit = Commit(commit_info, author, repo)
	fmodinfo = commit_info.modifications[0]
	file = File(fmodinfo.filename)
	filemod = Modification(fmodinfo, file, commit)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.add(commit)
	session.add(file)
	session.add(filemod)
	session.commit()

	filemoddb = session.query(Modification).get(1)
	commitdb = filemoddb.commit
	filedb = filemoddb.file

	assert commitdb.msg == 'Branch for 1.0.x (starts with version 1.0.6).'
	assert commitdb.date.strftime('%Y-%m-%d %H:%M:%S') == '2007-06-29 13:35:09'
	assert commitdb.hash == '6f8f85d378dbb27da3855892a1cee294e7154a3d'
	assert commitdb.author.name == 'David Gilbert'
	assert commitdb.author.email == 'jfree@users.noreply.github.com'
	assert filedb.fullpath == 'ChangeLog'
	assert filemoddb.old_path == None
	assert filemoddb.new_path == 'ChangeLog'
	assert filemoddb.added == 5759
	assert filemoddb.removed == 0
	assert filemoddb.status == 'ADD'	

	sec_hash = git.commit_hashs_reverse(2)[-1]
	commit_info = miner.get_commit_info(sec_hash)

	assert commit_info.msg == 'Clean up.'
	assert commit_info.date.strftime('%Y-%m-%d %H:%M:%S') == '2007-07-02 07:30:11'
	assert commit_info.hash == 'a5119ef9ba0146bba26a23bffbd200e8fb7aa17b'
	assert commit_info.author_name == 'David Gilbert'
	assert commit_info.author_email == 'jfree@users.noreply.github.com'
	assert len(commit_info.modifications) == 0 # Why zero?

	t3th_hash = git.commit_hashs_reverse(23)[-1]
	commit_info = miner.get_commit_info(t3th_hash)

	assert '2007-07-10  David Gilbert  <david.gilbert@object-refinery.com>' in commit_info.msg
	assert commit_info.date.strftime('%Y-%m-%d %H:%M:%S') == '2007-07-10 14:26:29'
	assert commit_info.hash == 'b0301dd7089d526cedc95a766a183a49fe1fedb9'
	assert commit_info.author_name == 'David Gilbert'
	assert commit_info.author_email == 'jfree@users.noreply.github.com'
	assert len(commit_info.modifications) == 3
	assert commit_info.modifications[0].filename == 'ChangeLog'
	assert commit_info.modifications[0].old_path == 'ChangeLog'
	assert commit_info.modifications[0].new_path == 'ChangeLog'
	assert commit_info.modifications[0].added == 10
	assert commit_info.modifications[0].removed == 0	
	assert commit_info.modifications[0].status == 'MODIFY'

	commit = Commit(commit_info, author, repo)
	fmodinfo = commit_info.modifications[0]
	filemod = Modification(fmodinfo, file, commit)
	session.add(commit)
	session.add(filemod)
	session.commit()
	
	filemoddb2 = session.query(Modification).get(2)
	commitdb2 = filemoddb2.commit
	filedb2 = filemoddb2.file

	assert '2007-07-10  David Gilbert  <david.gilbert@object-refinery.com>' in commitdb2.msg
	assert commitdb2.date.strftime('%Y-%m-%d %H:%M:%S') == '2007-07-10 14:26:29'
	assert commitdb2.hash == 'b0301dd7089d526cedc95a766a183a49fe1fedb9'
	assert commitdb2.author.name == 'David Gilbert'
	assert commitdb2.author.email == 'jfree@users.noreply.github.com'
	assert filedb2.fullpath == 'ChangeLog'
	assert filemoddb2.old_path == 'ChangeLog'
	assert filemoddb2.new_path == 'ChangeLog'
	assert filemoddb2.added == 10
	assert filemoddb2.removed == 0	
	assert filemoddb2.status == 'MODIFY'		

	filemoddb1 = session.query(Modification).get(1)
	commitdb1 = filemoddb1.commit
	filedb1 = filemoddb1.file

	assert commitdb1.msg == 'Branch for 1.0.x (starts with version 1.0.6).'
	assert commitdb1.date.strftime('%Y-%m-%d %H:%M:%S') == '2007-06-29 13:35:09'
	assert commitdb1.hash == '6f8f85d378dbb27da3855892a1cee294e7154a3d'
	assert commitdb1.author.name == 'David Gilbert'
	assert commitdb1.author.email == 'jfree@users.noreply.github.com'
	assert filedb1.fullpath == 'ChangeLog'
	assert filemoddb1.old_path == None
	assert filemoddb1.new_path == 'ChangeLog'
	assert filemoddb1.added == 5759
	assert filemoddb1.removed == 0
	assert filemoddb1.status == 'ADD'		

	session.close()
	db.drop_all()
	
def test_extract():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_java_extract'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	repo = Repository('repo/jfreechart')
	sys = System('JFreeChart', repo)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.commit()
	miner = RepositoryMiner(repo, sys)
	miner.add_ignore_dir_with('experimental')
	miner.add_ignore_dir_with('tests')
	git = GitPython(repo.path)
	first_hash = git.commit_hashs_reverse(1)[0]
	miner.extract(session, first_hash)
	filedb = session.query(File).filter_by(fullpath = 'source/org/jfree/chart/JFreeChart.java').first()
	srcfiledb = session.query(SourceFile).filter_by(file_id = filedb.id).first()
	commitdb = session.query(Commit).filter(Commit.hash == first_hash).one()
	assert commitdb.msg == 'Branch for 1.0.x (starts with version 1.0.6).'
	authordb = session.query(Author).filter(Author.id == commitdb.author_id).one()
	assert authordb.name == 'David Gilbert'
	modificationsdb = session.query(Modification).filter_by(commit_id = commitdb.id).all()

	files_mod = {
		'source/org/jfree/chart/ChartColor.java': True,
		'source/org/jfree/chart/ChartFactory.java': True,
		'source/org/jfree/chart/ChartFrame.java': True,
		'source/org/jfree/chart/ChartMouseEvent.java': True,
		'source/org/jfree/chart/ChartMouseListener.java': True,
		'source/org/jfree/chart/ChartPanel.java': True,
		'source/org/jfree/chart/ChartRenderingInfo.java': True,
		'source/org/jfree/chart/ChartUtilities.java': True,
		'source/org/jfree/chart/ClipPath.java': True,
		'source/org/jfree/chart/DrawableLegendItem.java': True,
		'source/org/jfree/chart/Effect3D.java': True,
		'source/org/jfree/chart/HashUtilities.java': True,
		'source/org/jfree/chart/JFreeChart.java': True,
		'source/org/jfree/chart/LegendItem.java': True,
		'source/org/jfree/chart/LegendItemCollection.java': True,
		'source/org/jfree/chart/LegendItemSource.java': True,
		'source/org/jfree/chart/LegendRenderingOrder.java': True,
		'source/org/jfree/chart/PaintMap.java': True,
		'source/org/jfree/chart/PolarChartPanel.java': True,
		'source/org/jfree/chart/StrokeMap.java': True,
		'source/org/jfree/chart/annotations/AbstractXYAnnotation.java': True,
		'source/org/jfree/chart/annotations/CategoryAnnotation.java': True,
		'source/org/jfree/chart/annotations/CategoryLineAnnotation.java': True,
		'source/org/jfree/chart/annotations/CategoryPointerAnnotation.java': True,
		'source/org/jfree/chart/annotations/CategoryTextAnnotation.java': True,
		'source/org/jfree/chart/annotations/TextAnnotation.java': True,
		'source/org/jfree/chart/axis/NumberAxis.java': True,
		'source/org/jfree/chart/axis/NumberAxis3D.java': True,
		'source/org/jfree/chart/renderer/xy/HighLowRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/StackedXYAreaRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/StackedXYAreaRenderer2.java': True,
		'source/org/jfree/chart/renderer/xy/StackedXYBarRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/StandardXYItemRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/VectorRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/WindItemRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYAreaRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYAreaRenderer2.java': True,
		'source/org/jfree/chart/renderer/xy/XYBarRenderer.java': True,
		'source/org/jfree/chart/annotations/XYAnnotation.java': True,
		'source/org/jfree/chart/annotations/XYBoxAnnotation.java': True,
		'source/org/jfree/chart/annotations/XYDrawableAnnotation.java': True,
		'source/org/jfree/chart/annotations/XYImageAnnotation.java': True,
		'source/org/jfree/chart/annotations/XYLineAnnotation.java': True,
		'source/org/jfree/chart/annotations/XYPointerAnnotation.java': True,
		'source/org/jfree/chart/annotations/XYPolygonAnnotation.java': True,
		'source/org/jfree/chart/annotations/XYShapeAnnotation.java': True,
		'source/org/jfree/chart/annotations/XYTextAnnotation.java': True,
		'source/org/jfree/chart/axis/Axis.java': True,
		'source/org/jfree/chart/axis/AxisCollection.java': True,
		'source/org/jfree/chart/axis/AxisLocation.java': True,
		'source/org/jfree/chart/axis/AxisSpace.java': True,
		'source/org/jfree/chart/axis/AxisState.java': True,
		'source/org/jfree/chart/axis/CategoryAnchor.java': True,
		'source/org/jfree/chart/axis/CategoryAxis.java': True,
		'source/org/jfree/chart/axis/CategoryAxis3D.java': True,
		'source/org/jfree/chart/axis/CategoryLabelPosition.java': True,
		'source/org/jfree/chart/axis/CategoryLabelPositions.java': True,
		'source/org/jfree/chart/axis/CategoryLabelWidthType.java': True,
		'source/org/jfree/chart/axis/CategoryTick.java': True,
		'source/org/jfree/chart/axis/ColorBar.java': True,
		'source/org/jfree/chart/axis/CompassFormat.java': True,
		'source/org/jfree/chart/axis/CyclicNumberAxis.java': True,
		'source/org/jfree/chart/axis/DateAxis.java': True,
		'source/org/jfree/chart/axis/DateTick.java': True,
		'source/org/jfree/chart/axis/DateTickMarkPosition.java': True,
		'source/org/jfree/chart/axis/DateTickUnit.java': True,
		'source/org/jfree/chart/axis/ExtendedCategoryAxis.java': True,
		'source/org/jfree/chart/axis/LogarithmicAxis.java': True,
		'source/org/jfree/chart/axis/MarkerAxisBand.java': True,
		'source/org/jfree/chart/axis/ModuloAxis.java': True,
		'source/org/jfree/chart/axis/MonthDateFormat.java': True,
		'source/org/jfree/chart/axis/NumberTick.java': True,
		'source/org/jfree/chart/axis/NumberTickUnit.java': True,
		'source/org/jfree/chart/axis/PeriodAxis.java': True,
		'source/org/jfree/chart/axis/PeriodAxisLabelInfo.java': True,
		'source/org/jfree/chart/axis/QuarterDateFormat.java': True,
		'source/org/jfree/chart/axis/SegmentedTimeline.java': True,
		'source/org/jfree/chart/axis/StandardTickUnitSource.java': True,
		'source/org/jfree/chart/axis/SubCategoryAxis.java': True,
		'source/org/jfree/chart/axis/SymbolAxis.java': True,
		'source/org/jfree/chart/axis/Tick.java': True,
		'source/org/jfree/chart/axis/TickUnit.java': True,
		'source/org/jfree/chart/axis/TickUnitSource.java': True,
		'source/org/jfree/chart/axis/TickUnits.java': True,
		'source/org/jfree/chart/axis/Timeline.java': True,
		'source/org/jfree/chart/axis/ValueAxis.java': True,
		'source/org/jfree/chart/demo/TimeSeriesChartDemo1.java': True,
		'source/org/jfree/chart/renderer/xy/XYBlockRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYBoxAndWhiskerRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYBubbleRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYDifferenceRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYDotRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYErrorRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYItemRenderer.java': True,
		'source/org/jfree/chart/axis/ValueTick.java': True,
		'source/org/jfree/chart/block/AbstractBlock.java': True,
		'source/org/jfree/chart/block/Arrangement.java': True,
		'source/org/jfree/chart/block/Block.java': True,
		'source/org/jfree/chart/block/BlockBorder.java': True,
		'source/org/jfree/chart/block/BlockContainer.java': True,
		'source/org/jfree/chart/block/BlockFrame.java': True,
		'source/org/jfree/chart/block/BlockParams.java': True,
		'source/org/jfree/chart/entity/CategoryItemEntity.java': True,
		'source/org/jfree/chart/block/BlockResult.java': True,
		'source/org/jfree/chart/block/BorderArrangement.java': True,
		'source/org/jfree/chart/block/CenterArrangement.java': True,
		'source/org/jfree/chart/block/ColorBlock.java': True,
		'source/org/jfree/chart/block/ColumnArrangement.java': True,
		'source/org/jfree/chart/block/EmptyBlock.java': True,
		'source/org/jfree/chart/block/EntityBlockParams.java': True,
		'source/org/jfree/chart/block/EntityBlockResult.java': True,
		'source/org/jfree/chart/block/FlowArrangement.java': True,
		'source/org/jfree/chart/block/GridArrangement.java': True,
		'source/org/jfree/chart/block/LabelBlock.java': True,
		'source/org/jfree/chart/block/LengthConstraintType.java': True,
		'source/org/jfree/chart/block/LineBorder.java': True,
		'source/org/jfree/chart/block/RectangleConstraint.java': True,
		'source/org/jfree/chart/demo/BarChartDemo1.java': True,
		'source/org/jfree/chart/demo/PieChartDemo1.java': True,
		'source/org/jfree/chart/editor/ChartEditor.java': True,
		'source/org/jfree/chart/editor/ChartEditorFactory.java': True,
		'source/org/jfree/chart/editor/ChartEditorManager.java': True,
		'source/org/jfree/chart/editor/DefaultAxisEditor.java': True,
		'source/org/jfree/chart/editor/DefaultChartEditor.java': True,
		'source/org/jfree/chart/editor/DefaultChartEditorFactory.java': True,
		'source/org/jfree/chart/editor/DefaultColorBarEditor.java': True,
		'source/org/jfree/chart/editor/DefaultNumberAxisEditor.java': True,
		'source/org/jfree/chart/editor/DefaultPlotEditor.java': True,
		'source/org/jfree/chart/editor/DefaultTitleEditor.java': True,
		'source/org/jfree/chart/entity/XYItemEntity.java': True,
		'source/org/jfree/chart/editor/PaletteChooserPanel.java': True,
		'source/org/jfree/chart/editor/PaletteSample.java': True,
		'source/org/jfree/chart/encoders/EncoderUtil.java': True,
		'source/org/jfree/chart/encoders/ImageEncoder.java': True,
		'source/org/jfree/chart/encoders/ImageEncoderFactory.java': True,
		'source/org/jfree/chart/encoders/ImageFormat.java': True,
		'source/org/jfree/chart/encoders/KeypointPNGEncoderAdapter.java': True,
		'source/org/jfree/chart/encoders/SunJPEGEncoderAdapter.java': True,
		'source/org/jfree/chart/encoders/SunPNGEncoderAdapter.java': True,
		'source/org/jfree/chart/entity/CategoryLabelEntity.java': True,
		'source/org/jfree/chart/entity/ChartEntity.java': True,
		'source/org/jfree/chart/entity/ContourEntity.java': True,
		'source/org/jfree/chart/entity/EntityCollection.java': True,
		'source/org/jfree/chart/entity/LegendItemEntity.java': True,
		'source/org/jfree/chart/entity/PieSectionEntity.java': True,
		'source/org/jfree/chart/entity/StandardEntityCollection.java': True,
		'source/org/jfree/chart/entity/TickLabelEntity.java': True,
		'source/org/jfree/chart/entity/XYAnnotationEntity.java': True,
		'source/org/jfree/chart/event/AxisChangeEvent.java': True,
		'source/org/jfree/chart/event/AxisChangeListener.java': True,
		'source/org/jfree/chart/event/ChartChangeEvent.java': True,
		'source/org/jfree/chart/event/ChartChangeEventType.java': True,
		'source/org/jfree/chart/event/ChartChangeListener.java': True,
		'source/org/jfree/chart/renderer/category/StackedBarRenderer3D.java': True,
		'source/org/jfree/chart/renderer/category/StatisticalBarRenderer.java': True,
		'source/org/jfree/chart/renderer/category/StatisticalLineAndShapeRenderer.java': True,
		'source/org/jfree/chart/renderer/category/WaterfallBarRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/AbstractXYItemRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/CandlestickRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/ClusteredXYBarRenderer.java': True,
		'source/org/jfree/chart/event/ChartProgressEvent.java': True,
		'source/org/jfree/chart/event/ChartProgressListener.java': True,
		'source/org/jfree/chart/event/MarkerChangeEvent.java': True,
		'source/org/jfree/chart/event/MarkerChangeListener.java': True,
		'source/org/jfree/chart/event/PlotChangeEvent.java': True,
		'source/org/jfree/chart/event/PlotChangeListener.java': True,
		'source/org/jfree/chart/event/RendererChangeEvent.java': True,
		'source/org/jfree/chart/event/RendererChangeListener.java': True,
		'source/org/jfree/chart/event/TitleChangeEvent.java': True,
		'source/org/jfree/chart/event/TitleChangeListener.java': True,
		'source/org/jfree/chart/renderer/xy/CyclicXYItemRenderer.java': True,
		'source/org/jfree/chart/imagemap/DynamicDriveToolTipTagFragmentGenerator.java': True,
		'source/org/jfree/chart/imagemap/ImageMapUtilities.java': True,
		'source/org/jfree/chart/imagemap/OverLIBToolTipTagFragmentGenerator.java': True,
		'source/org/jfree/chart/imagemap/StandardToolTipTagFragmentGenerator.java': True,
		'source/org/jfree/chart/imagemap/StandardURLTagFragmentGenerator.java': True,
		'source/org/jfree/data/general/DefaultKeyedValuesDataset.java': True,
		'source/org/jfree/chart/imagemap/ToolTipTagFragmentGenerator.java': True,
		'source/org/jfree/chart/imagemap/URLTagFragmentGenerator.java': True,
		'source/org/jfree/chart/labels/AbstractCategoryItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/AbstractPieItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/AbstractXYItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/BoxAndWhiskerToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/BoxAndWhiskerXYToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/BubbleXYItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/CategoryItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/CategorySeriesLabelGenerator.java': True,
		'source/org/jfree/chart/labels/CategoryToolTipGenerator.java': True,
		'source/org/jfree/data/general/DefaultPieDataset.java': True,
		'source/org/jfree/data/general/DefaultValueDataset.java': True,
		'source/org/jfree/chart/labels/ContourToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/CustomXYToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/HighLowItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/IntervalCategoryItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/IntervalCategoryToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/ItemLabelAnchor.java': True,
		'source/org/jfree/chart/labels/ItemLabelPosition.java': True,
		'source/org/jfree/chart/labels/MultipleXYSeriesLabelGenerator.java': True,
		'source/org/jfree/chart/labels/PieSectionLabelGenerator.java': True,
		'source/org/jfree/chart/labels/PieToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/StandardCategoryItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/StandardCategorySeriesLabelGenerator.java': True,
		'source/org/jfree/chart/labels/StandardCategoryToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/StandardContourToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/StandardPieSectionLabelGenerator.java': True,
		'source/org/jfree/chart/labels/StandardPieToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/StandardXYItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/StandardXYSeriesLabelGenerator.java': True,
		'source/org/jfree/chart/labels/StandardXYToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/StandardXYZToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/SymbolicXYItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/XYItemLabelGenerator.java': True,
		'source/org/jfree/chart/labels/XYSeriesLabelGenerator.java': True,
		'source/org/jfree/chart/labels/XYToolTipGenerator.java': True,
		'source/org/jfree/chart/labels/XYZToolTipGenerator.java': True,
		'source/org/jfree/chart/needle/ArrowNeedle.java': True,
		'source/org/jfree/chart/needle/LineNeedle.java': True,
		'source/org/jfree/chart/needle/LongNeedle.java': True,
		'source/org/jfree/chart/needle/MeterNeedle.java': True,
		'source/org/jfree/chart/needle/MiddlePinNeedle.java': True,
		'source/org/jfree/chart/needle/PinNeedle.java': True,
		'source/org/jfree/chart/needle/PlumNeedle.java': True,
		'source/org/jfree/chart/needle/PointerNeedle.java': True,
		'source/org/jfree/chart/needle/ShipNeedle.java': True,
		'source/org/jfree/chart/needle/WindNeedle.java': True,
		'source/org/jfree/chart/plot/AbstractPieLabelDistributor.java': True,
		'source/org/jfree/chart/plot/CategoryMarker.java': True,
		'source/org/jfree/chart/plot/CategoryPlot.java': True,
		'source/org/jfree/chart/plot/ColorPalette.java': True,
		'source/org/jfree/chart/plot/CombinedDomainCategoryPlot.java': True,
		'source/org/jfree/chart/plot/CombinedDomainXYPlot.java': True,
		'source/org/jfree/chart/plot/CombinedRangeCategoryPlot.java': True,
		'source/org/jfree/chart/plot/CombinedRangeXYPlot.java': True,
		'source/org/jfree/chart/plot/CompassPlot.java': True,
		'source/org/jfree/chart/plot/ContourPlot.java': True,
		'source/org/jfree/data/time/Year.java': True,
		'source/org/jfree/chart/plot/ContourPlotUtilities.java': True,
		'source/org/jfree/chart/plot/ContourValuePlot.java': True,
		'source/org/jfree/chart/plot/CrosshairState.java': True,
		'source/org/jfree/chart/plot/DatasetRenderingOrder.java': True,
		'source/org/jfree/chart/plot/DefaultDrawingSupplier.java': True,
		'source/org/jfree/chart/plot/DialShape.java': True,
		'source/org/jfree/chart/plot/DrawingSupplier.java': True,
		'source/org/jfree/chart/plot/FastScatterPlot.java': True,
		'source/org/jfree/data/xml/PieDatasetHandler.java': True,
		'source/org/jfree/chart/plot/GreyPalette.java': True,
		'source/org/jfree/chart/plot/IntervalMarker.java': True,
		'source/org/jfree/chart/plot/JThermometer.java': True,
		'source/org/jfree/chart/plot/Marker.java': True,
		'source/org/jfree/chart/plot/MeterInterval.java': True,
		'source/org/jfree/chart/plot/MeterPlot.java': True,
		'source/org/jfree/chart/plot/MultiplePiePlot.java': True,
		'source/org/jfree/chart/plot/PieLabelDistributor.java': True,
		'source/org/jfree/chart/plot/PieLabelRecord.java': True,
		'source/org/jfree/chart/plot/PiePlot.java': True,
		'source/org/jfree/chart/plot/PiePlot3D.java': True,
		'source/org/jfree/chart/plot/PiePlotState.java': True,
		'source/org/jfree/chart/plot/Plot.java': True,
		'source/org/jfree/chart/plot/PlotOrientation.java': True,
		'source/org/jfree/chart/plot/PlotRenderingInfo.java': True,
		'source/org/jfree/chart/plot/PlotState.java': True,
		'source/org/jfree/chart/plot/PolarPlot.java': True,
		'source/org/jfree/chart/plot/RainbowPalette.java': True,
		'source/org/jfree/chart/plot/RingPlot.java': True,
		'source/org/jfree/chart/plot/SeriesRenderingOrder.java': True,
		'source/org/jfree/chart/plot/SpiderWebPlot.java': True,
		'source/org/jfree/chart/plot/ThermometerPlot.java': True,
		'source/org/jfree/chart/plot/ValueAxisPlot.java': True,
		'source/org/jfree/chart/plot/ValueMarker.java': True,
		'source/org/jfree/chart/plot/WaferMapPlot.java': True,
		'source/org/jfree/chart/plot/XYPlot.java': True,
		'source/org/jfree/data/xy/DefaultWindDataset.java': True,
		'source/org/jfree/chart/plot/Zoomable.java': True,
		'source/org/jfree/chart/renderer/AbstractRenderer.java': True,
		'source/org/jfree/chart/renderer/AreaRendererEndType.java': True,
		'source/org/jfree/chart/renderer/DefaultPolarItemRenderer.java': True,
		'source/org/jfree/chart/renderer/GrayPaintScale.java': True,
		'source/org/jfree/chart/renderer/LookupPaintScale.java': True,
		'source/org/jfree/chart/renderer/NotOutlierException.java': True,
		'source/org/jfree/chart/renderer/Outlier.java': True,
		'source/org/jfree/chart/renderer/OutlierList.java': True,
		'source/org/jfree/chart/renderer/OutlierListCollection.java': True,
		'source/org/jfree/chart/renderer/PaintScale.java': True,
		'source/org/jfree/chart/renderer/PolarItemRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/DefaultXYItemRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/DeviationRenderer.java': True,
		'source/org/jfree/chart/renderer/RendererState.java': True,
		'source/org/jfree/chart/renderer/RendererUtilities.java': True,
		'source/org/jfree/chart/renderer/WaferMapRenderer.java': True,
		'source/org/jfree/chart/renderer/category/AbstractCategoryItemRenderer.java': True,
		'source/org/jfree/chart/renderer/category/AreaRenderer.java': True,
		'source/org/jfree/chart/renderer/category/BarRenderer.java': True,
		'source/org/jfree/chart/renderer/category/BarRenderer3D.java': True,
		'source/org/jfree/chart/renderer/category/BoxAndWhiskerRenderer.java': True,
		'source/org/jfree/chart/renderer/category/CategoryItemRenderer.java': True,
		'source/org/jfree/chart/renderer/category/CategoryItemRendererState.java': True,
		'source/org/jfree/chart/renderer/category/CategoryStepRenderer.java': True,
		'source/org/jfree/chart/renderer/category/DefaultCategoryItemRenderer.java': True,
		'source/org/jfree/chart/renderer/category/GanttRenderer.java': True,
		'source/org/jfree/chart/renderer/category/GroupedStackedBarRenderer.java': True,
		'source/org/jfree/chart/renderer/category/IntervalBarRenderer.java': True,
		'source/org/jfree/chart/renderer/category/LayeredBarRenderer.java': True,
		'source/org/jfree/chart/renderer/category/LevelRenderer.java': True,
		'source/org/jfree/chart/renderer/category/LineAndShapeRenderer.java': True,
		'source/org/jfree/chart/renderer/category/LineRenderer3D.java': True,
		'source/org/jfree/chart/renderer/category/MinMaxCategoryRenderer.java': True,
		'source/org/jfree/chart/renderer/category/StackedAreaRenderer.java': True,
		'source/org/jfree/chart/renderer/category/StackedBarRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYItemRendererState.java': True,
		'source/org/jfree/chart/renderer/xy/XYLine3DRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYLineAndShapeRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYStepAreaRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/XYStepRenderer.java': True,
		'source/org/jfree/chart/renderer/xy/YIntervalRenderer.java': True,
		'source/org/jfree/chart/resources/JFreeChartResources.java': True,
		'source/org/jfree/chart/servlet/ChartDeleter.java': True,
		'source/org/jfree/chart/servlet/DisplayChart.java': True,
		'source/org/jfree/chart/servlet/ServletUtilities.java': True,
		'source/org/jfree/chart/title/CompositeTitle.java': True,
		'source/org/jfree/chart/title/DateTitle.java': True,
		'source/org/jfree/chart/title/ImageTitle.java': True,
		'source/org/jfree/chart/title/LegendGraphic.java': True,
		'source/org/jfree/chart/title/LegendItemBlockContainer.java': True,
		'source/org/jfree/chart/title/LegendTitle.java': True,
		'source/org/jfree/chart/title/PaintScaleLegend.java': True,
		'source/org/jfree/chart/title/TextTitle.java': True,
		'source/org/jfree/chart/title/Title.java': True,
		'source/org/jfree/chart/urls/CategoryURLGenerator.java': True,
		'source/org/jfree/chart/urls/CustomPieURLGenerator.java': True,
		'source/org/jfree/chart/urls/CustomXYURLGenerator.java': True,
		'source/org/jfree/chart/urls/PieURLGenerator.java': True,
		'source/org/jfree/chart/urls/StandardCategoryURLGenerator.java': True,
		'source/org/jfree/chart/urls/StandardPieURLGenerator.java': True,
		'source/org/jfree/chart/urls/StandardXYURLGenerator.java': True,
		'source/org/jfree/chart/urls/StandardXYZURLGenerator.java': True,
		'source/org/jfree/chart/urls/TimeSeriesURLGenerator.java': True,
		'source/org/jfree/chart/urls/URLUtilities.java': True,
		'source/org/jfree/chart/urls/XYURLGenerator.java': True,
		'source/org/jfree/data/xy/DefaultXYDataset.java': True,
		'source/org/jfree/data/xy/DefaultXYZDataset.java': True,
		'source/org/jfree/chart/urls/XYZURLGenerator.java': True,
		'source/org/jfree/chart/util/HexNumberFormat.java': True,
		'source/org/jfree/chart/util/RelativeDateFormat.java': True,
		'source/org/jfree/data/ComparableObjectItem.java': True,
		'source/org/jfree/data/ComparableObjectSeries.java': True,
		'source/org/jfree/data/DataUtilities.java': True,
		'source/org/jfree/data/DefaultKeyedValue.java': True,
		'source/org/jfree/data/DefaultKeyedValues.java': True,
		'source/org/jfree/data/DefaultKeyedValues2D.java': True,
		'source/org/jfree/data/DomainInfo.java': True,
		'source/org/jfree/data/DomainOrder.java': True,
		'source/org/jfree/data/KeyToGroupMap.java': True,
		'source/org/jfree/data/KeyedObject.java': True,
		'source/org/jfree/data/KeyedObjects.java': True,
		'source/org/jfree/data/KeyedObjects2D.java': True,
		'source/org/jfree/data/KeyedValue.java': True,
		'source/org/jfree/data/KeyedValueComparator.java': True,
		'source/org/jfree/data/xy/XYDataItem.java': True,
		'source/org/jfree/data/xy/XYDataset.java': True,
		'source/org/jfree/data/xy/XYDatasetTableModel.java': True,
		'source/org/jfree/data/KeyedValueComparatorType.java': True,
		'source/org/jfree/data/KeyedValues.java': True,
		'source/org/jfree/data/KeyedValues2D.java': True,
		'source/org/jfree/data/Range.java': True,
		'source/org/jfree/data/RangeInfo.java': True,
		'source/org/jfree/data/RangeType.java': True,
		'source/org/jfree/data/UnknownKeyException.java': True,
		'source/org/jfree/data/Value.java': True,
		'source/org/jfree/data/Values.java': True,
		'source/org/jfree/data/Values2D.java': True,
		'source/org/jfree/data/category/CategoryDataset.java': True,
		'source/org/jfree/data/category/CategoryToPieDataset.java': True,
		'source/org/jfree/data/category/DefaultCategoryDataset.java': True,
		'source/org/jfree/data/category/DefaultIntervalCategoryDataset.java': True,
		'source/org/jfree/data/category/IntervalCategoryDataset.java': True,
		'source/org/jfree/data/contour/ContourDataset.java': True,
		'source/org/jfree/data/contour/DefaultContourDataset.java': True,
		'source/org/jfree/data/contour/NonGridContourDataset.java': True,
		'source/org/jfree/data/function/Function2D.java': True,
		'source/org/jfree/data/function/LineFunction2D.java': True,
		'source/org/jfree/data/function/NormalDistributionFunction2D.java': True,
		'source/org/jfree/data/function/PowerFunction2D.java': True,
		'source/org/jfree/data/gantt/GanttCategoryDataset.java': True,
		'source/org/jfree/data/gantt/Task.java': True,
		'source/org/jfree/data/gantt/TaskSeries.java': True,
		'source/org/jfree/data/gantt/TaskSeriesCollection.java': True,
		'source/org/jfree/data/general/AbstractDataset.java': True,
		'source/org/jfree/data/general/AbstractSeriesDataset.java': True,
		'source/org/jfree/data/general/CombinationDataset.java': True,
		'source/org/jfree/data/general/CombinedDataset.java': True,
		'source/org/jfree/data/general/Dataset.java': True,
		'source/org/jfree/data/general/DatasetChangeEvent.java': True,
		'source/org/jfree/data/general/DatasetChangeListener.java': True,
		'source/org/jfree/data/general/DatasetGroup.java': True,
		'source/org/jfree/data/general/DatasetUtilities.java': True,
		'source/org/jfree/data/general/DefaultKeyedValueDataset.java': True,
		'source/org/jfree/data/general/DefaultKeyedValues2DDataset.java': True,
		'source/org/jfree/data/general/KeyedValueDataset.java': True,
		'source/org/jfree/data/general/KeyedValues2DDataset.java': True,
		'source/org/jfree/data/general/KeyedValuesDataset.java': True,
		'source/org/jfree/data/general/PieDataset.java': True,
		'source/org/jfree/data/general/Series.java': True,
		'source/org/jfree/data/general/SeriesChangeEvent.java': True,
		'source/org/jfree/data/general/SeriesChangeListener.java': True,
		'source/org/jfree/data/general/SeriesDataset.java': True,
		'source/org/jfree/data/general/SeriesException.java': True,
		'source/org/jfree/data/general/SubSeriesDataset.java': True,
		'source/org/jfree/data/general/ValueDataset.java': True,
		'source/org/jfree/data/general/WaferMapDataset.java': True,
		'source/org/jfree/data/io/CSV.java': True,
		'source/org/jfree/data/jdbc/JDBCCategoryDataset.java': True,
		'source/org/jfree/data/jdbc/JDBCPieDataset.java': True,
		'source/org/jfree/data/jdbc/JDBCXYDataset.java': True,
		'source/org/jfree/data/resources/DataPackageResources.java': True,
		'source/org/jfree/data/resources/DataPackageResources_de.java': True,
		'source/org/jfree/data/resources/DataPackageResources_es.java': True,
		'source/org/jfree/data/resources/DataPackageResources_fr.java': True,
		'source/org/jfree/data/resources/DataPackageResources_pl.java': True,
		'source/org/jfree/data/resources/DataPackageResources_ru.java': True,
		'source/org/jfree/data/statistics/BoxAndWhiskerCalculator.java': True,
		'source/org/jfree/data/statistics/BoxAndWhiskerCategoryDataset.java': True,
		'source/org/jfree/data/statistics/BoxAndWhiskerItem.java': True,
		'source/org/jfree/data/statistics/BoxAndWhiskerXYDataset.java': True,
		'source/org/jfree/data/statistics/DefaultBoxAndWhiskerCategoryDataset.java': True,
		'source/org/jfree/data/statistics/DefaultBoxAndWhiskerXYDataset.java': True,
		'source/org/jfree/data/statistics/DefaultStatisticalCategoryDataset.java': True,
		'source/org/jfree/data/statistics/HistogramBin.java': True,
		'source/org/jfree/data/statistics/HistogramDataset.java': True,
		'source/org/jfree/data/statistics/HistogramType.java': True,
		'source/org/jfree/data/statistics/MeanAndStandardDeviation.java': True,
		'source/org/jfree/data/statistics/Regression.java': True,
		'source/org/jfree/data/statistics/SimpleHistogramBin.java': True,
		'source/org/jfree/data/statistics/SimpleHistogramDataset.java': True,
		'source/org/jfree/data/statistics/StatisticalCategoryDataset.java': True,
		'source/org/jfree/data/statistics/Statistics.java': True,
		'source/org/jfree/data/time/DateRange.java': True,
		'source/org/jfree/data/time/Day.java': True,
		'source/org/jfree/data/time/DynamicTimeSeriesCollection.java': True,
		'source/org/jfree/data/time/FixedMillisecond.java': True,
		'source/org/jfree/data/time/Hour.java': True,
		'source/org/jfree/data/time/Millisecond.java': True,
		'source/org/jfree/data/time/Minute.java': True,
		'source/org/jfree/data/time/Month.java': True,
		'source/org/jfree/data/time/MovingAverage.java': True,
		'source/org/jfree/data/time/Quarter.java': True,
		'source/org/jfree/data/time/RegularTimePeriod.java': True,
		'source/org/jfree/data/time/Second.java': True,
		'source/org/jfree/data/time/SimpleTimePeriod.java': True,
		'source/org/jfree/data/time/TimePeriod.java': True,
		'source/org/jfree/data/time/TimePeriodAnchor.java': True,
		'source/org/jfree/data/time/TimePeriodFormatException.java': True,
		'source/org/jfree/data/time/TimePeriodValue.java': True,
		'source/org/jfree/data/time/TimePeriodValues.java': True,
		'source/org/jfree/data/time/TimePeriodValuesCollection.java': True,
		'source/org/jfree/data/time/TimeSeries.java': True,
		'source/org/jfree/data/time/TimeSeriesCollection.java': True,
		'source/org/jfree/data/time/TimeSeriesDataItem.java': True,
		'source/org/jfree/data/time/TimeSeriesTableModel.java': True,
		'source/org/jfree/data/time/TimeTableXYDataset.java': True,
		'source/org/jfree/data/time/Week.java': True,
		'source/org/jfree/data/time/ohlc/OHLC.java': True,
		'source/org/jfree/data/time/ohlc/OHLCItem.java': True,
		'source/org/jfree/data/time/ohlc/OHLCSeries.java': True,
		'source/org/jfree/data/time/ohlc/OHLCSeriesCollection.java': True,
		'source/org/jfree/data/xml/CategoryDatasetHandler.java': True,
		'source/org/jfree/data/xml/CategorySeriesHandler.java': True,
		'source/org/jfree/data/xml/DatasetReader.java': True,
		'source/org/jfree/data/xml/DatasetTags.java': True,
		'source/org/jfree/data/xml/ItemHandler.java': True,
		'source/org/jfree/data/xml/KeyHandler.java': True,
		'source/org/jfree/data/xml/RootHandler.java': True,
		'source/org/jfree/data/xml/ValueHandler.java': True,
		'source/org/jfree/data/xy/AbstractIntervalXYDataset.java': True,
		'source/org/jfree/data/xy/AbstractXYDataset.java': True,
		'source/org/jfree/data/xy/AbstractXYZDataset.java': True,
		'source/org/jfree/data/xy/CategoryTableXYDataset.java': True,
		'source/org/jfree/data/xy/DefaultHighLowDataset.java': True,
		'source/org/jfree/data/xy/DefaultIntervalXYDataset.java': True,
		'source/org/jfree/data/xy/DefaultOHLCDataset.java': True,
		'source/org/jfree/data/xy/DefaultTableXYDataset.java': True,
		'source/org/jfree/data/xy/IntervalXYDataset.java': True,
		'source/org/jfree/data/xy/IntervalXYDelegate.java': True,
		'source/org/jfree/data/xy/IntervalXYZDataset.java': True,
		'source/org/jfree/data/xy/MatrixSeries.java': True,
		'source/org/jfree/data/xy/MatrixSeriesCollection.java': True,
		'source/org/jfree/data/xy/NormalizedMatrixSeries.java': True,
		'source/org/jfree/data/xy/OHLCDataItem.java': True,
		'source/org/jfree/data/xy/OHLCDataset.java': True,
		'source/org/jfree/data/xy/TableXYDataset.java': True,
		'source/org/jfree/data/xy/Vector.java': True,
		'source/org/jfree/data/xy/VectorDataItem.java': True,
		'source/org/jfree/data/xy/VectorSeries.java': True,
		'source/org/jfree/data/xy/VectorSeriesCollection.java': True,
		'source/org/jfree/data/xy/VectorXYDataset.java': True,
		'source/org/jfree/data/xy/WindDataset.java': True,
		'source/org/jfree/data/xy/XIntervalDataItem.java': True,
		'source/org/jfree/data/xy/XIntervalSeries.java': True,
		'source/org/jfree/data/xy/XIntervalSeriesCollection.java': True,
		'source/org/jfree/data/xy/XYBarDataset.java': True,
		'source/org/jfree/data/xy/XYCoordinate.java': True,
		'source/org/jfree/data/xy/XYInterval.java': True,
		'source/org/jfree/data/xy/XYIntervalDataItem.java': True,
		'source/org/jfree/data/xy/XYIntervalSeries.java': True,
		'source/org/jfree/data/xy/XYIntervalSeriesCollection.java': True,
		'source/org/jfree/data/xy/XYSeries.java': True,
		'source/org/jfree/data/xy/XYSeriesCollection.java': True,
		'source/org/jfree/data/xy/XYZDataset.java': True,
		'source/org/jfree/data/xy/XisSymbolic.java': True,
		'source/org/jfree/data/xy/YInterval.java': True,
		'source/org/jfree/data/xy/YIntervalDataItem.java': True,
		'source/org/jfree/data/xy/YIntervalSeries.java': True,
		'source/org/jfree/data/xy/YIntervalSeriesCollection.java': True,
		'source/org/jfree/data/xy/YWithXInterval.java': True,
		'source/org/jfree/data/xy/YisSymbolic.java': True	
 	}

	for mod in modificationsdb:
		assert files_mod[mod.new_path]

	operationsdb = session.query(Operation).filter_by(source_file_id = srcfiledb.id).all()

	operations = {
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
		'main': True,
		'clone': True,
		'getLogo': True
	}

	operationsdb_dict = {}
	for op in operationsdb:
		operationsdb_dict[op.name] = True
		assert operations[op.name]

	for k in operations.keys():
		assert operationsdb_dict[k]

	calls = {
		'getColor': True,
		'setMargin': True,
		'setFrame': True,
		'setPosition': True,
		'add': True,
		'setText': True,
		'iterator': True,
		'hasNext': True,
		'next': True,
		'size': True,
		'get': True,
		'clear': True,
		'remove': True,
		'put': True,
		'setChartArea': True,
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
		'getEntityCollection': True,
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
		'setChart': True,
		'equal': True,
		'defaultWriteObject': True,
		'writeStroke': True,
		'writePaint': True,
		'defaultReadObject': True,
		'readStroke': True,
		'readPaint': True,
		'println': True,
		'toString': True,
		'getBundle': True,
		'setName': True,
		'getString': True,
		'setVersion': True,
		'setInfo': True,
		'setCopyright': True,
		'setLogo': True,
		'setLicenceName': True,
		'setLicenceText': True,
		'getLGPL': True,
		'setContributors': True,
		'asList': True,
		'addLibrary': True,
		'getClass': True,
		'getClassLoader': True,
		'getResource': True,
		'getImage': True
	}

	callsdb = session.query(Call).filter_by(source_file_id = srcfiledb.id).all()	
	callsdb_dict = {}	
	for call in callsdb:
		callsdb_dict[call.name] = True
		assert calls[call.name]

	for k in calls.keys():
		assert callsdb_dict[k]

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
		'java/net/URL': True,
		'java/util/ArrayList': True,
		'java/util/Arrays': True,
		'java/util/Iterator': True,
		'java/util/List': True,
		'java/util/ResourceBundle': True,
		'javax/swing/ImageIcon': True,
		'javax/swing/UIManager': True,
		'javax/swing/event/EventListenerList': True,
		'org/jfree/JCommon': True,
		'org/jfree/chart/block/BlockParams': True,
		'org/jfree/chart/block/EntityBlockResult': True,
		'org/jfree/chart/block/LengthConstraintType': True,
		'org/jfree/chart/block/LineBorder': True,
		'org/jfree/chart/block/RectangleConstraint': True,
		'org/jfree/chart/entity/EntityCollection': True,
		'org/jfree/chart/event/ChartChangeEvent': True,
		'org/jfree/chart/event/ChartChangeListener': True,
		'org/jfree/chart/event/ChartProgressEvent': True,
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
		'org/jfree/data/Range': True,
		'org/jfree/io/SerialUtilities': True,
		'org/jfree/ui/Align': True,
		'org/jfree/ui/Drawable': True,
		'org/jfree/ui/HorizontalAlignment': True,
		'org/jfree/ui/RectangleEdge': True,
		'org/jfree/ui/RectangleInsets': True,
		'org/jfree/ui/Size2D': True,
		'org/jfree/ui/VerticalAlignment': True,
		'org/jfree/ui/about/Contributor': True,
		'org/jfree/ui/about/Licences': True,
		'org/jfree/ui/about/ProjectInfo': True,
		'org/jfree/util/ObjectUtilities': True,
		'org/jfree/util/PaintUtilities': True
	}

	assocsdb = session.query(Association).filter_by(source_file_id = srcfiledb.id).all()		
	assocsdb_dict = {}	
	for assoc in assocsdb:
		assocsdb_dict[assoc.name] = True
		assert associations[assoc.name]
		#print('\'' + assoc.name + '\': ' + 'True,')

	for k in associations.keys():
		assert assocsdb_dict[k]

	session.close()
	db.drop_all()

def test_get_commit_source_file():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_java_sources'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	repo = Repository('repo/jfreechart')
	sys = System('JFreeChart', repo)
	miner = RepositoryMiner(repo, sys)
	miner.add_ignore_dir_with('experimental')
	miner.add_ignore_dir_with('tests')
	git = GitPython(repo.path)
	first_hash = git.commit_hashs_reverse(1)[0]	
	commit_info = miner.get_commit_info(first_hash)
	author = Author(Person(commit_info.author_name, commit_info.author_email))
	commit = Commit(commit_info, author, repo)
	session = db.create_session()
	for mod_info in commit_info.modifications:
		file = File(mod_info.new_path)
		sys.add_file(file)
		mod = Modification(mod_info, file, commit)
		if miner.is_source_file(file):
			srcfile = SourceFile(file)
			code_elements = miner.extract_code_elements(srcfile, mod)
			for element in code_elements:
			 	element.modification = mod
			 	session.add(element)		
			session.add(mod)			

	session.commit()
	afile = sys.get_file('source/org/jfree/chart/JFreeChart.java')
	srcfiledb = session.query(SourceFile).filter_by(file_id = afile.id).first()
	assert srcfiledb.ext == 'java'
	assert srcfiledb.name == 'JFreeChart'
	assert srcfiledb.code_elements_len() == 198

	functions = session.query(Operation).filter_by(source_file_id = srcfiledb.id).all()	
	assert srcfiledb.code_element_exists(functions[0])
	assert functions[0].name == 'getRenderingHints'

	session.close()
	db.drop_all()

def test_extract_tag_interval():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_java_tag_interval'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	repo = Repository('repo/jfreechart')
	sys = System('JFreeChart', repo)
	session = db.create_session()
	session.add(repo)
	session.add(sys)
	session.commit()
	miner = RepositoryMiner(repo, sys)
# 	#miner.commit_interval('80a562be869dbb984229f608ae9a04d05c5e1689', 
# 	#					'082dff5e822ea1b4491911b7bf434a7f47a4be26') TODO: not working
	miner.tag_interval('v1.0.18', 'v1.0.19')
	miner.extract(session, max_count=10)

	commits = session.query(Commit).all()

	assert len(commits) == 10

	session.close()
	db.drop_all()	

# def test_extract_deleted_files():
# 	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_del_files'
# 	db = SQLAlchemyORM(db_url)
# 	db.create_all(True)
# 	repo = Repository('repo/terrame')
# 	sys = System('terrame', repo)
# 	session = db.create_session()
# 	session.add(repo)
# 	session.add(sys)
# 	session.commit()
# 	miner = RepositoryMiner(repo, sys)

# 	miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')
# 	file = session.query(File).filter_by(fullpath = 'src/lua/terrame.lua').one()
# 	mod = session.query(Modification).filter_by(file_id = file.id).first()

# 	assert mod.new_path == 'src/lua/terrame.lua'
# 	assert mod.old_path == None
# 	assert mod.status == 'ADD'
# 	assert sys.file_exists('src/lua/terrame.lua')

# 	miner.extract(session, 'f2e117598feee9db8cabbd1c300e143199e12d92')	
# 	file = session.query(File).filter_by(fullpath = 'src/lua/terrame.lua').one()
# 	mod = session.query(Modification).filter_by(file_id = file.id).filter_by(status = 'DELETE').first()
	
# 	assert mod.new_path == None
# 	assert mod.old_path == 'src/lua/terrame.lua'	
# 	assert mod.status == 'DELETE'
# 	assert sys.file_exists('src/lua/terrame.lua')

# 	session.close()
# 	db.drop_all()

# def test_extract_renamed_files():
# 	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_rename_file'
# 	db = SQLAlchemyORM(db_url)
# 	db.create_all(True)
# 	repo = Repository('repo/terrame')
# 	sys = System('terrame', repo)
# 	session = db.create_session()
# 	session.add(repo)
# 	session.add(sys)
# 	session.commit()
# 	miner = RepositoryMiner(repo, sys)
	
# 	miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')
# 	file = session.query(File).filter_by(fullpath = 'base/lua/Observer.lua').one()
# 	mod = session.query(Modification).filter_by(file_id = file.id).first()

# 	assert mod.new_path == 'base/lua/Observer.lua'
# 	assert mod.old_path == None
# 	assert mod.status == 'ADD'
# 	assert sys.file_exists('base/lua/Observer.lua')

# 	miner.extract(session, 'c57b6d69461abf10ba5950e0577dff3c982f3ea4')	
# 	file = session.query(File).filter_by(fullpath = 'src/lua/observer.lua').one()
# 	mod = session.query(Modification).filter_by(file_id = file.id).filter_by(status = 'RENAME').first()
	
# 	assert mod.new_path == 'src/lua/observer.lua'
# 	assert mod.old_path == 'base/lua/Observer.lua'
# 	assert mod.status == 'RENAME'
# 	assert sys.file_exists('src/lua/observer.lua')
# 	assert sys.file_exists('base/lua/Observer.lua')

# 	session.close()	
# 	db.drop_all()

# def test_extract_same_commit():
# 	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_rename_file'
# 	db = SQLAlchemyORM(db_url)
# 	db.create_all(True)
# 	repo = Repository('repo/terrame')
# 	sys = System('terrame', repo)
# 	session = db.create_session()
# 	session.add(repo)
# 	session.add(sys)
# 	session.commit()
# 	miner = RepositoryMiner(repo, sys)
	
# 	miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')
# 	file_count = session.query(File).count()	
# 	srcfile_count = session.query(SourceFile).count()
# 	mod_count = session.query(Modification).count()	

# 	#TODO(#41) miner.extract(session, '082dff5e822ea1b4491911b7bf434a7f47a4be26')

# 	assert file_count == session.query(File).count()
# 	assert srcfile_count == session.query(SourceFile).count()
# 	assert mod_count == session.query(Modification).count()

# 	session.close()	
# 	db.drop_all()

def test_extract_current_files():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_java_curr_files'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)	
	repo = Repository('repo/jfreechart')
	sys = System('JFreeChart', repo)
	miner = RepositoryMiner(repo, sys)
	miner.add_ignore_dir_with('tests')
	miner.add_ignore_dir_with('experimental')

	session = db.create_session()		
	miner.extract_current_files(session)

	assert session.query(File).count() >= 990

	session.close()
	db.drop_all()

def test_extract_last_commits():
	db_url = 'postgresql://postgres:postgres@localhost:5432/miner_java_last_commits'
	db = SQLAlchemyORM(db_url)
	db.create_all(True)
	repo = Repository('repo/jfreechart')
	sys = System('JFreeChart', repo)
	miner = RepositoryMiner(repo, sys)
	miner.add_ignore_dir_with('test')
	miner.add_ignore_dir_with('data')
	miner.add_ignore_dir_with('statistics')
	miner.add_ignore_dir_with('xy')

	session = db.create_session()		
	miner.extract_last_commits(session)

	srcfile = session.query(SourceFile).join(SourceFile.file)\
				.filter_by(fullpath = 'src/main/java/org/jfree/chart/entity/PlotEntity.java').one()

	code_elements = {
		'getPlot': True,
		'toString': True,
		'equals': True,
		'hashCode': True,
		'clone': True,
		'writeObject': True,
		'readObject': True,
		'nullNotPermitted': True,
		'append': True,
		'getToolTipText': True,
		'getArea': True,
		'equal': True,
		'getURLText': True,
		'defaultWriteObject': True,
		'writeShape': True,
		'defaultReadObject': True,
		'setArea': True,
		'readShape': True,
		'Override': True, #TODO: Annotations
		'java/awt/Shape': True,
		'java/io/IOException': True,
		'java/io/ObjectInputStream': True,
		'java/io/ObjectOutputStream': True,
		'org/jfree/chart/plot/Plot': True,
		'org/jfree/chart/HashUtils': True,
		'org/jfree/chart/util/ObjectUtils': True,
		'org/jfree/chart/util/Args': True,
		'org/jfree/chart/util/SerialUtils': True
	}

	src_code_elements = srcfile.code_elements()

	for k in src_code_elements:
		assert code_elements[srcfile.code_element_by_key(k).name]
		#print('\'' + srcfile.code_element_by_key(k).name + '\': ' + 'True,')

	assert srcfile.code_elements_len() == 26

	file_mod = session.query(Modification).\
					filter_by(file_id = srcfile.file_id).one()	

	assert file_mod.nloc == file_mod.added == 79

	session.close()
	db.drop_all()