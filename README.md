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
```

or, if wanting to bypass Ansible:

```zsh
python3 library/get_rocky_cloud.py =(echo -n '{"ANSIBLE_MODULE_ARGS":{}}')
```

## License

MIT

## Author Information

Ben Dronen
