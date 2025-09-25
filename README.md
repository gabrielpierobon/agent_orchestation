# ACP (Agent Communication Protocol) Proof of Concept

## Overview

This is a demonstration implementation of the Agent Communication Protocol (ACP) - an open standard for AI agent communication that enables autonomous agents from different platforms to discover and collaborate with each other dynamically without central orchestration.

## Why ACP?

ACP provides the best solution for multi-platform agent orchestration because it acts as a universal translation layer that enables agents built on completely different platforms (AWS Bedrock, Salesforce Agentforce, SAP Joule, etc.) to discover and communicate with each other directly without requiring custom integrations for each platform combination. Unlike traditional orchestration approaches that force all communication through a central hub with platform-specific connectors, ACP's HTTP-based protocol allows agents to find each other dynamically based on capabilities and collaborate as autonomous peers.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agent A       │    │   ACP Server    │    │   Agent B       │
│  (Salesforce)   │◄──►│                 │◄──►│   (SAP ERP)     │
└─────────────────┘    │  Agent Registry │    └─────────────────┘
                       │  Discovery      │    
┌─────────────────┐    │  Message Router │    ┌─────────────────┐
│   Agent C       │◄──►│                 │◄──►│   Agent D       │
│  (AWS Bedrock)  │    └─────────────────┘    │   (n8n Flow)    │
└─────────────────┘                           └─────────────────┘
```

### Key Components:

- **ACP Server**: Central HTTP-based registry and message routing service
- **Agent Registry**: Database of available agents, their capabilities, and endpoints
- **Discovery Service**: Allows agents to find other agents based on capabilities
- **Direct Communication**: Agents communicate peer-to-peer via HTTP REST calls

## Features Demonstrated

✅ **Agent Registration**: Agents register themselves with capabilities and webhook URLs  
✅ **Dynamic Discovery**: Find agents based on required capabilities  
✅ **Single-Agent Orchestration**: Route tasks to appropriate agents  
✅ **Multi-Agent Collaboration**: Coordinate complex workflows across multiple agents  
✅ **Direct Agent Communication**: Agents call each other without central orchestration  
✅ **Platform Agnostic**: Works with any agent that can receive HTTP webhooks  

## Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. **Clone and setup environment:**
```bash
git clone <your-repo>
cd agent_orchestation
```

2. **Create virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Configuration

Before running, update the webhook URLs in `acp_poc.py` (lines 229-240) with your actual n8n or agent webhook endpoints:

```python
# Replace these URLs with your actual agent webhooks
webhook_url="https://your-n8n-instance.com/webhook/your-webhook-id"
```

### Run the Server

```bash
python acp_poc.py
```

Server starts on `http://localhost:8080`

## API Endpoints

### Standard ACP Endpoints

#### Register Agent
```bash
POST /agents/register
Content-Type: application/json

{
  "agent_id": "my-agent",
  "capabilities": ["data_processing", "analysis"],
  "webhook_url": "https://my-agent.com/webhook"
}
```

#### Discover Agents
```bash
GET /agents/discover/{capability}

# Example
curl http://localhost:8080/agents/discover/customer_processing
```

#### Single-Agent Orchestration
```bash
POST /orchestrate
Content-Type: application/json

{
  "task": "process customer data",
  "data": {"customer_id": "12345"}
}
```

#### Multi-Agent Orchestration
```bash
POST /orchestrate-multi
Content-Type: application/json

{
  "task": "process and validate customer data",
  "data": {"customer_id": "12345"}
}
```

## Example Usage Scenarios

### 1. Customer Data Processing (Single Agent)
```bash
curl -X POST http://localhost:8080/orchestrate \
  -H "Content-Type: application/json" \
  -d '{"task": "process customer data", "data": {"customer_id": "12345"}}'
```

**ACP Flow:**
1. Server analyzes task: "customer" → needs `customer_processing` capability
2. Discovery: Finds agents with `customer_processing` capability
3. Routes to first available agent
4. Agent processes request and returns result

### 2. Multi-Agent Workflow (Process + Validate)
```bash
curl -X POST http://localhost:8080/orchestrate-multi \
  -H "Content-Type: application/json" \
  -d '{"task": "process and validate customer", "data": {"customer_id": "12345"}}'
```

**ACP Flow:**
1. **Step 1**: Route to `customer_processing` agent → Process data
2. **Step 2**: Route to `data_validation` agent → Validate processed data
3. **Result**: Combined workflow with results from both agents

