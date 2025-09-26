# Multi-Agent Orchestrator Demo

## Overview

This is a comprehensive demonstration of multi-agent orchestration that showcases how AI agents from different platforms can collaborate seamlessly to accomplish complex tasks. The project demonstrates three different orchestration approaches:

1. **Basic ACP Implementation** (`acp_poc.py`) - 2-agent n8n workflow orchestration
2. **Advanced Multi-Platform Orchestration** (`multi_agent_orchestrator.py`) - 3-agent system combining n8n and Azure AI
3. **Interactive Frontend Demo** (`agent_orchestrator_demo.html`) - Visual interface for orchestration workflows

## Why Multi-Agent Orchestration?

Multi-agent orchestration enables organizations to leverage specialized AI agents from different platforms (n8n, Azure AI Foundry, AWS Bedrock, Salesforce Agentforce, etc.) without being locked into a single vendor ecosystem. This approach provides:

- **Platform Flexibility**: Use the best agent for each specific task
- **Scalability**: Add new agents without restructuring existing workflows
- **Resilience**: Distribute workloads across multiple platforms
- **Cost Optimization**: Choose cost-effective platforms for different capabilities

## System Architecture

### 3-Agent Energy Consultation Workflow

```
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   STEP 1: n8n      │    │   STEP 2: Azure AI  │    │   STEP 3: n8n      │
│ Customer Processor  │───►│  Energy Consultant  │───►│ Validator Agent     │
│                     │    │                     │    │                     │
│ • Data validation   │    │ • GPT-4 analysis    │    │ • Compliance check  │
│ • Insight extraction│    │ • Personalized recs │    │ • Risk assessment   │
│ • Structure prep    │    │ • Savings estimates │    │ • Final approval    │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### Key Components:

- **Multi-Agent Registry**: Manages agent registration and capability discovery
- **Orchestration Engine**: Coordinates workflows across different agent platforms
- **n8n Integration**: Webhook-based communication with n8n workflow agents
- **Azure AI Integration**: Direct API communication with Azure AI Foundry agents
- **Interactive Frontend**: Real-time visualization of orchestration workflows

## Features Demonstrated

### Core Orchestration Features
✅ **Multi-Platform Integration**: n8n workflows + Azure AI Foundry agents  
✅ **Sequential Workflow**: 3-step energy consultation process  
✅ **Agent Registry**: Dynamic agent registration and capability discovery  
✅ **Real-time Coordination**: Live status updates and progress tracking  
✅ **Error Handling**: Comprehensive error handling and recovery  

### Frontend Demo Features
✅ **Interactive Task Visualization**: Clean task list with real-time status updates  
✅ **Agent Management**: Visual agent registry with registration simulation  
✅ **Live Progress Tracking**: Animated task progression with status indicators  
✅ **Results Export**: JSON export functionality for orchestration results  
✅ **Smart Validation Summary**: Intelligent parsing of validation results  

### Technical Features
✅ **CORS Support**: Full frontend-backend integration  
✅ **Webhook Integration**: n8n workflow agent communication  
✅ **Azure AI API**: Direct integration with Azure AI Foundry Agent Service  
✅ **Health Monitoring**: System health checks and agent status monitoring  

## Quick Start

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- Azure AI Foundry project (for Azure AI agent integration)
- n8n instance with webhook endpoints (for n8n agent integration)

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

#### Azure AI Foundry Setup
Create a `.env` file with your Azure AI Foundry configuration:
```bash
AZURE_AI_FOUNDRY_PROJECT_ENDPOINT=https://your-ai-service.services.ai.azure.com/api/projects/your-project-name
```

#### n8n Webhook Configuration
Update webhook URLs in the orchestrator files with your actual n8n webhook endpoints:
- Customer processing webhook
- Validation webhook

### Running the Demo

#### Option 1: Basic ACP Demo (2 agents)
```bash
python acp_poc.py
```

#### Option 2: Advanced Multi-Agent Demo (3 agents)
```bash
python multi_agent_orchestrator.py
```

#### Option 3: Interactive Frontend Demo
1. Start the orchestrator server:
```bash
python multi_agent_orchestrator.py
```

2. Open `agent_orchestrator_demo.html` in your browser

Server runs on `http://localhost:8080`

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

### 1. Energy Consultation Workflow (3-Agent Orchestration)

**Use Case**: Customer wants to reduce their electricity bill

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
   - Prepares structured data for AI analysis

2. **Step 2**: Azure AI Energy Consultant
   - Analyzes customer profile with GPT-4
   - Generates personalized energy efficiency recommendations
   - Estimates potential savings

