# CDSS Clinical User Guide

## System Overview
### Key Features:
- Real-time treatment optimization
- Probabilistic outcome simulations
- EHR-integrated workflow
- Interactive decision timelines

## Getting Started
1. **Login**: Use your institutional SSO credentials
2. **Patient Search**: 
```
Search by:
- Medical Record Number
- Name + DOB
- Current Diagnosis
```
3. **Dashboard Overview
![Dashboard zones:
- Patient Summary
- Active Alerts
- Treatment Options
- Simulation Panel

## Core Workflow
1. Load patient data
2. Review system-generated alerts
3. Adjust treatment constraints
4. Run simulation (Ctrl+Alt+S)
5. Compare outcome probabilities
6. Select final treatment path

## Advanced Features
- **What-If Analysis**: Modify lab values to see outcome impacts
- **Temporal Projections**: View 6-month outcome probabilities
- **Evidence Grading**: 
```
A: Strong evidence
B: Moderate evidence
C: Expert opinion
```

## Best Practices
- Always validate against latest lab results
- Use simulation for complex comorbidities
- Review confidence intervals
- Flag uncertain recommendations

## FAQ
Q: How often is model updated?
A: Nightly retraining with latest EHR data

Q: Missing diagnosis?
A: Contact CDSS admin team
