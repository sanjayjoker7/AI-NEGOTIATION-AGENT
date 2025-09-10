#!/usr/bin/env python3
"""
negotiation_agent_sanjay_full.py - Final Corrected Version

Fixes the ValueError by implementing a more robust regex for price parsing.
"""

from __future__ import annotations
import re
import json
import argparse
import requests
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

# -------------------------
# Try Concordia imports (optional fallback)
# -------------------------
try:
    from concordia.language_model import language_model
    from concordia.agents.entity_agent import EntityAgent
    from concordia.components.agent import observation
    CONCORDIA_AVAILABLE = True
except ImportError:
    CONCORDIA_AVAILABLE = False
    class language_model:
        class LanguageModel:
            def sample_text(self, prompt: str, **kwargs) -> str:
                raise NotImplementedError()
    class EntityAgent:
        def __init__(self, agent_name: str, components: List[Any], model: Any):
            self.agent_name = agent_name
            self.components = components
            self.model = model
        def act(self) -> Tuple[str, Dict]:
            pre_act_values = [c.make_pre_act_value() for c in self.components if hasattr(c, "make_pre_act_value")]
            prompt = "\n\n".join(pre_act_values)
            return self.model.sample_text(prompt), {}
    class observation:
        class Observation:
            def __init__(self, agent_name: str, memory: Any):
                self.agent_name = agent_name
                self.memory = memory
            def make_pre_act_value(self) -> str: return ""

# -------------------------
# Data structures
# -------------------------
@dataclass
class Product:
    name: str
    market_price: float
    description: str
    quantity: int = 1

    def __str__(self) -> str:
        return f"{self.name} (Market Price: ₹{self.market_price:,.2f}, Quantity: {self.quantity})"

class DealStatus(Enum):
    ONGOING = "ongoing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"

# -------------------------
# Simple associative memory
# -------------------------
class BasicAssociativeMemory:
    def __init__(self) -> None:
        self._store: List[Dict[str, Any]] = []

    def add(self, text: str, tags: Optional[List[str]] = None) -> None:
        self._store.append({"text": text, "tags": tags or []})

    def retrieve_all(self) -> List[str]:
        return [e["text"] for e in self._store]

    def clear(self) -> None:
        self._store.clear()

# -------------------------
# Agent Components
# -------------------------
class PersonalityComponent:
    def name(self) -> str: return "Personality"
    def make_pre_act_value(self) -> str:
        return ("You are Dr. Maya Patel, the Diplomatic Buyer.\n"
                "Traits: respectful, analytical, collaborative. Always justify offers with data and remain within budget.\n"
                "Signature phrases: 'Based on my analysis...', 'Let's find a mutually beneficial solution.'")

class ContextComponent:
    def __init__(self, product: Product, budget: float):
        self.product = product
        self.budget = float(budget)
    def name(self) -> str: return "Negotiation Context"
    def make_pre_act_value(self) -> str:
        pct = (self.budget / self.product.market_price * 100) if self.product.market_price else 0
        return (f"Product: {self.product.name}\n"
                f"Market Price: ₹{self.product.market_price:,.2f}\n"
                f"Maximum Budget: ₹{self.budget:,.2f} ({pct:.1f}% of market price)\n"
                "Objective: secure a deal within budget while maintaining rapport.")

class DecisionComponent:
    def __init__(self, agent_name: str, memory: BasicAssociativeMemory, product: Product, budget: float):
        self.agent_name = agent_name
        self.memory = memory
        self.product = product
        self.budget = budget
    def name(self) -> str: return "Decision"
    def _history(self) -> Tuple[int, List[float], List[float]]:
        mems = self.memory.retrieve_all()
        buyer_offers, seller_offers = [], []
        for m in mems:
            # Use a more robust regex to find numbers
            price_match = re.search(r'₹?(\d[\d,]*\.?\d*)', m)
            if price_match:
                try:
                    price = float(price_match.group(1).replace(",", ""))
                    if "[type: buyer_offer]" in m: buyer_offers.append(price)
                    if "[type: seller_offer]" in m: seller_offers.append(price)
                except (ValueError, IndexError):
                    continue
        return len(buyer_offers) + 1, buyer_offers, seller_offers

    def make_pre_act_value(self) -> str:
        round_num, buyer_offers, seller_offers = self._history()
        prompt_parts = [f"Strategic Analysis — Round {round_num}"]
        
        if round_num == 1:
            suggested = min(self.product.market_price * 0.80, self.budget)
            prompt_parts.append(f"Suggested opening offer: ₹{suggested:,.2f}")
        elif seller_offers:
            last_seller = seller_offers[-1]
            last_buyer = buyer_offers[-1] if buyer_offers else self.product.market_price * 0.80
            
            if last_seller <= self.budget * 0.95:
                prompt_parts.append(f"Strategic Goal: ACCEPT THE DEAL at seller price ₹{last_seller:,.2f}")
            elif last_seller > self.budget:
                prompt_parts.append(f"Strategic Goal: POLITELY WALK AWAY — seller's price ₹{last_seller:,.2f} exceeds budget ₹{self.budget:,.2f}")
            else:
                gap = last_seller - last_buyer
                concession_factor = 0.20 if round_num >= 7 else 0.15
                suggested = min(last_buyer + gap * concession_factor, self.budget)
                prompt_parts.append(f"Suggested counter-offer: ₹{suggested:,.2f}")
        return "\n".join(prompt_parts)