3. **Step 3**: n8n Validation Agent
   - Validates recommendations for compliance
   - Performs risk assessment
   - Provides final approval status

**Expected Result:**
- Comprehensive energy consultation report
- Personalized recommendations (community solar, energy retrofits, etc.)
- Estimated savings: $7.50 - $37.50 per month
- Compliance validation with risk assessment

### 2. Interactive Frontend Demo

**Use Case**: Visual demonstration of multi-agent orchestration

**Features:**
- Real-time task progression visualization
- Agent registry management
- Live status updates and animations
- Results export functionality
- Validation summary with intelligent parsing

**Access**: Open `agent_orchestrator_demo.html` in your browser while the server is running

## File Structure

```
agent_orchestation/
├── README.md                           # This documentation
├── requirements.txt                    # Python dependencies
├── .env                               # Azure AI configuration (create this)
│
├── acp_poc.py                         # Basic 2-agent ACP implementation
├── multi_agent_orchestrator.py       # Advanced 3-agent orchestrator
├── azure_ai_foundry_client.py        # Azure AI Foundry integration
├── agent_orchestrator_demo.html      # Interactive frontend demo
│
└── venv/                              # Virtual environment (created by you)
```

## Key Technologies

### Backend Technologies
- **Python Flask**: Web server and API endpoints
- **Azure AI Foundry**: GPT-4 powered energy consultation agent
- **n8n Integration**: Webhook-based workflow agents
- **CORS Support**: Cross-origin resource sharing for frontend integration

### Frontend Technologies
- **HTML/CSS/JavaScript**: Interactive demo interface
- **Real-time Updates**: Live task progression and status updates
- **JSON Export**: Results download functionality
- **Responsive Design**: Clean, professional UI with animations

### Integration Patterns
- **Webhook Communication**: n8n agent integration
- **REST API**: Azure AI Foundry agent communication
- **Sequential Orchestration**: Step-by-step workflow coordination
- **Error Handling**: Comprehensive error recovery and reporting

## Development Roadmap

### Phase 1: Foundation ✅ (Completed)
- [x] Basic ACP server implementation (`acp_poc.py`)
- [x] Agent registry and discovery
- [x] Multi-agent orchestration (2-agent workflow)
- [x] n8n webhook integration

### Phase 2: Advanced Multi-Platform ✅ (Completed)
- [x] 3-agent orchestration system (`multi_agent_orchestrator.py`)
- [x] Azure AI Foundry integration (`azure_ai_foundry_client.py`)
- [x] Interactive frontend demo (`agent_orchestrator_demo.html`)
- [x] Real-time progress tracking and visualization
- [x] CORS support and error handling
- [x] Results export functionality
- [x] Smart validation parsing

### Phase 3: Enterprise Extensions 🚧 (Future)
- [ ] Salesforce Agentforce integration
- [ ] AWS Bedrock AgentCore wrapper
- [ ] Microsoft Copilot Studio integration
- [ ] Authentication and security layer
- [ ] Agent health monitoring and failover
- [ ] Performance metrics and analytics

## Configuration

### Environment Variables (.env file)
```bash
# Azure AI Foundry Configuration (Required)
AZURE_AI_FOUNDRY_PROJECT_ENDPOINT=https://your-ai-service.services.ai.azure.com/api/projects/your-project-name

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
python-dotenv==1.0.0
```

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

2. **Validation Shows 'Failed'**: 
   - This was fixed in the latest version
   - Refresh browser and try again

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

### Sample Energy Consultation Output

**Customer Input:**
- Inquiry: "I want to generate solar power electricity"  
- Home Type: Apartment
- Current Bill: $150/month

**3-Agent Orchestration Results:**
1. **Customer Processing**: Identified apartment solar challenges, recommended community solar programs
2. **AI Consultation**: Generated 5 personalized programs with savings estimates ($7.50-$37.50/month)
3. **Validation**: Compliance score 78/100, "Needs Review" status, Medium risk level

**Frontend Features Demonstrated:**
- Real-time task progression with animations
- Intelligent validation parsing (Fixed "Failed" → "Needs Review")
- Results export with full orchestration metadata
- Agent registration simulation

## References

- [Azure AI Foundry Documentation](https://docs.microsoft.com/en-us/azure/ai-services/)
- [n8n Webhook Integration Guide](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)
- [Flask-CORS Documentation](https://flask-cors.readthedocs.io/)
- [Multi-Agent Systems Research](https://arxiv.org/abs/2505.02279)

---

**Built with ❤️ for demonstrating the future of multi-platform AI agent orchestration**
