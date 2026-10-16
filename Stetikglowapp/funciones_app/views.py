from django.shortcuts import render, get_object_or_404, redirect
from .models import Sucursal, Inventario
from .forms import InventarioForm

def InventarioList(request, sucursal_id=None):
    sucursales = Sucursal.objects.all()
    
    if not sucursal_id and sucursales.exists():
        sucursal_actual = sucursales.first()
    elif sucursal_id:
        sucursal_actual = get_object_or_404(Sucursal, id=sucursal_id)
    else:
        sucursal_actual = None

    inventarios = Inventario.objects.filter(sucursal=sucursal_actual) if sucursal_actual else []

    context = {
        'sucursales': sucursales,
        'sucursal_actual': sucursal_actual,
        'inventarios': inventarios,
    }
    return render(request, 'inventariolista.html', context)

def InventarioCreate(request):
    if request.method == 'POST':
        form = InventarioForm(request.POST)
        if form.is_valid():
            inv = form.save()
            return redirect('inventario_list_sucursal', sucursal_id=inv.sucursal.id)
    else:
        form = InventarioForm()
    return render(request, 'inventarioFrom.html', {'form': form, 'titulo': 'Agregar Stock'})

def InventarioUpdate(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            inv = form.save()
            return redirect('inventario_list_sucursal', sucursal_id=inv.sucursal.id)
    else:
        form = InventarioForm(instance=inventario)
    return render(request, 'inventarioFrom.html', {'form': form, 'titulo': 'Editar Stock'})

def InventarioDelete(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    sucursal_id = inventario.sucursal.id
    if request.method == 'POST':
        inventario.delete()
        return redirect('inventario_list_sucursal', sucursal_id=sucursal_id)
    return render(request, 'inventarioDelete.html', {'inventario': inventario})