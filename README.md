# opsdroid skill vault

A skill for [opsdroid](https://github.com/opsdroid/opsdroid) to interact with [Hashicorp's Vault](https://www.vaultproject.io).

## Requirements

* An instance of Vault to interact with.
* A token with seal permissions (Pro Tip: create a [seal only token](https://www.jacobtomlinson.co.uk/security/2017/06/14/seal-only-token-hashicorp-vault/) just for opsdroid).

## Configuration

```yaml
- name: vault
  # Required
  vault-url: https://vault.example.com:8443
  vault-token: aabbccddee1122334455
  # Optional
  announce-on-seal: false  # Announce the vault status in the default room on seal
  announce-sealed: true  # Announce the vault is sealed hourly
  announce-unsealed: false  # Announce the vault is unsealed hourly
```

## Usage

#### `is the vault sealed?`

Checks if the vault is sealed.

> user: is the vault sealed?
>
> opsdroid: The vault is not sealed.

#### `seal the vault`

Seals the vault.

> user: please seal the vault!!!!1!
>
> opsdroid: I sealed the vault.
>
> opsdroid (in default room): The vault is sealed.
