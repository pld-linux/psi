#ifndef RICHLISTVIEW_H
#define RICHLISTVIEW_H

#include "qlistview.h"
#include "common.h"
class RichListViewItem : public QListViewItem  
{
	int v_widthUsed;
protected:
	virtual void paintCell( QPainter * p, const QColorGroup & cg, int column, int width, int align );	
//	virtual QString expandTemplate(int column = 0) { return QString("<nobr>") + expandEntities(text(column)) + "</nobr>";};
	virtual QString expandTemplate(int column = 0) { return QString::null;};
public:
	RichListViewItem( QListView * parent );
	RichListViewItem( QListViewItem * parent );
	virtual ~RichListViewItem();
	int widthUsed();
};

#endif
