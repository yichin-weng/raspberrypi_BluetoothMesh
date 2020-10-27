import subprocess
import sys
import asyncio
from multiprocessing import Pool, Process
from joblib import Parallel, delayed
import multiprocessing as mp

"""
mesh-cfgclient:
    Menu main:
        Available commands:
        -------------------
        config                                            Configuration Model Submenu
        create [unicast_range_low]                        Create new mesh network with one initial node
        discover-unprovisioned <on/off> [seconds]         Look for devices to provision
        appkey-create <net_idx> <app_idx>                 Create a new local AppKey
        appkey-import <net_idx> <app_idx> <key>           Import a new local AppKey
        appkey-update <app_idx>                           Update local AppKey
        appkey-delete <app_idx>                           Delete local AppKey
        subnet-create <net_idx>                           Create a new local subnet (NetKey)
        subnet-import <net_idx> <key>                     Import a new local subnet (NetKey)
        subnet-update <net_idx>                           Update local subnet (NetKey)
        subnet-delete <net_idx>                           Delete local subnet (NetKey)
        subnet-set-phase <net_idx> <phase>                Set subnet (NetKey) phase
        list-unprovisioned                                List unprovisioned devices
        provision <uuid>                                  Initiate provisioning
        node-import <uuid> <net_idx> <primary> <ele_count> <dev_key> Import an externally provisioned remote node
        node-delete <primary> <ele_count>                 Delete a remote node
        list-nodes                                        List remote mesh nodes
        keys                                              List available keys
        menu <name>                                       Select submenu
        version                                           Display version
        quit                                              Quit program
        exit                                              Quit program
        help                                              Display help about this program
        export                                            Print environment variables



    Menu config:
        Available commands:
        -------------------
        target <unicast>                                  Set target node to configure
        timeout <seconds>                                 Set response timeout (seconds)
        composition-get [page_num]                        Get composition data
        netkey-add <net_idx>                              Add NetKey
        netkey-update <net_idx>                           Update NetKey
        netkey-del <net_idx>                              Delete NetKey
        netkey-get                                        List NetKeys known to the node
        appkey-add <app_idx>                              Add AppKey
        appkey-update <app_idx>                           Add AppKey
        appkey-del <app_idx>                              Delete AppKey
        appkey-get <net_idx>                              List AppKeys bound to the NetKey
        bind <ele_addr> <app_idx> <model_id> [vendor_id]  Bind AppKey to a model
        unbind <ele_addr> <app_idx> <model_id> [vendor_id] Remove AppKey from a model
        mod-appidx-get <ele_addr> <model_id> [vendor_id]  Get model app_idx
        ttl-set <ttl>                                     Set default TTL
        ttl-get                                           Get default TTL
        pub-set <ele_addr> <pub_addr> <app_idx> <per (step|res)> <re-xmt (cnt|per)> <model_id> [vendor_id] Set publication
        pub-get <ele_addr> <model_id> [vendor_id]         Get publication
        proxy-set <proxy>                                 Set proxy state
        proxy-get                                         Get proxy state
        ident-set <net_idx> <state>                       Set node identity state
        ident-get <net_idx>                               Get node identity state
        beacon-set <state>                                Set node identity state
        beacon-get                                        Get node beacon state
        relay-set <relay> <rexmt count> <rexmt steps>     Set relay
        relay-get                                         Get relay
        friend-set <state>                                Set friend state
        friend-get                                        Get friend state
        network-transmit-get                              Get network transmit state
        network-transmit-set <count> <steps>              Set network transmit state
        hb-pub-set <pub_addr> <count> <period> <ttl> <features> <net_idx> Set heartbeat publish
        hb-pub-get                                        Get heartbeat publish
        hb-sub-set <src_addr> <dst_addr> <period>         Set heartbeat subscribe
        hb-sub-get                                        Get heartbeat subscribe
        virt-add                                          Generate and add a virtual label
        group-list                                        Display existing group addresses and virtual labels
        sub-add <ele_addr> <sub_addr> <model_id> [vendor] Add subscription
        sub-del <ele_addr> <sub_addr> <model_id> [vendor] Delete subscription
        sub-wrt <ele_addr> <sub_addr> <model_id> [vendor] Overwrite subscription
        sub-del-all <ele_addr> <model_id> [vendor]        Delete subscription
        sub-get <ele_addr> <model_id> [vendor]            Get subscription
        node-reset                                        Reset a node and remove it from network
        back                                              Return to main menu
        version                                           Display version
        quit                                              Quit program
        exit                                              Quit program
        help                                              Display help about this program
        export                                            Print environment variables


    Target:
        Get sensor data through mesh-cfgclient and store in a file by python.
        
        1. Need to implement parallel processes to deal with data log and file storage
    
    procedure: discover-unprovisioned on: search the unprovision node. 
    
    one task to hold this task : sudo ~/bluez-5.54/mesh/bluetooth-meshd -nd 
    one task to hold this task : mesh-cfgclient
    
    discover-unprovisioned on -> scan result 
    
    get device [UUID] 
    
    provision [UUID] 
    
    menu config [
    
    
"""


def setup_mesh():
    proc = subprocess.run(["meshctl", "discover-unprovisioned", "on"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(proc.stdout.decode("utf8"))


def test(que, cmd):
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(proc.stdout.decode("cp932"))
    que.put(proc.stdout.decode("cp932"))


async def open_python_shell(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = await proc.communicate()

    print(f'[stdout])


if __name__ == '__main__':
    mp.get_context("spawn")
    q = mp.Queue()  # It is used to store the tasks which need to be coped with
    p1 = Process(target=open_python_shell, args=(q,))
    p2 = Process(target=test, args=(q, "python -V"))
    p3 = Process(target=test, args=(q, "dir"))
    p2.start()
    p3.start()
