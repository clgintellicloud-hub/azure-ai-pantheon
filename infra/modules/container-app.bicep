// Reusable module for Container Apps (orchestrator, hermes, openclaw)
// Parameterized for different images, scaling, envs as per architecture.md

param name string
param image string
param environment string
param acaEnvName string
param targetPort int = 8080
param externalIngress bool = true
param enableDapr bool = false
param daprAppId string = ''
param envVars object = {}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: resourceGroup().location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: resourceId('Microsoft.App/managedEnvironments', acaEnvName)
    configuration: {
      ingress: {
        external: externalIngress
        targetPort: targetPort
      }
      dapr: enableDapr ? {
        enabled: true
        appId: empty(daprAppId) ? name : daprAppId
        appPort: targetPort
        appProtocol: 'http'
      } : null
    }
    template: {
      containers: [
        {
          name: 'app'
          image: image
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          // SECURITY: env vars for config only. Secrets via Key Vault references or Managed Identity.
          env: [for item in items(envVars): {
            name: item.key
            value: item.value
          }]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 10
      }
    }
  }
}

output fqdn string = app.properties.configuration.ingress.fqdn
output principalId string = app.identity.principalId
