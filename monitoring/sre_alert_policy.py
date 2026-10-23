"""Política SRE de clasificación y agregación de alertas PSI.

Esta política es una pieza nueva de auditoría; no sustituye un detector PSI.
Recibe los valores PSI ya calculados por un monitor externo.
"""
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class AlertDecision:
    level: str
    action: str
    variables: tuple[str, ...]
    max_psi: float


def classify_psi(psi_by_feature: Mapping[str, float]) -> AlertDecision:
    """Agrega PSI por lote para evitar una notificación por cada variable.

    Umbrales de la guía del proyecto: <0.10 normal; 0.10–<0.25 moderado;
    >=0.25 severo. Una sola variable severa crea ticket de investigación;
    dos o más variables severas escalan a alerta operativa inmediata.
    """
    if not psi_by_feature:
        return AlertDecision("record", "registrar lote sin PSI", (), 0.0)
    clean = {str(k): max(0.0, float(v)) for k, v in psi_by_feature.items()}
    max_psi = max(clean.values())
    moderate = tuple(sorted(k for k, v in clean.items() if v >= 0.10))
    severe = tuple(sorted(k for k, v in clean.items() if v >= 0.25))
    if len(severe) >= 2:
        return AlertDecision("alert", "pausar promoción y evaluar reentrenamiento", severe, max_psi)
    if severe:
        return AlertDecision("ticket", "investigar variable severa antes de promover", severe, max_psi)
    if moderate:
        return AlertDecision("ticket", "revisar tendencia en la siguiente ventana", moderate, max_psi)
    return AlertDecision("record", "conservar para diagnóstico", (), max_psi)
