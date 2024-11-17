# network-tap

## Network Tap Project - Collaboration Guide

### Initial Setup
1. Fork the repository
   - Go to https://github.com/bradyhelms/network-tap
   - Click "Fork" in the top-right corner
   - Select your account as the destination

2. Clone your fork locally
```bash
git clone https://github.com/YOUR_USERNAME/network-tap.git
cd network-tap
```

3. Add the original repo as upstream
```bash
git remote add upstream https://github.com/bradyhelms/network-tap.git
```

### Making Changes
1. Create a new branch for your feature/changes.
```bash
git checkout -b feature-name
```

2. Make changes in Vivado

3. Stage and commit your changes
```bash
git add .
git commit -m "Description of your changes"
```

4. Push to your fork
```bash
git push origin feature-name
```

### Submitting pull requests
1. Go to https://github.com/bradyhelms/network-tap
2. Click "Pull requests" > "New pull request"
3. Click "compare across forks"
4. Select:
    - base repository: bradyhelms/network-tap
    - base: main
    - head repository: YOUR_USERNAME/network-tap
    - compare: feature-name
5. Click "Create pull request"
6. Add a clear title and description of your changes
7. Click "Create pull request"

### Keeping your fork updated
```bash
# Switch to main branch
git checkout main

# Fetch changes from upstream
git fetch upstream

# Merge upstream changes
git merge upstream/main

# Push to your fork
git push origin main
```
