# Multi-Agent Orchestrator

## Overview

This is a comprehensive demonstration of **enterprise-grade multi-agent orchestration** that showcases how AI agents from different platforms can collaborate seamlessly to accomplish complex tasks. The project demonstrates a production-ready 5-agent orchestration system with a professional Microsoft Fluent Design interface:

1. **Basic ACP Implementation** (`acp_poc.py`) - 2-agent n8n workflow orchestration
2. **Advanced Multi-Platform Orchestration** (`multi_agent_orchestrator.py`) - **5-agent enterprise system** combining n8n, Azure AI, SAP AI Core, and Salesforce Agentforce
3. **Professional Frontend Demo** (`agent_orchestrator_demo.html`) - Microsoft Fluent Design UI for orchestration workflows

## Why Multi-Agent Orchestration?

Multi-agent orchestration enables organizations to leverage specialized AI agents from different platforms (n8n, Azure AI Foundry, AWS Bedrock, Salesforce Agentforce, etc.) without being locked into a single vendor ecosystem. This approach provides:

- **Platform Flexibility**: Use the best agent for each specific task
- **Scalability**: Add new agents without restructuring existing workflows
- **Resilience**: Distribute workloads across multiple platforms
- **Cost Optimization**: Choose cost-effective platforms for different capabilities

## System Architecture

### 5-Agent Enterprise Energy Consultation Workflow

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  STEP 1: n8n    │   │ STEP 2: SAP AI  │   │ STEP 3: Azure   │   │STEP 4: Salesf.  │   │  STEP 5: n8n    │
│   Customer      │──►│     Core        │──►│      AI         │──►│   Agentforce    │──►│   Validator     │
│   Processor     │   │  Data Enrich.   │   │   Consultant    │   │  Service Hist.  │   │     Agent       │
│                 │   │                 │   │                 │   │                 │   │                 │
│• Validation     │   │• Billing data   │   │• GPT-4 analysis │   │• CRM history    │   │• Compliance     │
│• Extraction     │   │• Consumption    │   │• AI recomm.     │   │• Open cases     │   │• Risk assess.   │
│• Structuring    │   │• Eligibility    │   │• Savings calc.  │   │• Customer tier  │   │• Approval       │
└─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘
```

### Key Components:

- **Multi-Agent Registry**: Manages agent registration and capability discovery
- **Orchestration Engine**: Coordinates workflows across 5 different agent platforms
- **n8n Integration**: Webhook-based communication with n8n workflow agents
- **SAP AI Core Integration**: Orchestration v2 API for enterprise data enrichment
- **Azure AI Integration**: Direct API communication with Azure AI Foundry agents (GPT-4o)
- **Salesforce Agentforce**: Real-time CRM integration with Agent API
- **Microsoft Fluent Design UI**: Professional, enterprise-ready frontend interface

## Features Demonstrated

### Core Orchestration Features
✅ **5-Platform Integration**: n8n + SAP AI Core + Azure AI + Salesforce Agentforce  
✅ **Enterprise Workflow**: 5-step energy consultation with enterprise data enrichment  
✅ **Agent Registry**: Dynamic agent registration and capability-based discovery  
✅ **Real-time Coordination**: Live status updates across multiple platforms  
✅ **Error Handling**: Comprehensive error handling with graceful fallbacks  
✅ **OAuth2 Integration**: Client credentials flow for Salesforce authentication  

### Frontend Demo Features (Microsoft Fluent Design)
✅ **Professional UI**: Microsoft Fluent Design System styling  
✅ **Interactive Visualization**: 5-task workflow with real-time progress tracking  
✅ **Agent Details Modal**: Complete API schemas, endpoints, and response formats  
✅ **Smart Status Updates**: Color-coded task states with Microsoft color palette  
✅ **Results Export**: Full orchestration metadata export to JSON  
✅ **Responsive Design**: Enterprise-grade professional interface  

### Technical Features
✅ **CORS Support**: Full frontend-backend integration  
✅ **n8n Webhooks**: Bidirectional workflow agent communication  
✅ **SAP AI Core Orchestration v2**: Templating, LLM, and grounding modules  
✅ **Azure AI Foundry**: GPT-4o integration with conversation threads  
✅ **Salesforce Agentforce API**: Session management with streaming responses  
✅ **Health Monitoring**: System health checks and agent status monitoring  
✅ **Fallback Mechanisms**: Graceful degradation when agents are unavailable  

## Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- **Azure AI Foundry project** (for Azure AI agent integration)
- **n8n instance** with webhook endpoints (for n8n agent integration)
- **Salesforce Developer/Sandbox** account with Agentforce enabled (optional - uses fallback data if unavailable)
- **SAP AI Core** instance (simulated in demo - no actual connection required)

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

#### Environment Variables Setup
Create a `.env` file in the project root with the following configuration:

```bash
# Azure AI Foundry (Required)
AZURE_AI_FOUNDRY_PROJECT_ENDPOINT=https://your-ai-service.services.ai.azure.com/api/projects/your-project-name

