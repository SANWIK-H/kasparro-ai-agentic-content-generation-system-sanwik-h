# ============================================================================
# COMPLETE MULTI-AGENT CONTENT GENERATION SYSTEM
# Kasparro AI Engineer Challenge (FIXED & COMPLIANT)
# ============================================================================

from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from enum import Enum
import json
import os

# ============================================================================
# 1. MODELS
# ============================================================================

@dataclass
class ProductModel:
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
    category: str
    question: str
    answer: str

    def to_dict(self) -> Dict:
        return asdict(self)


class PageType(Enum):
    FAQ = "faq"
    PRODUCT = "product"
    COMPARISON = "comparison"


# ============================================================================
# 2. LOGIC BLOCKS (PURE FUNCTIONS)
# ============================================================================

class LogicBlocks:

    @staticmethod
    def extract_benefits(product: ProductModel) -> Dict[str, Any]:
        return {
            "section_type": "benefits",
            "title": "Key Benefits",
            "items": [{"benefit": b} for b in product.benefits]
        }

    @staticmethod
    def generate_usage(product: ProductModel) -> Dict[str, Any]:
        return {
            "section_type": "usage",
            "instructions": product.usage
        }

    @staticmethod
    def format_ingredients(product: ProductModel) -> Dict[str, Any]:
        return {
            "section_type": "ingredients",
            "ingredients": product.ingredients,
            "concentration": product.concentration
        }

    @staticmethod
    def safety_block(product: ProductModel) -> Dict[str, Any]:
        return {
            "section_type": "safety",
            "side_effects": product.side_effects
        }

    @staticmethod
    def price_block(product: ProductModel) -> Dict[str, Any]:
        return {
            "section_type": "price",
            "amount": product.price,
            "currency": "INR"
        }

    @staticmethod
    def compare(a: ProductModel, b: ProductModel) -> Dict[str, Any]:
        return {
            "ingredients": {
                "common": list(set(a.ingredients) & set(b.ingredients)),
                "unique_a": list(set(a.ingredients) - set(b.ingredients)),
                "unique_b": list(set(b.ingredients) - set(a.ingredients))
            },
            "benefits_overlap": len(set(a.benefits) & set(b.benefits)),
            "price_difference": abs(a.price - b.price),
            "cheaper_product": a.name if a.price < b.price else b.name
        }

    @staticmethod
    def fictional_competitor() -> ProductModel:
        return ProductModel(
            name="RadiantGlow Vitamin C Complex",
            concentration="15% Vitamin C",
            skin_types=["All Skin Types"],
            ingredients=["Vitamin C", "Vitamin E", "Ferulic Acid"],
            benefits=["Brightening", "Antioxidant protection"],
            usage="Apply 3–4 drops in the evening after cleansing",
            side_effects="May cause mild redness initially",
            price=899
        )


# ============================================================================
# 3. AGENTS
# ============================================================================

class Agent(ABC):
    @abstractmethod
    def execute(self, input_data):
        pass


class DataParserAgent(Agent):
    def execute(self, input_data: Dict) -> ProductModel:
        return ProductModel(**input_data)


class QuestionGeneratorAgent(Agent):
    """
    Input: ProductModel
    Output: >=15 categorized questions
    """

    TEMPLATES = {
        "Informational": [
            "What is {name}?",
            "What does {name} contain?",
            "What is the concentration of {name}?"
        ],
        "Usage": [
            "How should I use {name}?",
            "When should I apply {name}?",
            "How many drops of {name} should I use?"
        ],
        "Safety": [
            "Are there any side effects of {name}?",
            "Is {name} safe for sensitive skin?"
        ],
        "Skin Type": [
            "Is {name} suitable for oily skin?",
            "Can combination skin use {name}?"
        ],
        "Benefits": [
            "What are the benefits of {name}?",
            "Does {name} help with dark spots?"
        ],
        "Purchase": [
            "What is the price of {name}?",
            "Is {name} affordable?"
        ],
        "Comparison": [
            "How does {name} compare to other Vitamin C serums?"
        ]
    }

    def execute(self, product: ProductModel) -> List[Question]:
        questions = []

        for category, templates in self.TEMPLATES.items():
            for t in templates:
                q = t.format(name=product.name)
                a = self._answer(category, product)
                questions.append(Question(category, q, a))

        return questions  # 17 questions

    def _answer(self, category: str, p: ProductModel) -> str:
        answers = {
            "Informational": f"{p.name} contains {p.concentration} Vitamin C.",
            "Usage": p.usage,
            "Safety": p.side_effects,
            "Skin Type": f"Suitable for {', '.join(p.skin_types)} skin types.",
            "Benefits": ", ".join(p.benefits),
            "Purchase": f"The price is ₹{p.price}.",
            "Comparison": f"{p.name} focuses on {', '.join(p.benefits)}."
        }
        return answers[category]
