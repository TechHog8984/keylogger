import json
import keyboard

configfile = open('config.json', 'r')
if configfile:
    try:
        config = json.loads(configfile.read())
        whitelistedkeys = config.get('keys')
        stopkey = config.get('stopkey')
    except Exception as exception:
        print(exception)

if not stopkey or len(stopkey) < 1:
    print('no stopkey, so End is being used')

if whitelistedkeys:
    timesdown = {}
    timesup = {}

    untilkey = 'End'
    try:
        untilkey = len(stopkey) > 0 and stopkey or 'End'
    except: pass
    record = keyboard.record(until = untilkey)

    for i in record:
        string = str(i)
        length = len(string)

        firstsub = string[14:length - 1]
        upsub = firstsub[len(firstsub) - 2:len(firstsub)]
        downsub = firstsub[len(firstsub) - 4:len(firstsub)]

        key = None
        method = None

        if upsub == 'up':
            key = firstsub[0:len(firstsub) - 3]
            method = 'up'
        elif downsub == 'down':
            key = firstsub[0:len(firstsub) - 5]
            method = 'down'

        if key and key in whitelistedkeys and method:
            print(key, timesup.get(key))
            print(key, timesdown.get(key))
            if not timesup.get(key):
                timesup[key] = 0
            if not timesdown.get(key):
                timesdown[key] = 0
            tu = timesup.get(key) or 0
            td = timesdown.get(key) or 0
            if method == 'up':
                tu += 1
            elif method == 'down':
                td += 1
            timesup[key] = tu
            timesdown[key] = td

    for i in timesdown:
        print(f'key {i} was held down {timesdown[i]} time(s)')
    for i in timesup:
        print(f'key {i} was released {timesup[i]} time(s)')
else:
    print('couldn\'t get whitelisted keys. check json file')
