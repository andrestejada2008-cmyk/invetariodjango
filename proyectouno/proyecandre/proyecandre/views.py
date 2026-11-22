from urllib import request

from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import connection
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render


from proyecandre.models import Proveedor
from proyecandre.models import Producto

def home(request):
    if request.user.is_authenticated:
        return render(request,'Proveedor/home.html')
    else:
        return redirect('/User/login')

def logint(request):
    if request.method=="POST": #validar que viene por post
        if request.POST.get('usu') and request.POST.get('pass'):
            user=authenticate(username=request.POST.get('usu'), password=request.POST.get('pass'))
            if user is not None:
                login(request, user)
                return redirect("/")
                #print('correcto')
            else:
                mensajeerror="Usuario o contraseña incorrecta, intente de nuevo"
                return render(request,'Usuarios/login.html', {'mensajeerror': mensajeerror})
                #print('incorrecto,')
    return render(request,'Usuarios/login.html')



def Registeruse(request):
    if request.method=="POST": #validar que viene por post
        if request.POST.get('user') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('email') and request.POST.get('pass'):
            #validar que todoslos campos viene llenos
            Usuario=User.objects.create_user(request.POST.get('user'),
                                             request.POST.get('email'),
                                             request.POST.get('pass') )
            Usuario.first_name=request.POST.get('nombre')
            Usuario.last_name=request.POST.get('apellido')
            Usuario.save()
            #nombre del procedimiento almacenado
            return redirect('/User/login')



def logoutuser(request):
    logout(request)
    return redirect('/User/login')

def Proinsertar(request):
    if request.method=="POST": #validar que viene por post
        if request.POST.get('nombre') and request.POST.get('direccion') and request.POST.get('nit') and request.POST.get('email') and request.POST.get('observaciones'):
            #validar que todos los campos viene llenos
            nombre=request.POST.get('nombre')
            direccion=request.POST.get('direccion')
            nit=request.POST.get('nit')
            email=request.POST.get('email')
            observaciones=request.POST.get('observaciones')
            insertar=connection.cursor()
            insertar.execute("call p_insertarproveedor(%s,%s,%s,%s,%s)", [nombre, direccion,nit,email,observaciones])
            #nombre del procedimiento almacenado
            return redirect('/Proveedor/mostrar')
        else:
            nombre=request.POST.get('nombre')
            direccion=request.POST.get('direccion')
            nit=request.POST.get('nit')
            email=request.POST.get('email')
            observaciones=request.POST.get('observaciones')
            mensa='Señor usuario falta datos'
            return render(request,'Proveedor/insertar.html',{'nombre':nombre,'direccion':direccion,
            'nit':nit,'email':email,'observaciones':observaciones,'mensa':mensa})

    else:
        return render(request,'Proveedor/insertar.html')


def Promostrar(request):
    mostrar=connection.cursor()
    mostrar.execute("call p_mostrarproveedores()")
        #nombre del procedimiento almacenado
    return render(request,'Proveedor/mostrar.html',{'mostrar': mostrar})


def Proeditar(request, idpro):
    if request.method=="POST": #validar que viene por post
        if request.POST.get('nombre') and request.POST.get('direccion') and request.POST.get('nit') and request.POST.get('email') and request.POST.get('observaciones'):
            #validar que todos los campos viene llenos
            nombre=request.POST.get('nombre')
            direccion=request.POST.get('direccion')
            nit=request.POST.get('nit')
            email=request.POST.get('email')
            observaciones=request.POST.get('observaciones')
            insertar=connection.cursor()
            insertar.execute("call p_editarproveedor(%s,%s,%s,%s,%s,%s)", [nombre, direccion,nit,email,observaciones,idpro])
            #nombre del procedimiento almacenado
            return redirect('/Proveedor/mostrar')
    else:
        proveedor=connection.cursor()
        proveedor.execute("call p_consuproveedor('"+idpro+"')")
        proveedor=proveedor.fetchone()
        # return render(request,'Proveedor/editar.html',{'prover':proveedor})
        return render(request,'Proveedor/editars.html',{'prover':proveedor})


def Proeliminarss(request, idpro):
    eliminar=connection.cursor()
    eliminar.execute("call p_eliminarproveedor(%s)", [idpro])
    #nombre del procedimiento almacenado
    return redirect('/Proveedor/mostrar')