### 3. Enterprise Scenario: Quarterly Report Generation

**Scenario**: Generate investor relations report using data from multiple enterprise systems

**Agents Involved:**
- **SAP Agent**: Provides financial data (`quarterly_revenue`, `operational_costs`)
- **Salesforce Agent**: Provides customer metrics (`customer_metrics`, `pipeline_data`)  
- **IR Agent**: Generates professional reports (`report_generation`)

**ACP Workflow:**
1. IR Agent discovers: "Who can provide revenue data?" → Finds SAP Agent
2. IR Agent → SAP Agent: "Get Q4 2024 revenue breakdown"
3. IR Agent discovers: "Who has customer data?" → Finds Salesforce Agent  
4. IR Agent → Salesforce Agent: "Get customer acquisition metrics"
5. IR Agent combines data → Generates comprehensive Q4 report

## Extending to Enterprise Platforms

This demo shows the foundation for integrating with enterprise agent platforms:

### Salesforce Agentforce Integration
- **Current**: n8n webhook agents
- **Enterprise**: Salesforce Agent API wrapper
- **ACP Translation**: HTTP messages ↔ Salesforce Agent API calls

### SAP Joule Integration  
- **Current**: n8n webhook agents
- **Enterprise**: SAP MCP/BTP integration
- **ACP Translation**: HTTP messages ↔ SAP Joule API calls

### AWS Bedrock AgentCore Integration
- **Current**: n8n webhook agents  
- **Enterprise**: InvokeAgentRuntime API wrapper
- **ACP Translation**: HTTP messages ↔ AWS Bedrock API calls

## ACP vs Other Protocols

| Feature | ACP | A2A | MCP |
|---------|-----|-----|-----|
| **Governance** | Open standard (Linux Foundation) | Google-led consortium | Anthropic-led |
| **Integration** | Standard HTTP (no SDK required) | Platform-specific | JSON-RPC based |
| **Discovery** | Offline capability-based | Online registry | Limited discovery |
| **Architecture** | Peer-to-peer | Hub-and-spoke | Client-server |
| **Enterprise** | Framework agnostic | Vendor ecosystem | Tool-specific |

## Development Roadmap

### Phase 1: Foundation (Current)
- [x] Basic ACP server implementation
- [x] Agent registry and discovery
- [x] Single and multi-agent orchestration
- [x] n8n webhook integration

### Phase 2: Enterprise Integration
- [ ] Salesforce Agentforce wrapper
- [ ] SAP Joule/MCP integration  
- [ ] AWS Bedrock AgentCore wrapper
- [ ] Authentication and security layer

### Phase 3: Advanced Features
- [ ] Agent health monitoring
- [ ] Load balancing and failover
- [ ] Workflow orchestration (Airflow integration)
- [ ] Advanced discovery algorithms
- [ ] Performance monitoring and metrics

## Configuration

### Environment Variables
```bash
# Server configuration
ACP_SERVER_PORT=8080
ACP_SERVER_HOST=0.0.0.0

# Agent timeouts
ACP_AGENT_TIMEOUT=30
ACP_DISCOVERY_TIMEOUT=5

# Security (future)
ACP_AUTH_ENABLED=false
ACP_API_KEY=""
```

### Agent Capability Mapping
The system uses keyword-to-capability mapping for task routing:

```python
capability_map = {
    "customer": "customer_processing",
    "data": "data_analysis", 
    "process": "data_processing",
    "invoice": "invoice_processing"
}
```

Add new mappings to handle different task types.

## Troubleshooting

### Common Issues

1. **Agent not found**: Check if agent is registered and webhook URL is accessible
2. **Timeout errors**: Verify agent webhook responds within 30 seconds
3. **Discovery fails**: Ensure agent capabilities match required capabilities exactly

### Debug Mode
Enable detailed logging by setting `debug=True` in the Flask app configuration.

### Testing Webhooks
Use tools like ngrok to expose local endpoints for testing:
```bash
ngrok http 8080
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## References

- [Agent Communication Protocol (ACP) - IBM Research](https://agentcommunicationprotocol.dev)
- [ACP Specification - Linux Foundation](https://github.com/i-am-bee/acp)
- [Agent Interoperability Protocols Survey](https://arxiv.org/abs/2505.02279)

---

**Built with ❤️ for the future of AI agent orchestration**
