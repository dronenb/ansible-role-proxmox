#!/usr/bin/python

from ansible.module_utils.basic import *
import urllib.request

def main():
    fields = {
        "codename" : {
            "default"   : "bullseye",
            "type"      : "str",
        },
        "major_version" : {
            "default"   : 11,
            "type"      : "int",
        },
        "arch" : {
            "default"   : "amd64",
            "type"      : "str"
        },
    }
    module = AnsibleModule(argument_spec=fields)

    base_url = "https://cloud.debian.org/images/cloud/{}/latest".format(module.params["codename"])
    image_name = "debian-%d-genericcloud-%s.qcow2" % (module.params["major_version"], module.params["arch"])
    image_url = "%s/%s" % (base_url, image_name)
    checksum_url = "%s/SHA512SUMS" % (base_url)

    with urllib.request.urlopen(checksum_url) as response:
        for line in response.read().decode().split("\n"):
            if line: 
                [checksum, filename] = line.split("  ")
                if filename == image_name:
                    ansible_response = {
                        "image_name"            : image_name,
                        "image_url"             : image_url,
                        "image_checksum"        : checksum,
                        "image_checksum_type"   : "SHA512",
                    }
                    module.exit_json(changed=False, meta=ansible_response)
    module.fail_json("Could not find checksum for %s" % (image_name))

if __name__ == '__main__':
    main()