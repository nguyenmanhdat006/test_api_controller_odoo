import odoo
import json
import logging
from odoo.exceptions import ValidationError, AccessError
_logger = logging.getLogger(__name__)

class MyPetAPI(odoo.http.Controller):
    @odoo.http.route(['/pet/<dbname>/<id>'], type='http', auth="user", methods=['GET'], sitemap=False, cors='*', csrf=False)
    def get_pet(self, dbname, id, **kw):
        model_name = "my.pet"
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.http.request.env.uid, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                if not rec:
                    return json.dumps({
                        "status": "error",
                        "content": "Pet not found"
                    })
                response = {
                    "status": "ok",
                    "content": {
                        "id": rec.id,
                        "name": rec.name,
                        "nickname": rec.nickname,
                        "description": rec.description,
                        "age": rec.age,
                        "weight": rec.weight,
                        "dob": rec.dob.strftime('%d/%m/%Y') if rec.dob else False,
                        "gender": rec.gender,
                    }
                }
                return json.dumps(response)
        except AccessError:
            return json.dumps({
                "status": "error",
                "content": "Access denied"
            })
        except Exception as e:
            return json.dumps({
                "status": "error",
                "content": str(e)
            })

    @odoo.http.route(['/pet/<dbname>'], type='json', auth="user", methods=['POST'], csrf=False)
    def create_pet(self, dbname, **kw):
        model_name = "my.pet"
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.http.request.env.uid, {})
                
                # Get data from request
                data = kw.get('data', {})
                _logger.info("Received data: %s", data)
                
                # Validate required fields
                if not data.get('name'):
                    return {
                        "status": "error",
                        "content": "Name is required"
                    }
                
                # Create new pet
                new_pet = env[model_name].create(data)
                return {
                    "status": "ok",
                    "content": {
                        "id": new_pet.id,
                        "message": "Pet created successfully"
                    }
                }
        except AccessError:
            return {
                "status": "error",
                "content": "Access denied"
            }
        except Exception as e:
            _logger.error("Error creating pet: %s", str(e))
            return {
                "status": "error",
                "content": str(e)
            }

    @odoo.http.route(['/pet/<dbname>/<id>'], type='json', auth="user", methods=['PUT'], csrf=False)
    def update_pet(self, dbname, id, **kw):
        model_name = "my.pet"
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.http.request.env.uid, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                if not rec:
                    return {
                        "status": "error",
                        "content": "Pet not found"
                    }
                
                # Get data from request
                data = kw.get('data', {})
                _logger.info("Received data: %s", data)
                
                # Validate required fields if name is being updated
                if 'name' in data and not data['name']:
                    return {
                        "status": "error",
                        "content": "Name cannot be empty"
                    }
                
                rec.write(data)
                return {
                    "status": "ok",
                    "content": {
                        "message": "Pet updated successfully"
                    }
                }
        except AccessError:
            return {
                "status": "error",
                "content": "Access denied"
            }
        except Exception as e:
            _logger.error("Error updating pet: %s", str(e))
            return {
                "status": "error",
                "content": str(e)
            }

    @odoo.http.route(['/pet/<dbname>/<id>'], type='json', auth="user", methods=['DELETE'], csrf=False)
    def delete_pet(self, dbname, id, **kw):
        model_name = "my.pet"
        try:
            registry = odoo.modules.registry.Registry(dbname)
            with registry.cursor() as cr:
                env = odoo.api.Environment(cr, odoo.http.request.env.uid, {})
                rec = env[model_name].search([('id', '=', int(id))], limit=1)
                if not rec:
                    return {
                        "status": "error",
                        "content": "Pet not found"
                    }
                rec.unlink()
                return {
                    "status": "ok",
                    "content": {
                        "message": "Pet deleted successfully"
                    }
                }
        except AccessError:
            return {
                "status": "error",
                "content": "Access denied"
            }
        except Exception as e:
            _logger.error("Error deleting pet: %s", str(e))
            return {
                "status": "error",
                "content": str(e)
            }