def Proeliminar(request):
    idpro = request.POST.get('idprover')
    eliminar = connection.cursor()
    eliminar.execute("call p_eliminarproveedor(%s)", [idpro])
    # nombre del procedimiento almacenado
    return redirect('/Proveedor/mostrar')

def Produinsertar(request):
    if request.method == "POST":  # validar que viene por post
        if (
            request.POST.get('nombre')
            and request.POST.get('precio')
            and request.POST.get('fecha')
            and request.FILES.get('foto')
            and request.POST.get('cantidad')
            and request.POST.get('prover')
            and request.POST.get('descri')
        ):
            # validar que todos los campos vienen llenos
            producto = Producto()
            producto.nombre = request.POST.get('nombre')
            producto.precio = request.POST.get('precio')
            producto.foto = request.FILES['foto']
            # location dentro FileSystemStorage(location) ubicacion diferente
            image = FileSystemStorage()  # almacenar la foto en el sistema
            image.save(producto.foto.name, producto.foto)  # archivo de la foto
            producto.cantidad = request.POST.get('cantidad')
            producto.descripcion = request.POST.get('descri')
            producto.fecha = request.POST.get('fecha')
            producto.proveedor = Proveedor.objects.get(id=request.POST.get('prover'))
            producto.save()
            # nombre del procedimiento almacenado
            return redirect('/Producto/mostrar')
        else:
            nombre = request.POST.get('nombre')
            precio = request.POST.get('precio')
            foto = request.FILES.get('foto')
            cantidad = request.POST.get('cantidad')
            descripcion = request.POST.get('descri')
            fecha = request.POST.get('fecha')
            mensa = 'Señor usuario falta datos'
            return render(
                request,
                'Productos/insertarpro.html',
                {
                    'nombre': nombre,
                    'precio': precio,
                    'fecha': fecha,
                    'foto': foto,
                    'cantidad': cantidad,
                    'descripcion': descripcion,
                    'mensa': mensa,
                },
            )
    else:
        prover = Proveedor.objects.all()
        return render(request, 'Productos/insertarpro.html', {'provers': prover})


def Produmostrar(request):
    mostrar = Producto.objects.all()
    # mostrar = connection.cursor()
    # mostrar.execute("call p_mostrarproductos()")
    # nombre del procedimiento almacenado
    return render(request, 'Productos/mostrarpro.html', {'mostrar': mostrar})

def Produeditar(request, idpro):
    if request.method == "POST":  # validar que viene por post
        if request.POST.get('nombre') and request.POST.get('precio') and request.POST.get('fecha') and request.POST.get('cantidad') and request.POST.get('prover') and request.POST.get('descri'):
            # validar que todos los campos viene llenos
            producto = Producto()
            producto.id = idpro  # busque el id y lo actulice en vez de guardar nuevo
            producto.nombre = request.POST.get('nombre')
            producto.precio = request.POST.get('precio')
            try:
                if request.FILES['foto']:
                    producto.foto = request.FILES['foto']
                    # location dentro FileSystemStorage(location) ubicacion diferente
                    image = FileSystemStorage()   ##almacenar la foto en elsistema
                    image.delete(request.POST.get('fotoan'))
                    image.save(producto.foto.name, producto.foto)  # archivo de la foto
            except:
                producto.foto = request.POST.get('fotoan')
            producto.cantidad = request.POST.get('cantidad')
            producto.descripcion = request.POST.get('descri')
            producto.fecha = request.POST.get('fecha')
            producto.proveedor = Proveedor.objects.get(id=request.POST.get('prover'))
            producto.save()
            # nombre del procedimiento almacenado
            return redirect('/Producto/mostrar')
    else:
        prover = Proveedor.objects.all()
        # produc=Producto.objects.get(id=idpro)
        produc = Producto.objects.filter(id=idpro)
        # print(produc.proveedor)
        return render(request, 'Productos/editarpro.html', {'producs': produc, 'prover': prover})

def Produdetalle(request, idpro=None):
    # Implementa aquí la lógica de detalle o consulta del producto
    return JsonResponse({})

def Produeliminar(request):
    if request.method == "POST":
        producto = Producto()
        producto.id = request.POST.get('idprover')
        producto.delete()
        eliminafoto = FileSystemStorage()
        if request.POST.get('foto'):
            eliminafoto.delete(request.POST.get('foto'))
    return redirect('/Producto/mostrar')