# Salesforce Agentforce (Optional - uses fallback if not configured)
SALESFORCE_CONSUMER_KEY=your_connected_app_consumer_key
SALESFORCE_CONSUMER_SECRET=your_connected_app_consumer_secret
SALESFORCE_AGENT_ID=0XxKj000001I9DuKAK
SALESFORCE_INSTANCE_URL=https://your-domain.my.salesforce.com
```

#### n8n Webhook Configuration
Update webhook URLs in `multi_agent_orchestrator.py` with your actual n8n webhook endpoints:
- Line 518: Customer processing webhook
- Line 554: Validation webhook

#### Salesforce Agentforce Setup (Optional)
1. Create a Connected App in Salesforce with OAuth enabled
2. Enable **Client Credentials Flow** and set a "Run As" user
3. Link the Connected App to your Agentforce Agent
4. Add Consumer Key and Secret to `.env` file

See `salesforce_agent_test.py` for a standalone test script.

### Running the Demo

#### Option 1: Basic ACP Demo (2 agents)
```bash
python acp_poc.py
```

#### Option 2: Enterprise Multi-Agent Demo (5 agents)
```bash
python multi_agent_orchestrator.py
```

This starts the full 5-agent orchestration system with:
- n8n Customer Processor
- SAP AI Core Data Enrichment
- Azure AI Energy Consultant
- Salesforce Agentforce Service History
- n8n Recommendation Validator

#### Option 3: Interactive Frontend Demo (Recommended)
1. Start the orchestrator server:
```bash
python multi_agent_orchestrator.py
```

2. Open `agent_orchestrator_demo.html` in your browser

3. Click "Execute 5-Agent Orchestration" to see the full workflow in action

Server runs on `http://localhost:8080`

#### Option 4: Test Salesforce Agent Standalone
```bash
python salesforce_agent_test.py
```

Tests direct communication with Salesforce Agentforce agent.

## API Endpoints

### Basic ACP Server (`acp_poc.py`)

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

#### Multi-Agent Orchestration
```bash
POST /orchestrate-multi
Content-Type: application/json

{
  "task": "process and validate customer data",
  "data": {"customer_id": "12345"}
}
```

### Advanced Multi-Agent Server (`multi_agent_orchestrator.py`)

#### Register Multi-Platform Agent
```bash
POST /agents/register
Content-Type: application/json

{
  "agent_id": "azure-ai-consultant",
  "agent_type": "azure_ai",
  "capabilities": ["energy_consultation", "customer_service"],
  "config": {
    "agent_id": "asst_aq7lhFm8W8ldxwte9pynGlsk",
    "model": "gpt-4o"
  }
}
```

#### Energy Consultation Orchestration
```bash
POST /orchestrate-energy
Content-Type: application/json

{
  "task": "energy efficiency consultation",
  "data": {
    "customer_id": "12345",
    "inquiry": "I want to reduce my electricity bill",
    "home_type": "apartment",
    "current_bill": 150
  }
}
```

#### Health Check
```bash
GET /health

# Response
{
  "status": "healthy",
  "agents_registered": 3,
  "azure_ai_ready": true
}
```

## Demo Scenarios

### 1. Enterprise Energy Consultation Workflow (5-Agent Orchestration)

**Use Case**: Customer wants to reduce their electricity bill with full enterprise context

