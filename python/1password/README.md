# Create 1Password secret

Depdencenies: 1password CLI, Python 3, PyYAML library, Click library
  * 1password CLI: https://developer.1password.com/docs/cli/get-started
  * PyYAML: https://pyyaml.org/wiki/PyYAMLDocumentation
  * Click: https://click.palletsprojects.com/en/8.0.x/

Scriptname: create-1p-secret.py

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

```
Usage: create-1p-secret.py [OPTIONS]

  Reads a Kubernetes Secret YAML, decodes the values, and pushes them to
  1Password.

Options:
  --secret-file PATH  Path to the Kubernetes secret YAML file.  [required]
  --vault TEXT        The name of the 1Password Vault.  [required]
  --item-name TEXT    The name of the item to create in 1Password.  [required]
  --force             Overwrite the item if it already exists.
  --dry-run           Simulate the output without changing data.
  --help              Show this message and exit.
```

This script will create an item in 1password from a kubernetes secret exported from kubernetes. It will then create an item in 1password with keys and values from the kubernetes secret. This is useful for storing secrets in 1password and then using them in kubernetes via the 1password connect operator.

Example secret.yaml file:
```
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
  namespace: my-namespace
type: Opaque
data:
  username: dXNlcm5hbWU= # base64 encoded value of "username"
  password: cGFzc3dvcmQ= # base64 encoded value of "password"
```
To run the script, use the following command:

````
./create-1p-secret.py --secret-file secret.yaml --vault MyVault --item-name item-name
```

This will create an item in the "MyVault" vault in 1Password with the name "item-name" and two fields: "username" with the value "username" and "password" with the value "password".
