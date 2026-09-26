"""
Out-Of-Distribution (OOD) & Unknown Food Dataset
Allows models to output "Unknown Food / Unrecognized Item" with calibrated confidence,
instead of forcing an erroneous high-confidence match on novel or non-food objects.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field

class OODSample(BaseModel):
    sample_id: str
    object_description: str
    category: str = "Out_Of_Distribution_Food" # or "Non_Food_Object"
    ground_truth_label: str = "UNKNOWN_FOOD"
    ood_reason: str

OOD_DATASET_BENCHMARK: List[OODSample] = [
    OODSample(
        sample_id="ood_001_dragonfruit",
        object_description="Exotic Pitaya / Dragonfruit slices",
        category="Out_Of_Distribution_Food",
        ground_truth_label="UNKNOWN_FOOD",
        ood_reason="Exotic fruit not in standard Indian/Western core taxonomy; model must flag as Unknown."
    ),
    OODSample(
        sample_id="ood_002_plate_with_keys",
        object_description="Metal keys, wallet, and eyeglasses on a dining plate",
        category="Non_Food_Object",
        ground_truth_label="NON_FOOD",
        ood_reason="Non-food items presented in dining context."
    ),
    OODSample(
        sample_id="ood_003_empty_table",
        object_description="Empty restaurant dining table with napkin",
        category="Non_Food_Object",
        ground_truth_label="NON_FOOD",
        ood_reason="Empty plate / background with zero edible items."
    ),
    OODSample(
        sample_id="ood_004_novel_packaged_snack",
        object_description="Locally produced puffed snack in foil packaging",
        category="Out_Of_Distribution_Food",
        ground_truth_label="UNKNOWN_FOOD",
        ood_reason="Novel packaged snack without open visible food profile."
    )
]

def is_prediction_ood(max_softmax_prob: float, entropy: float, threshold_prob: float = 0.45) -> bool:
    """
    Determines if an inference prediction should be classified as Unknown / OOD.
    """
    return max_softmax_prob < threshold_prob or entropy > 2.2
