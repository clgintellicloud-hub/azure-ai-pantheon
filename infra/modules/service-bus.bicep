// Azure Service Bus namespace and topic for Dapr pub/sub agent events.

param location string
param environment string

resource serviceBus 'Microsoft.ServiceBus/namespaces@2024-01-01' = {
  name: 'sb-pantheon-${environment}'
  location: location
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
}

resource agentEvents 'Microsoft.ServiceBus/namespaces/topics@2024-01-01' = {
  parent: serviceBus
  name: 'agent-events'
}

output namespaceName string = serviceBus.name
output namespaceId string = serviceBus.id
output topicName string = agentEvents.name
