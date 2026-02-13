---
name: Feature Engineering
description: Systematic techniques for transforming raw data into features that better represent the underlying problem structure, improving ML model performance
---

# Feature Engineering Patterns

## What It Is
A systematic collection of techniques for transforming raw data into features that better represent the underlying problem structure, improving machine learning model performance. Feature engineering is the process of using domain knowledge and statistical methods to create, select, and transform variables that make ML algorithms work more effectively. Often the difference between mediocre and excellent model performance comes from feature engineering, not algorithm selection.

## When to Use It
- Raw data doesn't directly match model input requirements (text, images, categorical data)
- Model performance plateaus despite hyperparameter tuning
- Domain knowledge suggests relationships not captured in raw features
- High-cardinality categorical variables need encoding
- Time series or sequential data requires temporal features
- Need to reduce dimensionality while preserving information

## Execution Steps

### 1. Understand the Data and Problem
Before engineering features, deeply understand the data types, distributions, and domain context. Feature engineering without domain knowledge often adds noise rather than signal.

**Action**: Perform EDA (exploratory data analysis): plot distributions (histograms, box plots), compute summary statistics (mean, median, std, quantiles), identify missing values, detect outliers, check correlations. Ask domain experts: "What matters here? What patterns indicate the outcome?" Document data types for each column: numeric (continuous/discrete), categorical (ordinal/nominal), text, datetime, boolean.

### 2. Handle Missing Values
Missing data is a feature engineering problem, not just a preprocessing step. How you handle missingness affects model performance and can encode useful information.

**Action**: Choose strategy based on missingness mechanism:
- **MCAR (Missing Completely At Random)**: Mean/median imputation for numeric, mode for categorical
- **MAR (Missing At Random)**: Model-based imputation (KNN, regression)
- **MNAR (Missing Not At Random)**: Create "is_missing" indicator feature, use special category for categorical
For time series: forward-fill or interpolation. Never delete rows unless missingness is <1% and MCAR.

### 3. Encode Categorical Variables
Convert categorical variables to numeric representations that preserve information and match model requirements. Different encodings suit different algorithms and cardinality levels.

**Action**: Apply encoding based on cardinality and ordinality:
- **Low cardinality (<10 categories), nominal**: One-hot encoding (create binary column per category)
- **Low cardinality, ordinal**: Label encoding (map to integers preserving order)
- **High cardinality (>10 categories)**: Target encoding (mean target per category), frequency encoding (count of each category), or embeddings (for neural networks)
Always use out-of-fold encoding for target encoding to prevent leakage.

### 4. Transform Numerical Features
Apply mathematical transformations to improve distributions, handle skewness, and meet algorithm assumptions. Many algorithms (linear models, k-NN) perform better with normalized features.

**Action**: Choose transformations:
- **Scaling**: StandardScaler (zero mean, unit variance) for algorithms sensitive to scale (SVM, k-NN, neural nets), MinMaxScaler (0-1 range) for bounded features
- **Skewness**: Log transform for right-skewed (log(x+1)), Box-Cox or Yeo-Johnson for general skewness
- **Outliers**: Winsorization (cap at percentiles), or robust scaling (median, IQR instead of mean, std)
- **Binning**: Discretize continuous variables when relationship is non-monotonic (age groups, income brackets)

### 5. Create Interaction and Domain Features
Engineer features that capture relationships between variables and domain-specific patterns. These often provide the biggest performance gains.

**Action**: Generate features based on domain knowledge:
- **Interactions**: Multiply features (price × quantity), divide (ratio features like debt-to-income), polynomial features (x², x³)
- **Aggregations**: Group-by statistics (customer's average transaction, product's median rating)
- **Temporal**: Extract from datetime (day of week, month, hour, is_weekend, days_since_event)
- **Geospatial**: Distance features (haversine distance, proximity to landmarks)
- **Text**: Length, word count, character patterns, TF-IDF, sentiment scores
Start with domain-informed features; avoid exhaustive feature generation (leads to overfitting).

### 6. Select and Validate Features
Not all engineered features improve performance; some add noise or redundancy. Use feature selection to identify the most valuable subset.

**Action**: Apply selection methods:
- **Filter methods**: Correlation with target (Pearson for regression, chi-square for classification), mutual information, variance threshold (remove low-variance features)
- **Wrapper methods**: Recursive feature elimination (RFE), forward/backward selection
- **Embedded methods**: L1 regularization (Lasso), tree-based feature importances
Validate with cross-validation: does performance improve on held-out data? If train improves but validation doesn't, features are overfitting.

## Real-World Applications

**Financial Services**
- Credit scoring: Debt-to-income ratio, payment history aggregations (missed_payments_last_12mo), account age
- Fraud detection: Transaction velocity (transactions per hour), deviation from user's typical behavior, geographic anomalies
- Algorithmic trading: Technical indicators (moving averages, RSI, MACD), volume-weighted averages, volatility measures

**E-Commerce & Marketing**
- Customer LTV prediction: Recency, frequency, monetary (RFM) features, product category diversity, average order value
- Churn prediction: Days since last activity, engagement trend (slope of activity), feature momentum (current vs historical mean)
- Recommendation systems: User-item interaction counts, category preferences, time-of-day patterns

