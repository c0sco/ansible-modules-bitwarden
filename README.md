# ansible-modules-bitwarden

Bitwarden integrations for Ansible

## Lookup plugin

Use `lookup()` with the `bitwarden` argument, followed by the items you want to retrieve. The default field is `password`, but any other field can be specified. If you need to specify the path to the Bitwarden CLI binary, use the `path` named argument. For example:

```yaml
# Get username for Slashdot and Google
- debug: msg="{{ lookup('bitwarden', 'Slashdot', 'Google', field='username', path='/not/in/my/path/bw') }}"
```

If you want to run the plugin directly for testing, you must first specify the field, then list the items to fetch.

```bash
lib/ansible/plugins/lookup/bitwarden.py username Google Slashdot
```
