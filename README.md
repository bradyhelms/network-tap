# network-tap

## [Build Instructions](docs/build_instructions.md)

## Network Tap Project - Collaboration Guide

### Initial Setup
1. Clone the repository
   - Go to https://github.com/bradyhelms/network-tap
   - Click "Code" > "Clone"
   - Clone the repository locally
```bash
git clone https://github.com/bradyhelms/network-tap
cd network-tap
```

2. Confirm your access and verify the `origin` remote:
```bash
git remote -v
```

### Making Changes
1. Create a new branch for your feature/changes:
```bash
git checkout -b feature-name
```

2. Make changes in Vivado.

3. Stage and commit your changes.
```bash
git add .
git commit -m "Description of changes"
```

4. Push your branch to the central repo:
```bash
git push origin feature-name
```

### Submitting a pull request
1. Go to https://github.com/bradyhelms/network-tap

2. Click "Pull requests" > "New pull request"

3. Select:
* base: `main`
* compare: `feature-name`

4. Add a clear title and description of your changes.

5. Click "Create pull request"

### Keeping Your Branch Updated
1. Switch to your local `main` branch:
```bash
git checkout main
```

2. Getch changes from the central repository
```bash
git fetch origin
```

3. Merge the changes into your branch
```bash
git merge origin/main
```

4. Push updates to your feature branch (if necessary):
```bash
git push origin feature-name
```
