// Reusable module for Container Apps (orchestrator, hermes, openclaw)
// Parameterized for different images, scaling, envs as per architecture.md

param name string
param image string
param environment string
param acaEnvName string

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: name
  location: resourceGroup().location
  properties: {
    managedEnvironmentId: resourceId('Microsoft.App/managedEnvironments', acaEnvName)
    configuration: {
      ingress: {
        external: true
        targetPort: 8080
      }
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
