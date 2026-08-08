# Ransomware-Detection-System-using-machine-learning-techniques
Machine learning based system for detecting and classifying ransomware activity using data preprocessing, feature extraction, and classification techniques.
# Ransomware Detection ML System

A full-stack machine learning-powered ransomware detection web application that analyzes Windows executable files using PE header features and a trained Random Forest classifier.

## 🎯 Overview

This application provides a dark-themed cybersecurity dashboard for detecting ransomware in Windows executables (.exe files) using machine learning. The system analyzes PE (Portable Executable) header features and returns a classification ("Ransomware" or "Benign") with confidence scores and feature importance analysis.

## 🏗️ Architecture

### Frontend (React + TypeScript)
- **Framework**: React 19 with Tailwind CSS 4
- **Theme**: Dark cybersecurity aesthetic with OKLCH color space
- **Components**:
  - Landing page with feature showcase
  - Dashboard with sidebar navigation
  - File upload interface
  - Manual PE feature input form
  - Real-time analysis results display
  - Scan history table
  - Statistics dashboard with charts

### Backend (Node.js + Express)
- **Framework**: Express 4 with tRPC 11
- **Database**: MySQL/TiDB with Drizzle ORM
- **Authentication**: Manus OAuth
- **ML Integration**: Python child process invocation

### Machine Learning (Python)
- **Framework**: scikit-learn
- **Model**: Random Forest Classifier
- **Features**: 10 PE header features (entropy, sections, imports, exports, etc.)
- **Training Data**: Synthetic dataset (2,000 samples)
- **Output**: Prediction, confidence score, feature importance

## 📋 Features

### Core Functionality
1. **File Upload Analysis** - Upload .exe files for ransomware detection
2. **Manual Feature Input** - Enter PE header features directly without file upload
3. **Real-Time Predictions** - ML model inference via Python backend
4. **Threat-Level Indicators** - Color-coded risk badges (Red=Critical, Green=Safe)
5. **Feature Importance** - Top 5 features that influenced the prediction
6. **Scan History** - Database persistence of all scans with timestamps
7. **Statistics Dashboard** - Analytics with pie charts, bar charts, and trend lines
8. **Confidence Scores** - 0-100% confidence with probability breakdown

### PE Header Features Analyzed
- **Entropy**: File entropy (higher = more likely ransomware)
- **Sections**: Number of PE sections
- **Imports**: Number of imported functions
- **Exports**: Number of exported functions
- **Debug Info**: Presence of debug information
- **Relocation Info**: Presence of relocation information
- **Virtual Size**: Virtual memory size
- **Raw Size**: Raw file size
- **Resources**: Number of resources
- **Is DLL**: Whether file is a DLL

## 🚀 Getting Started

### Prerequisites
- Node.js 22.13.0+
- Python 3.11+
- pnpm package manager
- MySQL/TiDB database

### Installation

1. **Install dependencies**:
```bash
cd /home/ubuntu/ransomware-detection-ml
pnpm install
sudo pip3 install scikit-learn numpy
```

2. **Set up database**:
```bash
pnpm drizzle-kit generate
# Apply migrations via webdev_execute_sql
```

3. **Train ML model**:
```bash
cd ml_backend
python3 ransomware_detector.py train
```

4. **Start development server**:
```bash
pnpm dev
```

The application will be available at `http://localhost:3000`

## 📁 Project Structure

```
ransomware-detection-ml/
├── client/                    # React frontend
│   └── src/
│       ├── pages/
│       │   ├── Home.tsx      # Landing page
│       │   ├── Dashboard.tsx # Main dashboard
│       │   ├── ScanUpload.tsx # File upload & manual input
│       │   ├── ScanResults.tsx # Results display
│       │   ├── ScanHistory.tsx # Scan log
│       │   └── Statistics.tsx # Analytics
│       └── index.css         # Dark theme colors
├── server/                    # Node.js backend
│   ├── routers.ts            # tRPC procedures
│   ├── db.ts                 # Database helpers
│   ├── ml.ts                 # ML backend integration
│   └── scan.predict.test.ts  # ML router tests
├── ml_backend/               # Python ML backend
│   ├── ransomware_detector.py # Model & inference
│   ├── model.pkl             # Trained model
│   └── scaler.pkl            # Feature scaler
├── drizzle/                  # Database schema
│   └── schema.ts             # scanResults table
└── todo.md                   # Feature checklist
```

