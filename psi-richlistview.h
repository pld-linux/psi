#ifndef RICHLISTVIEW_H
#define RICHLISTVIEW_H

#include "qlistview.h"
class QSimpleRichText;
class RichListViewItem : public QListViewItem  
{
	int v_widthUsed;
	bool v_selected, v_active;
	QSimpleRichText* v_rt;
protected:
	virtual void paintCell( QPainter * p, const QColorGroup & cg, int column, int width, int align );	
	virtual QString expandTemplate(int column = 0) { return QString::null;};
public:
	RichListViewItem( QListView * parent );
	RichListViewItem( QListViewItem * parent );
    virtual void setup();
	virtual ~RichListViewItem();
	int widthUsed();
};

#endif
