from django.shortcuts import render
from .models import ProducaoCafe
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json

@login_required
def index(request):
    if request.method == "POST":
        terreno = float(request.POST.get("terreno"))
        pes = int(request.POST.get("pes"))
        producao = float(request.POST.get("producao").replace(",","."))

        total = pes * producao

        ProducaoCafe.objects.create(
            usuario=request.user,
            terreno=terreno,
            pes=pes,
            producao_por_pe=producao,
            total=total
        )

        return render(request, "index.html", {"resultado": total})

    return render(request, "index.html")


@login_required
def historico(request):
    dados = ProducaoCafe.objects.filter(usuario=request.user).order_by('-id')

    totais = json.dumps([d.total for d in dados])
    labels = json.dumps([f"Registro {d.id}" for d in dados])

    return render(request, "historico.html", {
        "dados": dados,
        "totais": totais,
        "labels": labels
    })


@login_required
def dashboard(request):
    dados = ProducaoCafe.objects.filter(usuario=request.user)

    totais_lista = [d.total for d in dados]
    labels_lista = [f"Registro {d.id}" for d in dados]

    totais = json.dumps(totais_lista)
    labels = json.dumps(labels_lista)

    total_registros = dados.count()
    soma_total = dados.aggregate(Sum('total'))['total__sum'] or 0

    return render(request, "dashboard.html", {
        "totais": totais,
        "labels": labels,
        "total_registros": total_registros,
        "soma_total": soma_total
    })