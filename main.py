# ============================================================================
# COMPLETE MULTI-AGENT CONTENT GENERATION SYSTEM
# Kasparro AI Engineer Challenge
# ============================================================================

# ============================================================================
# 1. MODELS - Data structures
# ============================================================================

from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from enum import Enum
import json
from copy import deepcopy

@dataclass
class ProductModel:
    """Internal representation of product data"""
    name: str
    concentration: str
    skin_types: List[str]
    ingredients: List[str]
    benefits: List[str]
    usage: str
    side_effects: str
    price: int
    
    def to_dict(self) -> Dict:
        return asdict(self)

@dataclass
class Question:
    """Structured question with category"""
    category: str
    question: str
    answer: str
    
    def to_dict(self) -> Dict:
        return asdict(self)

class PageType(Enum):
    """Supported page types"""
    FAQ = "faq"
    PRODUCT = "product"
    COMPARISON = "comparison"


# ============================================================================
# 2. LOGIC BLOCKS - Reusable content transformation functions
# ============================================================================

class LogicBlocks:
    """Pure functions that transform product data into content segments"""
    
    @staticmethod
    def extract_benefits(product: ProductModel) -> Dict[str, Any]:
        """Transform benefits into structured format"""
        return {
            "section_type": "benefits",
            "title": "Key Benefits",
            "items": [
                {
                    "benefit": benefit,
                    "emphasis": "high"
                }
                for benefit in product.benefits
            ]
        }
    
    @staticmethod
    def generate_usage_instructions(product: ProductModel) -> Dict[str, Any]:
        """Create structured usage guide"""
        return {
            "section_type": "usage",
            "title": "How to Use",
            "instructions": product.usage,
            "frequency": "Daily",
            "timing": "Morning",
            "application_method": "Topical"
        }
    
    @staticmethod
    def format_ingredients(product: ProductModel) -> Dict[str, Any]:
        """Structure ingredient information"""
        return {
            "section_type": "ingredients",
            "title": "Active Ingredients",
            "primary": product.ingredients[0] if product.ingredients else None,
            "all_ingredients": product.ingredients,
            "concentration": product.concentration
        }
    
    @staticmethod
    def create_safety_content(product: ProductModel) -> Dict[str, Any]:
        """Generate safety warnings from side effects"""
        return {
            "section_type": "safety",
            "title": "Safety Information",
            "side_effects": product.side_effects,
            "severity": "mild",
            "recommendation": "Patch test recommended for sensitive skin"
        }
    
    @staticmethod
    def format_price(product: ProductModel) -> Dict[str, Any]:
        """Format price with currency"""
        return {
            "section_type": "price",
            "amount": product.price,
            "currency": "INR",
            "formatted": f"₹{product.price}"
        }
    
    @staticmethod
    def skin_type_matcher(product: ProductModel) -> Dict[str, Any]:
        """Format skin type recommendations"""
        return {
            "section_type": "skin_types",
            "title": "Suitable For",
            "types": product.skin_types,
            "recommendation": f"Ideal for {' and '.join(product.skin_types)} skin"
        }
    
    @staticmethod
    def compare_ingredients(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
        """Compare ingredients between products"""
        common = set(product_a.ingredients) & set(product_b.ingredients)
        unique_a = set(product_a.ingredients) - set(product_b.ingredients)
        unique_b = set(product_b.ingredients) - set(product_a.ingredients)
        
        return {
            "comparison_type": "ingredients",
            "common_ingredients": list(common),
            "unique_to_product_a": list(unique_a),
            "unique_to_product_b": list(unique_b)
        }
    
    @staticmethod
    def compare_benefits(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
        """Compare benefits between products"""
        return {
            "comparison_type": "benefits",
            "product_a_benefits": product_a.benefits,
            "product_b_benefits": product_b.benefits,
            "overlap": len(set(product_a.benefits) & set(product_b.benefits))
        }
    
    @staticmethod
    def compare_price(product_a: ProductModel, product_b: ProductModel) -> Dict[str, Any]:
        """Price comparison logic"""
        diff = product_a.price - product_b.price
        cheaper = product_a.name if diff < 0 else product_b.name
        
        return {
            "comparison_type": "price",
            "product_a_price": product_a.price,
            "product_b_price": product_b.price,
            "difference": abs(diff),
            "cheaper_product": cheaper
        }
    
    @staticmethod
    def generate_fictional_competitor(product: ProductModel) -> ProductModel:
        """Create a realistic fictional competitor product"""
        return ProductModel(
            name="RadiantGlow Vitamin C Complex",
            concentration="15% Vitamin C",
            skin_types=["All Skin Types", "Sensitive"],
            ingredients=["Vitamin C", "Vitamin E", "Ferulic Acid"],
            benefits=["Anti-aging", "Brightening", "Antioxidant protection"],
            usage="Apply 3-4 drops in the evening after cleansing",
            side_effects="May cause slight redness initially",
            price=899
        )


# ============================================================================
# 3. AGENTS - Single-responsibility autonomous units
# ============================================================================

class Agent(ABC):
    """Base class for all agents"""
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute agent logic"""
        pass
    
    def get_name(self) -> str:
        return self.__class__.__name__


class DataParserAgent(Agent):
    """Parses raw product JSON into internal ProductModel"""
    
    def execute(self, input_data: Dict) -> ProductModel:
        """
        Input: Raw product dictionary
        Output: ProductModel instance
        """
        return ProductModel(
            name=input_data["name"],
            concentration=input_data["concentration"],
            skin_types=input_data["skin_types"],
            ingredients=input_data["ingredients"],
            benefits=input_data["benefits"],
            usage=input_data["usage"],
            side_effects=input_data["side_effects"],
            price=input_data["price"]
        )


class QuestionGeneratorAgent(Agent):
    """Generates categorized user questions from product data"""
    
    QUESTION_TEMPLATES = {
        "Informational": [
            "What is {product_name}?",
            "What makes {product_name} effective?",
            "What is the concentration of active ingredients in {product_name}?"
        ],
        "Usage": [
            "How do I use {product_name}?",
            "When should I apply {product_name}?",
            "Can I use {product_name} with other products?",
            "How many drops of {product_name} should I use?"
        ],
        "Safety": [
            "Are there any side effects of {product_name}?",
            "Is {product_name} safe for sensitive skin?",
            "What precautions should I take when using {product_name}?"
        ],
        "Skin Type": [
            "Is {product_name} suitable for my skin type?",
            "Can oily skin use {product_name}?",
            "Is {product_name} good for combination skin?"
        ],
        "Benefits": [
            "What are the main benefits of {product_name}?",
            "How long until I see results from {product_name}?",
            "Does {product_name} help with dark spots?"
        ],
        "Purchase": [
            "How much does {product_name} cost?",
            "Where can I buy {product_name}?",
            "Is {product_name} worth the price?"
        ],
        "Comparison": [
            "How does {product_name} compare to other vitamin C serums?",
            "What makes {product_name} different?",
            "Should I choose {product_name} or another serum?"
        ]
    }
    
    def execute(self, input_data: ProductModel) -> List[Question]:
        """
        Input: ProductModel
        Output: List of Question objects (minimum 15)
        """
        questions = []
        
        for category, templates in self.QUESTION_TEMPLATES.items():
            for template in templates:
                question_text = template.format(product_name=input_data.name)
                answer = self._generate_answer(category, input_data)
                
                questions.append(Question(
                    category=category,
                    question=question_text,
                    answer=answer
                ))
        
        return questions[:20]  # Return 20 questions
    
    def _generate_answer(self, category: str, product: ProductModel) -> str:
        """Generate contextual answers based on category"""
        answers = {
            "Informational": f"{product.name} is a {product.concentration} serum designed for {', '.join(product.skin_types)} skin types.",
            "Usage": f"{product.usage}",
            "Safety": f"Possible side effects include: {product.side_effects}",
            "Skin Type": f"Yes, {product.name} is suitable for {', '.join(product.skin_types)} skin types.",
            "Benefits": f"Key benefits include: {', '.join(product.benefits)}",
            "Purchase": f"The price is ₹{product.price}",
            "Comparison": f"{product.name} features {', '.join(product.ingredients)} at {product.concentration}."
        }
        return answers.get(category, f"Based on product data: {product.name}")


class ContentStrategyAgent(Agent):
    """Decides which logic blocks to use for each page type"""
    
    def execute(self, input_data: Dict) -> Dict[str, Any]:
        """
        Input: {'product': ProductModel, 'page_type': PageType}
        Output: {'page_type': str, 'required_blocks': List[str], 'composition_order': List[str]}
        """
        page_type = input_data['page_type']
        
        strategies = {
            PageType.FAQ: {
                'required_blocks': [
                    'extract_benefits',
                    'generate_usage_instructions',
                    'create_safety_content',
                    'format_price'
                ],
                'composition_order': ['informational', 'usage', 'safety', 'purchase']
            },
            PageType.PRODUCT: {
                'required_blocks': [
                    'extract_benefits',
                    'format_ingredients',
                    'generate_usage_instructions',
                    'skin_type_matcher',
                    'format_price',
                    'create_safety_content'
                ],
                'composition_order': ['hero', 'benefits', 'ingredients', 'usage', 'skin_types', 'price', 'safety']
            },
            PageType.COMPARISON: {
                'required_blocks': [
                    'compare_ingredients',
                    'compare_benefits',
                    'compare_price'
                ],
                'composition_order': ['products', 'comparison_matrix', 'recommendation']
            }
        }
        
        strategy = strategies[page_type]
        return {
            'page_type': page_type.value,
            'required_blocks': strategy['required_blocks'],
            'composition_order': strategy['composition_order']
        }


class ComparisonAgent(Agent):
    """Generates fictional competitor and comparison data"""
    
    def execute(self, input_data: ProductModel) -> Dict[str, Any]:
        """
        Input: ProductModel (our product)
        Output: {'competitor': ProductModel, 'comparison_data': Dict}
        """
        competitor = LogicBlocks.generate_fictional_competitor(input_data)
        
        return {
            'product_a': input_data,
            'product_b': competitor,
            'comparisons': {
                'ingredients': LogicBlocks.compare_ingredients(input_data, competitor),
                'benefits': LogicBlocks.compare_benefits(input_data, competitor),
                'price': LogicBlocks.compare_price(input_data, competitor)
            }
        }


class TemplateRendererAgent(Agent):
    """Applies templates and logic blocks to generate final pages"""
    
    def __init__(self):
        self.logic_blocks = LogicBlocks()
    
    def execute(self, input_data: Dict) -> Dict[str, Any]:
        """
        Input: {
            'template_type': PageType,
            'data': Dict (product, questions, comparison, etc.),
            'strategy': ContentStrategy
        }
        Output: Rendered page as Dict
        """
        template_type = input_data['template_type']
        data = input_data['data']
        strategy = input_data.get('strategy', {})
        
        renderers = {
            PageType.FAQ: self._render_faq,
            PageType.PRODUCT: self._render_product,
            PageType.COMPARISON: self._render_comparison
        }
        
        return renderers[template_type](data, strategy)
    
    def _render_faq(self, data: Dict, strategy: Dict) -> Dict[str, Any]:
        """Render FAQ page"""
        product = data['product']
        questions = data['questions']
        
        # Select 5 diverse questions
        selected_questions = []
        categories_used = set()
        
        for q in questions:
            if q.category not in categories_used and len(selected_questions) < 5:
                selected_questions.append(q)
                categories_used.add(q.category)
        
        return {
            "page_type": "faq",
            "product_name": product.name,
            "total_questions": len(selected_questions),
            "questions": [q.to_dict() for q in selected_questions],
            "metadata": {
                "generated_from": "product_data",
                "categories": list(categories_used)
            }
        }
    
    def _render_product(self, data: Dict, strategy: Dict) -> Dict[str, Any]:
        """Render product page"""
        product = data['product']
        
        return {
            "page_type": "product",
            "hero": {
                "product_name": product.name,
                "tagline": f"Professional {product.concentration} serum for visible results"
            },
            "details": {
                "benefits": self.logic_blocks.extract_benefits(product),
                "ingredients": self.logic_blocks.format_ingredients(product),
                "usage": self.logic_blocks.generate_usage_instructions(product),
                "skin_types": self.logic_blocks.skin_type_matcher(product)
            },
            "pricing": self.logic_blocks.format_price(product),
            "safety": self.logic_blocks.create_safety_content(product),
            "metadata": {
                "product_category": "Skincare",
                "product_type": "Serum"
            }
        }
    
    def _render_comparison(self, data: Dict, strategy: Dict) -> Dict[str, Any]:
        """Render comparison page"""
        comparison_data = data['comparison']
        product_a = comparison_data['product_a']
        product_b = comparison_data['product_b']
        comparisons = comparison_data['comparisons']
        
        return {
            "page_type": "comparison",
            "products": {
                "product_a": {
                    "name": product_a.name,
                    "concentration": product_a.concentration,
                    "price": product_a.price,
                    "ingredients": product_a.ingredients,
                    "benefits": product_a.benefits
                },
                "product_b": {
                    "name": product_b.name,
                    "concentration": product_b.concentration,
                    "price": product_b.price,
                    "ingredients": product_b.ingredients,
                    "benefits": product_b.benefits
                }
            },
            "comparison_matrix": {
                "ingredients": comparisons['ingredients'],
                "benefits": comparisons['benefits'],
                "price": comparisons['price']
            },
            "recommendation": {
                "summary": f"{product_a.name} offers great value with {product_a.concentration} while {product_b.name} provides higher concentration at {product_b.concentration}",
                "best_for_budget": comparisons['price']['cheaper_product']
            }
        }


# ============================================================================
# 4. ORCHESTRATOR - DAG-based workflow coordinator
# ============================================================================

class WorkflowOrchestrator:
    """Coordinates agent execution using DAG pattern"""
    
    def __init__(self):
        self.agents = {
            'parser': DataParserAgent(),
            'questions': QuestionGeneratorAgent(),
            'strategy': ContentStrategyAgent(),
            'comparison': ComparisonAgent(),
            'renderer': TemplateRendererAgent()
        }
        self.state = {}
        self.execution_log = []
    
    def execute_pipeline(self, raw_product_data: Dict) -> Dict[str, Any]:
        """
        Execute complete pipeline using DAG pattern
        Returns all three generated pages
        """
        # Step 1: Parse product data
        self._log_step("Parsing product data")
        self.state['product'] = self.agents['parser'].execute(raw_product_data)
        
        # Step 2: Generate questions
        self._log_step("Generating user questions")
        self.state['questions'] = self.agents['questions'].execute(self.state['product'])
        
        # Step 3: Generate FAQ page
        self._log_step("Planning FAQ page strategy")
        faq_strategy = self.agents['strategy'].execute({
            'product': self.state['product'],
            'page_type': PageType.FAQ
        })
        
        self._log_step("Rendering FAQ page")
        faq_page = self.agents['renderer'].execute({
            'template_type': PageType.FAQ,
            'data': {
                'product': self.state['product'],
                'questions': self.state['questions']
            },
            'strategy': faq_strategy
        })
        
        # Step 4: Generate Product page
        self._log_step("Planning Product page strategy")
        product_strategy = self.agents['strategy'].execute({
            'product': self.state['product'],
            'page_type': PageType.PRODUCT
        })
        
        self._log_step("Rendering Product page")
        product_page = self.agents['renderer'].execute({
            'template_type': PageType.PRODUCT,
            'data': {
                'product': self.state['product']
            },
            'strategy': product_strategy
        })
        
        # Step 5: Generate comparison data
        self._log_step("Generating competitor and comparison data")
        comparison_data = self.agents['comparison'].execute(self.state['product'])
        
        # Step 6: Generate Comparison page
        self._log_step("Planning Comparison page strategy")
        comparison_strategy = self.agents['strategy'].execute({
            'product': self.state['product'],
            'page_type': PageType.COMPARISON
        })
        
        self._log_step("Rendering Comparison page")
        comparison_page = self.agents['renderer'].execute({
            'template_type': PageType.COMPARISON,
            'data': {
                'comparison': comparison_data
            },
            'strategy': comparison_strategy
        })
        
        return {
            'faq': faq_page,
            'product': product_page,
            'comparison': comparison_page
        }
    
    def _log_step(self, message: str):
        """Log execution steps"""
        self.execution_log.append(message)
        print(f"[Orchestrator] {message}")


# ============================================================================
# 5. MAIN EXECUTION
# ============================================================================

def main():
    """Main execution function"""
    
    # Input data (exactly as specified in assignment)
    raw_product_data = {
        "name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_types": ["Oily", "Combination"],
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "usage": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": 699
    }
    
    print("="*70)
    print("MULTI-AGENT CONTENT GENERATION SYSTEM")
    print("="*70)
    print()
    
    # Initialize orchestrator
    orchestrator = WorkflowOrchestrator()
    
    # Execute pipeline
    print("Starting pipeline execution...\n")
    results = orchestrator.execute_pipeline(raw_product_data)
    
    print("\n" + "="*70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("="*70)
    
    # Output results as JSON
    print("\n[Output] Generated Pages:\n")
    
    print("1. FAQ Page:")
    print(json.dumps(results['faq'], indent=2))
    print("\n" + "-"*70 + "\n")
    
    print("2. Product Page:")
    print(json.dumps(results['product'], indent=2))
    print("\n" + "-"*70 + "\n")
    
    print("3. Comparison Page:")
    print(json.dumps(results['comparison'], indent=2))

    save_outputs(results)

    
    return results


# Run the system
if __name__ == "__main__":
    def save_outputs(results):
        """Save generated pages to JSON files"""
        import os
        os.makedirs('output', exist_ok=True)
        with open('output/faq.json', 'w', encoding='utf-8') as f:
            json.dump(results['faq'], f, indent=2, ensure_ascii=False)
        with open('output/product_page.json', 'w', encoding='utf-8') as f:
            json.dump(results['product'], f, indent=2, ensure_ascii=False)
        with open('output/comparison_page.json', 'w', encoding='utf-8') as f:
            json.dump(results['comparison'], f, indent=2, ensure_ascii=False)
        print("\n✅ JSON files saved to output/ directory")

    output = main()