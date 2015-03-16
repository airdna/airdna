# coding: utf-8
from datetime import timedelta, datetime, date
from flask import session, abort, flash, redirect, url_for, g
from permission import Rule
from ..models import db, User, Piece


class VisitorRule(Rule):
    def check(self):
        return 'user_id' not in session

    def deny(self):
        return redirect(url_for('site.index'))


class UserRule(Rule):
    def check(self):
        return 'user_id' in session

    def deny(self):
        return redirect(url_for('account.signin'))


class AdminRule(Rule):
    def base(self):
        return UserRule()

    def check(self):
        user_id = int(session['user_id'])
        user = User.query.filter(User.id == user_id).first()
        return user and user.is_admin

    def deny(self):
        abort(403)


class CollectionOwnerRule(Rule):
    def __init__(self, collection):
        self.collection = collection
        super(CollectionOwnerRule, self).__init__()

    def base(self):
        return UserRule()

    def check(self):
        return self.collection and self.collection.user_id == g.user.id

    def deny(self):
        abort(403)


class PieceOwnerRule(Rule):
    def __init__(self, piece):
        self.piece = piece
        super(PieceOwnerRule, self).__init__()

    def base(self):
        return UserRule()

    def check(self):
        return self.piece and self.piece.user_id == g.user.id

    def deny(self):
        abort(403)


class PieceAddRule(Rule):
    def base(self):
        return UserRule()

    def check(self):
        today_pieces_count = g.user.created_pieces.filter(
            db.func.date(Piece.created_at) == date.today()).count()
        return today_pieces_count < 2

    def deny(self):
        abort(403)


class PieceOwnerEditRule(Rule):
    def __init__(self, piece):
        self.piece = piece
        super(PieceOwnerEditRule, self).__init__()

    def base(self):
        return PieceOwnerRule(self.piece)

    def check(self):
        return self.piece.created_at > datetime.now() - timedelta(minutes=20)

    def deny(self):
        abort(403)