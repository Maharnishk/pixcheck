# PixCheck - AI Image Forgery Detection Frontend

This is the front-end interface built for presenting the PixCheck ML Model at the hackathon. It provides a stunning, modern mock UI with drag-and-drop file upload, a scanning animation with progress ring, and a result card that mimics ML outputs. 

## Tech Stack
- **Svelte** via Vite
- **Vanilla CSS** with a robust glassmorphic design system and CSS animations
- **Inter** Font Family

## How to Run Locally

1. Make sure you have Node.js installed on your machine.
2. In this directory (`frontend`), install the dependencies (if you haven't already):
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
4. Follow the local host link provided in the terminal (usually `http://localhost:5173`) to view the application.

## Modifying the Mock Responses

To integrate the frontend with your backend API, modify `src/App.svelte`.
Currently it simulates a response after 2.8s:

```javascript
// Simulate network request to ml backend
setTimeout(() => {
  isScanning = false;
  
  // Randomly mock result for hackathon presentation purposes
  const isTampered = Math.random() > 0.5;
  const confidence = isTampered ? (0.85 + Math.random() * 0.14) : (0.90 + Math.random() * 0.09);

  result = {
    isTampered,
    confidence
  };
}, 2800);
```

You can replace this `setTimeout` block with an actual `fetch()` call to your python backend.
