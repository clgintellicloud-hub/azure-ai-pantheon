// Role assignments for the MAF orchestrator managed identity.
// Grants data-plane access to Cosmos workflow state and Key Vault secrets.

param cosmosAccountName string
param keyVaultName string
param orchestratorPrincipalId string

resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2024-08-15' existing = {
  name: cosmosAccountName
}

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' existing = {
  name: keyVaultName
}

resource orchestratorCosmosDataContributor 'Microsoft.DocumentDB/databaseAccounts/sqlRoleAssignments@2024-08-15' = {
  parent: cosmosAccount
  name: guid(cosmosAccountName, 'orchestrator-cosmos-data-contributor')
  properties: {
    principalId: orchestratorPrincipalId
    roleDefinitionId: '${cosmosAccount.id}/sqlRoleDefinitions/00000000-0000-0000-0000-000000000002'
    scope: cosmosAccount.id
  }
}

resource orchestratorKeyVaultSecretsUser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(keyVault.id, 'orchestrator-key-vault-secrets-user')
  scope: keyVault
  properties: {
    principalId: orchestratorPrincipalId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId(
      'Microsoft.Authorization/roleDefinitions',
      '4633458b-17de-408a-b874-0445c86b69e6'
    )
  }
}
