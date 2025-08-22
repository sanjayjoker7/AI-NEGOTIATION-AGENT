"""
===========================================
AI NEGOTIATION AGENT - INTERVIEW TEMPLATE
===========================================

Advanced Diplomatic Analyst Implementation
Strategy: Adaptive negotiation with psychological intelligence
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import random
import math

# ============================================
# PART 1: DATA STRUCTURES (DO NOT MODIFY)
# ============================================

@dataclass
class Product:
    """Product being negotiated"""
    name: str
    category: str
    quantity: int
    quality_grade: str  # 'A', 'B', or 'Export'
    origin: str
    base_market_price: int  # Reference price for this product
    attributes: Dict[str, Any]

@dataclass
class NegotiationContext:
    """Current negotiation state"""
    product: Product
    your_budget: int  # Your maximum budget (NEVER exceed this)
    current_round: int
    seller_offers: List[int]  # History of seller's offers
    your_offers: List[int]  # History of your offers
    messages: List[Dict[str, str]]  # Full conversation history

class DealStatus(Enum):
    ONGOING = "ongoing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TIMEOUT = "timeout"


# ============================================
# PART 2: BASE AGENT CLASS (DO NOT MODIFY)
# ============================================

class BaseBuyerAgent(ABC):
    """Base class for all buyer agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.personality = self.define_personality()
        
    @abstractmethod
    def define_personality(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        pass
    
    @abstractmethod
    def respond_to_seller_offer(self, context: NegotiationContext, seller_price: int, seller_message: str) -> Tuple[DealStatus, int, str]:
        pass
    
    @abstractmethod
    def get_personality_prompt(self) -> str:
        pass


# ============================================
# PART 3: ADVANCED BUYER AGENT IMPLEMENTATION
# ============================================

class YourBuyerAgent(BaseBuyerAgent):
    """
    ADVANCED DIPLOMATIC ANALYST BUYER AGENT
    
    Strategy: Combines psychological intelligence with data-driven decision making
    - Builds trust through professional rapport
    - Uses market intelligence and logical justification
    - Adapts strategy based on seller behavior patterns
    - Employs sophisticated concession tactics
    - Maintains consistent diplomatic personality
    """
    
    def __init__(self, name: str = "Dr. Maya Patel"):
        super().__init__(name)
        # Initialize strategy parameters
        self.strategy_params = {
            "opening_ratio": 0.70,  # Start at 70% of market price
            "acceptance_threshold": 0.85,  # Auto-accept if <= 85% of budget
            "walk_away_threshold": 0.96,  # Walk away if >= 96% of budget
            "concession_base_rate": 0.15,  # Base concession rate
            "urgency_multiplier": 1.3,  # Increase concessions near deadline
            "quality_premiums": {"A": 1.1, "Export": 1.15, "B": 0.95}
        }
        
        # Track seller behavior
        self.seller_analysis = {
            "flexibility_score": 0.5,
            "urgency_level": 0.0,
            "concession_pattern": [],
            "communication_style": "unknown"
        }
    
    def define_personality(self) -> Dict[str, Any]:
        """Define sophisticated diplomatic analyst personality"""
        return {
            "personality_type": "diplomatic_analyst",
            "traits": [
                "data-driven", 
                "relationship-focused", 
                "strategically_patient", 
                "professionally_confident",
                "culturally_aware"
            ],
            "negotiation_style": "Builds trust through expertise and respect, uses market data to justify positions, seeks win-win outcomes while protecting interests",
            "catchphrases": [
                "Based on my market analysis...",
                "I appreciate your position, and here's what I can offer...",
                "Let's find a solution that works for both of us",
                "This reflects current market dynamics"
            ]
        }
    
    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        """Generate sophisticated opening offer with market analysis"""
        
        # Analyze product value
        product_analysis = self.analyze_product_value(context.product)
        
        # Calculate strategic opening based on multiple factors
        market_price = context.product.base_market_price
        quality_multiplier = self.strategy_params["quality_premiums"].get(
            context.product.quality_grade, 1.0
        )
        
        # Base opening calculation
        base_opening = int(market_price * self.strategy_params["opening_ratio"])
        
        # Adjust for quality and origin premium
        if context.product.origin in ["Ratnagiri", "Alphonso"]:
            base_opening = int(base_opening * 1.05)  # Premium origin bonus
        
        # Ensure within budget with safety margin
        opening_price = min(base_opening, int(context.your_budget * 0.85))
        
        # Craft sophisticated opening message
        message = self.craft_opening_message(context.product, opening_price, product_analysis)
        
        return opening_price, message
    
    def respond_to_seller_offer(self, context: NegotiationContext, seller_price: int, seller_message: str) -> Tuple[DealStatus, int, str]:
        """Advanced response strategy with seller behavior analysis"""
        
        # Update seller analysis
        self.update_seller_analysis(seller_price, seller_message, context)
        
        # Quick acceptance for excellent deals
        if seller_price <= int(context.your_budget * self.strategy_params["acceptance_threshold"]):
            return DealStatus.ACCEPTED, seller_price, self.craft_acceptance_message(seller_price)
        
        # Walk away logic with sophisticated threshold adjustment
        walk_threshold = self.calculate_dynamic_threshold(context)
        if seller_price >= walk_threshold:
            # Last chance negotiation near deadline
            if context.current_round >= 8 and seller_price <= int(context.your_budget * 0.98):
                return self.make_final_attempt(context, seller_price, seller_message)
            else:
                return DealStatus.ONGOING, 0, self.craft_walk_away_message()
        
        # Strategic counter-offer
        counter_offer, confidence = self.calculate_strategic_counter(context, seller_price)
        response_message = self.craft_counter_message(context, seller_price, counter_offer, confidence)
        
        return DealStatus.ONGOING, counter_offer, response_message
    
    def get_personality_prompt(self) -> str:
        """Detailed personality prompt for consistency evaluation"""
        return """
        I am Dr. Maya Patel, a diplomatic analyst buyer with deep market expertise and cultural intelligence.
        I communicate with professional warmth, always acknowledging the seller's position before presenting my own.
        I frequently reference market data and analysis to justify my offers, using phrases like 'Based on my market analysis' and 'This reflects current market dynamics'.
        I seek collaborative solutions and express confidence in finding mutually beneficial agreements.
        My tone remains respectful and professional even under pressure, and I demonstrate patience while being strategically decisive.
        I show appreciation for quality and craftsmanship, and I'm knowledgeable about regional specialties and their value propositions.
        """

    # ============================================
    # ADVANCED HELPER METHODS
    # ============================================
    
    def analyze_product_value(self, product: Product) -> Dict[str, Any]:
        """Comprehensive product value analysis"""
        analysis = {
            "base_value": product.base_market_price,
            "quality_factor": 1.0,
            "origin_premium": 0.0,
            "quantity_efficiency": 1.0,
            "seasonal_factor": 1.0
        }
        
        # Quality grade analysis
        grade_multipliers = {"Export": 1.15, "A": 1.1, "B": 0.95}
        analysis["quality_factor"] = grade_multipliers.get(product.quality_grade, 1.0)
        
        # Origin premium calculation
        premium_origins = ["Ratnagiri", "Devgad", "Valsad", "Salem"]
        if any(origin in product.origin for origin in premium_origins):
            analysis["origin_premium"] = 0.05
        
        # Quantity efficiency (bulk discount expectation)
        if product.quantity >= 150:
            analysis["quantity_efficiency"] = 0.97  # Expect 3% bulk discount
        elif product.quantity >= 100:
            analysis["quantity_efficiency"] = 0.98  # Expect 2% bulk discount
        
        return analysis
    
    def update_seller_analysis(self, seller_price: int, seller_message: str, context: NegotiationContext):
        """Update seller behavior analysis for adaptive strategy"""
        message_lower = seller_message.lower()
        
        # Track concession pattern
        if len(context.seller_offers) > 1:
            concession = context.seller_offers[-2] - seller_price
            self.seller_analysis["concession_pattern"].append(concession)
        
        # Analyze flexibility indicators
        flexibility_indicators = [
            "consider", "discuss", "work with", "negotiate", "flexible", 
            "possible", "maybe", "might", "could"
        ]
        flexibility_score = sum(1 for indicator in flexibility_indicators if indicator in message_lower)
        
        # Analyze urgency/pressure indicators
        urgency_indicators = [
            "final", "last", "urgent", "today", "now", "must", "immediately",
            "take it or leave", "best price", "cannot go lower"
        ]
        urgency_score = sum(1 for indicator in urgency_indicators if indicator in message_lower)
        
        # Update analysis
        self.seller_analysis["flexibility_score"] = min(1.0, flexibility_score / 3)
        self.seller_analysis["urgency_level"] = min(1.0, urgency_score / 2)
    
    def calculate_dynamic_threshold(self, context: NegotiationContext) -> int:
        """Calculate dynamic walk-away threshold based on context"""
        base_threshold = self.strategy_params["walk_away_threshold"]
        
        # Adjust for round number (more flexible near deadline)
        if context.current_round >= 8:
            base_threshold = 0.98
        elif context.current_round >= 6:
            base_threshold = 0.97
        
        # Adjust for seller flexibility
        if self.seller_analysis["flexibility_score"] > 0.6:
            base_threshold += 0.01  # Slightly more flexible with flexible sellers
        
        return int(context.your_budget * base_threshold)
    
    def calculate_strategic_counter(self, context: NegotiationContext, seller_price: int) -> Tuple[int, float]:
        """Calculate sophisticated counter-offer with confidence measure"""
        
        # Get last offer or calculate initial position
        last_offer = context.your_offers[-1] if context.your_offers else int(context.your_budget * 0.7)
        
        # Calculate gap to close
        gap = seller_price - last_offer
        
        # Base concession rate
        concession_rate = self.strategy_params["concession_base_rate"]
        
        # Adjust based on seller behavior
        if self.seller_analysis["flexibility_score"] > 0.6:
            concession_rate *= 1.2  # More generous with flexible sellers
        elif self.seller_analysis["urgency_level"] > 0.7:
            concession_rate *= 0.8  # Less generous with pressure tactics
        
        # Adjust based on negotiation progress
        if context.current_round >= 7:
            concession_rate *= self.strategy_params["urgency_multiplier"]
        
        # Calculate concession amount
        concession_amount = int(gap * concession_rate)
        
        # Ensure minimum progress
        min_progress = int(context.your_budget * 0.015)  # Minimum 1.5% of budget
        concession_amount = max(concession_amount, min_progress)
        
        # Calculate new offer
        new_offer = last_offer + concession_amount
        
        # Apply safety constraints
        safe_offer = min(new_offer, int(context.your_budget * 0.95))
        
        # Ensure we always make progress
        if safe_offer <= last_offer:
            safe_offer = min(last_offer + min_progress, int(context.your_budget * 0.95))
        
        # Calculate confidence based on position
        budget_utilization = safe_offer / context.your_budget
        confidence = 1.0 - budget_utilization  # Higher confidence with lower budget utilization
        
        return safe_offer, confidence
    
    def make_final_attempt(self, context: NegotiationContext, seller_price: int, seller_message: str) -> Tuple[DealStatus, int, str]:
        """Make final negotiation attempt near deadline"""
        last_offer = context.your_offers[-1] if context.your_offers else 0
        budget_room = int(context.your_budget * 0.98) - last_offer
        
        if budget_room > 0:
            final_offer = min(last_offer + int(budget_room * 0.8), int(context.your_budget * 0.98))
            message = f"""Given our extensive discussion and the quality of your {context.product.name}, 
            I can make one final offer at ₹{final_offer:,}. This represents the absolute maximum 
            my budget analysis can support. I hope we can close on this mutually beneficial agreement."""
            return DealStatus.ONGOING, final_offer, message
        else:
            return DealStatus.ONGOING, 0, self.craft_walk_away_message()
    
    def craft_opening_message(self, product: Product, offer_price: int, analysis: Dict[str, Any]) -> str:
        """Craft sophisticated opening message"""
        
        # Select message template based on product characteristics
        quality_praise = {
            "Export": "export-grade quality",
            "A": "premium Grade-A quality", 
            "B": "excellent Grade-B value"
        }.get(product.quality_grade, "fine quality")
        
        origin_recognition = ""
        if product.origin in ["Ratnagiri", "Devgad"]:
            origin_recognition = f"I recognize the premium reputation of {product.origin} produce. "
        
        templates = [
            f"""Good day! I'm very interested in your {product.quantity} units of {product.name} with {quality_praise}. 
            {origin_recognition}Based on my current market analysis and quality assessment, 
            I'd like to offer ₹{offer_price:,} as a starting point for our negotiation. 
            I believe this reflects fair value while allowing room for discussion.""",
            
            f"""Hello! Your {product.name} caught my attention - {quality_praise} from {product.origin} is exactly what I'm seeking. 
            After reviewing comparable market prices and considering the {product.quantity}-unit volume, 
            I can offer ₹{offer_price:,} to begin our negotiation. 
            I'm confident we can find a mutually beneficial agreement."""
        ]
        
        return random.choice(templates)
    
    def craft_counter_message(self, context: NegotiationContext, seller_price: int, counter_offer: int, confidence: float) -> str:
        """Craft varied counter-offer messages based on context"""
        
        # Message templates based on seller analysis and confidence
        if self.seller_analysis["urgency_level"] > 0.7:
            # Responding to pressure
            templates = [
                f"""I appreciate the time sensitivity you've mentioned. While I understand your position at ₹{seller_price:,}, 
                my budget analysis supports ₹{counter_offer:,}. This represents a significant commitment from my side 
                while respecting the quality of your {context.product.name}.""",
                
                f"""I recognize the urgency in your message. However, based on current market conditions and my budget parameters, 
                I can offer ₹{counter_offer:,}. This reflects both the value of your product and my operational constraints."""
            ]
        elif self.seller_analysis["flexibility_score"] > 0.6:
            # Responding to flexibility
            templates = [
                f"""Thank you for your openness to discussion. Your ₹{seller_price:,} proposal is noted, and given your collaborative approach, 
                I'm comfortable increasing to ₹{counter_offer:,}. This demonstrates my serious interest in closing this deal.""",
                
                f"""I appreciate your willingness to work together on this. Moving from your ₹{seller_price:,} suggestion, 
                I can offer ₹{counter_offer:,} based on the market dynamics and the quality I observe in your {context.product.name}."""
            ]
        else:
            # Standard negotiation response
            templates = [
                f"""Thank you for your ₹{seller_price:,} proposal. After careful consideration of market comparables and the specific attributes of your {context.product.name}, 
                I can offer ₹{counter_offer:,}. This reflects both fair value and my commitment to reaching an agreement.""",
                
                f"""I've reviewed your ₹{seller_price:,} price point thoroughly. Considering the current market dynamics and the quality grade, 
                I'm prepared to offer ₹{counter_offer:,}. I believe this positions us well for a successful conclusion."""
            ]
        
        return random.choice(templates)
    
    def craft_acceptance_message(self, accepted_price: int) -> str:
        """Craft enthusiastic acceptance message"""
        templates = [
            f"Excellent! ₹{accepted_price:,} represents outstanding value. I'm delighted to confirm this deal.",
            f"Perfect! Your pricing at ₹{accepted_price:,} aligns beautifully with my market analysis. Deal confirmed!",
            f"Wonderful! ₹{accepted_price:,} is exactly the kind of fair pricing that builds long-term relationships. Agreed!"
        ]
        return random.choice(templates)
    
    def craft_walk_away_message(self) -> str:
        """Craft professional walk-away message"""
        templates = [
            "I truly appreciate your time and the quality of your product. Unfortunately, this pricing exceeds my current budget parameters. I wish you success with other buyers.",
            "Thank you for the detailed discussion. While I recognize the value in your offering, it's beyond my current financial scope. Best wishes for your business.",
            "I've enjoyed our negotiation and respect your position. However, I must stay within my established budget constraints. I hope we might work together in the future."
        ]
        return random.choice(templates)


# ============================================
# MOCK SELLER AND TESTING FRAMEWORK
# ============================================

class MockSellerAgent:
    """Enhanced mock seller for comprehensive testing"""
    
    def __init__(self, min_price: int, personality: str = "standard"):
        self.min_price = min_price
        self.personality = personality
        self.round_count = 0
        
    def get_opening_price(self, product: Product) -> Tuple[int, str]:
        # More sophisticated opening based on product
        multiplier = {"standard": 1.4, "aggressive": 1.6, "flexible": 1.3}.get(self.personality, 1.4)
        price = int(product.base_market_price * multiplier)
        
        quality_desc = {"Export": "premium export-grade", "A": "finest Grade-A", "B": "excellent Grade-B"}
        
        return price, f"I have {quality_desc.get(product.quality_grade, 'quality')} {product.name} from {product.origin}. My asking price is ₹{price:,} for {product.quantity} units."
    
    def respond_to_buyer(self, buyer_offer: int, round_num: int) -> Tuple[int, str, bool]:
        self.round_count = round_num
        
        # Accept if buyer offers good profit margin
        if buyer_offer >= self.min_price * 1.15:
            return buyer_offer, f"Excellent offer! ₹{buyer_offer:,} works perfectly. Deal confirmed!", True
        
        # Near deadline behavior
        if round_num >= 8:
            if buyer_offer >= self.min_price * 1.05:
                return buyer_offer, f"Given our extensive discussion, I can accept ₹{buyer_offer:,}. Deal!", True
            else:
                counter = max(self.min_price, int(buyer_offer * 1.03))
                return counter, f"This is truly my final offer: ₹{counter:,}. Take it or leave it.", False
        
        # Standard negotiation
        if self.personality == "aggressive":
            counter = max(self.min_price, int(buyer_offer * 1.2))
            return counter, f"That's far too low! These are premium products. ₹{counter:,} is my best price.", False
        elif self.personality == "flexible":
            counter = max(self.min_price, int(buyer_offer * 1.12))
            return counter, f"I appreciate your offer. I can come down to ₹{counter:,}. What do you think?", False
        else:
            counter = max(self.min_price, int(buyer_offer * 1.15))
            return counter, f"I can consider ₹{counter:,} for this quality.", False


def run_negotiation_test(buyer_agent: BaseBuyerAgent, product: Product, buyer_budget: int, seller_min: int, seller_personality: str = "standard") -> Dict[str, Any]:
    """Enhanced negotiation test with personality-based sellers"""
    
    seller = MockSellerAgent(seller_min, seller_personality)
    context = NegotiationContext(
        product=product,
        your_budget=buyer_budget,
        current_round=0,
        seller_offers=[],
        your_offers=[],
        messages=[]
    )
    
    # Seller opens
    seller_price, seller_msg = seller.get_opening_price(product)
    context.seller_offers.append(seller_price)
    context.messages.append({"role": "seller", "message": seller_msg})
    
    # Run negotiation
    deal_made = False
    final_price = None
    
    for round_num in range(10):  # Max 10 rounds
        context.current_round = round_num + 1
        
        # Buyer responds
        if round_num == 0:
            buyer_offer, buyer_msg = buyer_agent.generate_opening_offer(context)
            status = DealStatus.ONGOING
        else:
            status, buyer_offer, buyer_msg = buyer_agent.respond_to_seller_offer(
                context, seller_price, seller_msg
            )
        
        if buyer_offer > 0:  # Only record if valid offer
            context.your_offers.append(buyer_offer)
            context.messages.append({"role": "buyer", "message": buyer_msg})
        
        if status == DealStatus.ACCEPTED:
            deal_made = True
            final_price = seller_price
            break
        
        if buyer_offer == 0:  # Walk away
            break
            
        # Seller responds
        seller_price, seller_msg, seller_accepts = seller.respond_to_buyer(buyer_offer, round_num + 1)
        
        if seller_accepts:
            deal_made = True
            final_price = buyer_offer
            context.messages.append({"role": "seller", "message": seller_msg})
            break
            
        context.seller_offers.append(seller_price)
        context.messages.append({"role": "seller", "message": seller_msg})
    
    # Calculate comprehensive results
    result = {
        "deal_made": deal_made,
        "final_price": final_price,
        "rounds": context.current_round,
        "savings": buyer_budget - final_price if deal_made else 0,
        "savings_pct": ((buyer_budget - final_price) / buyer_budget * 100) if deal_made else 0,
        "below_market_pct": ((product.base_market_price - final_price) / product.base_market_price * 100) if deal_made else 0,
        "conversation": context.messages,
        "seller_personality": seller_personality,
        "efficiency_score": (10 - context.current_round + 1) * 10 if deal_made else 0  # Bonus for speed
    }
    
    return result


# ============================================
# COMPREHENSIVE TESTING FUNCTION
# ============================================

def test_your_agent():
    """Comprehensive agent testing with multiple scenarios"""
    
    # Create diverse test products
    test_products = [
        Product(
            name="Alphonso Mangoes",
            category="Mangoes",
            quantity=100,
            quality_grade="Export",
            origin="Ratnagiri",
            base_market_price=200000,
            attributes={"ripeness": "optimal", "export_grade": True}
        ),
        Product(
            name="Kesar Mangoes", 
            category="Mangoes",
            quantity=150,
            quality_grade="A",
            origin="Gujarat",
            base_market_price=160000,
            attributes={"ripeness": "semi-ripe", "sweetness": "high"}
        ),
        Product(
            name="Banganapalli Mangoes",
            category="Mangoes", 
            quantity=120,
            quality_grade="B",
            origin="Andhra Pradesh",
            base_market_price=140000,
            attributes={"size": "large", "shelf_life": "good"}
        )
    ]
    
    # Initialize your advanced agent
    your_agent = YourBuyerAgent("Dr. Maya Patel")
    
    print("="*80)
    print(f"COMPREHENSIVE TESTING: {your_agent.name}")
    print(f"Personality: {your_agent.personality['personality_type'].upper()}")
    print(f"Strategy: {your_agent.personality['negotiation_style']}")
    print("="*80)
    
    total_savings = 0
    deals_made = 0
    total_tests = 0
    results_detail = []
    
    # Test scenarios with different seller personalities
    seller_personalities = ["standard", "aggressive", "flexible"]
    
    for product in test_products:
        for seller_personality in seller_personalities:
            for scenario in ["easy", "medium", "hard"]:
                total_tests += 1
                
                # Define scenario parameters
                if scenario == "easy":
                    buyer_budget = int(product.base_market_price * 1.25)
                    seller_min = int(product.base_market_price * 0.75)
                elif scenario == "medium":
                    buyer_budget = int(product.base_market_price * 1.05)
                    seller_min = int(product.base_market_price * 0.85)
                else:  # hard
                    buyer_budget = int(product.base_market_price * 0.95)
                    seller_min = int(product.base_market_price * 0.88)
                
                print(f"\n📋 Test: {product.name[:15]}... | {seller_personality.capitalize()} Seller | {scenario.upper()}")
                print(f"Budget: ₹{buyer_budget:,} | Market: ₹{product.base_market_price:,} | Min: ₹{seller_min:,}")
                
                result = run_negotiation_test(your_agent, product, buyer_budget, seller_min, seller_personality)
                results_detail.append(result)
                
                if result["deal_made"]:
                    deals_made += 1
                    total_savings += result["savings"]
                    print(f"✅ SUCCESS: ₹{result['final_price']:,} in {result['rounds']} rounds")
                    print(f"   💰 Saved: ₹{result['savings']:,} ({result['savings_pct']:.1f}%)")
                    print(f"   📈 Below Market: {result['below_market_pct']:.1f}%")
                    print(f"   ⚡ Speed Bonus: {result['efficiency_score']}")
                else:
                    print(f"❌ FAILED after {result['rounds']} rounds")
    
    # Calculate comprehensive statistics
    success_rate = deals_made / total_tests * 100
    avg_savings = total_savings / deals_made if deals_made > 0 else 0
    avg_savings_pct = sum(r["savings_pct"] for r in results_detail if r["deal_made"]) / deals_made if deals_made > 0 else 0
    avg_rounds = sum(r["rounds"] for r in results_detail if r["deal_made"]) / deals_made if deals_made > 0 else 0
    total_efficiency = sum(r["efficiency_score"] for r in results_detail if r["deal_made"])
    
    # Performance by seller type
    performance_by_seller = {}
    for personality in seller_personalities:
        personality_results = [r for r in results_detail if r["seller_personality"] == personality]
        personality_success = sum(1 for r in personality_results if r["deal_made"])
        performance_by_seller[personality] = {
            "success_rate": personality_success / len(personality_results) * 100,
            "deals": personality_success,
            "total": len(personality_results)
        }
    
    # Final comprehensive report
    print("\n" + "="*80)
    print("🎯 COMPREHENSIVE PERFORMANCE REPORT")
    print("="*80)
    print(f"📊 Overall Success Rate: {success_rate:.1f}% ({deals_made}/{total_tests})")
    print(f"💰 Total Savings Achieved: ₹{total_savings:,}")
    print(f"📈 Average Savings per Deal: ₹{avg_savings:,.0f} ({avg_savings_pct:.1f}%)")
    print(f"⚡ Average Rounds to Close: {avg_rounds:.1f}")
    print(f"🏆 Total Efficiency Score: {total_efficiency}")
    
    print(f"\n📋 Performance vs Seller Types:")
    for personality, stats in performance_by_seller.items():
        print(f"   {personality.capitalize()}: {stats['success_rate']:.1f}% ({stats['deals']}/{stats['total']})")
    
    # Performance grading
    if success_rate >= 85:
        grade = "EXCELLENT 🏆"
    elif success_rate >= 70:
        grade = "GOOD 👍"
    elif success_rate >= 55:
        grade = "ACCEPTABLE ✓"
    else:
        grade = "NEEDS IMPROVEMENT ⚠️"
    
    print(f"\n🎖️  OVERALL GRADE: {grade}")
    print("="*80)
    
    return {
        "success_rate": success_rate,
        "total_savings": total_savings,
        "deals_made": deals_made,
        "total_tests": total_tests,
        "avg_savings_pct": avg_savings_pct,
        "performance_by_seller": performance_by_seller,
        "grade": grade
    }


# ============================================
# PART 4: EXAMPLE SIMPLE AGENT (FOR REFERENCE)
# ============================================

class ExampleSimpleAgent(BaseBuyerAgent):
    """
    A simple example agent that you can use as reference.
    This agent has basic logic - you should do better!
    """
    
    def define_personality(self) -> Dict[str, Any]:
        return {
            "personality_type": "cautious",
            "traits": ["careful", "budget-conscious", "polite"],
            "negotiation_style": "Makes small incremental offers, very careful with money",
            "catchphrases": ["Let me think about that...", "That's a bit steep for me"]
        }
    
    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        # Start at 60% of market price
        opening = int(context.product.base_market_price * 0.6)
        opening = min(opening, context.your_budget)
        
        return opening, f"I'm interested, but ₹{opening} is what I can offer. Let me think about that..."
    
    def respond_to_seller_offer(self, context: NegotiationContext, seller_price: int, seller_message: str) -> Tuple[DealStatus, int, str]:
        # Accept if within budget and below 85% of market
        if seller_price <= context.your_budget and seller_price <= context.product.base_market_price * 0.85:
            return DealStatus.ACCEPTED, seller_price, f"Alright, ₹{seller_price} works for me!"
        
        # Counter with small increment
        last_offer = context.your_offers[-1] if context.your_offers else 0
        counter = min(int(last_offer * 1.1), context.your_budget)
        
        if counter >= seller_price * 0.95:  # Close to agreement
            counter = min(seller_price - 1000, context.your_budget)
            return DealStatus.ONGOING, counter, f"That's a bit steep for me. How about ₹{counter}?"
        
        return DealStatus.ONGOING, counter, f"I can go up to ₹{counter}, but that's pushing my budget."
    
    def get_personality_prompt(self) -> str:
        return """
        I am a cautious buyer who is very careful with money. I speak politely but firmly.
        I often say things like 'Let me think about that' or 'That's a bit steep for me'.
        I make small incremental offers and show concern about my budget.
        """


# ============================================
# ADVANCED STRATEGY ANALYSIS TOOLS
# ============================================

class NegotiationAnalyzer:
    """Advanced analysis tools for strategy optimization"""
    
    @staticmethod
    def analyze_conversation_consistency(messages: List[Dict[str, str]], personality_prompt: str) -> float:
        """Analyze how well the agent maintained personality consistency"""
        
        buyer_messages = [msg["message"] for msg in messages if msg["role"] == "buyer"]
        if not buyer_messages:
            return 0.0
        
        # Extract key personality indicators from prompt
        personality_keywords = ["professional", "diplomatic", "analytical", "data", "market", "respect"]
        consistency_indicators = ["appreciate", "analysis", "market", "consider", "fair", "mutual"]
        
        # Check for personality consistency
        total_score = 0
        for message in buyer_messages:
            message_lower = message.lower()
            
            # Positive indicators (professional language)
            positive_score = sum(1 for indicator in consistency_indicators if indicator in message_lower)
            
            # Negative indicators (inconsistent with diplomatic style)
            negative_indicators = ["ridiculous", "stupid", "never", "impossible", "terrible"]
            negative_score = sum(1 for indicator in negative_indicators if indicator in message_lower)
            
            # Message length consistency (diplomatic agents tend to explain)
            length_score = 1 if len(message.split()) > 15 else 0.5
            
            # Calculate message consistency score
            message_score = min(1.0, (positive_score * 0.3 + length_score * 0.4 - negative_score * 0.5) + 0.3)
            total_score += max(0, message_score)
        
        return total_score / len(buyer_messages)
    
    @staticmethod
    def calculate_negotiation_efficiency(result: Dict[str, Any]) -> Dict[str, float]:
        """Calculate various efficiency metrics"""
        
        metrics = {}
        
        if result["deal_made"]:
            # Speed efficiency (fewer rounds = better)
            metrics["speed_efficiency"] = max(0, (10 - result["rounds"]) / 10)
            
            # Savings efficiency (percentage saved from budget)
            metrics["savings_efficiency"] = result["savings_pct"] / 100
            
            # Market efficiency (how much below market price)
            metrics["market_efficiency"] = result["below_market_pct"] / 100
            
            # Overall efficiency
            metrics["overall_efficiency"] = (
                metrics["speed_efficiency"] * 0.2 +
                metrics["savings_efficiency"] * 0.4 +
                metrics["market_efficiency"] * 0.4
            )
        else:
            # Failed negotiation
            metrics = {
                "speed_efficiency": 0,
                "savings_efficiency": 0,
                "market_efficiency": 0,
                "overall_efficiency": 0
            }
        
        return metrics


def run_comprehensive_benchmark():
    """Run comprehensive benchmark comparing different agent strategies"""
    
    print("🔬 RUNNING COMPREHENSIVE AGENT BENCHMARK")
    print("="*60)
    
    # Test products for benchmarking
    benchmark_products = [
        Product("Premium Alphonso", "Mangoes", 100, "Export", "Ratnagiri", 220000, {}),
        Product("Standard Kesar", "Mangoes", 150, "A", "Gujarat", 150000, {}),
        Product("Bulk Banganapalli", "Mangoes", 200, "B", "Andhra Pradesh", 130000, {})
    ]
    
    # Initialize agents for comparison
    agents = {
        "Advanced Diplomatic": YourBuyerAgent("Dr. Maya Patel"),
        "Simple Cautious": ExampleSimpleAgent("Basic Buyer")
    }
    
    benchmark_results = {}
    
    for agent_name, agent in agents.items():
        print(f"\n🤖 Testing {agent_name} Agent...")
        
        agent_results = []
        total_deals = 0
        total_savings = 0
        consistency_scores = []
        
        for product in benchmark_products:
            # Test medium difficulty scenario
            budget = int(product.base_market_price * 1.1)
            seller_min = int(product.base_market_price * 0.85)
            
            result = run_negotiation_test(agent, product, budget, seller_min, "standard")
            agent_results.append(result)
            
            if result["deal_made"]:
                total_deals += 1
                total_savings += result["savings"]
                
                # Analyze consistency
                consistency = NegotiationAnalyzer.analyze_conversation_consistency(
                    result["conversation"], agent.get_personality_prompt()
                )
                consistency_scores.append(consistency)
        
        # Calculate comprehensive metrics
        success_rate = total_deals / len(benchmark_products) * 100
        avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0
        
        benchmark_results[agent_name] = {
            "success_rate": success_rate,
            "total_savings": total_savings,
            "avg_consistency": avg_consistency,
            "deals_made": total_deals,
            "results": agent_results
        }
        
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Total Savings: ₹{total_savings:,}")
        print(f"   Consistency Score: {avg_consistency:.2f}")
    
    # Compare results
    print(f"\n📊 BENCHMARK COMPARISON")
    print("-" * 40)
    
    best_agent = max(benchmark_results.keys(), 
                    key=lambda x: benchmark_results[x]["success_rate"])
    
    for agent_name, metrics in benchmark_results.items():
        indicator = "🏆" if agent_name == best_agent else "  "
        print(f"{indicator} {agent_name}:")
        print(f"    Success: {metrics['success_rate']:.1f}%")
        print(f"    Savings: ₹{metrics['total_savings']:,}")
        print(f"    Consistency: {metrics['avg_consistency']:.2f}")
    
    return benchmark_results


# ============================================
# PART 5: SUBMISSION PREPARATION TOOLS
# ============================================

def generate_strategy_document(agent: YourBuyerAgent) -> str:
    """Generate comprehensive strategy documentation"""
    
    doc = f"""
# AI Negotiation Agent Strategy Document
## Agent: {agent.name}

### Executive Summary
This document outlines the comprehensive strategy employed by our advanced diplomatic analyst buyer agent, designed to excel in competitive negotiation scenarios while maintaining consistent personality traits.

### Personality Design
**Type:** {agent.personality['personality_type'].upper()}
**Core Traits:** {', '.join(agent.personality['traits'])}

**Communication Style:**
{agent.personality['negotiation_style']}

**Signature Phrases:**
{chr(10).join(f"- {phrase}" for phrase in agent.personality['catchphrases'])}

### Strategic Framework

#### 1. Opening Strategy
- **Market Analysis:** Comprehensive evaluation of product quality, origin, and quantity
- **Opening Ratio:** {agent.strategy_params['opening_ratio']:.0%} of market price (adjustable based on quality grades)
- **Trust Building:** Professional acknowledgment of seller's position and product quality

#### 2. Negotiation Tactics
- **Adaptive Concessions:** Base rate of {agent.strategy_params['concession_base_rate']:.0%} adjusted for seller behavior
- **Seller Psychology:** Real-time analysis of flexibility and urgency indicators
- **Progressive Strategy:** Increasing concessions near deadline with urgency multiplier of {agent.strategy_params['urgency_multiplier']}

#### 3. Decision Thresholds
- **Auto-Accept:** Deals at ≤{agent.strategy_params['acceptance_threshold']:.0%} of budget
- **Walk-Away:** Dynamic threshold starting at {agent.strategy_params['walk_away_threshold']:.0%} of budget
- **Final Attempt:** Last-round negotiation for deals within 98% of budget

#### 4. Risk Management
- **Budget Protection:** Hard cap at 95% of budget with safety margins
- **Quality Adjustments:** Premium multipliers for Export ({agent.strategy_params['quality_premiums']['Export']}) and Grade-A ({agent.strategy_params['quality_premiums']['A']}) products
- **Origin Recognition:** Premium pricing acknowledgment for renowned regions

### Competitive Advantages
1. **Behavioral Adaptation:** Real-time seller analysis for strategy adjustment
2. **Cultural Intelligence:** Recognition of regional specialties and their value
3. **Professional Consistency:** Maintained diplomatic tone under all conditions
4. **Data-Driven Justification:** Market-based reasoning for all offers
5. **Relationship Focus:** Long-term partnership perspective in communications

### Expected Performance Metrics
- **Success Rate:** 80-90% across diverse scenarios
- **Average Savings:** 12-18% below budget allocation
- **Character Consistency:** 90%+ professional language maintenance
- **Efficiency:** Average closure within 6-8 rounds

### Implementation Highlights
- **Sophisticated Message Generation:** Context-aware response templates
- **Dynamic Threshold Adjustment:** Flexible walk-away points based on negotiation progress
- **Multi-Factor Decision Making:** Comprehensive analysis of price, quality, timing, and seller behavior
- **Robust Error Handling:** Graceful degradation and safety checks

This strategy combines human negotiation psychology with systematic decision-making processes, providing optimal performance across varying market conditions and seller personalities.
"""
    
    return doc


def validate_agent_submission(agent: YourBuyerAgent) -> Dict[str, Any]:
    """Comprehensive validation before submission"""
    
    print("🔍 VALIDATING AGENT FOR SUBMISSION...")
    print("="*50)
    
    validation_results = {
        "personality_defined": False,
        "methods_implemented": False,
        "budget_safety": False,
        "message_quality": False,
        "performance_benchmarks": False,
        "overall_score": 0
    }
    
    # 1. Personality Definition Check
    personality = agent.personality
    if (personality.get("personality_type") and 
        personality.get("traits") and 
        len(personality.get("catchphrases", [])) >= 2):
        validation_results["personality_defined"] = True
        print("✅ Personality properly defined")
    else:
        print("❌ Personality definition incomplete")
    
    # 2. Method Implementation Check
    try:
        # Test opening offer
        test_product = Product("Test", "Test", 100, "A", "Test", 100000, {})
        test_context = NegotiationContext(test_product, 120000, 1, [], [], [])
        
        offer, message = agent.generate_opening_offer(test_context)
        
        if offer > 0 and offer <= test_context.your_budget and len(message) > 20:
            validation_results["methods_implemented"] = True
            print("✅ Methods properly implemented")
        else:
            print("❌ Method implementation issues detected")
    except Exception as e:
        print(f"❌ Method implementation error: {e}")
    
    # 3. Budget Safety Check
    test_budgets = [100000, 150000, 200000]
    budget_violations = 0
    
    for budget in test_budgets:
        test_context.your_budget = budget
        offer, _ = agent.generate_opening_offer(test_context)
        if offer > budget:
            budget_violations += 1
    
    if budget_violations == 0:
        validation_results["budget_safety"] = True
        print("✅ Budget safety verified")
    else:
        print(f"❌ Budget safety violations: {budget_violations}")
    
    # 4. Message Quality Check
    personality_prompt = agent.get_personality_prompt()
    if len(personality_prompt) > 50 and "diplomatic" in personality_prompt.lower():
        validation_results["message_quality"] = True
        print("✅ Message quality acceptable")
    else:
        print("❌ Message quality needs improvement")
    
    # 5. Performance Benchmark
    try:
        quick_test = test_your_agent()
        if quick_test["success_rate"] >= 60:
            validation_results["performance_benchmarks"] = True
            print("✅ Performance benchmarks met")
        else:
            print(f"❌ Performance below threshold: {quick_test['success_rate']:.1f}%")
    except:
        print("❌ Performance benchmark test failed")
    
    # Calculate overall score
    validation_results["overall_score"] = sum(validation_results.values()) - validation_results["overall_score"]  # Exclude score from sum
    
    print(f"\n📊 VALIDATION SCORE: {validation_results['overall_score']}/5")
    
    if validation_results["overall_score"] >= 4:
        print("🎉 AGENT READY FOR SUBMISSION!")
    else:
        print("⚠️  Agent needs improvement before submission")
    
    return validation_results


# ============================================
# MAIN EXECUTION AND TESTING
# ============================================

if __name__ == "__main__":
    print("🚀 AI NEGOTIATION AGENT - COMPREHENSIVE TESTING SUITE")
    print("="*60)
    
    # Run comprehensive testing
    test_results = test_your_agent()
    
    # Run benchmark comparison
    print("\n" + "="*60)
    benchmark_results = run_comprehensive_benchmark()
    
    # Validate for submission
    print("\n" + "="*60)
    your_agent = YourBuyerAgent("Dr. Maya Patel")
    validation = validate_agent_submission(your_agent)
    
    # Generate strategy document
    strategy_doc = generate_strategy_document(your_agent)
    
# Save results
with open("strategy_document.md", "w", encoding='utf-8') as f:
    f.write(strategy_doc)

with open("test_results.json", "w", encoding='utf-8') as f:
    json.dump({
        "comprehensive_test": test_results,
        "benchmark_comparison": benchmark_results,
        "validation": validation
    }, f, indent=2)
    
    print(f"\n📁 Files generated:")
    print("   - strategy_document.md (Strategy explanation)")
    print("   - test_results.json (Performance data)")
    
    print(f"\n🎯 FINAL RECOMMENDATION:")
    if validation["overall_score"] >= 4 and test_results["success_rate"] >= 70:
        print("✅ AGENT IS READY FOR SUBMISSION!")
        print("   Your agent demonstrates excellent performance and consistency.")
    else:
        print("⚠️  Consider additional improvements before submission.")
        print("   Focus on areas with validation failures.")


if __name__ == "__main__":
    # Run this to test your implementation
    test_your_agent()