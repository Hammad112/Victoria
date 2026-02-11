"""
Archetype Detector - Detects entrepreneurial archetype based on trait scores
"""

import logging
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Archetype:
    """Represents an entrepreneurial archetype"""
    name: str
    description: str
    key_traits: List[str]
    color: str
    score: float = 0.0

class ArchetypeDetector:
    """Detects entrepreneurial archetype based on trait scores"""
    
    def __init__(self):
        """Initialize archetype detector with predefined archetypes"""
        self.archetypes = {
            "strategic_innovation": Archetype(
                name="Strategic Innovation",
                description="This archetype is characterized by Risk Taking, Innovation and Orientation, Critical Thinking, and Decision Making. It emphasizes calculated and strategic innovative efforts.",
                key_traits=["Risk Taking", "Innovation Orientation", "Critical Thinking", "Decision Making"],
                color="#667eea"
            ),
            "resilient_leadership": Archetype(
                name="Resilient Leadership", 
                description="This archetype combines Resilience and Grit, Team Building, Servant Leadership, Adaptability, and Risk Taking. It highlights the importance of leading with empathy while building cohesive teams that can thrive amidst challenges.",
                key_traits=["Resilience and Grit", "Team Building", "Servant Leadership", "Adaptability", "Risk Taking"],
                color="#764ba2"
            ),
            "collaborative_responsibility": Archetype(
                name="Collaborative Responsibility",
                description="This archetype includes Servant Leadership, Team Building, and Accountability. It focuses on the growth and well-being of a team, emphasizing ownership of actions for building trust and a successful business.",
                key_traits=["Servant Leadership", "Team Building", "Accountability"],
                color="#f093fb"
            ),
            "ambitious_drive": Archetype(
                name="Ambitious Drive",
                description="This archetype is defined by Drive and Ambition, Resilience and Grit, and Problem Solving. These traits are essential for staying motivated and persevering through business challenges.",
                key_traits=["Drive and Ambition", "Resilience and Grit", "Problem Solving"],
                color="#4facfe"
            ),
            "adaptive_intelligence": Archetype(
                name="Adaptive Intelligence",
                description="This archetype is characterized by Critical Thinking, Problem Solving, Emotional Intelligence, and Adaptability. It emphasizes the ability to navigate complex situations with both analytical and emotional intelligence.",
                key_traits=["Critical Thinking", "Problem Solving", "Emotional Intelligence", "Adaptability"],
                color="#43e97b"
            )
        }
        
        # Mapping from full trait names to trait codes
        self.trait_name_to_code = {
            "Risk Taking": "RT",
            "Innovation Orientation": "IO", 
            "Critical Thinking": "CT",
            "Decision Making": "DM",
            "Resilience and Grit": "RG",
            "Team Building": "TB",
            "Servant Leadership": "SL",
            "Adaptability": "AD",
            "Accountability": "A",
            "Drive and Ambition": "DA",
            "Problem Solving": "PS",
            "Emotional Intelligence": "EI",
            "Relationship-Building": "RB",
            "Negotiation": "N",
            "Conflict Resolution": "C",
            "Approach to Failure": "F",
            "Social Orientation": "IN"
        }
    
    def detect_archetype(self, trait_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        Detect the best matching archetype for given trait scores
        
        Args:
            trait_scores: Dictionary of trait scores (trait_code: score)
            
        Returns:
            Dictionary containing detected archetype and confidence
        """
        best_archetype = None
        best_score = 0.0
        archetype_scores = {}
        
        for archetype_id, archetype in self.archetypes.items():
            # Calculate average score for key traits
            key_trait_scores = []
            for trait_name in archetype.key_traits:
                trait_code = self.trait_name_to_code.get(trait_name, trait_name)
                if trait_code in trait_scores:
                    key_trait_scores.append(trait_scores[trait_code])
            
            if key_trait_scores:
                avg_score = sum(key_trait_scores) / len(key_trait_scores)
                archetype_scores[archetype_id] = avg_score
                
                if avg_score > best_score:
                    best_score = avg_score
                    best_archetype = archetype
        
        if best_archetype:
            # Calculate confidence (0-1)
            confidence = min(best_score, 1.0)
            
            return {
                'archetype_name': best_archetype.name,
                'archetype_description': best_archetype.description,
                'archetype_color': best_archetype.color,
                'archetype_score': best_score,
                'confidence': confidence,
                'key_traits': best_archetype.key_traits,  # Add key traits to result
                'all_scores': archetype_scores
            }
        else:
            return {
                'archetype_name': 'Unknown',
                'archetype_description': 'Unable to determine archetype',
                'archetype_color': '#666666',
                'archetype_score': 0.0,
                'confidence': 0.0,
                'key_traits': [],  # Empty list for unknown archetype
                'all_scores': {}
            }
    
    def _calculate_trait_archetype_correlation(self, trait_name: str, archetype: Archetype) -> float:
        """
        Calculate correlation score between a trait and an archetype dynamically based on semantic categories.
        
        This replaces previous hardcoded defaults with a logic-based approach:
        1. Key Traits: 0.85 - 0.95 (Defining characteristics)
        2. Primary Category Match: 0.55 - 0.65 (Strongly related)
        3. Secondary Category Match: 0.40 - 0.50 (Moderately related)
        4. No Category Match: 0.20 - 0.35 (Foundational/Background)
        
        Args:
            trait_name: Full name of the trait
            archetype: Archetype object
            
        Returns:
            Correlation score between 0.0 and 1.0 (approximated)
        """
        # EXPLICIT OVERRIDE: Social Orientation should always be 0.0 as requested
        if trait_name == "Social Orientation":
            return 0.0

        # 1. Check if it's a Key Trait (Highest Correlation)
        if trait_name in archetype.key_traits:
            # Base score 0.85 + slight position variance
            trait_index = archetype.key_traits.index(trait_name)
            # 1st trait gets bonus, others slightly less
            return round(0.85 + max(0, 0.05 - (trait_index * 0.01)), 2)

        # Define Trait Semantic Categories
        trait_categories = {
            # Social / Interpersonal
            "Social Orientation": "Social",
            "Relationship-Building": "Social",
            "Team Building": "Social",
            "Servant Leadership": "Social",
            "Negotiation": "Social",
            "Conflict Resolution": "Social",
            "Emotional Intelligence": "Social",
            
            # Cognitive / Strategic
            "Decision Making": "Cognitive",
            "Decision-Making": "Cognitive", # Handle both formats
            "Problem Solving": "Cognitive",
            "Problem-Solving": "Cognitive", # Handle both formats
            "Critical Thinking": "Cognitive",
            "Innovation Orientation": "Cognitive",
            
            # Resilience / Drive / Execution
            "Resilience and Grit": "Resilience",
            "Resilience & Grit": "Resilience", # Handle variation
            "Drive and Ambition": "Resilience",
            "Drive & Ambition": "Resilience", # Handle variation
            "Risk Taking": "Resilience",
            "Risk-Taking": "Resilience", # Handle variation
            "Approach to Failure": "Resilience",
            "Adaptability": "Resilience",
            "Accountability": "Resilience"
        }
        
        # Define Archetype Category Focus (Primary, Secondary)
        # Derived from functionality and description
        archetype_focus = {
            "Strategic Innovation": {"primary": "Cognitive", "secondary": "Resilience"},
            "Resilient Leadership": {"primary": "Social", "secondary": "Resilience"},
            "Collaborative Responsibility": {"primary": "Social", "secondary": "Resilience"},
            "Ambitious Drive": {"primary": "Resilience", "secondary": "Cognitive"},
            "Adaptive Intelligence": {"primary": "Cognitive", "secondary": "Social"}
        }

        # Get categories
        this_trait_category = trait_categories.get(trait_name, "General")
        this_archetype_focus = archetype_focus.get(archetype.name, {"primary": "None", "secondary": "None"})
        
        # 2. Check for Primary Category Match (High Correlation)
        if this_trait_category == this_archetype_focus["primary"]:
            # Range 0.55 - 0.65
            # Use seed based on both trait and archetype to ensure uniqueness
            seed = sum(ord(c) for c in trait_name + archetype.name)
            variation = (seed % 11) * 0.01  # 0.00 to 0.10
            return round(0.55 + variation, 2)
            
        # 3. Check for Secondary Category Match (Medium Correlation)
        elif this_trait_category == this_archetype_focus["secondary"]:
            # Range 0.40 - 0.50
            seed = sum(ord(c) for c in trait_name + archetype.name)
            variation = (seed % 11) * 0.01 # 0.00 to 0.10
            return round(0.40 + variation, 2)
            
        # 4. No Match (Low / Foundational Correlation)
        else:
            # Range 0.20 - 0.35
            # Ensure "Social Orientation" specifically isn't 0.0 unless truly irrelevant (it never is fully)
            # Use deterministic hash-like value for stability
            # value between 0.20 and 0.35
            seed = sum(ord(c) for c in trait_name + archetype.name)
            variation = (seed % 15) * 0.01  # 0.00 to 0.14
            return round(0.20 + variation, 2)
    
    def get_archetype_correlation_data(self) -> Dict[str, List[float]]:
        """
        Get correlation data for heatmap visualization.
        
        Returns 17 values per archetype in the specific order required by visualization_engine.
        
        Returns:
            Dictionary mapping archetype names to lists of 17 correlation scores
        """
        # Define all traits in the exact order used by the heatmap
        # Note: This order must match the trait_names order in visualization_engine.py
        all_traits = [
            "Social Orientation",           # 0 - IN
            "Resilience and Grit",          # 1 - RG
            "Servant Leadership",           # 2 - SL
            "Emotional Intelligence",       # 3 - EI
            "Decision Making",              # 4 - DM
            "Problem Solving",              # 5 - PS
            "Drive and Ambition",           # 6 - DA
            "Innovation Orientation",       # 7 - IO
            "Adaptability",                 # 8 - AD
            "Critical Thinking",            # 9 - CT
            "Team Building",                # 10 - TB
            "Risk Taking",                  # 11 - RT
            "Accountability",               # 12 - A
            "Relationship-Building",        # 13 - RB
            "Negotiation",                  # 14 - N
            "Conflict Resolution",          # 15 - C
            "Approach to Failure"           # 16 - F
        ]
        
        correlation_data = {}
        
        # Calculate correlation scores for each archetype
        for archetype_id, archetype in self.archetypes.items():
            archetype_name = archetype.name
            correlation_scores = []
            
            for trait_name in all_traits:
                # Calculate correlation score dynamically
                score = self._calculate_trait_archetype_correlation(trait_name, archetype)
                correlation_scores.append(score)
            
            correlation_data[archetype_name] = correlation_scores
        
        # Add this at the end of the method
        logger.info(f"Archetype correlation data generated:")
        for arch_name, scores in correlation_data.items():
            logger.info(f"  {arch_name}: {len(scores)} traits, range: {min(scores):.2f}-{max(scores):.2f}")
        
        return correlation_data