**Healthcare**
- Disease prediction: Age-gender interactions, BMI, family history encodings, lab value ratios (glucose/insulin)
- Readmission risk: Length of stay, number of diagnoses, medication count, social determinants (zip code features)
- Medical imaging: Texture features (Haralick), shape descriptors, intensity histograms from images

**Natural Language Processing**
- Sentiment analysis: TF-IDF scores, word embeddings (Word2Vec, GloVe, BERT), negation handling, emoticon counts
- Spam detection: Email metadata (sender reputation, subject patterns), text statistics (uppercase ratio, link count)
- Document classification: N-gram frequencies (unigrams, bigrams), topic model features (LDA), named entity counts

**Time Series Forecasting**
- Sales forecasting: Lag features (values from previous timesteps), rolling statistics (7-day moving average), seasonal indicators
- Energy demand: Weather features (temperature, humidity), calendar effects (holidays, day-of-week), trend decomposition
- Financial forecasting: Technical indicators, ARIMA residuals as features, changepoint detection outputs

## Anti-Patterns

**Target leakage** → Using features that contain information about the target not available at prediction time; causes unrealistic performance estimates.

**Ignoring temporal ordering** → Computing statistics using future information in time series; validate on strictly future data.

**One-hot encoding high cardinality** → Creates thousands of sparse columns, explodes dimensionality; use target/frequency encoding instead.

**Not scaling features for distance-based algorithms** → Features with large ranges dominate distance calculations; always scale for k-NN, SVM, neural nets.

**Engineering features blindly** → Creating hundreds of arbitrary interactions without domain insight; adds noise and overfitting risk.

**Overfitting to validation set** → Iteratively engineering features while checking validation performance; final test set performance will be lower than expected.

## Success Metrics
- Model performance improves on held-out test set (not just validation)
- Feature importance analysis shows engineered features rank highly
- Features are interpretable and align with domain knowledge
- Dimensionality remains manageable (features << samples to avoid curse of dimensionality)
- Feature generation pipeline is reproducible and documented

## Related Frameworks
- **Automated Feature Engineering**: Tools like Featuretools, tsfresh for systematic feature generation
- **Feature Selection Methods**: Techniques for identifying most valuable features
- **Dimensionality Reduction**: PCA, t-SNE, autoencoders for compressing feature space
- **Feature Stores**: MLOps pattern for managing and serving features (Feast, Tecton)

## Common Pitfalls
- Not handling train/test split properly (fit scaler on train, transform test)
- Creating features that are constant or near-constant (zero variance)
- Ignoring multicollinearity (highly correlated features confuse linear models)
- Using mean imputation without creating missingness indicator
- Encoding test set categories not seen in training (handle unknowns with special category)
- Forgetting to save feature engineering pipeline for deployment (use sklearn Pipeline or custom transform classes)
- Over-engineering features before establishing strong baseline

## Tools & Resources
- **Libraries**: scikit-learn (preprocessing, encoding), pandas (data manipulation), category_encoders (advanced encodings)
- **Specialized**: featuretools (automated feature engineering), tsfresh (time series features), geopy (geospatial features)
- **Books**: "Feature Engineering for Machine Learning" (Zheng & Casari), "Feature Engineering and Selection" (Kuhn & Johnson)
- **Visualization**: Pandas Profiling, sweetviz for automated EDA and feature insights
- **Cheat Sheets**: Scikit-learn preprocessing guide, feature engineering for Kaggle competitions

## Feature Engineering Workflow

**Numeric Features**
1. Handle missing: impute + create is_missing flag
2. Transform: log for skewness, standardize/normalize
3. Discretize: bin into quantiles if non-linear relationship
4. Interactions: ratios, products with other features

**Categorical Features**
1. Handle missing: create "unknown" category
2. Encode: one-hot (<10 cats), target encoding (>10 cats)
3. Frequency: encode by count of occurrences
4. Groupby stats: aggregate numeric features by category

**Text Features**
1. Clean: lowercase, remove punctuation, tokenize
2. Basic: length, word count, character n-grams
3. Vectorize: TF-IDF (sklearn), word embeddings (Word2Vec, BERT)
4. Domain-specific: sentiment, entity extraction, topic models

**Datetime Features**
1. Extract: year, month, day, day_of_week, hour, minute
2. Cyclical: sin/cos encoding for periodic features (month, hour)
3. Relative: days_since_reference, time_until_event
4. Boolean: is_weekend, is_holiday, is_business_hours

**Image Features** (when not using CNNs)
1. Statistics: mean, std, histogram of pixel intensities
2. Texture: Haralick features, local binary patterns
3. Shape: contours, edge detection, connected components
4. Pre-trained: Extract features from pre-trained CNN layers

---
*Framework Type*: Data Transformation Methodology
*Domain*: Machine Learning, Data Science
*Practitioner Score*: 10/10 - Often the highest-leverage activity in ML projects, learned through practice
*Complexity*: Medium - Techniques are straightforward but knowing which to apply requires experience and domain knowledge
*Prerequisites*: Pandas, scikit-learn, basic statistics, understanding of ML algorithms' assumptions
