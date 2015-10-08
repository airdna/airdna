# coding: utf-8
from datetime import date, timedelta
from flask import render_template, Blueprint, request, g
from ..models import Piece, Collection, CollectionKind

from ..utils import cache
mc = cache.cache

bp = Blueprint('site', __name__)


# @bp.route('/page/<int:page>')
# @bp.route('/', defaults={'page': 1})
# def index(page):
# """Index page."""
#     target_day = date.today() - timedelta(days=page - 1)
#     pieces = Piece.get_pieces_data_by_day(target_day)
#     if page == 1:
#         pre_page = None
#     else:
#         pre_page = page - 1
#     next_page = page + 1
#     return render_template('site/index.html', pieces=pieces, page=page, pre_page=pre_page,
#                            next_page=next_page)

@bp.route('/')
def index():
    """Index page."""
    today = date.today()
    today_pieces = Piece.get_pieces_data_by_day(today)
    yesterday = today - timedelta(days=1)
    yesterday_pieces = Piece.get_pieces_data_by_day(yesterday)
    the_day_before_yesterday = today - timedelta(days=2)
    the_day_before_yesterday_pieces = Piece.get_pieces_data_by_day(the_day_before_yesterday)
    if today_pieces['pieces'].count():
        first_piece = today_pieces['pieces'].first()
    elif yesterday_pieces['pieces'].count():
        first_piece = yesterday_pieces['pieces'].first()
    elif the_day_before_yesterday_pieces['pieces'].count():
        first_piece = the_day_before_yesterday_pieces['pieces'].first()
    else:
        first_piece = None
    start_date = (the_day_before_yesterday - timedelta(days=1)).strftime("%Y-%m-%d")
    return render_template('site/index.html', today_pieces=today_pieces,
                           yesterday_pieces=yesterday_pieces,
                           the_day_before_yesterday_pieces=the_day_before_yesterday_pieces,
                           first_piece=first_piece, start_date=start_date)


@bp.route('/about')
def about():
    """About page."""
    return render_template('site/about.html')


@bp.route('/search')
def search():
    return render_template('site/search.html')


@bp.route('/collections', defaults={'page': 1})
@bp.route('/collections/page/<int:page>')
def collections(page):
    kind_id = request.args.get('kind_id')
    current_kind = CollectionKind.query.get_or_404(kind_id) if kind_id else None
    collection_kinds = CollectionKind.query.order_by(CollectionKind.show_order.asc())
    if kind_id:
        collections = current_kind.collections
    else:
        collections = Collection.query
    collections = collections.order_by(Collection.created_at.desc()).paginate(page, 20)
    return render_template('site/collections.html', collections=collections,
                           collection_kinds=collection_kinds, kind_id=kind_id)


@bp.route('/test')
def test():
    from jinja2 import Markup
    from ..utils.helpers import generate_lcs_html

    return Markup(generate_lcs_html('ABCBDAB', 'BDCABA'))