## 🧪 Testing

Run the test suite to verify ML prediction functionality:

```bash
pnpm test
```

Tests include:
- Benign file prediction (low entropy, high imports)
- Ransomware prediction (high entropy, low imports)
- Probability calculation validation
- Feature importance verification

All tests pass with 30-second timeout for Python ML inference.

## 🔌 API Endpoints

### tRPC Procedures

**`scan.predict`** - Predict ransomware classification
```typescript
Input: {
  filename: string
  entropy: number
  num_sections: number
  num_imports: number
  num_exports: number
  has_debug_info: number (0|1)
  has_relocation_info: number (0|1)
  virtual_size: number
  raw_size: number
  num_resources: number
  is_dll: number (0|1)
}

Output: {
  prediction: "Ransomware" | "Benign"
  confidence: number (0-100)
  probability_benign: number
  probability_ransomware: number
  top_features: Array<{name: string, importance: number}>
}
```

**`scan.getHistory`** - Retrieve scan history for authenticated user
```typescript
Output: Array<{
  id: number
  filename: string
  timestamp: Date
  predictionResult: "Ransomware" | "Benign"
  confidenceScore: number
  peFeatures: string (JSON)
}>
```

## 🎨 Dark Theme Colors

The application uses OKLCH color space for precise cybersecurity aesthetics:
- **Background**: `oklch(0.08 0.02 0)` - Deep black
- **Foreground**: `oklch(0.95 0.01 0)` - Off-white
- **Accent**: `oklch(0.5 0.3 120)` - Bright green
- **Threat Critical**: `oklch(0.65 0.35 0)` - Red
- **Threat Safe**: `oklch(0.5 0.25 150)` - Cyan

## 📊 Statistics Dashboard

The statistics page provides:
- **Total Scans**: Cumulative count
- **Ransomware Found**: Count of ransomware detections
- **Detection Rate**: Percentage of files classified as ransomware
- **Benign Files**: Count of benign files
- **Distribution Chart**: Pie chart of ransomware vs. benign
- **Confidence Chart**: Average confidence by prediction type
- **Recent Activity**: Line chart of last 7 scans

## 🔐 Security Considerations

1. **No File Storage**: Files are not stored; only PE features are persisted
2. **Server-Side Analysis**: ML inference happens on the server
3. **Database Encryption**: Use SSL/TLS for database connections
4. **Authentication**: Manus OAuth for user authentication
5. **Input Validation**: All PE features validated before ML inference

## 🚀 Deployment

To deploy to production:

1. **Create a checkpoint**:
```bash
webdev_save_checkpoint
```

2. **Click Publish** in the Manus Management UI

The application will be deployed to Manus hosting with:
- Autoscale serverless infrastructure
- Custom domain support
- Automatic SSL/TLS
- Database persistence

## 📝 Notes

- The ML model is trained on synthetic data for demonstration purposes
- Production use should train on real PE header datasets (VirusTotal, etc.)
- Python process timeout is set to 10 seconds for predictions
- ML model files (model.pkl, scaler.pkl) are persisted in ml_backend/

## 🤝 Contributing

To add new features:

1. Update `todo.md` with new feature
2. Implement backend changes in `server/`
3. Implement frontend changes in `client/src/`
4. Add tests in `server/*.test.ts`
5. Run `pnpm test` to verify
6. Create checkpoint before deployment

## 📄 License

This project is part of the Manus AI platform.
