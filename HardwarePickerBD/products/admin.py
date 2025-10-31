from django.contrib import admin
from .models import CPU, MOBO, CPUCooler, RAM, Storage, PSU, GPU, CASE

# Register your models here.
class CPUAdmin(admin.ModelAdmin):
    save_as = True  # Enable "Save as new" feature

class MOBOAdmin(admin.ModelAdmin):
    save_as = True  # Enable "Save as new" feature

class CPUCoolerAdmin(admin.ModelAdmin):
    save_as = True  # Enable "Save as new" feature

class RAMAdmin(admin.ModelAdmin):
    save_as = True  # Enable "Save as new" feature

class StorageAdmin(admin.ModelAdmin):
    save_as = True  # Enable "Save as new" feature

class PSUAdmin(admin.ModelAdmin):
    save_as = True  # Enable "Save as new" feature

class GPUAdmin(admin.ModelAdmin):
    save_as = True  # Enable "Save as new" feature

class CASEAdmin(admin.ModelAdmin):
    save_as = True

# Register the models with their respective ModelAdmins
admin.site.register(CPU, CPUAdmin)
admin.site.register(MOBO, MOBOAdmin)
admin.site.register(CPUCooler, CPUCoolerAdmin)
admin.site.register(RAM, RAMAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(PSU, PSUAdmin)
admin.site.register(GPU, GPUAdmin)
admin.site.register(CASE, CASEAdmin)

from django.contrib import admin
from .models import CartItem, Order, OrderItem

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
