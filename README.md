# ansible-role-proxmox

Configures Proxmox the way I want.

## Role Variables

TODO

## Dependencies

- dronenb.debian

## Example Playbook

TODO

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

## Testing modules locally

```bash
ANSIBLE_LIBRARY=./library ansible -m get_rocky_cloud localhost
ANSIBLE_LIBRARY=./library ansible -m get_scos localhost
```

or, if wanting to bypass Ansible:

```zsh
python3 library/get_rocky_cloud.py =(echo -n '{"ANSIBLE_MODULE_ARGS":{}}')
python3 library/get_scos.py =(echo -n '{"ANSIBLE_MODULE_ARGS":{}}')
```

## VM Templates

This role automatically creates the following VM templates in Proxmox:

- **debian-latest**: Latest Debian cloud image
- **ubuntu-latest**: Latest Ubuntu cloud image
- **rocky-latest**: Latest Rocky Linux cloud image
- **fcos-latest**: Latest Fedora CoreOS image
- **scos-latest**: Latest SCOS (Single Node CoreOS for OKD) image - automatically fetched from the latest OKD release

## License

MIT

## Author Information

Ben Dronen
