// Cosmos DB module for MAF workflow state, checkpoints, and long-term memory
// Follows architecture.md recommendations

param location string
param environment string

resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2024-08-15' = {
  name: 'cosmos-pantheon-${environment}'
  location: location
  kind: 'GlobalDocumentDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    capabilities: [
      { name: 'EnableServerless' }
    ]
  }
}

resource db 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2024-08-15' = {
  parent: cosmos
  name: 'pantheon'
  properties: {
    resource: { id: 'pantheon' }
  }
}

// Collections for state, memory, etc.
resource workflows 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2024-08-15' = {
  parent: db
  name: 'workflow_state'
  properties: {
    resource: {
      id: 'workflow_state'
      partitionKey: { paths: ['/id'], kind: 'Hash' }
    }
  }
}

output endpoint string = cosmos.properties.documentEndpoint
output accountName string = cosmos.name
