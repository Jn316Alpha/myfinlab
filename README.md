<div align="center">
   <h1>MyFinLab</h1>
   <h3>Unified Financial Machine Learning & Statistical Arbitrage Library</h3>
   <p>Combining the best of mlfinlab and arbitragelab into one powerful package</p>
</div>

# MyFinLab

**MyFinLab** is a unified Python library that combines two powerful quantitative finance libraries:

- **mlfinlab** - Financial machine learning algorithms based on "Advances in Financial Machine Learning" by Marcos Lopez de Prado
- **arbitragelab** - Statistical arbitrage and pairs trading algorithms from academic research

## What is MyFinLab?

MyFinLab provides a comprehensive toolkit for quantitative finance, combining cutting-edge machine learning techniques with advanced statistical arbitrage strategies. This unified library makes it easy to leverage both financial ML and arbitrage algorithms in your trading and research workflows.

## Installation

```bash
pip install myfinlab
```

### Optional Dependencies

```bash
# With TensorFlow support
pip install myfinlab[tensorflow]

# With convex optimization
pip install myfinlab[cvxpy]

# With all optional dependencies
pip install myfinlab[all]

# For development
pip install myfinlab[dev]
```

## Quick Start

```python
import myfinlab

# Check version
print(myfinlab.get_version())  # 1.0.0

# Check available modules
print(myfinlab.is_mlfinlab_available())  # True
print(myfinlab.is_arbitragelab_available())  # True
```

## Features

### From mlfinlab:

- **Cross-validation**: Financial cross-validation methods (purging, embargoing)
- **Data Structures**: Imbalance bars, standard bars
- **Labeling**: Triple barrier, meta-labeling
- **Features**: Fractional differentiation
- **Bet Sizing**: Kelly criterion, ERC predictions
- **Feature Importance**: MDI, MDA, SFI importance
- **Sampling**: Sequential bootstrapping
- **Portfolio Optimization**: Hierarchical risk parity

### From arbitragelab:

- **Codependence**: Distance correlation, mutual information
- **Cointegration Approach**: Engle-Granger, Johansen, multi-cointegration
- **Copula Approach**: Archimedean, elliptical, and vine copulas
- **Distance Approach**: Various distance-based pair selection
- **Hedge Ratios**: ADF optimal, Box-Tiao, half-life
- **ML Approach**: Neural networks, clustering, feature expansion
- **Optimal Mean Reversion**: Ornstein-Uhlenbeck, CIR models
- **Time Series Approach**: ARIMA, OU optimal thresholds
- **Trading**: Z-score, minimum profit strategies

## Usage Examples

### Machine Learning (from mlfinlab)

```python
from myfinlab import labeling, bet_sizing

# Create triple barrier labels
events = labeling.get_events(
    close_prices,
    tp_sl=1,  # Take profit and stop loss threshold
    min_ret=0.01,  # Minimum return
    num_threads=3
)
```

### Statistical Arbitrage (from arbitragelab)

```python
from myfinlab import cointegration_approach, trading

# Find cointegrated pairs
coint_pairs = cointegration_approach.run_johansen(
    prices_dataframe,
    target_beta=0.5,
    significance_level=0.9
)

# Execute trading strategy
strategy = trading.ZScoreStrategy(
    entry_threshold=2.0,
    exit_threshold=0.0,
    close_threshold=0.5
)
```

## License

This project is licensed under the BSD-3-Clause License - see the [LICENSE.txt](LICENSE.txt) file for details.

## Acknowledgments

MyFinLab is built upon the excellent work of:

- **mlfinlab** - Originally by Hudson and Thames Quantitative Research
- **arbitragelab** - Originally by Hudson and Thames Quantitative Research

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For bug reports and feature requests, please open an issue on [GitHub](https://github.com/myfinlab/myfinlab/issues).

## Links

- [Documentation](https://myfinlab.readthedocs.io)
- [GitHub Repository](https://github.com/myfinlab/myfinlab)
- [Bug Reports](https://github.com/myfinlab/myfinlab/issues)
