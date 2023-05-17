import json

from flask import request
from flask_restx import Api, Resource
from werkzeug.datastructures import MultiDict


from apps.api import blueprint
from apps.authentication.decorators import token_required

from apps.api.forms import *
from apps.models import *

api = Api(blueprint)


@api.route('/books/', methods=['POST', 'GET', 'DELETE', 'PUT'])
@api.route('/books/<int:model_id>/', methods=['GET', 'DELETE', 'PUT'])
class BookRoute(Resource):
    def get(self, model_id: int = None):
        if model_id is None:
            all_objects = Book.query.all()
            output = [{'id': obj.id, **BookForm(obj=obj).data}
                      for obj in all_objects]
        else:
            obj = Book.query.get(model_id)
            if obj is None:
                return {
                    'message': 'matching record not found',
                    'success': False
                }, 404
            output = {'id': obj.id, **BookForm(obj=obj).data}
        return {
            'data': output,
            'success': True
        }, 200

    @token_required
    def post(self):
        try:
            body_of_req = request.form
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}
        form = BookForm(MultiDict(body_of_req))
        if form.validate():
            try:
                obj = Book(**body_of_req)
                Book.query.session.add(obj)
                Book.query.session.commit()
            except Exception as e:
                return {
                    'message': str(e),
                    'success': False
                }, 400
        else:
            return {
                'message': form.errors,
                'success': False
            }, 400
        return {
            'message': 'record saved!',
            'success': True
        }, 200

    @token_required
    def put(self, model_id: int):
        try:
            body_of_req = request.form
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}

        to_edit_row = Book.query.filter_by(id=model_id)

        if not to_edit_row:
            return {
                'message': 'matching record not found',
                'success': False
            }, 404

        obj = to_edit_row.first()

        if not obj:
            return {
                'message': 'matching record not found',
                'success': False
            }, 404

        form = BookForm(MultiDict(body_of_req), obj=obj)
        if not form.validate():
            return {
                'message': form.errors,
                'success': False
            }, 404

        table_cols = [attr.name for attr in to_edit_row.__dict__[
            '_raw_columns'][0].columns._all_columns]

        for col in table_cols:
            value = body_of_req.get(col, None)
            if value:
                setattr(obj, col, value)
        Book.query.session.add(obj)
        Book.query.session.commit()
        return {
            'message': 'record updated',
            'success': True
        }

    @token_required
    def delete(self, model_id: int):
        to_delete = Book.query.filter_by(id=model_id)
        if to_delete.count() == 0:
            return {
                'message': 'matching record not found',
                'success': False
            }, 404
        to_delete.delete()
        Book.query.session.commit()
        return {
            'message': 'record deleted!',
            'success': True
        }, 200


@api.route('/users/', methods=['POST', 'GET', 'DELETE', 'PUT'])
@api.route('/users/<int:model_id>/', methods=['GET', 'DELETE', 'PUT'])
class UsersRoute(Resource):
    def get(self, model_id: int = None):
        if model_id is None:
            all_objects = Users.query.all()
            output = [
                {'id': obj.id, "name": obj.username, "total_invest": obj.total_invest, "change": obj.change, "interest_rate": obj.interest_rate, "current_balance": obj.current_balance, "balance_update_date": obj.balance_update_date} for obj in all_objects]
        elif model_id == 0:
            all_objects = Users.query.all()
            total_interest_rate = 0
            total_invest = 0
            total_balance = 0
            for obj in all_objects:
                total_interest_rate = total_interest_rate + obj.interest_rate
                total_invest = total_invest + obj.total_invest
                total_balance = total_balance + obj.current_balance
            output = [{'id': 'Total','total_interest_rate': round(total_interest_rate,8), 'total_invest':total_invest, 'total_balance':round(total_balance,2)}]
        else:
            obj = Users.query.get(model_id)
            if obj is None:
                return {
                    'message': 'matching record not found',
                    'success': False
                }, 404
            output = {'id': obj.id}
        return {
            'data': output,
            'success': True
        }, 200

    def post(self):
        try:
            body_of_req = request.form
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}
        form = UsersForm(MultiDict(body_of_req))
        if form.validate():
            try:
                obj = Users(**body_of_req)
                Users.query.session.add(obj)
                Users.query.session.commit()
            except Exception as e:
                return {
                    'message': str(e),
                    'success': False
                }, 400
        else:
            return {
                'message': form.errors,
                'success': False
            }, 400
        return {
            'message': 'record saved!',
            'success': True
        }, 200

    def put(self, model_id: int):
        try:
            body_of_req = request.form
            if not body_of_req:
                raise Exception()
        except Exception:
            if len(request.data) > 0:
                body_of_req = json.loads(request.data)
            else:
                body_of_req = {}

        to_edit_row = Users.query.filter_by(id=model_id)

        if not to_edit_row:
            return {
                'message': 'matching record not found',
                'success': False
            }, 404

        obj = to_edit_row.first()

        if not obj:
            return {
                'message': 'matching record not found',
                'success': False
            }, 404

        form = UsersForm(MultiDict(body_of_req), obj=obj)
        if not form.validate():
            return {
                'message': form.errors,
                'success': False
            }, 404

        table_cols = [attr.name for attr in to_edit_row.__dict__[
            '_raw_columns'][0].columns._all_columns]

        for col in table_cols:
            value = body_of_req.get(col, None)
            if value:
                setattr(obj, col, value)
        Users.query.session.add(obj)
        Users.query.session.commit()
        return {
            'message': 'record updated',
            'success': True
        }

    @token_required
    def delete(self, model_id: int):
        to_delete = Users.query.filter_by(id=model_id)
        if to_delete.count() == 0:
            return {
                'message': 'matching record not found',
                'success': False
            }, 404
        to_delete.delete()
        Users.query.session.commit()
        return {
            'message': 'record deleted!',
            'success': True
        }, 200
