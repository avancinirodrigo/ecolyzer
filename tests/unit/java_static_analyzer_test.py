from ecolyzer.repository import Repository  # TODO: why?
from ecolyzer.parser import StaticAnalyzer
from ecolyzer.system import File, SourceFile, Call, Operation


def test_all_code_elements():
	src = """
package org.jfree.chart;

import java.awt.AlphaComposite;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Composite;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Paint;
import java.awt.RenderingHints;
import java.awt.Shape;
import java.awt.Stroke;
import java.awt.geom.AffineTransform;
import java.awt.geom.Point2D;
import java.awt.geom.Rectangle2D;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import javax.swing.UIManager;
import javax.swing.event.EventListenerList;

import org.jfree.chart.block.BlockParams;
import org.jfree.chart.block.EntityBlockResult;
import org.jfree.chart.block.LengthConstraintType;
import org.jfree.chart.block.RectangleConstraint;
import org.jfree.chart.entity.EntityCollection;
import org.jfree.chart.entity.JFreeChartEntity;
import org.jfree.chart.event.ChartChangeEvent;
import org.jfree.chart.event.ChartChangeListener;
import org.jfree.chart.event.ChartProgressEvent;
import org.jfree.chart.event.ChartProgressEventType;
import org.jfree.chart.event.ChartProgressListener;
import org.jfree.chart.event.PlotChangeEvent;
import org.jfree.chart.event.PlotChangeListener;
import org.jfree.chart.event.TitleChangeEvent;
import org.jfree.chart.event.TitleChangeListener;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.Plot;
import org.jfree.chart.plot.PlotRenderingInfo;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.title.LegendTitle;
import org.jfree.chart.title.TextTitle;
import org.jfree.chart.title.Title;
import org.jfree.chart.ui.Align;
import org.jfree.chart.ui.Drawable;
import org.jfree.chart.ui.HorizontalAlignment;
import org.jfree.chart.ui.RectangleEdge;
import org.jfree.chart.ui.RectangleInsets;
import org.jfree.chart.ui.Size2D;
import org.jfree.chart.ui.VerticalAlignment;
import org.jfree.chart.util.ObjectUtils;
import org.jfree.chart.util.PaintUtils;
import org.jfree.chart.util.SerialUtils;
import org.jfree.data.Range;

public class JFreeChart implements Drawable, TitleChangeListener,
        PlotChangeListener, Serializable, Cloneable {	

    private static final long serialVersionUID = -3470703747817429120L;		
    public static final Font DEFAULT_TITLE_FONT
            = new Font("SansSerif", Font.BOLD, 18);	
    public static final Paint DEFAULT_BACKGROUND_PAINT
            = UIManager.getColor("Panel.background");
	public static final Image DEFAULT_BACKGROUND_IMAGE = null;
	public static final int DEFAULT_BACKGROUND_IMAGE_ALIGNMENT = Align.FIT;		
	public static final float DEFAULT_BACKGROUND_IMAGE_ALPHA = 0.5f;  

    public static final RenderingHints.Key KEY_SUPPRESS_SHADOW_GENERATION
            = new RenderingHints.Key(0) {
        @Override
        public boolean isCompatibleValue(Object val) {
            return val instanceof Boolean; // <<< TODO: does consider it?
        }
    };		

    private transient RenderingHints renderingHints;	
    private String id;  
    private boolean borderVisible;
    private transient Stroke borderStroke;
    private transient Paint borderPaint;
    private RectangleInsets padding;	
    private TextTitle title;	 
    private List<Title> subtitles; 
    private Plot plot;    
		private transient Paint backgroundPaint;
	private transient Image backgroundImage;  // todo: not serialized yet	
	private int backgroundImageAlignment = Align.FIT;
    private float backgroundImageAlpha = 0.5f;
    private transient EventListenerList changeListeners;
    private transient EventListenerList progressListeners;
    private boolean notify; 
    private boolean elementHinting;	

    public JFreeChart(Plot plot) {
        this(null, null, plot, true);
    }	

    public JFreeChart(String title, Plot plot) {
        this(title, JFreeChart.DEFAULT_TITLE_FONT, plot, true);
    }	

    public JFreeChart(String title, Font titleFont, Plot plot,
                      boolean createLegend) {

        Objects.requireNonNull(plot, "plot");	
        this.id = null;
        plot.setChart(this);
        this.progressListeners = new EventListenerList();
        this.changeListeners = new EventListenerList();
        this.notify = true;  	
        this.renderingHints = new RenderingHints(
                RenderingHints.KEY_ANTIALIASING,
                RenderingHints.VALUE_ANTIALIAS_ON);		
        this.renderingHints.put(RenderingHints.KEY_STROKE_CONTROL,
                RenderingHints.VALUE_STROKE_PURE);	
        this.borderVisible = false;
        this.borderStroke = new BasicStroke(1.0f);
        this.borderPaint = Color.BLACK;	
		this.padding = RectangleInsets.ZERO_INSETS;
		this.plot = plot;
		plot.addChangeListener(this);	
		this.subtitles = new ArrayList<>();	  
        if (createLegend) {
            LegendTitle legend = new LegendTitle(this.plot);
            legend.setMargin(new RectangleInsets(1.0, 1.0, 1.0, 1.0));
            legend.setBackgroundPaint(Color.WHITE);
            legend.setPosition(RectangleEdge.BOTTOM);
            this.subtitles.add(legend);
            legend.addChangeListener(this);
        }    
        if (title != null) {
            if (titleFont == null) {
                titleFont = DEFAULT_TITLE_FONT;
            }
            this.title = new TextTitle(title, titleFont);
            this.title.addChangeListener(this);
        }
        this.backgroundPaint = DEFAULT_BACKGROUND_PAINT;
        this.backgroundImage = DEFAULT_BACKGROUND_IMAGE;
        this.backgroundImageAlignment = DEFAULT_BACKGROUND_IMAGE_ALIGNMENT;
        this.backgroundImageAlpha = DEFAULT_BACKGROUND_IMAGE_ALPHA;		        		            		      	                	                                
    }	   

    public String getID() {
        return this.id;
    }

    public void setID(String id) {
        this.id = id;
    }	

    public boolean getElementHinting() {
        return this.elementHinting;
    }		

    public void setElementHinting(boolean hinting) {
        this.elementHinting = hinting;
    }

    public RenderingHints getRenderingHints() {
        return this.renderingHints;
    }	

    public void setRenderingHints(RenderingHints renderingHints) {
        Objects.requireNonNull(renderingHints, "renderingHints");
        this.renderingHints = renderingHints;
        fireChartChanged();
    }

    public boolean isBorderVisible() {
        return this.borderVisible;
    }     	

    public void setBorderVisible(boolean visible) {
        this.borderVisible = visible;
        fireChartChanged();
    }    

    public Stroke getBorderStroke() {
        return this.borderStroke;
    }     

    public void setBorderStroke(Stroke stroke) {
        this.borderStroke = stroke;
        fireChartChanged();
    }     

    public Paint getBorderPaint() {
        return this.borderPaint;
    }

    public void setBorderPaint(Paint paint) {
        this.borderPaint = paint;
        fireChartChanged();
    }   

    public RectangleInsets getPadding() {
        return this.padding;
    }

    public void setPadding(RectangleInsets padding) {
        Objects.requireNonNull(padding, "padding");
        this.padding = padding;
        notifyListeners(new ChartChangeEvent(this));
    }  

    public TextTitle getTitle() {
        return this.title;
    }

    public void setTitle(TextTitle title) {
        if (this.title != null) {
            this.title.removeChangeListener(this);
        }
        this.title = title;
        if (title != null) {
            title.addChangeListener(this);
        }
        fireChartChanged();
    }  

    public void addLegend(LegendTitle legend) {
        addSubtitle(legend);
    }  

    public LegendTitle getLegend() {
        return getLegend(0);
    } 

    public LegendTitle getLegend(int index) {
        int seen = 0;
        for (Title subtitle : this.subtitles) {
            if (subtitle instanceof LegendTitle) {
                if (seen == index) {
                    return (LegendTitle) subtitle;
                }
                else {
                    seen++;
                }
            }
        }
        return null;
    } 

    public void removeLegend() {
        removeSubtitle(getLegend());
    }   

    public List<Title> getSubtitles() {
        return new ArrayList<>(this.subtitles);
    }    

    public void setSubtitles(List<Title> subtitles) {
        Objects.requireNonNull(subtitles, "subtitles");
        setNotify(false);
        clearSubtitles();
        for (Title t: subtitles) {
            if (t != null) {
                addSubtitle(t);
            }
        }
        setNotify(true);  // this fires a ChartChangeEvent
    }

    public int getSubtitleCount() {
        return this.subtitles.size();
    }      

    public Title getSubtitle(int index) {
        if ((index < 0) || (index >= getSubtitleCount())) {
            throw new IllegalArgumentException("Index out of range.");
        }
        return this.subtitles.get(index);
    }      

    public void addSubtitle(Title subtitle) {
        Objects.requireNonNull(subtitle, "subtitle");
        this.subtitles.add(subtitle);
        subtitle.addChangeListener(this);
        fireChartChanged();
    }   

    public void addSubtitle(int index, Title subtitle) {
        if (index < 0 || index > getSubtitleCount()) {
            throw new IllegalArgumentException(
                    "The 'index' argument is out of range.");
        }
        Objects.requireNonNull(subtitle, "subtitle");
        this.subtitles.add(index, subtitle);
        subtitle.addChangeListener(this);
        fireChartChanged();
    }       

    public void clearSubtitles() {
        for (Title t : this.subtitles) {
            t.removeChangeListener(this);
        }
        this.subtitles.clear();
        fireChartChanged();
    } 

    public void removeSubtitle(Title title) {
        this.subtitles.remove(title);
        fireChartChanged();
    }    

    public Plot getPlot() {
        return this.plot;
    }  

    public boolean getAntiAlias() {
        Object val = this.renderingHints.get(RenderingHints.KEY_ANTIALIASING);
        return RenderingHints.VALUE_ANTIALIAS_ON.equals(val);
    }         

    public void setAntiAlias(boolean flag) {
        Object hint = flag ? RenderingHints.VALUE_ANTIALIAS_ON 
                : RenderingHints.VALUE_ANTIALIAS_OFF;
        this.renderingHints.put(RenderingHints.KEY_ANTIALIASING, hint);
        fireChartChanged();
    }  

    public Object getTextAntiAlias() {
        return this.renderingHints.get(RenderingHints.KEY_TEXT_ANTIALIASING);
    }   

    public void setTextAntiAlias(boolean flag) {
        if (flag) {
            setTextAntiAlias(RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
        }
        else {
            setTextAntiAlias(RenderingHints.VALUE_TEXT_ANTIALIAS_OFF);
        }
    } 

    public void setTextAntiAlias(Object val) {
        this.renderingHints.put(RenderingHints.KEY_TEXT_ANTIALIASING, val);
        notifyListeners(new ChartChangeEvent(this));
    }   

    public Paint getBackgroundPaint() {
        return this.backgroundPaint;
    }      

    public void setBackgroundPaint(Paint paint) {

        if (this.backgroundPaint != null) {
            if (!this.backgroundPaint.equals(paint)) {
                this.backgroundPaint = paint;
                fireChartChanged();
            }
        }
        else {
            if (paint != null) {
                this.backgroundPaint = paint;
                fireChartChanged();
            }
        }
    }  

    public Image getBackgroundImage() {
        return this.backgroundImage;
    }

    public void setBackgroundImage(Image image) {

        if (this.backgroundImage != null) {
            if (!this.backgroundImage.equals(image)) {
                this.backgroundImage = image;
                fireChartChanged();
            }
        }
        else {
            if (image != null) {
                this.backgroundImage = image;
                fireChartChanged();
            }
        }
    }

    public int getBackgroundImageAlignment() {
        return this.backgroundImageAlignment;
    }

    public void setBackgroundImageAlignment(int alignment) {
        if (this.backgroundImageAlignment != alignment) {
            this.backgroundImageAlignment = alignment;
            fireChartChanged();
        }
    }   

    public float getBackgroundImageAlpha() {
        return this.backgroundImageAlpha;
    }

    public void setBackgroundImageAlpha(float alpha) {
        if (this.backgroundImageAlpha != alpha) {
            this.backgroundImageAlpha = alpha;
            fireChartChanged();
        }
    }      

    public boolean isNotify() {
        return this.notify;
    }

    public void setNotify(boolean notify) {
        this.notify = notify;
        if (notify) {
            notifyListeners(new ChartChangeEvent(this));
        }
    }    

    public void draw(Graphics2D g2, Rectangle2D area) {
        draw(g2, area, null, null);
    }

    public void draw(Graphics2D g2, Rectangle2D area, ChartRenderingInfo info) {
        draw(g2, area, null, info);
    }       

    public void draw(Graphics2D g2, Rectangle2D chartArea, Point2D anchor,
             ChartRenderingInfo info) {

        notifyListeners(new ChartProgressEvent(this, this,
                ChartProgressEventType.DRAWING_STARTED, 0));
        
        if (this.elementHinting) {
            Map<String, String> m = new HashMap<>();
            if (this.id != null) {
                m.put("id", this.id);
            }
            m.put("ref", "JFREECHART_TOP_LEVEL");            
            g2.setRenderingHint(ChartHints.KEY_BEGIN_ELEMENT, m);            
        }

        EntityCollection entities = null;
        if (info != null) {
            info.clear();
            info.setChartArea(chartArea);
            entities = info.getEntityCollection();
        }
        if (entities != null) {
            entities.add(new JFreeChartEntity((Rectangle2D) chartArea.clone(),
                    this));
        }   

       Shape savedClip = g2.getClip();
        g2.clip(chartArea);

        g2.addRenderingHints(this.renderingHints);

        if (this.backgroundPaint != null) {
            g2.setPaint(this.backgroundPaint);
            g2.fill(chartArea);
        }

        if (this.backgroundImage != null) {
            Composite originalComposite = g2.getComposite();
            g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER,
                    this.backgroundImageAlpha));
            Rectangle2D dest = new Rectangle2D.Double(0.0, 0.0,
                    this.backgroundImage.getWidth(null),
                    this.backgroundImage.getHeight(null));
            Align.align(dest, chartArea, this.backgroundImageAlignment);
            g2.drawImage(this.backgroundImage, (int) dest.getX(),
                    (int) dest.getY(), (int) dest.getWidth(),
                    (int) dest.getHeight(), null);
            g2.setComposite(originalComposite);
        }     

        if (isBorderVisible()) {
            Paint paint = getBorderPaint();
            Stroke stroke = getBorderStroke();
            if (paint != null && stroke != null) {
                Rectangle2D borderArea = new Rectangle2D.Double(
                        chartArea.getX(), chartArea.getY(),
                        chartArea.getWidth() - 1.0, chartArea.getHeight()
                        - 1.0);
                g2.setPaint(paint);
                g2.setStroke(stroke);
                g2.draw(borderArea);
            }
        } 

        Rectangle2D nonTitleArea = new Rectangle2D.Double();
        nonTitleArea.setRect(chartArea);
        this.padding.trim(nonTitleArea);

        if (this.title != null && this.title.isVisible()) {
            EntityCollection e = drawTitle(this.title, g2, nonTitleArea,
                    (entities != null));
            if (e != null && entities != null) {
                entities.addAll(e);
            }
        }    

        for (Title currentTitle : this.subtitles) {
            if (currentTitle.isVisible()) {
                EntityCollection e = drawTitle(currentTitle, g2, nonTitleArea,
                        (entities != null));
                if (e != null && entities != null) {
                    entities.addAll(e);
                }
            }
        }  

        Rectangle2D plotArea = nonTitleArea;

        PlotRenderingInfo plotInfo = null;
        if (info != null) {
            plotInfo = info.getPlotInfo();
        }
        this.plot.draw(g2, plotArea, anchor, null, plotInfo);
        g2.setClip(savedClip);
        if (this.elementHinting) {         
            g2.setRenderingHint(ChartHints.KEY_END_ELEMENT, Boolean.TRUE);            
        }

        notifyListeners(new ChartProgressEvent(this, this,
                ChartProgressEventType.DRAWING_FINISHED, 100));                                      
    }    

    private Rectangle2D createAlignedRectangle2D(Size2D dimensions,
            Rectangle2D frame, HorizontalAlignment hAlign,
            VerticalAlignment vAlign) {
        Objects.requireNonNull(hAlign, "hAlign");
        Objects.requireNonNull(vAlign, "vAlign");
        double x = Double.NaN;
        double y = Double.NaN;
        switch (hAlign) {
            case LEFT:
                x = frame.getX();
                break;
            case CENTER:
                x = frame.getCenterX() - (dimensions.width / 2.0);
                break;
            case RIGHT:
                x = frame.getMaxX() - dimensions.width;
                break;
            default:
                throw new IllegalStateException("Unexpected enum value " + hAlign);
        }
        switch (vAlign) {
            case TOP:
                y = frame.getY();
                break;
            case CENTER:
                y = frame.getCenterY() - (dimensions.height / 2.0);
                break;
            case BOTTOM:
                y = frame.getMaxY() - dimensions.height;
                break;
            default:
                throw new IllegalStateException("Unexpected enum value " + hAlign);
        }

        return new Rectangle2D.Double(x, y, dimensions.width,
                dimensions.height);
    }

    protected EntityCollection drawTitle(Title t, Graphics2D g2,
                                         Rectangle2D area, boolean entities) {

        Objects.requireNonNull(t, "t");
        Objects.requireNonNull(area, "area");
        Rectangle2D titleArea;
        RectangleEdge position = t.getPosition();
        double ww = area.getWidth();
        if (ww <= 0.0) {
            return null;
        }
        double hh = area.getHeight();
        if (hh <= 0.0) {
            return null;
        }
        RectangleConstraint constraint = new RectangleConstraint(ww,
                new Range(0.0, ww), LengthConstraintType.RANGE, hh,
                new Range(0.0, hh), LengthConstraintType.RANGE);
        Object retValue = null;
        BlockParams p = new BlockParams();
        p.setGenerateEntities(entities);
        if (position == RectangleEdge.TOP) {
            Size2D size = t.arrange(g2, constraint);
            titleArea = createAlignedRectangle2D(size, area,
                    t.getHorizontalAlignment(), VerticalAlignment.TOP);
            retValue = t.draw(g2, titleArea, p);
            area.setRect(area.getX(), Math.min(area.getY() + size.height,
                    area.getMaxY()), area.getWidth(), Math.max(area.getHeight()
                    - size.height, 0));
        } else if (position == RectangleEdge.BOTTOM) {
            Size2D size = t.arrange(g2, constraint);
            titleArea = createAlignedRectangle2D(size, area,
                    t.getHorizontalAlignment(), VerticalAlignment.BOTTOM);
            retValue = t.draw(g2, titleArea, p);
            area.setRect(area.getX(), area.getY(), area.getWidth(),
                    area.getHeight() - size.height);
        } else if (position == RectangleEdge.RIGHT) {
            Size2D size = t.arrange(g2, constraint);
            titleArea = createAlignedRectangle2D(size, area,
                    HorizontalAlignment.RIGHT, t.getVerticalAlignment());
            retValue = t.draw(g2, titleArea, p);
            area.setRect(area.getX(), area.getY(), area.getWidth()
                    - size.width, area.getHeight());
        } else if (position == RectangleEdge.LEFT) {
            Size2D size = t.arrange(g2, constraint);
            titleArea = createAlignedRectangle2D(size, area,
                    HorizontalAlignment.LEFT, t.getVerticalAlignment());
            retValue = t.draw(g2, titleArea, p);
            area.setRect(area.getX() + size.width, area.getY(), area.getWidth()
                    - size.width, area.getHeight());
        }
        else {
            throw new RuntimeException("Unrecognised title position.");
        }
        EntityCollection result = null;
        if (retValue instanceof EntityBlockResult) {
            EntityBlockResult ebr = (EntityBlockResult) retValue;
            result = ebr.getEntityCollection();
        }
        return result;
    }     

    public BufferedImage createBufferedImage(int width, int height) {
        return createBufferedImage(width, height, null);
    }    

    public BufferedImage createBufferedImage(int width, int height,
                                             ChartRenderingInfo info) {
        return createBufferedImage(width, height, BufferedImage.TYPE_INT_ARGB,
                info);
    } 

    public BufferedImage createBufferedImage(int width, int height,
            int imageType, ChartRenderingInfo info) {
        BufferedImage image = new BufferedImage(width, height, imageType);
        Graphics2D g2 = image.createGraphics();
        draw(g2, new Rectangle2D.Double(0, 0, width, height), null, info);
        g2.dispose();
        return image;
    }        

    public BufferedImage createBufferedImage(int imageWidth,
                                             int imageHeight,
                                             double drawWidth,
                                             double drawHeight,
                                             ChartRenderingInfo info) {

        BufferedImage image = new BufferedImage(imageWidth, imageHeight,
                BufferedImage.TYPE_INT_ARGB);
        Graphics2D g2 = image.createGraphics();
        double scaleX = imageWidth / drawWidth;
        double scaleY = imageHeight / drawHeight;
        AffineTransform st = AffineTransform.getScaleInstance(scaleX, scaleY);
        g2.transform(st);
        draw(g2, new Rectangle2D.Double(0, 0, drawWidth, drawHeight), null,
                info);
        g2.dispose();
        return image;
    }   

    public void handleClick(int x, int y, ChartRenderingInfo info) {
        this.plot.handleClick(x, y, info.getPlotInfo());
    }   

    public void addChangeListener(ChartChangeListener listener) {
        Objects.requireNonNull(listener, "listener");
        this.changeListeners.add(ChartChangeListener.class, listener);
    }    

    public void removeChangeListener(ChartChangeListener listener) {
        Objects.requireNonNull(listener, "listener");
        this.changeListeners.remove(ChartChangeListener.class, listener);
    }    

    public void fireChartChanged() {
        ChartChangeEvent event = new ChartChangeEvent(this);
        notifyListeners(event);
    }     

    protected void notifyListeners(ChartChangeEvent event) {
        if (this.notify) {
            Object[] listeners = this.changeListeners.getListenerList();
            for (int i = listeners.length - 2; i >= 0; i -= 2) {
                if (listeners[i] == ChartChangeListener.class) {
                    ((ChartChangeListener) listeners[i + 1]).chartChanged(
                            event);
                }
            }
        }
    }   

    public void addProgressListener(ChartProgressListener listener) {
        this.progressListeners.add(ChartProgressListener.class, listener);
    }

    public void removeProgressListener(ChartProgressListener listener) {
        this.progressListeners.remove(ChartProgressListener.class, listener);
    }         

    protected void notifyListeners(ChartProgressEvent event) {
        Object[] listeners = this.progressListeners.getListenerList();
        for (int i = listeners.length - 2; i >= 0; i -= 2) {
            if (listeners[i] == ChartProgressListener.class) {
                ((ChartProgressListener) listeners[i + 1]).chartProgress(event);
            }
        }
    }  

    @Override
    public void titleChanged(TitleChangeEvent event) {
        event.setChart(this);
        notifyListeners(event);
    }        

    @Override
    public void plotChanged(PlotChangeEvent event) {
        event.setChart(this);
        notifyListeners(event);
    }        

    @Override
    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }
        if (!(obj instanceof JFreeChart)) {
            return false;
        }
        JFreeChart that = (JFreeChart) obj;
        if (!this.renderingHints.equals(that.renderingHints)) {
            return false;
        }
        if (this.borderVisible != that.borderVisible) {
            return false;
        }
        if (!ObjectUtils.equal(this.borderStroke, that.borderStroke)) {
            return false;
        }
        if (!PaintUtils.equal(this.borderPaint, that.borderPaint)) {
            return false;
        }
        if (!this.padding.equals(that.padding)) {
            return false;
        }
        if (!ObjectUtils.equal(this.title, that.title)) {
            return false;
        }
        if (!ObjectUtils.equal(this.subtitles, that.subtitles)) {
            return false;
        }
        if (!ObjectUtils.equal(this.plot, that.plot)) {
            return false;
        }
        if (!PaintUtils.equal(
            this.backgroundPaint, that.backgroundPaint
        )) {
            return false;
        }
        if (!ObjectUtils.equal(this.backgroundImage,
                that.backgroundImage)) {
            return false;
        }
        if (this.backgroundImageAlignment != that.backgroundImageAlignment) {
            return false;
        }
        if (this.backgroundImageAlpha != that.backgroundImageAlpha) {
            return false;
        }
        if (this.notify != that.notify) {
            return false;
        }
        return true;
    }  

    private void writeObject(ObjectOutputStream stream) throws IOException {
        stream.defaultWriteObject();
        SerialUtils.writeStroke(this.borderStroke, stream);
        SerialUtils.writePaint(this.borderPaint, stream);
        SerialUtils.writePaint(this.backgroundPaint, stream);
    }     

    private void readObject(ObjectInputStream stream)
        throws IOException, ClassNotFoundException {
        stream.defaultReadObject();
        this.borderStroke = SerialUtils.readStroke(stream);
        this.borderPaint = SerialUtils.readPaint(stream);
        this.backgroundPaint = SerialUtils.readPaint(stream);
        this.progressListeners = new EventListenerList();
        this.changeListeners = new EventListenerList();
        this.renderingHints = new RenderingHints(
                RenderingHints.KEY_ANTIALIASING,
                RenderingHints.VALUE_ANTIALIAS_ON);
        this.renderingHints.put(RenderingHints.KEY_STROKE_CONTROL,
                RenderingHints.VALUE_STROKE_PURE);
        
        if (this.title != null) {
            this.title.addChangeListener(this);
        }

        for (int i = 0; i < getSubtitleCount(); i++) {
            getSubtitle(i).addChangeListener(this);
        }
        this.plot.addChangeListener(this);
    }   

    @Override
    public Object clone() throws CloneNotSupportedException {
        JFreeChart chart = (JFreeChart) super.clone();

        chart.renderingHints = (RenderingHints) this.renderingHints.clone();

        if (this.title != null) {
            chart.title = (TextTitle) this.title.clone();
            chart.title.addChangeListener(chart);
        }

        chart.subtitles = new ArrayList<>();
        for (int i = 0; i < getSubtitleCount(); i++) {
            Title subtitle = (Title) getSubtitle(i).clone();
            chart.subtitles.add(subtitle);
            subtitle.addChangeListener(chart);
        }

        if (this.plot != null) {
            chart.plot = (Plot) this.plot.clone();
            chart.plot.addChangeListener(chart);
        }

        chart.progressListeners = new EventListenerList();
        chart.changeListeners = new EventListenerList();
        return chart;
    }               		        	    		     	    	    	
}
    """

	file = File('JFreeChart.java')
	src_file = SourceFile(file)
	analyzer = StaticAnalyzer()
	code_elements = analyzer.reverse_engineering(src_file, src)    
	
	calls = []
	operations = []
	for c in code_elements:
	    if isinstance(c, Call):
	        calls.append(c)
	    elif isinstance(c, Operation):
	        operations.append(c)

	parser_expected_calls = {
		'plot.Plot.clone': 1,
		'title.TextTitle.clone': 1,
		'renderingHints.RenderingHints.clone': 1,
		'super.Object.clone': 1,
		'throws.CloneNotSupportedException.CloneNotSupportedException': 1,
		'SerialUtils.SerialUtils.readPaint': 2,
		'SerialUtils.SerialUtils.readStroke': 1,
		'stream.ObjectInputStream.defaultReadObject': 1,
		'throws.ClassNotFoundException.ClassNotFoundException': 1,
		'SerialUtils.SerialUtils.writePaint': 2,
		'SerialUtils.SerialUtils.writeStroke': 1,
		'SerialUtils.SerialUtils.writeStroke': 1,
		'stream.ObjectOutputStream.defaultWriteObject': 1,
		'throws.IOException.IOException': 2,
		'padding.RectangleInsets.equals': 1,
		'PaintUtils.PaintUtils.equal': 2,
		'ObjectUtils.ObjectUtils.equal': 5,
		'renderingHints.RenderingHints.equals': 1,
		'event.PlotChangeEvent.setChart': 1,
		'event.TitleChangeEvent.setChart': 1,
		'progressListeners.EventListenerList.getListenerList': 1,
		'progressListeners.EventListenerList.remove': 1,
		'progressListeners.EventListenerList.add': 1,
		'listeners.Object.length': 2,
		'changeListeners.EventListenerList.getListenerList': 1,
		'changeListeners.EventListenerList.remove': 1,
		'changeListeners.EventListenerList.add': 1,
		'plot.Plot.handleClick': 1,
		'g2.Graphics2D.transform': 1,
		'AffineTransform.AffineTransform.getScaleInstance': 1,
		'g2.Graphics2D.dispose': 2,
		'image.BufferedImage.createGraphics': 2,
		'new.BufferedImage.BufferedImage': 2,
		'BufferedImage.BufferedImage.TYPE_INT_ARGB': 2,
		'ebr.EntityBlockResult.getEntityCollection': 1,
		'new.RuntimeException.RuntimeException': 1,
		'HorizontalAlignment.HorizontalAlignment.LEFT': 1,
		'RectangleEdge.RectangleEdge.LEFT': 1,
		'size.Size2D.width': 3,
		't.Title.getVerticalAlignment': 2,
		'HorizontalAlignment.HorizontalAlignment.RIGHT': 1,
		'RectangleEdge.RectangleEdge.RIGHT': 1,
		'VerticalAlignment.VerticalAlignment.BOTTOM': 1,
		'Math.Math.max': 1,
		'area.Rectangle2D.getMaxY': 1,
		'size.Size2D.height': 3,
		'area.Rectangle2D.getY': 4,
		'Math.Math.min': 1,
		'area.Rectangle2D.getX': 4,
		'area.Rectangle2D.setRect': 4,
		't.Title.draw': 4,
		'VerticalAlignment.VerticalAlignment.TOP': 1,
		't.Title.getHorizontalAlignment': 2,
		't.Title.arrange': 4,
		'RectangleEdge.RectangleEdge.TOP': 1,
		'p.BlockParams.setGenerateEntities': 1,
		'new.BlockParams.BlockParams': 1,
		'LengthConstraintType.LengthConstraintType.RANGE': 2,
		'new.Range.Range': 2,
		'new.RectangleConstraint.RectangleConstraint': 1,
		'area.Rectangle2D.getHeight': 5,
		'area.Rectangle2D.getWidth': 5,
		't.Title.getPosition': 1,
		'frame.Rectangle2D.getMaxY': 1,
		'dimensions.Size2D.height': 3,
		'frame.Rectangle2D.getCenterY': 1,
		'frame.Rectangle2D.getY': 1,
		'new.IllegalStateException.IllegalStateException': 2,
		'frame.Rectangle2D.getMaxX': 1,
		'dimensions.Size2D.width': 3,
		'frame.Rectangle2D.getCenterX': 1,
		'frame.Rectangle2D.getX': 1,
		'Double.Double.NaN': 2,
		'ChartProgressEventType.ChartProgressEventType.DRAWING_FINISHED': 1,
		'Boolean.Boolean.TRUE': 1,
		'ChartHints.ChartHints.KEY_END_ELEMENT': 1,
		'g2.Graphics2D.setClip': 1,
		'plot.Plot.draw': 1,
		'info.ChartRenderingInfo.getPlotInfo': 2,
		'currentTitle.Title.isVisible': 1,
		'entities.EntityCollection.addAll': 2,
		'title.TextTitle.isVisible': 1,
		'padding.RectangleInsets.trim': 1,
		'nonTitleArea.Rectangle2D.setRect': 1,
		'g2.Graphics2D.draw': 1,
		'g2.Graphics2D.setStroke': 1,
		'chartArea.Rectangle2D.getHeight': 1,
		'chartArea.Rectangle2D.getWidth': 1, 
		'chartArea.Rectangle2D.getY': 1,
		'chartArea.Rectangle2D.getX': 1,
		'Rectangle2D.Rectangle2D.Double': 6,
		'dest.Rectangle2D.getHeight': 1,
		'dest.Rectangle2D.getWidth': 1,
		'dest.Rectangle2D.getY': 1,
		'dest.Rectangle2D.getX': 1,
		'g2.Graphics2D.drawImage': 1,
		'Align.Align.align': 1,
		'backgroundImage.Image.getHeight': 1,
		'backgroundImage.Image.getWidth': 1,
		'new.Rectangle2D.Rectangle2D': 6,
		'AlphaComposite.AlphaComposite.SRC_OVER': 1,
		'AlphaComposite.AlphaComposite.getInstance': 1,
		'g2.Graphics2D.setComposite': 2,
		'g2.Graphics2D.getComposite': 1,
		'g2.Graphics2D.fill': 1,
		'g2.Graphics2D.setPaint': 2,
		'g2.Graphics2D.addRenderingHints': 1,
		'g2.Graphics2D.clip': 1,
		'g2.Graphics2D.getClip': 1,
		'chartArea.Rectangle2D.clone': 1,
		'new.JFreeChartEntity.JFreeChartEntity': 1,
		'entities.EntityCollection.add': 1,
		'info.ChartRenderingInfo.getEntityCollection': 1,
		'info.ChartRenderingInfo.setChartArea': 1,
		'info.ChartRenderingInfo.clear': 1,
		'ChartHints.ChartHints.KEY_BEGIN_ELEMENT': 1,
		'g2.Graphics2D.setRenderingHint': 2,
		'm.Map.put': 2,
		'new.HashMap.HashMap': 1,
		'ChartProgressEventType.ChartProgressEventType.DRAWING_STARTED': 1,
		'new.ChartProgressEvent.ChartProgressEvent': 2,
		'backgroundImage.Image.equals': 1,
		'backgroundPaint.Paint.equals': 1,
		'RenderingHints.RenderingHints.VALUE_TEXT_ANTIALIAS_OFF': 1,
		'RenderingHints.RenderingHints.VALUE_TEXT_ANTIALIAS_ON': 1,
		'RenderingHints.RenderingHints.KEY_TEXT_ANTIALIASING': 2,
		'RenderingHints.RenderingHints.VALUE_ANTIALIAS_OFF': 1,
		'renderingHints.RenderingHints.get': 2,
		'subtitles.List.remove': 1,
		'subtitles.List.clear': 1,
		't.Title.removeChangeListener': 1,
		'subtitle.Title.addChangeListener': 3,
		'subtitles.List.get': 1,
		'new.IllegalArgumentException.IllegalArgumentException': 2,
		'subtitles.List.size': 1,
		'title.TextTitle.removeChangeListener': 1,
		'new.ChartChangeEvent.ChartChangeEvent': 4,
		'title.TextTitle.addChangeListener': 4,
		'new.TextTitle.TextTitle': 1,
		'legend.LegendTitle.addChangeListener': 1,
		'subtitles.List.add': 4,
		'RectangleEdge.RectangleEdge.BOTTOM': 2,
		'legend.LegendTitle.setPosition': 1,
		'Color.Color.WHITE': 1,
		'legend.LegendTitle.setBackgroundPaint': 1,
		'new.RectangleInsets.RectangleInsets': 1,
		'legend.LegendTitle.setMargin': 1,
		'new.LegendTitle.LegendTitle': 1,
		'new.ArrayList.ArrayList': 3,
		'plot.Plot.addChangeListener': 3,
		'RectangleInsets.RectangleInsets.ZERO_INSETS': 1,
		'Color.Color.BLACK': 1,
		'new.BasicStroke.BasicStroke': 1,
		'RenderingHints.RenderingHints.VALUE_STROKE_PURE': 2,
		'RenderingHints.RenderingHints.KEY_STROKE_CONTROL': 2,
		'renderingHints.RenderingHints.put': 4,
		'RenderingHints.RenderingHints.VALUE_ANTIALIAS_ON': 4,
		'RenderingHints.RenderingHints.KEY_ANTIALIASING': 4,
		'new.EventListenerList.EventListenerList': 6,
		'plot.Plot.setChart': 1,
		'Objects.Objects.requireNonNull': 12,
		'@.Override.@': 5,
		'RenderingHints.RenderingHints.Key': 1,
		'new.RenderingHints.RenderingHints': 3,
		'Align.Align.FIT': 2,
		'UIManager.UIManager.getColor': 1,
		'Font.Font.BOLD': 1,
		'new.Font.Font': 1,
		'implements.implements.Cloneable': 1,
		'implements.implements.Serializable': 1,
		'implements.implements.PlotChangeListener': 1,
		'implements.implements.TitleChangeListener': 1,
		'implements.implements.Drawable': 1,
	}

	expected_calls = {}
	for c in parser_expected_calls:
		call_caller = c.split('.')
		if len(call_caller) > 2:
			key = f'{call_caller[1]}.{call_caller[2]}'
			expected_calls[key] = 1
		else:
			expected_calls[c] = 1

	parser_expected_operations = {
		'public.JFreeChart.clone': 1,
		'public.JFreeChart.equals': 1,
		'public.JFreeChart.plotChanged': 1,
		'public.JFreeChart.titleChanged': 1,
		'public.JFreeChart.removeProgressListener': 1,
		'public.JFreeChart.addProgressListener': 1,
		'protected.JFreeChart.notifyListeners': 2,
		'public.JFreeChart.fireChartChanged': 1,
		'public.JFreeChart.removeChangeListener': 1,
		'public.JFreeChart.addChangeListener': 1,
		'public.JFreeChart.handleClick': 1,
		'public.JFreeChart.createBufferedImage': 4,
		'protected.JFreeChart.drawTitle': 1,
		'public.JFreeChart.draw': 3,
		'public.JFreeChart.setNotify': 1,
		'public.JFreeChart.isNotify': 1,
		'public.JFreeChart.setBackgroundImageAlpha': 1,
		'public.JFreeChart.getBackgroundImageAlpha': 1,
		'public.JFreeChart.setBackgroundImageAlignment': 1,
		'public.JFreeChart.getBackgroundImageAlignment': 1,
		'public.JFreeChart.setBackgroundImage': 1,
		'public.JFreeChart.getBackgroundImage': 1,
		'public.JFreeChart.setBackgroundPaint': 1,
		'public.JFreeChart.getBackgroundPaint': 1,
		'public.JFreeChart.setTextAntiAlias': 2,
		'public.JFreeChart.getTextAntiAlias': 1,
		'public.JFreeChart.setAntiAlias': 1,
		'public.JFreeChart.getAntiAlias': 1,
		'public.JFreeChart.getPlot': 1,
		'public.JFreeChart.removeSubtitle': 1,
		'public.JFreeChart.clearSubtitles': 1,
		'public.JFreeChart.addSubtitle': 2,
		'public.JFreeChart.getSubtitle': 1,
		'public.JFreeChart.getSubtitleCount': 1,
		'public.JFreeChart.setSubtitles': 1,
		'public.JFreeChart.getSubtitles': 1,
		'public.JFreeChart.removeLegend': 1,
		'public.JFreeChart.getLegend': 2,
		'public.JFreeChart.addLegend': 1,
		'public.JFreeChart.setTitle': 1,
		'public.JFreeChart.getTitle': 1,
		'public.JFreeChart.setPadding': 1,
		'public.JFreeChart.getPadding': 1,
		'public.JFreeChart.setBorderPaint': 1,
		'public.JFreeChart.getBorderPaint': 1,
		'public.JFreeChart.setBorderStroke': 1,
		'public.JFreeChart.getBorderStroke': 1,
		'public.JFreeChart.setBorderVisible': 1,
		'public.JFreeChart.isBorderVisible': 1,
		'public.JFreeChart.setRenderingHints': 1,
		'public.JFreeChart.getRenderingHints': 1,
		'public.JFreeChart.setElementHinting': 1,
		'public.JFreeChart.getElementHinting': 1,
		'public.JFreeChart.setID': 1,
		'public.JFreeChart.getID': 1,
		'public.JFreeChart.isCompatibleValue': 1,
		'final.public.static.JFreeChart.KEY_SUPPRESS_SHADOW_GENERATION': 1,
		'final.public.static.JFreeChart.DEFAULT_BACKGROUND_IMAGE_ALPHA': 1,
		'final.public.static.JFreeChart.DEFAULT_BACKGROUND_IMAGE_ALIGNMENT': 1,
		'final.public.static.JFreeChart.DEFAULT_BACKGROUND_IMAGE': 1,
		'final.public.static.JFreeChart.DEFAULT_BACKGROUND_PAINT': 1,
		'final.public.static.JFreeChart.DEFAULT_TITLE_FONT': 1,
		'public.JFreeChart.JFreeChart': 3,
		'public.extends.JFreeChart': 1,
	}	

	expected_operations = {}
	for c in parser_expected_operations:
		operation_modifiers = c.split('.')
		key = f'{operation_modifiers[-2]}.{operation_modifiers[-1]}'
		expected_operations[key] = 1

	calls_dict = {}
	for c in calls:
		key = c.name
		if key not in calls_dict:
			calls_dict[key] = 0 
		calls_dict[key] += 1

	for key in expected_calls:
		assert key in calls_dict
		assert key in expected_calls
		assert calls_dict[key] == expected_calls[key]

	operations_dict = {}
	for o in operations:
		key = o.name
		if key not in operations_dict:
			operations_dict[key] = 0 
		operations_dict[key] += 1

	for key in expected_operations:
		assert key in operations_dict
		assert key in expected_operations
		assert operations_dict[key] == expected_operations[key]		
