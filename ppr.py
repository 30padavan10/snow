import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def add_resources_to_ppr(ppr, service):
    """Добавление ресурса в ППР"""
    contract, ppr_resource = service
    url_contract = f'https://cis.corp.itmh.ru/mvc/Autocomplete/ContractByFullName?term={contract}'
    req_contract = requests.get(url_contract, verify=False, auth=HTTPBasicAuth('login', 'password'))
    contract_list = req_contract.json()

    if len(contract_list) == 1:
        id_contract = (contract_list[0]['ID'])

        url_id_contract = f'https://cis.corp.itmh.ru/mvc/Demand/MaintenanceSimList?contract={id_contract}'
        req = requests.get(url_id_contract, verify=False, auth=HTTPBasicAuth('login', 'password'))
        resources = req.json()

        for resource in resources:
            if resource['SimName'] == ppr_resource:
                #print(resource['Sim'])
                url = 'https://cis.corp.itmh.ru/mvc/Demand/MaintenanceObjectAddSim'
                data = {'contract_name': contract, 'sim': resource['Sim'], 'demand': ppr}
                req = requests.post(url, verify=False, auth=HTTPBasicAuth('login', 'password'), data=data)
                if req.status_code == 200:
                    return f'{contract} {ppr_resource} added'
                return f'{contract} {ppr_resource} error'
    return f'Более одного контракта {contract_list}'


def add_links_to_ppr(ppr, link):
    """Добавление линка в ППР"""
    sw, ppr_port = link
    url_sw = f'https://cis.corp.itmh.ru/mvc/Autocomplete/EnabledSwitchWithNodeName?term={sw}'
    req_contract = requests.get(url_sw, verify=False, auth=HTTPBasicAuth('login', 'password'))
    sw_list = req_contract.json()
    for found_sw in sw_list:
        if found_sw['Name'] == sw:
            id_sw = (found_sw['ID'])
            url_id_ports = f'https://cis.corp.itmh.ru/mvc/Autocomplete/SwitchPort?device={id_sw}&has_links=true'
            req = requests.get(url_id_ports, verify=False, auth=HTTPBasicAuth('login', 'password'))
            ports = req.json()
            found_ports = []
            for port in ports:
                if ppr_port in port['Name']:
                    found_ports.append(port)
            for found_port in found_ports:
                url = 'https://cis.corp.itmh.ru/mvc/Demand/MaintenanceObjectAddLink'
                data = {'device_name': sw, 'device_port': found_port['id'], 'demand': ppr}
                req = requests.post(url, verify=False, auth=HTTPBasicAuth('login', 'password'), data=data)

                if f'{sw} [<span class="port_name">{ppr_port}</span>]' in req.content.decode('utf-8'):
                    return f'{sw} {ppr_port} added'
            return f'{sw} {ppr_port} error'
    return f'{sw} не оказалось в списке коммутаторов'


def get_services(file):
    """Выборка ресурсов и получение из них пар(договор, реквизиты)"""
    disable_list = file.split('\n')
    services = []
    while True:
        if '' in disable_list:
            disable_list.remove('')
        else:
            break
    for disable_resource in disable_list:
        if ', IP-адрес или подсеть;' in disable_resource:
            contract, ppr_resource = disable_resource.strip('"').split(', IP-адрес или подсеть;')
            services.append((contract, ppr_resource))
        elif 'IP-адрес или подсеть' in disable_resource:
            contract, ppr_resource = disable_resource.strip('"').split('IP-адрес или подсеть ')
            services.append((contract, ppr_resource))
        elif ', Etherline;' in disable_resource:
            contract, ppr_resource = disable_resource.strip('"').split(', Etherline;')
            services.append((contract, ppr_resource))
        elif ', Предоставление в аренду оптического воло;' in disable_resource:
            contract, ppr_resource = disable_resource.strip('"').split(', Предоставление в аренду оптического воло;')
            services.append((contract, ppr_resource))
    return services


def get_links(file):
    """Выборка линков и получение из них данных об одной стороне линка(коммутатор, порт)"""
    disable_list = file.split('\n')
    links = []
    while True:
        if '' in disable_list:
            disable_list.remove('')
        else:
            break
    for disable_resource in disable_list:
        if '-->' in disable_resource:
            sw = disable_resource.split('-->')[0].split(',')[-2].strip()
            port = disable_resource.split('-->')[0].split(',')[-1].strip()
            links.append((sw, port))
    return links


fl = """"""



services = get_services(fl)
links = get_links(fl)
#ppr = 7626022




for service in services:
    result = add_resources_to_ppr(ppr, service)
    print(result)

for link in links:
    result = add_links_to_ppr(ppr, link)
    print(result)
