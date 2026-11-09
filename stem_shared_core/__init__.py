# -*- coding: utf-8 -*-
"""
STEM Shared Core
Lõi công nghệ dùng chung cho hệ sinh thái phần mềm giáo dục STEM:
- cad_math_v2 (CAD Math Studio)
- geosolver (GeoSolver Studio)
- phys_solver (PhysLab Studio)
- chem_solver (ChemLab Studio)
- bio_solver (BioLab Studio)
"""
from pathlib import Path

CORE_DIR = Path(__file__).resolve().parent

try:
    from stem_shared_core.ai_model_hub import AIModelHub, HubConfig, ModelSource
except ImportError:
    pass

try:
    from stem_shared_core.ai_local_manager import (
        AILocalManager,
        AIPaths,
        MemoryMonitor,
        GeometryProblemContext,
        GenerationResult,
        ModelProfile,
        PROFILES,
    )
except ImportError:
    pass
