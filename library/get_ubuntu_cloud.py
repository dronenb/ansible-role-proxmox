#!/usr/bin/env python3

from ansible.module_utils.basic import *
import urllib.request

def main():
    fields = {
        "codename" : {
            "default"   : "jammy",
            "type"      : "str",
        },
        "arch" : {
            "default"   : "amd64",
            "type"      : "str"
        },
        "template_name" : {
            "default"   : "ubuntu-latest",
            "type"      : "str",
        },
    }
    module = AnsibleModule(argument_spec=fields)

    base_url = "https://cloud-images.ubuntu.com/{}/current".format(module.params["codename"])
    image_name = "%s-server-cloudimg-%s.img" % (module.params["codename"], module.params["arch"])
    image_url = "%s/%s" % (base_url, image_name)
    checksum_url = "%s/SHA256SUMS" % (base_url)

    with urllib.request.urlopen(checksum_url) as response:
        for line in response.read().decode().split("\n"):
            if line: 
                [checksum, filename] = line.split(" *")
                if filename == image_name:
                    ansible_response = {
                        "image_name"            : image_name,
                        "image_url"             : image_url,
                        "image_checksum"        : checksum,
                        "image_checksum_type"   : "SHA256",
                        "image_version"         : module.params["codename"],
                        "template_name"         : module.params["template_name"],
                    }
                    module.exit_json(changed=False, meta=ansible_response)
    module.fail_json("Could not find checksum for %s" % (image_name))

if __name__ == '__main__':
    main()