# -*- coding: utf-8 -*-
from .physics_kernel import (
    solve_harmonic_oscillator,
    solve_rlc_circuit,
    get_fundamental_dimensions,
    check_dimensional_consistency,
    PhysicsKernelError,
)
from .physics_engine_ultimate import (
    Vector3D,
    OscillationPhysicsSolver,
    FluidDynamicsSolver,
    ThermodynamicsSolver,
    ElectromagnetismSolver,
    WavePhysicsSolver,
    CircuitPhysicsSolver,
    MechanicsPhysicsSolver,
    OpticsPhysicsSolver,
    NuclearPhysicsSolver,
    run_self_verification,
)

__all__ = [
    "solve_harmonic_oscillator",
    "solve_rlc_circuit",
    "get_fundamental_dimensions",
    "check_dimensional_consistency",
    "PhysicsKernelError",
    "Vector3D",
    "OscillationPhysicsSolver",
    "FluidDynamicsSolver",
    "ThermodynamicsSolver",
    "ElectromagnetismSolver",
    "WavePhysicsSolver",
    "CircuitPhysicsSolver",
    "MechanicsPhysicsSolver",
    "OpticsPhysicsSolver",
    "NuclearPhysicsSolver",
    "run_self_verification",
]
