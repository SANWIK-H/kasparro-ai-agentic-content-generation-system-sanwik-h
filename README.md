Multi-Agent Content Generation System
Show Image
Show Image

Kasparro AI Engineer Challenge: A production-grade multi-agent system for automated content page generation.

🎯 Project Overview
This system transforms a single product dataset into multiple machine-readable content pages using a modular, multi-agent architecture. It demonstrates proper software engineering principles applied to AI/automation workflows.

Key Features:

✅ 5 specialized agents with clear boundaries
✅ DAG-based workflow orchestration
✅ 9+ reusable content logic blocks
✅ Schema-driven template engine
✅ Generates 3 page types: FAQ, Product, Comparison
✅ 100% machine-readable JSON output
🏗️ Architecture
Raw Product JSON
       ↓
┌─────────────────────────────┐
│  Workflow Orchestrator      │ ← State Machine / DAG
└─────────────────────────────┘
       ↓
   5 Specialized Agents
       ├─→ DataParserAgent
       ├─→ QuestionGeneratorAgent
       ├─→ ContentStrategyAgent
       ├─→ ComparisonAgent
       └─→ TemplateRendererAgent
       ↓
   Logic Block Layer (9 blocks)
       ↓
   Template Engine
       ↓
   3 JSON Pages
📂 Project Structure
kasparro-ai-agentic-content-generation-system/
├── main.py                    # Main execution script (all-in-one)
├── output/                    # Generated JSON pages
│   ├── faq.json
│   ├── product_page.json
│   └── comparison_page.json
├── docs/
│   └── projectdocumentation.md  # Complete system documentation
├── requirements.txt           # Python dependencies (stdlib only)
└── README.md                  # This file
🚀 Quick Start
Prerequisites
Python 3.8 or higher
No external dependencies (uses Python standard library only)
Installation
bash
# Clone the repository
git clone https://github.com/sanwik-h/kasparro-ai-agentic-content-generation-system-<your-name>.git
cd kasparro-ai-agentic-content-generation-system-<your-name>

# No pip install needed - uses standard library only!
Running the System
bash
python main.py
Expected Output
The system will:

Parse the product data
Generate 20 categorized questions
Execute agents through the orchestration pipeline
Output 3 JSON files to console
==================================================================
MULTI-AGENT CONTENT GENERATION SYSTEM
==================================================================

Starting pipeline execution...

[Orchestrator] Parsing product data
[Orchestrator] Generating user questions
[Orchestrator] Planning FAQ page strategy
[Orchestrator] Rendering FAQ page
[Orchestrator] Planning Product page strategy
[Orchestrator] Rendering Product page
[Orchestrator] Generating competitor and comparison data
[Orchestrator] Planning Comparison page strategy
[Orchestrator] Rendering Comparison page

==================================================================
PIPELINE COMPLETED SUCCESSFULLY
==================================================================

[Output] Generated Pages:

1. FAQ Page:
{...}

2. Product Page:
{...}

3. Comparison Page:
{...}
🧩 System Components
1. Agents (5 Total)
Agent	Responsibility	Input	Output
DataParserAgent	Parse raw JSON into typed model	Dict	ProductModel
QuestionGeneratorAgent	Generate categorized questions	ProductModel	List[Question]
ContentStrategyAgent	Decide which blocks to use	ProductModel + PageType	ContentStrategy
ComparisonAgent	Generate competitor & comparison	ProductModel	ComparisonData
TemplateRendererAgent	Render final pages	Strategy + Data	Dict (JSON)
2. Logic Blocks (9+ Total)
Content Extraction:

extract_benefits() - Benefits with emphasis
format_ingredients() - Ingredient structure
generate_usage_instructions() - Usage guide
create_safety_content() - Safety warnings
format_price() - Price formatting
skin_type_matcher() - Skin type recommendations
Comparison:

compare_ingredients() - Ingredient comparison
compare_benefits() - Benefit analysis
compare_price() - Price comparison
Generation:

generate_fictional_competitor() - Create competitor
3. Orchestrator
Pattern: State Machine with DAG execution
Responsibilities:
Manages agent execution order
Maintains state between steps
Routes data between agents
Logs execution flow
4. Templates
Three schema-driven templates:

