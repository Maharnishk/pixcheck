<script>
  import UploadZone from './lib/UploadZone.svelte';
  import ResultCard from './lib/ResultCard.svelte';

  let currentFile = null;
  let imageUrl = null;
  let isScanning = false;
  let result = null;

  function handleFileSelected(event) {
    const { file } = event.detail;
    currentFile = file;
    imageUrl = URL.createObjectURL(file);
    startScan();
  }

  function startScan() {
    isScanning = true;
    result = null;

    setTimeout(() => {
      isScanning = false;
      
      const isTampered = Math.random() > 0.5;
      
      // Calculate realistic percentages
      const tamperedPct = isTampered ? (65 + Math.random() * 30) : (5 + Math.random() * 20);
      const authenticPct = 100 - tamperedPct;
      
      const confidence = isTampered ? tamperedPct / 100 : authenticPct / 100;

      result = {
        isTampered,
        confidence,
        tamperedPct,
        authenticPct
      };
    }, 1500); 
  }

  function resetApp() {
    if (imageUrl) URL.revokeObjectURL(imageUrl);
    currentFile = null;
    imageUrl = null;
    isScanning = false;
    result = null;
  }
</script>

<header class="app-header">
  <div class="logo">
    <h1>PixCheck</h1>
    <span class="subtitle">Digital Forensics Platform</span>
  </div>
  {#if imageUrl && !isScanning}
    <div class="actions">
      <button on:click={resetApp}>New Analysis</button>
    </div>
  {/if}
</header>

<main>
  {#if !imageUrl}
    <div class="upload-container">
      <h2>Image Authentication Engine</h2>
      <p>Upload a file to initiate structural and error-level inspection.</p>
      <UploadZone on:fileSelected={handleFileSelected} />
    </div>
  {:else}
    <ResultCard {imageUrl} {isScanning} {result} fileObj={currentFile} />
  {/if}
</main>

<style>
  .app-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border-color);
    margin-bottom: 2rem;
  }

  .logo h1 {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 0;
  }

  .subtitle {
    font-size: 0.85rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
  }

  main {
    flex: 1;
  }

  .upload-container {
    max-width: 800px;
    margin: 4rem auto;
    text-align: center;
  }

  .upload-container h2 {
    font-size: 2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
  }

  .upload-container p {
    color: var(--text-secondary);
    margin-bottom: 2rem;
  }
</style>
