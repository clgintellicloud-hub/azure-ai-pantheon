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

// Container Apps
module orchestrator 'modules/container-app.bicep' = {
  name: 'orchestrator'
  scope: rg
  params: {
    name: 'maf-orchestrator-${environment}'
    image: '${acr.outputs.loginServer}/maf-orchestrator:latest'
    environment: environment
    acaEnvName: acaEnv.outputs.name
    // Pass non-secret config; secrets via Key Vault + Managed Identity
    envVars: {
      COSMOS_ENDPOINT: cosmos.outputs.endpoint
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
  }
}

output acrLoginServer string = acr.outputs.loginServer
output orchestratorFqdn string = orchestrator.outputs.fqdn
