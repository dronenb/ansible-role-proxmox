#!/usr/bin/python

from ansible.module_utils.basic import *
import urllib.request
from bs4 import BeautifulSoup

def main():
    fields = {
        "arch" : {
            "default"   : "x86_64",
            "type"      : "str"
        },
    }
    module = AnsibleModule(argument_spec=fields)

    base_url = "https://download.rockylinux.org/pub/rocky"

    with urllib.request.urlopen(base_url) as response:
        soup = BeautifulSoup(response.read().decode(), "lxml")
        version = 0.0
        for tag in soup.find_all("a"):
            match = re.search("(\d+\.\d+)/", tag.get_text())
            if match and float(match.group(1)) > version:
                version = float(match.group(1))
        image_name = "Rocky-%.0f-GenericCloud.latest.x86_64.qcow2" % (version)
        image_url = "%s/%s/images/%s/%s" % (base_url, str(version), module.params["arch"], image_name)
        checksum_url = "%s.CHECKSUM" % (image_url)
        with urllib.request.urlopen(checksum_url) as checksum_response:
            regex = "^SHA256 \(%s\) = (.*)$"
            for line in checksum_response.read().decode().split("\n"):
                checksum_match = re.search("^SHA256 \(%s\) = (.*)$" % (image_name), line)
                if checksum_match:
                    checksum = checksum_match.group(1)
                    ansible_response = {
                        "image_name"            : image_name,
                        "image_url"             : image_url,
                        "image_checksum"        : checksum,
                        "image_checksum_type"   : "SHA256",
                    }
                    module.exit_json(changed=False, meta=ansible_response)
        module.fail_json("Could not find checksum for %s" % (image_name))
    module.fail_json("Could not find latest version of rocky")

if __name__ == '__main__':
    main()