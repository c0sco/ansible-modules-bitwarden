# ansible-modules-bitwarden

Bitwarden integration for Ansible.

## Installation

The easiest way to install this lookup plugin is to use the
`ansible-galaxy` command:

    ansible-galaxy install git+https://github.com/c0sco/ansible-modules-bitwarden

This will place the `ansible-modules-bitwarden` role into
`$HOME/.ansible/roles`, where it will be available to all playbooks
you run on your system.

## Lookup plugin

To use this plugin, you will need to activate it by including the role
in your play.  For example:

    - hosts: localhost
      roles:
        - ansible-modules-bitwarden

Use Ansible's `lookup()` function with the `bitwarden` argument,
followed by the items you want to retrieve. The default field is
`password`, but any other field can be specified using the `field`
named argument. If you need to specify the path to the Bitwarden CLI
binary, use the `path` named argument.

## Examples

### Get a single password

```yaml
# Get password for Google
- debug:
    msg: {{ lookup('bitwarden', 'Google') }}
```

The above might result in:

```
TASK [debug] *********************************************************
ok: [localhost] => {
    "msg": "mysecret"
    }
```

### Get a single username

```yaml
# Get username for Google
- debug:
    msg: {{ lookup('bitwarden', 'Google', field='username' }}
```

The above might result in:

```
TASK [debug] *********************************************************
ok: [localhost] => {
    "msg": "alice"
    }
```

### See all available fields

```yaml
# Get all available fields for an entry
- debug:
    msg: {{ lookup('bitwarden', 'Google', field='item' }}
```

The above might result in:

```
TASK [debug] *********************************************************
ok: [localhost] => {
    "msg": {
        "favorite": false, 
        "folderId": null, 
        "id": "12345678-0123-4321-0000-a97001342c31", 
        "login": {
            "password": "mysecret", 
            "passwordRevisionDate": null, 
            "totp": null, 
            "username": "alice"
        }, 
        "name": "Google", 
        "notes": null, 
        "object": "item", 
        "organizationId": "87654321-1234-9876-0000-a96800ed2b47", 
        "revisionDate": "2018-10-19T19:20:17.923Z", 
        "type": 1
    }
}
```
