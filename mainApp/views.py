from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Alertas, Informe001
from .forms import AlertForm, ResetPassForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.core.paginator import Paginator
import logging
from . import constants
# import tablib
# from import_export import resources
import json

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)-23s %(levelname)-8s %(name)-12s %(message)s'
            # 'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
})

logger = logging.getLogger(__name__)

# Create your views here.
def redirect_login(request):
    return redirect('login')
    # return render(request, '/login.html', {})

@login_required
def home(request):
    from math import trunc
    
    # Cargamos información de alertas pendientes
    alerts = Alertas.objects.filter(estado='P').order_by('-falta')

    num_registros=alerts.count
    paginator = Paginator(alerts, constants.N_REG_PAGINA)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Cargamos información para el grafico: "Deuda EE por segmentos - 2020"
    # results = Informe001.objects.raw("select mes \
    #     , max(id) as id \
    #     ,sum(case when segmento='B2B' then importe else 0 end) as imp_b2b \
    #     ,sum(case when segmento='B2C' then importe else 0 end) as imp_b2c \
    # from ddd_informe001 \
    # where anio=2020 and cemptitu=20 \
    # group by mes order by mes")

    categorias_datos = []
    serieB2B_datos = []
    serieB2C_datos = []
    # for result in results:
    #     # logger.debug('mes:'+ str(result.mes) + '- seg:'+ result.segmento + '- imp:'+ str(result.importe))
    #     categorias_datos.append('2020%s' % str(f'{result.mes:02}'))
    #     serieB2B_datos.append(trunc(result.imp_b2b))
    #     serieB2C_datos.append(trunc(result.imp_b2c))
    
    # logger.debug(categorias_datos)
    # logger.debug(serieB2B_datos)
    # logger.debug(serieB2C_datos)
    
    serieB2B = {
        'name': 'B2B',
        'data': serieB2B_datos,
        'color': 'blue'
    }
    
    serieB2C = {
        'name': 'B2C',
        'data': serieB2C_datos,
        'color': 'green'
    }

    chart = {
        'chart': {'type': 'line'},
        'title': {'text': 'Deuda EE por segmento - 2020', 'align': 'left'},
        'xAxis': {'categories': categorias_datos},
        'series': [serieB2B, serieB2C]
    }

    dump = json.dumps(chart)

    # Próxima gráfica: Facturación EE por segmentos - 2020
    

    return render(request, 'mainApp/home.html', {'alerts':page_obj, 'home_page':'active', 'num_registros':num_registros, 'chart': dump})

@login_required
def examples(request):
    logger.info('Logger, Iniciando view: examples')
    return render(request, 'mainApp/prueba.html', {'examples_page':'active'})

@login_required
def alert_detail(request, pk):
    alert = get_object_or_404(Alertas, pk=pk)
    if request.method == "POST":
        form = AlertForm(request.POST, instance=alert)
        if form.is_valid():
            alert = form.save()
            alert.estado = 'R'
            alert.ffin = timezone.now()
            alert.save()
            return redirect('alerts')
    else:
        form = AlertForm(instance=alert)
    return render(request, 'mainApp/alert_detail.html', {'form': form})

@login_required
def reset_pass(request):
    form = ResetPassForm()
    if request.method == 'POST':
        # logger.debug('Request POST')
        form = ResetPassForm(request.POST)
        if form.is_valid():
            # logger.debug('Formulario es valido')
            data = form.cleaned_data

            if data.get('pass_user')!=data.get('pass_confirm'):
                # logger.debug(form)
                return render(request, 'mainApp/reset_pass.html', {'dropdown_page':'active', 'form': form, 'error':'Las claves deben coincidir'})

            logger.debug('User: ' + str(request.user))
            
            user = User.objects.get(username=request.user)
            # logger.debug('Objeto USER recuperado')
            # logger.debug('Nuevo pass: ' + str(data.get('pass_user')))
            
            user.set_password(data.get('pass_user'))
            user.save()
            # logger.debug('User modificado')

            # Hacemos login para que no nos redireccione a la página de login
            user = authenticate(username=request.user, password=data.get('pass_user'))
            if user is not None:
                login(request, user)
                return render(request, 'mainApp/reset_pass_done.html', {'dropdown_page':'active', 'mensaje':'La contraseña se ha cambiado con éxito'})
            else:
                return redirect('home')
    return render(request, 'mainApp/reset_pass.html', {'form': form, 'dropdown_page':'active'})

@login_required
def alerts(request):
    """
    if request.method == 'GET':
        findpass = request.GET.get('q','')
        logger.debug(request.GET['q'])
        findpass = ''
        alerts = Alertas.objects.filter(Q(titulo__contains=findpass) | Q(descrip__contains=findpass) | Q(idAlert__contains=findpass)).order_by('-falta')
    else:
        findpass = ''
        alerts = Alertas.objects.order_by('-falta')
    """
    
    findpass = request.GET.get('q','')
    alerts = Alertas.objects.filter(Q(titulo__contains=findpass) | Q(descrip__contains=findpass) | Q(idAlert__contains=findpass)).order_by('-falta')

    num_registros=alerts.count
    paginator = Paginator(alerts, constants.N_REG_PAGINA)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'mainApp/alerts.html', {'alerts':page_obj, 'dropdown_page':'active', 'findpass':findpass, 'numreg': num_registros})

@login_required
def load_file(request):

    # if request.method == 'POST':
    #     # mensaje = "El fichero ha sido cargado correctamente"
        
    #     inf_resource = resources.modelresource_factory(model=Informe001)() # to take the model as a reference
    #     new_events = request.FILES['csv_file'] # to get the file
    #     # this part is to add the a column with the user id
    #     dataset = tablib.Dataset(
    #         headers=['anio', 'mes', 'cemptitu', 'ddd_grp1', 'importe']
    #     ).load(new_events.read().decode('utf-8'), format='csv')
    #     """
    #     dataset.append_col(
    #         col=tuple(f'{user_id}' for _ in range(dataset.height)),
    #         header='user_id'
    #     )
    #     """
    #     result = inf_resource.import_data(dataset, dry_run=True)  # Test the data import

    #     if not result.has_errors():
    #         logger.debug("No se han producido errores")
    #         mensaje = "El fichero ha sido cargado correctamente"
    #         inf_resource.import_data(dataset, dry_run=False)  # Actually import now
    #     else:
    #         logger.debug("Se han producido errores")
    #         mensaje = "El fichero no ha sido cargado debido a errores"

        
    # else:
    #     mensaje = ""
    mensaje = "La carga de ficheros se ha deshabilitado temporalmente"

    return render (request, 'mainApp/load_file.html', {'dropdown_page':'active', "mensaje":mensaje})