```bash
curl -X POST http://localhost:8080/orchestrate-energy \
  -H "Content-Type: application/json" \
  -d '{
    "task": "energy efficiency consultation",
    "data": {
      "customer_id": "12345",
      "inquiry": "I want to reduce my electricity bill",
      "home_type": "apartment",
      "current_bill": 150
    }
  }'
```

**Orchestration Flow:**

1. **Step 1**: n8n Customer Processor
   - Validates customer input
   - Extracts insights from inquiry
   - Prepares structured data for downstream processing

2. **Step 2**: SAP AI Core Data Enrichment
   - Retrieves billing history from SAP ERP
   - Analyzes energy consumption patterns
   - Checks program eligibility in SAP CRM
   - Uses Orchestration v2 with templating and grounding modules

3. **Step 3**: Azure AI Energy Consultant (GPT-4o)
   - Analyzes customer profile + SAP enterprise data
   - Generates personalized energy efficiency recommendations
   - Estimates potential savings based on real billing data
   - Creates conversation thread for context retention

4. **Step 4**: Salesforce Agentforce Service History
   - Queries CRM for customer service history
   - Checks for open cases or complaints
   - Retrieves previous energy-related inquiries
   - Validates customer tier and standing

5. **Step 5**: n8n Validation Agent
   - Validates recommendations for compliance
   - Performs risk assessment considering service history
   - Provides final approval status
   - Generates executive summary

**Expected Result:**
- Comprehensive energy consultation with full enterprise context
- Personalized recommendations informed by billing data + service history
- Estimated savings: $23-$37 per month
- Compliance validation: 85-95/100 score
- Service history context: Previous inquiries and customer satisfaction

### 2. Interactive Frontend Demo (Microsoft Fluent Design)

**Use Case**: Professional visualization of 5-agent enterprise orchestration

**Features:**
- **Microsoft Fluent Design**: Professional UI matching Microsoft 365 style
- **5-Agent Visualization**: Real-time progress across all 5 agents
- **Agent Details Modal**: Click any agent to see API schemas and endpoints
- **Live Status Updates**: Color-coded task states with smooth animations
- **Results Export**: Full orchestration metadata export
- **Enterprise-Ready**: Production-quality interface design

**Access**: Open `agent_orchestrator_demo.html` in your browser while the server is running

