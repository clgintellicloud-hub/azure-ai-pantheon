// azure-ai-pantheon - Main Bicep orchestration for MAF-based agent orchestration
// Deploys: ACA environment, ACR, Cosmos DB, Key Vault, Container Apps (orchestrator + agents), Monitoring
// Follows the recommended architecture in docs/architecture.md
//
// SECURITY: Never hardcode secrets here. Use parameters + Key Vault references or Managed Identities.
// See docs/security-guidelines.md for IaC rules.

targetScope = 'subscription'

@description('Environment: dev or prod')
param environment string = 'dev'

@description('Azure region')
param location string = 'eastus'

@description('Unique suffix for resources')
param suffix string = 'pantheon01'

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: 'rg-pantheon-${environment}'
  location: location
}

// ACR
module acr 'modules/acr.bicep' = {
  name: 'acr'
  scope: rg
  params: {
    location: location
    suffix: suffix
  }
}

// ACA Environment + Monitoring (Log Analytics)
module acaEnv 'modules/aca-environment.bicep' = {
  name: 'acaEnv'
  scope: rg
  params: {
    location: location
    environment: environment
  }
}

// Cosmos DB for MAF state and memory
module cosmos 'modules/cosmos-db.bicep' = {
  name: 'cosmos'
  scope: rg
  params: {
    location: location
    environment: environment
  }
}

// Key Vault (for secrets - accessed via Managed Identity)
module kv 'modules/key-vault.bicep' = {
  name: 'keyVault'
  scope: rg
  params: {
    location: location
    environment: environment
  }
}

// Monitoring
module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring'
  scope: rg
  params: {
    location: location
    environment: environment
  }
}

// Foundry (sim for local)
module foundry 'modules/foundry.bicep' = {
  name: 'foundry'
  scope: rg
  params: {
    location: location
    environment: environment
  }
}

// Azure OpenAI for production LLM planning/tool calling
module openai 'modules/openai.bicep' = {
  name: 'openai'
  scope: rg
  params: {
    location: location
    environment: environment
  }
}

// Azure Service Bus for Dapr pub/sub agent events
module serviceBus 'modules/service-bus.bicep' = {
  name: 'serviceBus'
  scope: rg
  params: {
    location: location
    environment: environment
  }
}

// Dapr state/pubsub components hosted by the ACA environment
module daprComponents 'modules/dapr-components.bicep' = {
  name: 'daprComponents'
  scope: rg
  params: {
    acaEnvName: acaEnv.outputs.name
    cosmosEndpoint: cosmos.outputs.endpoint
    cosmosDatabase: 'pantheon'
    cosmosContainer: 'workflow_state'
    serviceBusNamespaceName: serviceBus.outputs.namespaceName
    serviceBusTopicName: serviceBus.outputs.topicName
  }
}

output monitoringKey string = monitoring.outputs.instrumentationKey
output foundryEndpoint string = foundry.outputs.foundryEndpoint
output azureOpenAiEndpoint string = openai.outputs.endpoint

// Container Apps
module orchestrator 'modules/container-app.bicep' = {
  name: 'orchestrator'
  scope: rg
  params: {
    name: 'maf-orchestrator-${environment}'
    image: '${acr.outputs.loginServer}/maf-orchestrator:latest'
    environment: environment
    acaEnvName: acaEnv.outputs.name
    targetPort: 8000
    enableDapr: true
    daprAppId: 'orchestrator'
    // Pass non-secret config; secrets via Key Vault + Managed Identity
    envVars: {
      COSMOS_ENDPOINT: cosmos.outputs.endpoint
      COSMOS_DATABASE: 'pantheon'
      COSMOS_CONTAINER: 'workflow_state'
      USE_COSMOS_STATE: 'true'
      HERMES_ENDPOINT: 'https://${hermesAgent.outputs.fqdn}'
      OPENCLAW_ENDPOINT: 'https://${openclawAgent.outputs.fqdn}'
      HERMES_DAPR_APP_ID: 'hermes-agent'
      OPENCLAW_DAPR_APP_ID: 'openclaw-agent'
      DAPR_STATE_STORE: daprComponents.outputs.stateComponentName
      DAPR_PUBSUB: daprComponents.outputs.pubsubComponentName
      FOUNDRY_ENDPOINT: foundry.outputs.foundryEndpoint
      AZURE_OPENAI_ENDPOINT: openai.outputs.endpoint
      AZURE_OPENAI_DEPLOYMENT: openai.outputs.deploymentName
    }
  }
}

module hermesAgent 'modules/container-app.bicep' = {
  name: 'hermesAgent'
  scope: rg
  params: {
    name: 'hermes-${environment}'
    image: '${acr.outputs.loginServer}/hermes-agent:latest'
    environment: environment
    acaEnvName: acaEnv.outputs.name
    enableDapr: true
    daprAppId: 'hermes-agent'
    externalIngress: false
  }
}

module openclawAgent 'modules/container-app.bicep' = {
  name: 'openclawAgent'
  scope: rg
  params: {
    name: 'openclaw-${environment}'
    image: '${acr.outputs.loginServer}/openclaw-agent:latest'
    environment: environment
    acaEnvName: acaEnv.outputs.name
    enableDapr: true
    daprAppId: 'openclaw-agent'
    externalIngress: false
  }
}

module orchestratorAccess 'modules/orchestrator-access.bicep' = {
  name: 'orchestratorAccess'
  scope: rg
  params: {
    cosmosAccountName: cosmos.outputs.accountName
    keyVaultName: kv.outputs.name
    serviceBusNamespaceName: serviceBus.outputs.namespaceName
    openAiAccountName: openai.outputs.accountName
    orchestratorPrincipalId: orchestrator.outputs.principalId
  }
}

output acrLoginServer string = acr.outputs.loginServer
output orchestratorFqdn string = orchestrator.outputs.fqdn
output hermesFqdn string = hermesAgent.outputs.fqdn
output openclawFqdn string = openclawAgent.outputs.fqdn
