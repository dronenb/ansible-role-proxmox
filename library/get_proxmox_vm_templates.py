#!/usr/bin/env python3

from ansible.module_utils.basic import *
import subprocess
import json
import re

def main():
    module = AnsibleModule(argument_spec={})
    result = subprocess.run(
        ['/usr/bin/pvesh', 'get', '/cluster/resources','-type', 'vm', '--output-format', 'json'],
        stdout=subprocess.PIPE,
    )
    templates = []
    for vm in json.loads(result.stdout.decode('utf-8')):
        if vm['template'] == 1:
            vm['tags'] = vm['tags'].split(',')
            vm['image_checksum'] = ""
            for tag in vm['tags']:
                match = re.search(r"checksum-(.*)", tag)
                if match:
                    vm['image_checksum'] = match.group(1)
                    break
                else:
                    print("Tag does not match: %s" % (tag))
            templates.append(vm)

    module.exit_json(changed=False, meta=templates)
    # module.fail_json("Could not find checksum for %s" % (image_name))

if __name__ == '__main__':
    main()
