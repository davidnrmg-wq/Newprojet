from django.shortcuts import render, get_object_or_404
from .models import ProducaoCafe, Produtor
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import json

@login_required
def index(request):
    resultado = None
    if request.method == "POST":
        try:
            produtor_id = request.POST.get("produtor_id")
            terreno = float(request.POST.get("terreno", 0))
            pes = int(request.POST.get("pes", 0))
            
            # Trata a entrada de produção que pode vir com vírgula ou ponto
            producao_raw = request.POST.get("producao", "0").replace(",", ".")
            producao = float(producao_raw) if producao_raw else 0.0

            resultado = pes * producao

            # Se não houver produtor_id, busca ou cria um padrão
            if produtor_id:
                produtor = get_object_or_404(Produtor, id=produtor_id)
            else:
                produtor, _ = Produtor.objects.get_or_create(
                    nome="Produtor Padrão",
                    defaults={"cidade": "Não informada", "telefone": "00000000"}
                )

            ProducaoCafe.objects.create(
                usuario=request.user,
                produtor=produtor,
                terreno=terreno,
                pes=pes,
                producao_por_pe=producao,
                total=resultado
            )
        except (ValueError, TypeError):
            # Em caso de erro de conversão, poderíamos passar uma mensagem de erro ao template
            pass

    produtores = Produtor.objects.all()
    return render(request, "index.html", {
        "produtores": produtores,
        "resultado": resultado
    })

@login_required
def historico(request):
    dados = ProducaoCafe.objects.filter(usuario=request.user).select_related('produtor').order_by('-id')

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
