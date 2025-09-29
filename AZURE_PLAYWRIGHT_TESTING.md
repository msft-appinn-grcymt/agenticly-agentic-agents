# Azure Playwright Testing Service Integration

This document provides detailed information about the Azure Playwright Testing service integration for this project.

## Overview

The project has been configured to run Playwright UI tests on **Azure Playwright Testing service**, a cloud-based testing platform that provides:

- **Scalable test execution**: Run tests on Microsoft's cloud infrastructure
- **Parallel test execution**: Faster test runs with cloud parallelization
- **Cross-browser support**: Test across multiple browsers without local browser installations
- **Enterprise security**: Azure AD authentication and secure test execution
- **Cost optimization**: Pay-per-use model with no infrastructure maintenance

## Configuration Files

### 1. `playwright.config.js`
The main Playwright configuration that conditionally connects to Azure service when `PLAYWRIGHT_SERVICE_URL` is set.

### 2. `playwright-azure.config.js`
Dedicated configuration for Azure Playwright Testing service with:
- All browser projects enabled (Chromium, Firefox, WebKit)
- Azure service connection settings
- Optimized timeouts and retry settings

## Required GitHub Secrets

The following secrets must be configured in your GitHub repository for CI/CD integration:

| Secret Name | Description | Example |
|-------------|-------------|---------|
| `PLAYWRIGHT_SERVICE_URL` | WebSocket endpoint URL for Azure service | `wss://your-region.playwright.microsoft.com/...` |
| `AZURE_CLIENT_ID` | Service principal client ID | `12345678-1234-1234-1234-123456789012` |
| `AZURE_TENANT_ID` | Azure Active Directory tenant ID | `87654321-4321-4321-4321-210987654321` |
| `AZURE_SUBSCRIPTION_ID` | Azure subscription identifier | `abcdef01-2345-6789-abcd-ef0123456789` |

## NPM Scripts

| Script | Description | Usage |
|--------|-------------|-------|
| `npm run test:ui` | Run tests with local browsers | Development & fallback |
| `npm run test:ui:azure` | Run tests with Azure service | CI/CD & cloud testing |
| `npm run test:ui:headed` | Run tests with visible browser (local only) | Debugging |
| `npm run test:ui:debug` | Run tests in debug mode (local only) | Development |
| `npm run validate:azure` | Validate Azure configuration | Setup verification |

## CI/CD Integration

### GitHub Actions Workflow

The `.github/workflows/ui-tests.yml` workflow:

1. **Authentication**: Uses Azure login action with service principal
2. **Build**: Compiles the application
3. **Test Execution**: Runs tests using `npm run test:ui:azure`
4. **No Browser Installation**: Azure service provides browsers in the cloud
5. **Report Upload**: Uploads test reports on failure

### Benefits in CI/CD

- **Faster execution**: No browser installation time
- **Consistent environment**: Same browsers across all runs
- **Better parallelization**: Cloud-based scaling
- **Reduced resource usage**: Offload browser execution to Azure
- **Enterprise features**: Advanced reporting and analytics

## Local Development

### Running Tests Locally

For local development, you have several options:

#### Option 1: Local Browsers (Default)
```bash
npm run test:ui
```
Uses locally installed browsers via the standard `playwright.config.js`.

#### Option 2: Azure Service (Optional)
```bash
# Set environment variables (optional for local testing)
export PLAYWRIGHT_SERVICE_URL="wss://your-service-url"
export AZURE_CLIENT_ID="your-client-id"
export AZURE_TENANT_ID="your-tenant-id"
export AZURE_SUBSCRIPTION_ID="your-subscription-id"

# Run tests with Azure service
npm run test:ui:azure
```

### Configuration Validation

Validate your setup at any time:

```bash
npm run validate:azure
```

This script checks:
- Required configuration files exist
- NPM scripts are properly configured
- Environment variables status (for Azure service)

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify Azure secrets are correctly set in GitHub
   - Check service principal permissions
   - Ensure tenant ID and subscription ID are correct

2. **Connection Timeouts**
   - Verify `PLAYWRIGHT_SERVICE_URL` format and accessibility
   - Check network connectivity to Azure service
   - Review timeout settings in `playwright-azure.config.js`

3. **Missing Environment Variables**
   - Run `npm run validate:azure` to check configuration
   - Verify secrets are set in GitHub repository settings
   - Check workflow file references correct secret names

### Debug Steps

1. **Check configuration**:
   ```bash
   npm run validate:azure
   ```

2. **Test local setup first**:
   ```bash
   npm run test:ui
   ```

3. **Review GitHub Actions logs**:
   - Check authentication step
   - Verify environment variables are passed correctly
   - Look for Azure service connection errors

4. **Validate Azure service access**:
   - Test service principal permissions
   - Verify subscription and resource access
   - Check Azure Playwright Testing service status

## Migration from Local Testing

If migrating from local-only testing:

1. **Backup existing configuration**: Save current `playwright.config.js`
2. **Add Azure configuration**: Create `playwright-azure.config.js`
3. **Update workflows**: Modify CI/CD to use Azure service
4. **Set up secrets**: Configure required GitHub secrets
5. **Test gradually**: Start with non-critical branches
6. **Validate results**: Compare test results between local and Azure

## Additional Resources

- [Azure Playwright Testing Documentation](https://docs.microsoft.com/en-us/azure/playwright-testing/)
- [Playwright Configuration Guide](https://playwright.dev/docs/test-configuration)
- [Azure Service Principal Setup](https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)

## Support

For issues specific to:
- **Azure Playwright Testing**: Contact Azure support
- **Playwright framework**: Check Playwright documentation
- **GitHub Actions**: Review GitHub Actions documentation
- **Project configuration**: Create an issue in this repository