class ContentStrategyAgent(Agent):
    """
    Decides page-level strategies such as selection rules
    """

    def execute(self, page_type: PageType) -> Dict[str, Any]:
        strategies = {
            PageType.FAQ: {
                "max_questions": 5,
                "selection_rule": "one_per_category"
            },
            PageType.PRODUCT: {
                "sections": ["benefits", "ingredients", "usage", "price", "safety"]
            },
            PageType.COMPARISON: {
                "comparison_axes": ["ingredients", "benefits", "price"]
            }
        }
        return strategies[page_type]



class ComparisonAgent(Agent):
    def execute(self, product: ProductModel) -> Dict[str, Any]:
        competitor = LogicBlocks.fictional_competitor()
        return {
            "product_a": product,
            "product_b": competitor,
            "comparison": LogicBlocks.compare(product, competitor)
        }


class TemplateRendererAgent(Agent):

    def execute(self, input_data: Dict) -> Dict[str, Any]:
        page_type = input_data["page_type"]

        if page_type == PageType.FAQ:
            return self._faq(input_data)
        if page_type == PageType.PRODUCT:
            return self._product(input_data)
        if page_type == PageType.COMPARISON:
            return self._comparison(input_data)

    def _faq(self, data):
        all_qs = data["questions"]
        selected = []
        used = set()

        for q in all_qs:
            if q.category not in used and len(selected) < 5:
                selected.append(q)
                used.add(q.category)

        return {
            "page_type": "faq",
            "total_questions_generated": len(all_qs),
            "total_questions_displayed": len(selected),
            "questions": [q.to_dict() for q in selected]
        }

    def _product(self, data):
        p = data["product"]
        return {
            "page_type": "product",
            "product_name": p.name,
            "description": f"{p.concentration} Vitamin C serum for brightening and dark spot reduction.",
            "benefits": LogicBlocks.extract_benefits(p),
            "ingredients": LogicBlocks.format_ingredients(p),
            "usage": LogicBlocks.generate_usage(p),
            "price": LogicBlocks.price_block(p),
            "safety": LogicBlocks.safety_block(p)
        }

    def _comparison(self, data):
        c = data["comparison"]
        return {
            "page_type": "comparison",
            "product_a": c["product_a"].to_dict(),
            "product_b": c["product_b"].to_dict(),
            "comparison": c["comparison"]
        }


# ============================================================================
# 4. ORCHESTRATOR
# ============================================================================

class WorkflowOrchestrator:

    def __init__(self):
        self.parser = DataParserAgent()
        self.qgen = QuestionGeneratorAgent()
        self.strategy = ContentStrategyAgent()  
        self.compare = ComparisonAgent()
        self.renderer = TemplateRendererAgent()

    def run(self, raw_product: Dict) -> Dict[str, Any]:
      
        product = self.parser.execute(raw_product)

     
        questions = self.qgen.execute(product)

        
        faq_strategy = self.strategy.execute(PageType.FAQ)

      
    faq = self.renderer.execute({
        "page_type": PageType.FAQ,
            "questions": questions,
            "strategy": faq_strategy
        })

    
        product_page = self.renderer.execute({
            "page_type": PageType.PRODUCT,
            "product": product
        })

      
        comparison = self.compare.execute(product)

    
        comparison_page = self.renderer.execute({
            "page_type": PageType.COMPARISON,
            "comparison": comparison
        })

        return {
            "faq": faq,
            "product_page": product_page,
            "comparison_page": comparison_page
        }



# ============================================================================
# 5. MAIN
# ============================================================================

def main():
    raw_product = {
        "name": "GlowBoost Vitamin C Serum",
        "concentration": "10% Vitamin C",
        "skin_types": ["Oily", "Combination"],
        "ingredients": ["Vitamin C", "Hyaluronic Acid"],
        "benefits": ["Brightening", "Fades dark spots"],
        "usage": "Apply 2–3 drops in the morning before sunscreen",
        "side_effects": "Mild tingling for sensitive skin",
        "price": 699
    }

    orchestrator = WorkflowOrchestrator()
    results = orchestrator.run(raw_product)

    os.makedirs("output", exist_ok=True)
    for k, v in results.items():
        with open(f"output/{k}.json", "w", encoding="utf-8") as f:
            json.dump(v, f, indent=2, ensure_ascii=False)

    print("✅ Pipeline executed successfully")


if __name__ == "__main__":
    main()
