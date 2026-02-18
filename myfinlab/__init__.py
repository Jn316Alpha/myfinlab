"""
MyFinLab - Unified Financial Machine Learning & Statistical Arbitrage Library

This package combines:
- mlfinlab: Financial machine learning algorithms based on "Advances in Financial Machine Learning" by Marcos Lopez de Prado
- arbitragelab: Statistical arbitrage and pairs trading algorithms from academic research

MyFinLab provides a comprehensive toolkit for quantitative finance, combining cutting-edge
machine learning techniques with advanced statistical arbitrage strategies.
"""

__version__ = "1.0.0"
__author__ = "MyFinLab Community"

# Import from mlfinlab
try:
    from mlfinlab import (
        cross_validation,
        data_structures,
        filters,
        labeling,
        features,
        sample_weights,
        sampling,
        bet_sizing,
        feature_importance,
        ensemble,
        multi_product,
        multi_asset_estimators,
        portfolio_optimisation,
        util,
    )
    _mlfinlab_available = True
except ImportError:
    _mlfinlab_available = False

# Import from arbitragelab
try:
    from arbitragelab import (
        codependence,
        cointegration_approach,
        copula_approach,
        distance_approach,
        hedge_ratios,
        ml_approach,
        optimal_mean_reversion,
        other_approaches,
        spread_selection,
        stochastic_control_approach,
        tearsheet,
        time_series_approach,
        trading,
        util as arb_util,
    )
    _arbitragelab_available = True
except ImportError:
    _arbitragelab_available = False


def get_version():
    """Return the version of MyFinLab."""
    return __version__


def is_mlfinlab_available():
    """Check if mlfinlab module is available."""
    return _mlfinlab_available


def is_arbitragelab_available():
    """Check if arbitragelab module is available."""
    return _arbitragelab_available


__all__ = [
    "__version__",
    "get_version",
    "is_mlfinlab_available",
    "is_arbitragelab_available",
]
