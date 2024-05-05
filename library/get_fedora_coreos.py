#!/usr/bin/env python3

from ansible.module_utils.basic import *
import urllib.request
import json
import os.path

def main():
    fields = {
        "arch" : {
            "default"   : "x86_64",
            "type"      : "str"
        },
        "template_name" : {
            "default"   : "fcos-latest",
            "type"      : "str",
        },
    }
    module = AnsibleModule(argument_spec=fields)
    base_url = "https://builds.coreos.fedoraproject.org/streams/stable.json"
    with urllib.request.urlopen(base_url) as response:
        latest = json.loads(response.read().decode())["architectures"][module.params["arch"]]["artifacts"]["qemu"]
        image_url = latest["formats"]["qcow2.xz"]["disk"]["location"]
        image_checksum = latest["formats"]["qcow2.xz"]["disk"]["sha256"]
        image_name = os.path.basename(image_url)
        ansible_response = {
            "image_name"            : image_name,
            "image_url"             : image_url,
            "image_checksum"        : image_checksum,
            "image_checksum_type"   : "SHA256",
            "image_version"         : latest["release"],
            "template_name"         : module.params["template_name"],
        }
        module.exit_json(changed=False, meta=ansible_response)
    module.fail_json("Could not retrieve Fedora CoreOS information")

if __name__ == '__main__':
    main()
