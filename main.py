import os, sys
import json
import threading

from config_control import initialize_server
server_configuration = initialize_server()

if server_configuration['dpm_module_location'] == 'YOUR_DPM_MODULE_ABSOLUTE_PATH':
    raise NotImplementedError("configuration에 maplestory_dpm_calc 레포의 path를 넣어주세요.")

import dpmModule.kernel.core as core

import dpmModule.character.characterTemplate as CT
import dpmModule.character.characterKernel as ck

import dpmModule.jobs as maplejobs
import dpmModule.util.optimizer as optimizer
import dpmModule.util.dpmgenerator as dpmgenerator
import dpmModule.util.extractMetadata as ex_meta
import dpmModule.util.dpmgenerator as dpmgen

from flask import Flask, request, session, render_template, url_for, redirect


server_run_on_dev = (server_configuration["run_type"] == "dev")

jobMap = maplejobs.jobMap
jobList = maplejobs.jobList
jobListOrder = maplejobs.jobListOrder

def getJobAndName(size = 6):
    ''' Returns linkname, korean pair.
    '''
    retli = []
    for i in range(0,len(jobListOrder),size):
        retli.append([[k,jobList[k]] for k in jobListOrder[i:i+size]])
    return retli

app = Flask(__name__, static_folder='templates/')

@app.route('/ajax/404')
def pageNotFound():
    return render_template('pageNotFound.html')

@app.route('/ajax/process2', methods = ['POST'])
def process2():
    if server_run_on_dev:
        jsonData=request.get_json()
        
        ulevel = jsonData["ulevel"]
        en_job = jsonData["job"]   
        ko_job = maplejobs.jobList[en_job]
        interface = dpmgen.DpmInterface()
        return json.dumps(interface.calculate_job(ko_job, int(ulevel), runtime = 480*1000))

@app.route('/4fd5d7a6b035457953addb5ae410001d.png')
def static_file():
    return app.send_static_file('4fd5d7a6b035457953addb5ae410001d.png')

@app.route('/bundle.js')
def bd():
    return app.send_static_file('bundle.js')

@app.route('/')
def redirection():
    return redirect(url_for('root', path='indiv/archmageFb'))

@app.route('/<path:path>')
def root(path):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    ip = "127.0.0.1"
    #ip='0.0.0.0'
    port = 8080 #For inner - local communication
    app.debug = True
    app.run(host=ip, port=port)
    #app.run(host=os.getenv('IP', ip),port=int(os.getenv('PORT', port)))