# -------------------------
# LLM Implementations
# -------------------------
class MockLLM(language_model.LanguageModel if CONCORDIA_AVAILABLE else object):
    def sample_text(self, prompt: str, **kwargs) -> str:
        if "ACCEPT THE DEAL" in prompt:
            m = re.search(r'at seller price ₹?([\d,]+\.?\d*)', prompt)
            price = m.group(1) if m else "the price"
            return f"Thank you, that is a fair price. I accept your offer of ₹{price}."
        if "POLITELY WALK AWAY" in prompt:
            return "I appreciate your time, but unfortunately that price is beyond my budget. I must walk away."
        
        m = re.search(r'Suggested.*?offer: ₹?([\d,]+(?:\.\d+)?)', prompt)
        if m:
            s = m.group(1)
            return f"Based on my analysis, I can offer ₹{s}."
        
        return "I am analyzing the offer. What is your best price?"

class OllamaLLM(language_model.LanguageModel if CONCORDIA_AVAILABLE else object):
    def __init__(self, model_name: str = "llama3", host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.host = host.rstrip("/")
    def sample_text(self, prompt: str, **kwargs) -> str:
        payload = {"model": self.model_name, "prompt": prompt, "stream": False}
        try:
            r = requests.post(f"{self.host}/api/generate", json=payload, timeout=60)
            r.raise_for_status()
            data = r.json()
            return data.get("response", "").strip()
        except Exception as e:
            return f"Ollama request failed: {e}"

# -------------------------
# Main Buyer Agent
# -------------------------
class ConcordiaBuyerAgent:
    def __init__(self, name: str, product: Product, budget: float, llm_model: Any):
        self.name = name
        self.budget = float(budget)
        self.memory = BasicAssociativeMemory()
        components = [
            PersonalityComponent(),
            ContextComponent(product, budget),
            DecisionComponent(name, self.memory, product, budget),
        ]
        self.entity_agent = EntityAgent(agent_name=name, components=components, model=llm_model)
        self.memory.add(components[1].make_pre_act_value(), tags=["context", "initial"])

    def negotiate(self, seller_message: str) -> Tuple[str, float, DealStatus]:
        if seller_message:
            self.memory.add(f"[type: seller_offer] Seller says: {seller_message}")
        
        response_text, _ = self.entity_agent.act()
        offer_price, status = self._parse_response(response_text)
        
        if offer_price > self.budget:
            offer_price = self.budget
            response_text += f"\n(Note: adjusted offer to respect budget cap of ₹{self.budget:,.2f}.)"

        self.memory.add(f"[type: buyer_offer] {response_text}")
        return response_text, offer_price, status

    def _parse_response(self, response: str) -> Tuple[float, DealStatus]:
        """
        Robustly parses the agent's response to find status and price.
        """
        text = response or ""
        low = text.lower()
        
        status = DealStatus.ONGOING
        if any(p in low for p in ["i accept", "i agree", "we have a deal"]):
            status = DealStatus.ACCEPTED
        elif any(p in low for p in ["walk away", "decline", "cannot accept"]):
            status = DealStatus.REJECTED
        
        # Use a more specific regex that requires at least one digit
        price_match = re.search(r'₹?(\d[\d,]*\.?\d*)', text)
        price = float(price_match.group(1).replace(",", "")) if price_match else 0.0
        
        return price, status

# -------------------------
# Mock Seller (for testing)
# -------------------------
class MockSellerAgent:
    def __init__(self, personality: str = "standard", min_price: float = 0.0):
        self.personality, self.min_price, self.round = personality, float(min_price), 0
    def respond(self, buyer_offer: float, market_price: float) -> Tuple[str, float]:
        self.round += 1
        is_deal = buyer_offer > 0 and buyer_offer >= self.min_price
        
        if is_deal:
            return f"Fine, you have a deal at ₹{buyer_offer:,.2f}.", buyer_offer

        if self.personality == "aggressive":
            offer = market_price * 1.25 if self.round == 1 else max(self.min_price, buyer_offer * 1.20)
            return f"My final price is ₹{offer:,.2f}. Take it or leave it.", offer
        
        elif self.personality == "flexible":
            offer = market_price * 1.05 if self.round == 1 else (buyer_offer + self.min_price) / 2
            return f"How about we meet at ₹{offer:,.2f}?", offer
            
        else: # standard
            offer = market_price * 1.10 if self.round == 1 else max(self.min_price, buyer_offer * 1.12)
            return f"I can come down to ₹{offer:,.2f}.", offer

# -------------------------
# Test harness (scenarios)
# -------------------------
def run_test_suite(use_ollama: bool = False, max_rounds: int = 10):
    print("=" * 80 + "\nAI NEGOTIATION AGENT TEST SUITE — Corrected\n" + "=" * 80)

    scenarios = [
        (Product("Grade-A Alphonso (100 boxes)", 180000.0, "..."), 200000.0, 150000.0),
        (Product("Grade-B Kesar (150 boxes)", 150000.0, "..."), 140000.0, 125000.0),
        (Product("Export-Grade Mangoes (50 boxes)", 200000.0, "..."), 190000.0, 175000.0),
    ]
    results = []

    for idx, (product, buyer_budget, seller_min) in enumerate(scenarios, 1):
        for personality in ["standard", "aggressive", "flexible"]:
            print(f"\n-- Scenario {idx} | Product: {product.name} | Seller: {personality.upper()} --")
            llm = OllamaLLM() if use_ollama else MockLLM()
            buyer_agent = ConcordiaBuyerAgent("Dr. Maya Patel", product, buyer_budget, llm)
            seller_agent = MockSellerAgent(personality, seller_min)
            
            final_price, deal_status = 0.0, DealStatus.ONGOING
            seller_msg, seller_offer = seller_agent.respond(0.0, product.market_price)

            for round_num in range(1, max_rounds + 1):
                print(f"\nRound {round_num}\n  Seller: {seller_msg}")
                buyer_resp, buyer_offer, deal_status = buyer_agent.negotiate(seller_msg)
                print(f"  Buyer: {buyer_resp}")

                if deal_status == DealStatus.ACCEPTED:
                    # If buyer accepts, the final price is the one they accepted (seller's last offer)
                    final_price = seller_offer
                    break
                if deal_status == DealStatus.REJECTED:
                    break
                
                seller_msg, seller_offer = seller_agent.respond(buyer_offer, product.market_price)
                if "deal" in seller_msg.lower():
                    # If seller accepts, the final price is the buyer's last offer
                    final_price = buyer_offer
                    deal_status = DealStatus.ACCEPTED
                    print(f"  Seller: {seller_msg}")
                    break
            
            success = deal_status == DealStatus.ACCEPTED and final_price > 0
            savings_pct = ((buyer_budget - final_price) / buyer_budget * 100) if success and buyer_budget > 0 else 0
            results.append({'success': success, 'savings_pct': savings_pct})
            status_msg = f"DEAL ACCEPTED at ₹{final_price:,.2f} (Savings: {savings_pct:.1f}%)" if success else "NO DEAL"
            print(f"  *** {status_msg} ***")

    # Summary
    print("\n" + "=" * 80 + "\nSUMMARY\n" + "=" * 80)
    successes = [r for r in results if r['success']]
    if results:
        success_rate = len(successes) / len(results) * 100
        print(f"Overall Success Rate: {success_rate:.1f}% ({len(successes)}/{len(results)})")
    if successes:
        avg_savings = sum(r['savings_pct'] for r in successes) / len(successes)
        print(f"Average Savings (successful deals): {avg_savings:.1f}%")
    print("=" * 80)

# -------------------------
# CLI
# -------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the AI Negotiation Agent Test Suite.")
    parser.add_argument("--ollama", action="store_true", help="Use Ollama instead of MockLLM")
    parser.add_argument("--max-rounds", type=int, default=10, help="Max negotiation rounds")
    args = parser.parse_args()
    
    if args.ollama:
        try:
            requests.get("http://localhost:11434", timeout=3).raise_for_status()
            print("Ollama server found. Using OllamaLLM.")
        except Exception:
            print("Warning: Could not connect to Ollama — falling back to MockLLM.")
            args.ollama = False
            
    run_test_suite(use_ollama=args.ollama, max_rounds=args.max_rounds)