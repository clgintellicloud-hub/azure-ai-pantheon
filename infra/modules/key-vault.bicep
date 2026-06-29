// Key Vault for secrets (LLM keys, connection strings, etc.)
// SECURITY: Use Managed Identity. Never hardcode secrets.

param location string
param environment string

resource kv 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: 'kv-pantheon-${environment}'
  location: location
  properties: {
    sku: { family: 'A', name: 'standard' }
    tenantId: subscription().tenantId
    // Recommended: use RBAC + Managed Identity.
    enableRbacAuthorization: true
  }
}

output vaultUri string = kv.properties.vaultUri
output name string = kv.name
output id string = kv.id
