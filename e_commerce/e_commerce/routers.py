# # e_commerce/routers.py

# class ProductAppRouter:
#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'product':
#             return 'product_db'
#         return None

#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'product':
#             return 'product_db'
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         if app_label == 'product':
#             return db == 'product_db'
#         return db == 'default'
