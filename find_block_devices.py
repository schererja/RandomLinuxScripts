import sys
import os
import re
import glob
import operator
import json
from pprint import pprint

class Drive:
    devices_to_check = ["scsi"]
    def __init__(self,
                DEBUG = False,
                SYS = "/sys",
                devices_to_check = ["scsi"],
                output_fields = ["hostnum",
                                "id",
                                "controller_Path",
                                "model",
                                "revision"]):
        self.devices = []
        self.output_fields = output_fields
        self.SYS = SYS
        self.devices_to_check = devices_to_check
        self.DEBUG = DEBUG
        self.get_drives()

    def get_drives(self):
        for bus in self.devices_to_check:
            bus_path = self.SYS + "/bus/" + bus + "/devices"
            if not os.path.exists(bus_path):
                if self.DEBUG:
                    print("No path for bus " + bus + ": " + bus_path)
                next
            for device in os.listdir(bus_path):
                dev_path = os.path.abspath(bus_path + "/" + device)
                dev_data = {}
                dev_data['device_path'] = dev_path
                block_path = glob.glob(dev_path + "/block")
                if not block_path:
                    if self.DEBUG:
                        print("Device {} has no block device associated with it".format(device))
                    block_path = glob.glob(dev_path + "/scsi_generic:*")
                    if not block_path:
                        if self.DEBUG:
                            print("Device {} has no generic device associated with it".format(device))
                        continue
                if self.DEBUG:
                    print("Block path for /block* is: {}".format(block_path))
                if os.path.basename((os.path.split(block_path[0])[1])) == "block" and \
                    os.path.exists(block_path[0]):
                    block_path = glob.glob(dev_path + "/block/*")
                if self.DEBUG:
                    print("Blockpath is: {}".format(block_path[0]))
                if os.path.exists(block_path[0] + "/removable"):
                    with open(block_path[0] + "/removable") as f:
                        dev_data["removable"] = f.readline().strip()
                else:
                    dev_data["removable"] = 0
                dev_data["blockname"] = os.path.split(block_path[0])[1]
                dev_data["blockdevice"] = "/dev/{}".format(dev_data["blockname"])

                if os.path.exists(dev_path + "/driver") and os.path.isfile(dev_path + "/driver"):
                    print("test")
                else:
                    dev_data["driver"] = "driver"

                if os.path.exists(dev_path + "/type") and os.path.isfile(dev_path + "/type"):
                    with open(dev_path + "/type") as f:
                        dev_data["typeval"] = f.readline().strip()
                        if dev_data["typeval"] == "0":
                            dev_data["typeval"] = "disk"
                        elif dev_data["typeval"] == "1":
                            dev_data["typeval"] = "tape"
                        elif dev_data["typeval"] == "2":
                            dev_data["typeval"] = "printer"
                        elif dev_data["typeval"] == "3":
                            dev_data["typeval"] = "processor"
                        elif dev_data["typeval"] == "4":
                            dev_data["typeval"] = "worm"
                        elif dev_data["typeval"] == "5":
                            dev_data["typeval"] = "rom"
                        elif dev_data["typeval"] == "6":
                            dev_data["typeval"] = "scanner"
                        elif dev_data["typeval"] == "7":
                            dev_data["typeval"] = "mod"
                        elif dev_data["typeval"] == "8":
                            dev_data["typeval"] = "changer"
                        elif dev_data["typeval"] == "9":
                            dev_data["typeval"] = "comm"
                        elif dev_data["typeval"] == "c":
                            dev_data["typeval"] = "raid"
                        elif dev_data["typeval"] == "d":
                            dev_data["typeval"] = "enclosure"
                        elif dev_data["typeval"] == "e":
                            dev_data["typeval"] = "rbc"
                        else:
                            dev_data["typeval"] = "unknown"
                else:
                    exit(1)
                controllerPath = os.path.abspath(dev_path)
                dev_data["hostnum"] = device.split(':')[0]
                dev_data["channel"] = device.split(':')[1]
                dev_data["id"] = device.split(':')[2]
                dev_data["lun"] = device.split(':')[3]
                with open(dev_path + "/model") as f:
                    dev_data["model"] = f.readline().split()[0]
                with open(dev_path + "/rev") as f:
                    dev_data["revision"] = f.readline().split()[0]
                self.devices.append(dev_data)


if __name__ == '__main__':
    d = Drive()
    pprint(d.devices)