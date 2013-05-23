# -*- coding: utf-8 -*-

from . import db, BaseNameMixin

__all__ = ['NetworkLink', 'networkbar_data']


class NetworkLink(BaseNameMixin, db.Model):
    __tablename__ = 'networklink'

    #: URL to link to
    url = db.Column(db.Unicode(250), nullable=True)
    #: Is this a menu section separator?
    sep = db.Column(db.Boolean, default=False)
    #: Sequence number for ordering
    seq = db.Column(db.SmallInteger, nullable=False)
    #: Parent for submenus
    parent_id = db.Column(None, db.ForeignKey('networklink.id'), nullable=True)
    parent = db.relationship('NetworkLink', remote_side='NetworkLink.id',
        backref=db.backref('children', order_by=seq))


def dictify_networklink(link):
    return {'name': link.name,
            'title': link.title,
            'url': link.url,
            'sep': link.sep,
            'children': [dictify_networklink(l) for l in link.children] if link.children else None
        }


def networkbar_data():
    return dict(links=[dictify_networklink(l) for l in NetworkLink.query.all() if l.parent is None])