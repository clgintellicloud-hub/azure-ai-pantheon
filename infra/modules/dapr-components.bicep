// Dapr components for ACA-hosted agent orchestration.
// State is backed by Cosmos DB; pub/sub is backed by Azure Service Bus.

param acaEnvName string
param cosmosEndpoint string
param cosmosDatabase string = 'pantheon'
param cosmosContainer string = 'workflow_state'
param serviceBusNamespaceName string
param serviceBusTopicName string = 'agent-events'

resource acaEnv 'Microsoft.App/managedEnvironments@2024-03-01' existing = {
  name: acaEnvName
}

resource workflowState 'Microsoft.App/managedEnvironments/daprComponents@2024-03-01' = {
  parent: acaEnv
  name: 'workflow-state'
  properties: {
    componentType: 'state.azure.cosmosdb'
    version: 'v1'
    ignoreErrors: false
    initTimeout: '5s'
    metadata: [
      {
        name: 'url'
        value: cosmosEndpoint
      }
      {
        name: 'database'
        value: cosmosDatabase
      }
      {
        name: 'collection'
        value: cosmosContainer
      }
      {
        name: 'actorStateStore'
        value: 'true'
      }
    ]
    scopes: [
      'orchestrator'
      'hermes-agent'
      'openclaw-agent'
    ]
  }
}

resource agentEvents 'Microsoft.App/managedEnvironments/daprComponents@2024-03-01' = {
  parent: acaEnv
  name: 'agent-events'
  properties: {
    componentType: 'pubsub.azure.servicebus'
    version: 'v1'
    ignoreErrors: false
    initTimeout: '5s'
    metadata: [
      {
        name: 'namespaceName'
        value: serviceBusNamespaceName
      }
      {
        name: 'topicName'
        value: serviceBusTopicName
      }
    ]
    scopes: [
      'orchestrator'
      'hermes-agent'
      'openclaw-agent'
    ]
  }
}

output stateComponentName string = workflowState.name
output pubsubComponentName string = agentEvents.name
