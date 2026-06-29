// Azure OpenAI account and model deployment for orchestrator planning/tool use.

param location string
param environment string
param deploymentName string = 'gpt-4o'
param modelName string = 'gpt-4o'
param modelVersion string = '2024-11-20'

resource account 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: 'aoai-pantheon-${environment}'
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  properties: {
    customSubDomainName: 'aoai-pantheon-${environment}'
    publicNetworkAccess: 'Enabled'
  }
}

resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: account
  name: deploymentName
  sku: {
    name: 'Standard'
    capacity: 10
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: modelName
      version: modelVersion
    }
  }
}

output endpoint string = account.properties.endpoint
output accountName string = account.name
output accountId string = account.id
output deploymentName string = deployment.name
