#include "richlistview.h"
#include <qsimplerichtext.h>
#include <qpainter.h>
#include <qpixmap.h>
RichListViewItem::RichListViewItem( QListView * parent ):
QListViewItem(parent)
{
//	setMultiLinesEnabled(true);	
}

RichListViewItem::RichListViewItem( QListViewItem * parent ):
QListViewItem(parent)
{
//	setMultiLinesEnabled(true);	
}

RichListViewItem::~RichListViewItem()
{
}

void RichListViewItem::paintCell(QPainter *p, const QColorGroup &cg, int column, int width, int align)
{
	QString txt = expandTemplate(column);
	if(txt.isEmpty()){
		QListViewItem::paintCell(p, cg, column, width, align);
		return;
	}

	p->save();

	QListView* lv = listView();
	
	int r = lv->itemMargin();
	
	const QBrush *paper;
	int h = 0;
	// setup (colors, sizes, ...)
	if ( isSelected() ) {
		paper = &cg.brush( QColorGroup::Highlight );
		txt = QString("<font color=\"%1\">").arg(cg.color( QColorGroup::HighlightedText ).name()) + txt + "</font>";
	}
	else{
		const QColorGroup::ColorRole crole = QPalette::backgroundRoleFromMode( lv->viewport()->backgroundMode() );
		paper = &cg.brush( crole );
		txt = txt;
	}

	const QPixmap * px = pixmap( column );
	QRect pxrect;
	int pxw = 0;
	int pxh = 0;
	if(px) {
		pxw = px->width();
		pxh = px->height();
		h = QMAX(h, pxh + 2 * lv->itemMargin());
		pxrect = QRect(r, (h - pxh)/2, pxw, pxh);
		r += pxw + 1;
	}

	QSimpleRichText rt(txt, lv->font());
	rt.setWidth(width - r);
	int rth = rt.height();
	int rtw = v_widthUsed = rt.widthUsed();

	h = QMAX(h, rth);

	if(px)
		pxrect.moveTop((h - pxh)/2);

	// make height odd number
    if(h % 2 > 0)
		h++;

	if(height() != h)
		setHeight(h);
	
	// start drawing
	QRect rtrect(r, (h - rth)/2, rtw, rth);
	rt.draw(p, rtrect.left(), rtrect.top(), rtrect, cg, paper);
	
	QRegion clip(0, 0, width, h);
	clip -= rtrect;
	p->setClipRegion(clip, QPainter::CoordPainter);
	p->fillRect( 0, 0, width, h, *paper );

	if(px)
		p->drawPixmap(pxrect, *px);

	p->restore();
}

int RichListViewItem::widthUsed()
{
	return v_widthUsed;
}
