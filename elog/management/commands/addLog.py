from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings

from elog.models import Log

import pytz

class Command(BaseCommand):
    est = pytz.timezone(settings.TIME_ZONE)

    def add_arguments(self, parser):
        parser.add_argument('runnumber', type=int)
        parser.add_argument('toggletype')
        parser.add_argument('date')
        parser.add_argument('time')
        parser.add_argument('title', type=str, nargs='?', default='')
        parser.add_argument('epicChannels')

    def handle(self, *args, **options):
        date = options['date'].split('/')
        time = options['time'].split(':')
        writetime = self.est.localize(timezone.datetime(int(date[2]), int(date[0]), int(date[1]), int(time[0]), int(time[1]), int(time[2])))

        fc73 = 0;
        fc74 = 0;
        fc75 = 0;
        gasPressure = 0;

        epicChannelFile = open(options['epicChannels'], 'r')
        lines = epicChannelFile.readlines()
        for line in lines:
            column = line.split(':')
            if column[0] == 'FLTCHAN73':
                fc73 = float(column[1])
            elif column[0] == 'FLTCHAN74':
                fc74 = float(column[1])
            elif column[0] == 'FLTCHAN75':
                fc75 = float(column[1])
            elif column[0] == 'GAS':
                gasPressure = float(column[1])
        
        if options['toggletype'] == "begin":
            newEntry = Log(run_number=options['runnumber'], start_time=writetime, title=options['title'], fc73_begin=fc73, fc74_begin=fc74, fc75_begin=fc75, ic_gas_pressure_begin=gasPressure)
            newEntry.save()
        elif options['toggletype'] == "end":
            modifyEntry = Log.objects.get(run_number=int(options['runnumber']),stop_time__isnull=True)
            modifyEntry.stop_time = writetime
            modifyEntry.fc73_end = fc73
            modifyEntry.fc74_end = fc74
            modifyEntry.fc75_end = fc75
            modifyEntry.ic_gas_pressure_end = gasPressure
            modifyEntry.save()
