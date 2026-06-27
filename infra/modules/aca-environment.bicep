// ACA Environment module
// Includes Log Analytics for monitoring.

param location string
param environment string

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: 'log-pantheon-${environment}'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource acaEnv 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'aca-env-pantheon-${environment}'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: listKeys(logAnalytics.id, logAnalytics.apiVersion).primarySharedKey
      }
    }
  }
}

output name string = acaEnv.name
output id string = acaEnv.id