**UI Highlights:**
- Microsoft Blue (#0078d4) primary color
- Fluent Design shadows and spacing
- Professional scrollbars and hover effects
- VS Code-style code blocks
- Responsive enterprise layout

## File Structure

```
agent_orchestation/
├── README.md                           # This comprehensive documentation
├── requirements.txt                    # Python dependencies
├── .env                               # Environment variables (create this)
│
├── acp_poc.py                         # Basic 2-agent ACP implementation
├── multi_agent_orchestrator.py       # ⭐ 5-agent enterprise orchestrator
├── azure_ai_foundry_client.py        # Azure AI Foundry integration
├── salesforce_agent_test.py          # ⭐ Salesforce Agentforce test client
├── agent_orchestrator_demo.html      # ⭐ Microsoft Fluent Design UI
│
├── FRAMEWORK_GOBIERNO_AGENTES.md     # Agent governance framework (Spanish)
└── venv/                              # Virtual environment (created by you)
```

## Key Technologies

### Backend Technologies
- **Python Flask**: Web server and REST API endpoints
- **Azure AI Foundry**: GPT-4o powered energy consultation with conversation threads
- **SAP AI Core Orchestration v2**: Templating, LLM, and grounding modules (simulated)
- **Salesforce Agentforce API**: Real-time CRM integration with OAuth2 + streaming
- **n8n Integration**: Webhook-based workflow agents
- **CORS Support**: Full cross-origin resource sharing

### Frontend Technologies  
- **Microsoft Fluent Design**: Professional enterprise UI system
- **HTML/CSS/JavaScript**: Modern, responsive interface
- **Real-time Updates**: Live 5-task progression with animations
- **Agent Details Modal**: Complete API documentation display
- **JSON Export**: Full orchestration metadata export
- **VS Code Themes**: Professional code block styling

### Integration Patterns
- **Webhook Communication**: Bidirectional n8n integration
- **REST APIs**: Azure AI, SAP AI Core, Salesforce Agentforce
- **OAuth2 Client Credentials**: Secure Salesforce authentication
- **Server-Sent Events**: Salesforce streaming response handling
- **Sequential Orchestration**: 5-step enterprise workflow
- **Fallback Mechanisms**: Graceful degradation when services unavailable
- **Error Handling**: Comprehensive error recovery and user feedback

## Development Roadmap

### Phase 1: Foundation ✅ (Completed)
- [x] Basic ACP server implementation (`acp_poc.py`)
- [x] Agent registry and discovery
- [x] Multi-agent orchestration (2-agent workflow)
- [x] n8n webhook integration

### Phase 2: Advanced Multi-Platform ✅ (Completed)
- [x] 3-agent orchestration system
- [x] Azure AI Foundry integration with GPT-4o
- [x] Interactive frontend demo
- [x] Real-time progress tracking and visualization
- [x] CORS support and error handling
- [x] Results export functionality
- [x] Smart validation parsing

### Phase 3: Enterprise Integration ✅ (Completed)
- [x] **5-agent enterprise orchestration system**
- [x] **SAP AI Core Orchestration v2 integration** (simulated)
- [x] **Salesforce Agentforce API integration** (`salesforce_agent_test.py`)
- [x] **OAuth2 Client Credentials Flow** for Salesforce
- [x] **Microsoft Fluent Design UI** transformation
- [x] Agent details modal with API schemas
- [x] Fallback mechanisms for unavailable services
- [x] Professional enterprise-grade interface

### Phase 4: Production Readiness 🚧 (Future)
- [ ] AWS Bedrock AgentCore wrapper
- [ ] Microsoft Copilot Studio integration
- [ ] Authentication and role-based access control
- [ ] Agent health monitoring dashboard
- [ ] Performance metrics and analytics
- [ ] Load balancing and horizontal scaling
- [ ] Audit logging and compliance reporting

## Configuration

### Environment Variables (.env file)
```bash
# Azure AI Foundry Configuration (Required)
AZURE_AI_FOUNDRY_PROJECT_ENDPOINT=https://your-ai-service.services.ai.azure.com/api/projects/your-project-name

# Salesforce Agentforce Configuration (Optional - uses fallback if not provided)
SALESFORCE_CONSUMER_KEY=your_connected_app_consumer_key
SALESFORCE_CONSUMER_SECRET=your_connected_app_consumer_secret
SALESFORCE_AGENT_ID=0XxKj000001I9DuKAK
SALESFORCE_INSTANCE_URL=https://your-domain.my.salesforce.com

# Azure Authentication (Optional - uses DefaultAzureCredential by default)
AZURE_CLIENT_ID=your-client-id
AZURE_CLIENT_SECRET=your-client-secret
AZURE_TENANT_ID=your-tenant-id

# Server Configuration (Optional)
FLASK_HOST=0.0.0.0
FLASK_PORT=8080
FLASK_DEBUG=true
```

### Agent Configuration
Update webhook URLs and agent IDs in the orchestrator files:

**multi_agent_orchestrator.py:**
```python
# n8n Customer Processor
webhook_url="https://your-n8n-instance.com/webhook/customer-processor"

# Azure AI Agent
agent_id="asst_your_agent_id"

# n8n Validator
webhook_url="https://your-n8n-instance.com/webhook/validator"
```

### Dependencies (requirements.txt)
```
flask==3.0.0
flask-cors==4.0.0
requests==2.31.0
azure-identity==1.15.0
azure-core==1.35.1
python-dotenv==1.0.0
```

**Note**: The system includes graceful fallbacks, so:
- SAP AI Core integration is simulated (no actual connection required)
- Salesforce Agentforce uses fallback data if not configured
- Only Azure AI Foundry and n8n are strictly required for core functionality

## Troubleshooting

### Common Issues

#### Azure AI Integration
1. **Authentication Failed**: 
   - Run `az login` to authenticate with Azure CLI
   - Verify `AZURE_AI_FOUNDRY_PROJECT_ENDPOINT` is correct
   - Check Azure AI Developer role permissions

2. **Agent Not Found**: 
   - Verify agent ID `asst_aq7lhFm8W8ldxwte9pynGlsk` exists
   - Check agent is in the correct Azure AI project

#### n8n Integration
1. **Webhook Timeout**: 
   - Verify n8n webhook URLs are accessible
   - Check webhook responds within 30 seconds
   - Test webhooks independently with curl

2. **CORS Errors**: 
   - Ensure `flask-cors` is installed
   - Verify CORS is enabled in the Flask app

#### Frontend Demo
1. **Cannot Connect to Server**: 
   - Start `multi_agent_orchestrator.py` first
   - Check server is running on `http://localhost:8080`
   - Verify CORS is enabled

2. **UI Styling Issues**: 
   - Clear browser cache (Ctrl+Shift+R)
   - Ensure latest `agent_orchestrator_demo.html` is loaded
   - Microsoft Fluent Design requires modern browser (Chrome 90+, Edge 90+, Firefox 88+)

#### Salesforce Agentforce Integration
1. **Authentication Failed**: 
   - Verify Connected App Consumer Key/Secret in `.env`
   - Check "Client Credentials Flow" is enabled in Connected App
   - Ensure "Run As" user is configured
   
2. **Agent Not Responding**: 
   - Verify Connected App is linked to the Agent
   - Check Agent ID is correct (18 characters)
   - System uses fallback data if agent unavailable - no error shown

#### SAP AI Core Integration
- **Note**: SAP integration is simulated with realistic data
- No actual SAP AI Core connection required
- All billing/consumption data is generated for demo purposes

### Debug Mode
Enable detailed logging:
```python
app.run(host='0.0.0.0', port=8080, debug=True)
```

### Testing Individual Components

#### Test Azure AI Client
```bash
python azure_ai_foundry_client.py
```

#### Test n8n Webhooks
```bash
curl -X POST https://your-n8n-webhook-url \
  -H "Content-Type: application/json" \
  -d '{"task": "test", "data": {"test": true}}'
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Demo Results

### Sample 5-Agent Energy Consultation Output

**Customer Input:**
- Customer ID: 12345
- Inquiry: "I want to reduce my electricity bill"
- Home Type: Apartment
- Current Bill: $150/month

**5-Agent Orchestration Results:**

1. **Step 1 - n8n Customer Processing**: 
   - Extracted: cost_reduction, efficiency concerns
   - Segment: residential, Priority: medium
   - Processing time: <1s

2. **Step 2 - SAP AI Core Data Enrichment**:
   - Retrieved billing history: $152.45 avg/month, increasing trend
   - Energy consumption: 890 kWh/month average
   - Eligible for 2 programs: energy_efficiency_rebate, smart_thermostat_program
   - Processing time: 2.8s

3. **Step 3 - Azure AI Consultation (GPT-4o)**:
   - Generated 5 personalized programs
   - Estimated savings: $23-$37/month
   - Implementation timeline provided
   - Processing time: 4.2s

4. **Step 4 - Salesforce Service History**:
   - 0 open cases, 2 closed cases last 12 months
   - Customer satisfaction: 4.5/5
   - Previous interest: smart thermostat compatibility
   - Processing time: 1.8s

5. **Step 5 - n8n Validation**:
   - Compliance score: 92/100
   - Status: "Approved"
   - Risk level: Low
   - Processing time: <1s

**Total Orchestration Time**: ~10 seconds  
**Frontend**: Microsoft Fluent Design with professional animations

## References

### Platform Documentation
- [Azure AI Foundry Documentation](https://learn.microsoft.com/en-us/azure/ai-studio/)
- [SAP AI Core Orchestration v2](https://help.sap.com/docs/ai-core/sap-ai-core-service-guide/orchestration)
- [Salesforce Agentforce Agent API](https://developer.salesforce.com/docs/einstein/genai-api/guide/agent-api.html)
- [n8n Webhook Integration Guide](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)

### Design Systems
- [Microsoft Fluent Design System](https://fluent2.microsoft.design/)
- [Fluent UI Components](https://developer.microsoft.com/en-us/fluentui)

### Technical Resources
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [OAuth 2.0 Client Credentials Flow](https://oauth.net/2/grant-types/client-credentials/)
- [Server-Sent Events (SSE) Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [Multi-Agent Systems Research](https://arxiv.org/abs/2505.02279)

---

**Built with ❤️ for demonstrating the future of enterprise multi-platform AI agent orchestration**

*Showcasing 5 agents across n8n, SAP AI Core, Azure AI Foundry, and Salesforce Agentforce platforms*