FAQ Template: Generates Q&A pages
Product Template: Complete product information
Comparison Template: Side-by-side comparison
📊 Input Data
The system operates on this exact dataset (as specified in the challenge):

json
{
  "name": "GlowBoost Vitamin C Serum",
  "concentration": "10% Vitamin C",
  "skin_types": ["Oily", "Combination"],
  "ingredients": ["Vitamin C", "Hyaluronic Acid"],
  "benefits": ["Brightening", "Fades dark spots"],
  "usage": "Apply 2–3 drops in the morning before sunscreen",
  "side_effects": "Mild tingling for sensitive skin",
  "price": 699
}
📤 Output Examples
FAQ Page (faq.json)
json
{
  "page_type": "faq",
  "product_name": "GlowBoost Vitamin C Serum",
  "total_questions": 5,
  "questions": [
    {
      "category": "Informational",
      "question": "What is GlowBoost Vitamin C Serum?",
      "answer": "GlowBoost Vitamin C Serum is a 10% Vitamin C serum..."
    }
    // ... 4 more questions
  ]
}
Product Page (product_page.json)
json
{
  "page_type": "product",
  "hero": {
    "product_name": "GlowBoost Vitamin C Serum",
    "tagline": "Professional 10% Vitamin C serum for visible results"
  },
  "details": {
    "benefits": {...},
    "ingredients": {...},
    "usage": {...}
  }
}
Comparison Page (comparison_page.json)
json
{
  "page_type": "comparison",
  "products": {
    "product_a": {...},
    "product_b": {...}
  },
  "comparison_matrix": {
    "ingredients": {...},
    "benefits": {...},
    "price": {...}
  }
}
🔧 Extending the System
Adding a New Page Type
Add to PageType enum:
python
class PageType(Enum):
    NEW_TYPE = "new_type"
Add strategy to ContentStrategyAgent:
python
strategies[PageType.NEW_TYPE] = {
    'required_blocks': ['block1', 'block2'],
    'composition_order': ['section1', 'section2']
}
Add render method to TemplateRendererAgent:
python
def _render_new_type(self, data, strategy):
    # Implementation
    pass
Adding a New Logic Block
Simply add a static method to LogicBlocks:

python
@staticmethod
def new_block(product: ProductModel) -> Dict[str, Any]:
    return {
        "section_type": "new_section",
        "data": transformed_data
    }
📚 Documentation
Comprehensive documentation is available in docs/projectdocumentation.md, including:

Problem statement
Solution overview
System design (architecture, agents, data flow)
Design decisions and rationale
Extensibility guide
🎯 Design Principles
Single Responsibility: Each agent has one clear purpose
Stateless Execution: Agents don't maintain internal state
Composability: Logic blocks can be mixed across templates
Type Safety: All functions have explicit type hints
No Hidden Dependencies: All data flows explicitly through orchestrator
✅ Evaluation Criteria Alignment
Criteria	Weight	Implementation
Agentic System Design	45%	✅ DAG orchestration, clear boundaries, extensible
Types & Quality of Agents	25%	✅ 5 specialized agents, proper I/O contracts
Content System Engineering	20%	✅ 9+ reusable blocks, composable templates
Data & Output Structure	10%	✅ Valid JSON, clean data mapping
🧪 Testing
Each component can be tested independently:

python
# Test a logic block
product = ProductModel(...)
result = LogicBlocks.extract_benefits(product)
assert result['section_type'] == 'benefits'

# Test an agent
agent = DataParserAgent()
output = agent.execute(raw_data)
assert isinstance(output, ProductModel)
📝 Technical Notes
Language: Python 3.8+
Dependencies: Standard library only (dataclasses, json, abc, enum)
Design Patterns: Abstract Factory, Strategy, State Machine
Code Style: PEP 8 compliant
Type Safety: Full type hints throughout
🚫 What This Is NOT
❌ Not a prompting exercise
❌ Not a "call GPT 3 times" wrapper
❌ Not a content writing test
❌ Not a UI/frontend challenge
This is a systems engineering and automation challenge.

📧 Contact
For questions about this implementation, please refer to the comprehensive documentation in docs/projectdocumentation.md.

Built for the Kasparro AI Engineer Challenge | Demonstrates production-grade multi-agent system design

