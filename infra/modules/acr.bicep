// ACR module
// SECURITY: Managed Identity used for image pulls in ACA.

param location string
param suffix string

resource acr 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'acrpantheon${suffix}'
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: false
  }
}

output loginServer string = acr.properties.loginServer
output acrId string = acr.id
