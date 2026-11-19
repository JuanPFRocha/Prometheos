from django.shortcuts import render, redirect
from usuario.models import *
from .forms import *

def bombeiro(request):
    bombeiros = Bombeiro.objects.all().order_by("-matricula")

    filtros = {
        "codigo" : request.GET.get("codigo", ""),
        "nome" : request.GET.get("nome", ""),
        "email" : request.GET.get("email", ""),
        "estatus" : request.GET.get("estatus", "")
    }

    if filtros["codigo"]:
        bombeiros = bombeiros.filter(matricula=filtros["codigo"])
    if filtros["nome"]:
        bombeiros = bombeiros.filter(id_usuario__nome=filtros["nome"])
    if filtros["email"]:
        bombeiros = bombeiros.filter(id_usuario__email=filtros["email"])
    if filtros["estatus"]:
        bombeiros = bombeiros.filter(estatus=filtros["estatus"])

    contexto = {
        "bombeiros" : bombeiros,
        "filtros" : filtros,
        "estatus_opcoes" : Bombeiro._meta.get_field("estatus").choices
    }


    return render(request, 'usuarios/bombeiros.html', contexto)
def editaBombeiro(request, matricula=None):
    bombeiro = Bombeiro.objects.get(pk=matricula)
    form = BombeiroEdicaoForm(request.POST or None, instance=bombeiro.id_usuario)

    if form.is_valid():
        form.save()
        return redirect('bombeiro')

    return render(request, 'usuarios/editaBombeiro.html', {"form" : form})
