import json
from datetime import datetime
import os
from subprocess import Popen, PIPE
import sys
#import psutil
import time

class main():
    def __init__(self):
        #Verifica o Sistema Operacional
        self.verify_system_host()       

        #Verifica se o ADB está instalado
        self.verify_installed_adb()    

        #Mata o processo
        #self.adb_kill()
        #Inicia o processo
        #self.adb_start()            

        #Verifica os dispisitivos conectados
        check_devices = self.verify_connect_devices()        
        if not check_devices:
            print("Nenhum dispositivo encontrado.")
            sys.exit()   
        else:
            self.choice_device(check_devices)
        
        self.rel = {
            "title": f"Relatório do Dispositivo {self.get_device()}",
        }
        self.get_info_android()
            
    def verify_system_host(self):
        so, hostname, release, version, arquitect = os.uname()
        output = f"""
        INFORMAÇÕES DO SISTEMA:
        Arquitetura:         {arquitect}
        Descrição:           {version}
        Hostname:            {hostname}
        Sistema Operacional: {so}
        Release:             {release}       
        """  
        print(output)

    #Metodo que verifica se tem dispistivo conectado
    def verify_connect_devices(self):
        devices = self.execute_cmd(options=1)
        devices = devices.strip().split('\n')
        #print(devices)
        if len(devices) > 1:            
            return devices[1:]      
        else:
            print("entrou no false")
            return False    
    
    #Metodo que seleciona o dispositivo a ser usado
    def choice_device(self, devices):
        aux = 0
        print("Os dispositivos conectados são:")
        for device in devices:
            print(device)

        if len(devices) > 0:            
            print("\nEscolha o seu dispositivo desejado:")            
            for device in devices:
                aux += 1
                print(f"{aux} - {device}")
            
            aux = 0
            while aux < 1 or aux > len(devices):                
                aux2 = input("\nEscolha: ")
                if aux2.isdigit():
                    aux = int(aux2)                    
                
        self._device = str(devices[aux-1]).split('\t')[0]
        print("\nDevice selecionado é: ",self._device)
    
    def get_device(self):
        return self._device
    
    def set_device(self, device):
        pass

    def adb_start(self):
        print("INICIANDO.........")
        self.execute_cmd(3)
        print("ADB SERVER INICIADO.")

    def adb_kill(self):
        self.execute_cmd(4)
        print("ADB SERVER FECHADO.")

    def verify_installed_adb(self):
        check = self.execute_cmd(2)
        if not check:
            print("Ferramenta ADB não instalada. Instale para continuar")
            sys.exit()

    def get_info_android(self):
        aux = ""
        aux_fast = {                                
            "Marca": "ro.product.manufacturer",
            "Modelo": "ro.product.model",
            "Serial Number": "ro.serialno",            
            "Versão do Android": "ro.build.version.release",
            "Versão do SDK": "ro.build.version.sdk",
            "Interface de rede": "wifi.interface",
            "Status Interface de rede": "wlan.driver.status",
        }
        info_fast, info_full = self.execute_cmd(5)                 
        info_fast = info_fast.replace("[","").replace("]","").strip(" ").split("\n")
        info_fast = [i for i in  info_fast if i != '']                                
        fast = dict()        
        fast = {k: j.split(":")[1].strip() for j in  info_fast for k,v in aux_fast.items() if v in j}       
        for key,value in fast.items():                        
            aux += f"{key} - {value.upper()}\n" 
        self.rel["info_fast"] = aux
        print("\n\n")
        print(self.rel["title"])
        print(self.rel["info_fast"])
        #print("Valor de info: ",info_full)
        #self.rel["info_fast"]
        #self.rel["info_full"]


    def logical_backup(self):
        pass

    def create_relatory(self):
        pass

    def export_relatory(self):
        pass

    def extract_data(self):
        pass

    def execute_cmd(self,options):

        def run(cmd):
            try: 
                out = Popen(cmd, stdout=PIPE)
                while out.poll() == None:
                    pass                
                output = out.communicate(timeout=15)[0].decode('UTF-8')                                
                #print("OUTPUT :",output)
                return output
            except:
                return False#Comando falhou
            
        if options == 1:
            return run(["adb","devices"])            
        
        elif options == 2:
            return run(["adb"])
        
        elif options == 3:
            return run(["adb","start-server"])
        
        elif options == 4:
            return run(["adb","kill-server"])
        
        elif options == 5:
            fast = ""
            full = ""
            fast = run(["adb","-s",f"{self.get_device()}","shell","getprop"])
            aux_full = {
                "Processos": "ps",
                "Soquets": "netstat",
                #"Estados do dispositivo": "dumpsys", esta gerando erro
                "Processador": "cat /proc/cpuinfo",
                "Memoria": "cat /proc/meminfo",
                "Pacotes instalados": "pm list packages",
                "Processador": "cat /proc/cpuinfo",
                "Informações da rede": "ip addr show wlan0",
                "Rotas": "route",  
                "IMEI": "service call iphonesubinfo 1",
            }
            #for key,value in aux_full.items():
            #    full += run(["adb","-s",f"{self.get_device()}","shell",value])            
            return fast,full
            

droid = main()
