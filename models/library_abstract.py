from odoo import models, fields, api

class LibraryAbstract(models.AbstractModel):
    _name = 'library.audit.mixing'
    _description = 'Modelo abstracto'
    
    #test = fields.Char()
    
    @api.model
    def create(self, values):
        res = super().create(values)
        vals_audit = {
            'user_id': self.env.user.id, # Modelo 'res.users' en el campo, se le introduce una ID de usuario.
            'operation': 'create',
            'date': fields.Datetime.now(),
            'res_model': self._name,
            'res_id': res
            }
        print(self.env['library.book'].search([('name','=',values['name'])]).id)
        self.env['library.audit'].create(vals_audit) 
        return res

    
    def unlink(self):        
        for record in self:
            vals_audit = {
                'user_id': self.env.uid,
                'operation': 'unlink',
                'date': fields.Datetime.now(),
                'res_model': self._name,
                'res_id': self
                }
            
            res = super().unlink()  #super(self, record).unlink() # solo devuelve true si puede eliminar, error si no
            self.env['library.audit'].create(vals_audit)
        return res
    
    def write(self, values):
        res = super().write(values)
        vals_audit = {
            'user_id': self.env.uid,
            'operation': 'write',
            'date': fields.Datetime.now(),
            'res_model': self._name,
            'res_id': self
            }
        self.env['library.audit'].create(vals_audit)
        return res