#!/usr/bin/python

from ansible.module_utils.basic import *
import urllib.request
import json
import os
import tempfile
import tarfile
import subprocess

def main():
    fields = {
        "arch" : {
            "default"   : "x86_64",
            "type"      : "str"
        },
        "template_name" : {
            "default"   : "scos-latest",
            "type"      : "str",
        },
    }
    module = AnsibleModule(argument_spec=fields)
    
    try:
        # Get latest OKD release
        github_api_url = "https://api.github.com/repos/okd-project/okd/releases/latest"
        with urllib.request.urlopen(github_api_url) as response:
            release_data = json.loads(response.read().decode())
            okd_version = release_data["tag_name"]
        
        # Determine download URL based on platform
        import platform
        system = platform.system().lower()
        machine = platform.machine()
        
        if system == "darwin":
            if machine == "arm64":
                installer_filename = f"openshift-install-mac-arm64-{okd_version}.tar.gz"
            else:
                installer_filename = f"openshift-install-mac-{okd_version}.tar.gz"
        else:
            installer_filename = f"openshift-install-linux-{okd_version}.tar.gz"
        
        installer_url = f"https://github.com/okd-project/okd/releases/download/{okd_version}/{installer_filename}"
        
        # Create temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            # Download openshift-install
            installer_tar_path = os.path.join(tmpdir, installer_filename)
            urllib.request.urlretrieve(installer_url, installer_tar_path)
            
            # Extract openshift-install
            with tarfile.open(installer_tar_path, 'r:gz') as tar:
                tar.extract('openshift-install', tmpdir)
            
            installer_path = os.path.join(tmpdir, 'openshift-install')
            os.chmod(installer_path, 0o755)
            
            # Run openshift-install coreos print-stream-json
            result = subprocess.run(
                [installer_path, 'coreos', 'print-stream-json'],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the CoreOS stream data
            stream_data = json.loads(result.stdout)
            arch_data = stream_data["architectures"][module.params["arch"]]
            qemu_artifact = arch_data["artifacts"]["qemu"]
            
            # Try to find the right format - SCOS might use different format names
            available_formats = list(qemu_artifact["formats"].keys())
            
            # Prefer qcow2.xz, but fall back to qcow2 or first available
            format_key = None
            for fmt in ["qcow2.xz", "qcow2", "qcow2.gz"]:
                if fmt in available_formats:
                    format_key = fmt
                    break
            
            if not format_key:
                # Use first available format
                format_key = available_formats[0] if available_formats else None
            
            if not format_key:
                raise Exception(f"No suitable QEMU format found. Available: {available_formats}")
            
            qcow2_format = qemu_artifact["formats"][format_key]
            
            image_url = qcow2_format["disk"]["location"]
            image_checksum = qcow2_format["disk"]["sha256"]
            image_name = os.path.basename(image_url)
            
            ansible_response = {
                "image_name"            : image_name,
                "image_url"             : image_url,
                "image_checksum"        : image_checksum,
                "image_checksum_type"   : "SHA256",
                "image_version"         : stream_data.get("stream", okd_version),
                "okd_version"           : okd_version,
                "template_name"         : module.params["template_name"],
            }
            module.exit_json(changed=False, meta=ansible_response)
    
    except Exception as e:
        module.fail_json(msg=f"Could not retrieve SCOS information: {str(e)}")

if __name__ == '__main__':
    main()
