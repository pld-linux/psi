#include "richlistview.h"
#include <qsimplerichtext.h>
#include <qpainter.h>
#include <qpixmap.h>
#include <qapplication.h>

RichListViewItem::RichListViewItem( QListView * parent ):
QListViewItem(parent)
{
	v_rt = 0;
	v_selected = false;
}

RichListViewItem::RichListViewItem( QListViewItem * parent ):
QListViewItem(parent)
{
	v_rt = 0;
	v_selected = false;
}

RichListViewItem::~RichListViewItem()
{
	if(v_rt)
		delete v_rt;
}

void RichListViewItem::setup()
{
	QListViewItem::setup();
	int h = height();

	QString txt = expandTemplate(0); // single column !!!
	if( txt.isEmpty() ){
		if(v_rt)
			delete v_rt;
		v_rt = 0;
		return;
	}
    
	const QListView* lv = listView();
	const QPixmap* px = pixmap(0);
	int left =  lv->itemMargin() + ((px)?(px->width() + lv->itemMargin()):0);

	v_active = lv->isActiveWindow();
	v_selected = isSelected();

	if ( v_selected  ) {
		txt = QString("<font color=\"%1\">").arg(listView()->colorGroup().color( QColorGroup::HighlightedText ).name()) + txt + "</font>";
	}
	
	if(v_rt)
		delete v_rt;
	v_rt = new QSimpleRichText(txt, lv->font());
	
	v_rt->setWidth(lv->columnWidth(0) - left - depth() * lv->treeStepSize());

	v_widthUsed = v_rt->widthUsed() + left;

	h = QMAX( h, v_rt->height() );

    if ( h % 2 > 0 )
	h++;
    setHeight( h );
}

void RichListViewItem::paintCell(QPainter *p, const QColorGroup &cg, int column, int width, int align)
{
	if(!v_rt){
		QListViewItem::paintCell(p, cg, column, width, align);
		return;
	}

	p->save();

	QListView* lv = listView();

	if ( isSelected() != v_selected || lv->isActiveWindow() != v_active) 
		setup();
	
	int r = lv->itemMargin();
	
	const QBrush *paper;
	// setup (colors, sizes, ...)
	if ( isSelected() ) {
		paper = &cg.brush( QColorGroup::Highlight );
	}
	else{
		const QColorGroup::ColorRole crole = QPalette::backgroundRoleFromMode( lv->viewport()->backgroundMode() );
		paper = &cg.brush( crole );
	}
	
	const QPixmap * px = pixmap( column );
	QRect pxrect;
	int pxw = 0;
	int pxh = 0;
	if(px) {
		pxw = px->width();
		pxh = px->height();
		pxrect = QRect(r, (height() - pxh)/2, pxw, pxh);
		r += pxw + lv->itemMargin();
	}

	if(px)
		pxrect.moveTop((height() - pxh)/2);

	// start drawing
	QRect rtrect(r, (height() - v_rt->height())/2, v_widthUsed, v_rt->height());
	v_rt->draw(p, rtrect.left(), rtrect.top(), rtrect, cg, paper);
	
	QRegion clip(0, 0, width, height());
	clip -= rtrect;
	p->setClipRegion(clip, QPainter::CoordPainter);
	p->fillRect( 0, 0, width, height(), *paper );

	if(px)
		p->drawPixmap(pxrect, *px);

	p->restore();
}

int RichListViewItem::widthUsed()
{
	return v_widthUsed;
}
