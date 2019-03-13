from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

from itertools import chain

from django.views import generic
from django.utils import timezone

from .models import Log

class IndexView(generic.ListView):
    template_name = 'elog/index.html'
    context_object_name = 'logs'

    def get_queryset(self):
        name = self.request.resolver_match.url_name
        if name == 'indexRunTypeSorted':
            main = Log.objects.exclude(run_type=-1).order_by('run_type', '-start_time')
            sub = Log.objects.filter(run_type=-1).order_by('run_type', '-start_time')
            return list(chain(main, sub))
        else:
            return Log.objects.order_by('-run_number', '-start_time')

def logForm(request):
    return render(request, 'elog/logForm.html', {'runTypeTextList': Log.runTypeText })

def logFormWithPrev(request):
    log = Log.objects.order_by('-id')
    if log:
        log = log[0]
        return render(request, 'elog/logForm.html', {"runTypeTextList": Log.runTypeText, "triggerTypeTextList": Log.triggerTypeText, "prevLog": log})
    else:
        return render(request, 'elog/logForm.html', {"runTypeTextList": Log.runTypeText, "triggerTypeTextList": Log.triggerTypeText})

def addLog(request):
    log = Log()
    log.run_number = int(request.POST['runNumber'])
    log.start_time = timezone.datetime.now()
    log.stop_time = timezone.datetime.now()
    log.fc73_begin = float(request.POST['fc73Begin'])
    log.fc74_begin = float(request.POST['fc74Begin'])
    log.fc75_begin = float(request.POST['fc75Begin'])
    log.ic_gas_pressure_begin = float(request.POST['icGasPressureBegin'])
    log.fc73_end = float(request.POST['fc73End'])
    log.fc74_end = float(request.POST['fc74End'])
    log.fc75_end = float(request.POST['fc75End'])
    log.ic_gas_pressure_end = float(request.POST['icGasPressureEnd'])
    log.scribe = request.POST['scribe']
    log.run_type = int(request.POST['runType'])
    log.trigger_type = int(request.POST['triggerType'])
    log.scaler1 = int(request.POST['scaler1'])
    log.scaler2 = int(request.POST['scaler2'])
    log.scaler3 = int(request.POST['scaler3'])
    log.title = request.POST['title']
    log.note = request.POST['note']
    log.save()
    return redirect('/elog/')

def modifyLog(request, pk):
    log = Log.objects.get(id=pk)
    log.run_number = int(request.POST['runNumber'])
    log.fc73_begin = float(request.POST['fc73Begin'])
    log.fc74_begin = float(request.POST['fc74Begin'])
    log.fc75_begin = float(request.POST['fc75Begin'])
    log.ic_gas_pressure_begin = float(request.POST['icGasPressureBegin'])
    log.fc73_end = float(request.POST['fc73End'])
    log.fc74_end = float(request.POST['fc74End'])
    log.fc75_end = float(request.POST['fc75End'])
    log.ic_gas_pressure_end = float(request.POST['icGasPressureEnd'])
    log.scribe = request.POST['scribe']
    log.run_type = int(request.POST['runType'])
    log.trigger_type = int(request.POST['triggerType'])
    log.scaler1 = int(request.POST['scaler1'])
    log.scaler2 = int(request.POST['scaler2'])
    log.scaler3 = int(request.POST['scaler3'])
    log.title = request.POST['title']
    log.note = request.POST['note']
    log.save()
    return redirect('/elog/')

class DetailView(generic.DetailView):
    model = Log
    template_name = 'elog/logDetail.html'
