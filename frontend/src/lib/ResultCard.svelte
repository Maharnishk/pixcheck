<script>
  export let imageUrl;
  export let fileObj;
  export let isScanning = false;
  export let result = null; 

  function formatDate() {
    return new Date().toISOString().replace('T', ' ').substring(0, 19);
  }
</script>

<!-- SVG Filters for Forensic Visuals -->
<svg style="width:0; height:0; position:absolute;">
  <defs>
    <!-- Heatmap filter mockup -->
    <filter id="forensic-heatmap">
      <feColorMatrix type="matrix" values="
        0.3 0.6 0.1 0 0 
        0.3 0.6 0.1 0 0 
        0.3 0.6 0.1 0 0 
        0   0   0   1 0" result="gray"/>
      <feComponentTransfer in="gray">
        <!-- Blue to Red transition logic (rough approx) -->
        <feFuncR type="table" tableValues="0 0 0 1 1 1"/>
        <feFuncG type="table" tableValues="0 0 1 1 0 0"/>
        <feFuncB type="table" tableValues="1 1 0 0 0 0"/>
      </feComponentTransfer>
    </filter>

    <!-- Edge/Error Level mockup (high pass proxy) -->
    <filter id="forensic-ela">
      <!-- We use a convolve matrix to find edges -->
      <feConvolveMatrix order="3 3" kernelMatrix="-1 -1 -1  -1 8 -1  -1 -1 -1" />
      <!-- boost contrast immensely -->
      <feComponentTransfer>
        <feFuncR type="linear" slope="5" intercept="0"/>
        <feFuncG type="linear" slope="5" intercept="0"/>
        <feFuncB type="linear" slope="5" intercept="0"/>
      </feComponentTransfer>
      <feColorMatrix type="saturate" values="2" />
    </filter>

    <!-- Compression artifact proxy -->
    <filter id="forensic-compression">
      <feColorMatrix type="matrix" values="
        3 0 0 0 0
        0 0 0 0 0
        0 0 0 0 0
        0 0 0 1 0" />
      <feComponentTransfer>
        <feFuncR type="discrete" tableValues="0 0.2 0.5 0.8 1" />
      </feComponentTransfer>
    </filter>
  </defs>
</svg>

{#if isScanning}
  <div class="scanning-state">
    <div class="spinner"></div>
    <p>Processing forensic matrices...</p>
  </div>
{:else if result}
  <div class="card">
    
    <!-- Top Result Bar -->
    <div class="verdict-bar {result.isTampered ? 'bar-red' : 'bar-green'}">
      <strong>VERDICT: {result.isTampered ? 'TAMPERED' : 'AUTHENTIC'}</strong>
      <span class="sep">|</span>
      <span>Confidence: {(result.confidence * 100).toFixed(1)}%</span>
      <span class="sep">|</span>
      <span>Authentic: {result.authenticPct.toFixed(1)}%</span>
      <span>Tampered: {result.tamperedPct.toFixed(1)}%</span>
    </div>

    <!-- 6 Panel Grid -->
    <div class="forensic-grid">
      
      <!-- Panel 1: Original -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">Original Image</span>
          <span class="panel-subtitle">&nbsp;</span>
        </div>
        <div class="panel-image">
          <img src={imageUrl} alt="Original" />
        </div>
      </div>

      <!-- Panel 2: Heatmap -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">Heatmap</span>
          <span class="panel-subtitle">red = most suspicious</span>
        </div>
        <div class="panel-image">
          <img src={imageUrl} alt="Heatmap" class="filter-heatmap" />
        </div>
      </div>

      <!-- Panel 3: Overlay -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">Heatmap Overlay</span>
          <span class="panel-subtitle">&nbsp;</span>
        </div>
        <div class="panel-image overlay-stack">
          <img src={imageUrl} alt="Original base" class="base-img" />
          <img src={imageUrl} alt="Heatmap overlay" class="filter-heatmap overlay-img" />
        </div>
      </div>

      <!-- Panel 4: ELA -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">ELA — Error Level Analysis</span>
          <span class="panel-subtitle">bright = edited regions</span>
        </div>
        <div class="panel-image bg-black">
          <img src={imageUrl} alt="ELA Map" class="filter-ela" />
        </div>
      </div>

      <!-- Panel 5: Compression -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">Compression Artifacts</span>
          <span class="panel-subtitle">inconsistent blocks = tampered</span>
        </div>
        <div class="panel-image bg-black">
          <img src={imageUrl} alt="Compression Map" class="filter-compression" />
        </div>
      </div>

      <!-- Panel 6: Metadata -->
      <div class="panel">
        <div class="panel-header">
          <span class="panel-title">Metadata Analysis</span>
          <span class="panel-subtitle">&nbsp;</span>
        </div>
        <div class="metadata-box">
          <div class="meta-inner">
            <div class="meta-section">IMAGE METADATA</div>
            <br/>
            <div class="meta-key">Software:</div>
            <div class="meta-val">{result.isTampered ? 'Adobe Photoshop 2024' : 'Unknown / Original'}</div>
            <br/>
            <div class="meta-key">DateTime:</div>
            <div class="meta-val">{formatDate()}</div>
            <br/>
            {#if result.isTampered}
              <div class="meta-key">ALERT:</div>
              <div class="meta-val">Signature metadata suggests file modification.</div>
            {/if}
          </div>
        </div>
      </div>

    </div>
  </div>
{/if}

<style>
  .scanning-state {
    padding: 4rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    background: var(--surface-color);
    border: 1px solid var(--border-color);
  }

  .spinner {
    width: 32px;
    height: 32px;
    border: 3px solid #e5e7eb;
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1s infinite linear;
  }

  @keyframes spin { to { transform: rotate(360deg); } }

  .card {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin: 0 auto;
    background: white;
  }

  /* Verdict Bar styling from picture */
  .verdict-bar {
    text-align: center;
    padding: 1rem;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 2rem;
    text-transform: uppercase;
  }

  .bar-red {
    color: #ff0000;
  }
  
  .bar-green {
    color: #008000;
  }

  .sep {
    margin: 0 0.75rem;
    color: rgba(0,0,0,0.3);
  }

  /* Grid Layout */
  .forensic-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.5rem 1rem;
    width: 100%;
  }

  .panel {
    display: flex;
    flex-direction: column;
  }

  .panel-header {
    text-align: center;
    margin-bottom: 0.5rem;
    min-height: 2.5rem;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
  }

  .panel-title {
    font-size: 0.95rem;
    color: #000;
  }

  .panel-subtitle {
    font-size: 0.8rem;
    color: #000;
    margin-top: 0.1rem;
  }

  .panel-image {
    width: 100%;
    aspect-ratio: 16/10;
    background: #fff;
    border: 1px solid #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    position: relative;
  }

  .bg-black { background: #000; }

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  /* SVG Filters applied */
  .filter-heatmap {
    filter: url(#forensic-heatmap);
  }

  .filter-ela {
    filter: url(#forensic-ela);
  }

  .filter-compression {
    filter: url(#forensic-compression);
  }

  /* Overlay panel */
  .overlay-stack { position: relative; }
  .base-img { position: absolute; inset: 0; }
  .overlay-img { position: absolute; inset: 0; opacity: 0.5; mix-blend-mode: multiply; }

  /* Metadata Box matching screenshot */
  .metadata-box {
    width: 100%;
    aspect-ratio: 16/10;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 1rem;
  }

  .meta-inner {
    border: 1px solid #000;
    background: #ffffe0;
    width: 90%;
    padding: 1rem;
    font-family: Arial, sans-serif;
    font-size: 0.75rem;
    color: #000;
  }

  .meta-section {
    text-decoration: underline;
    margin-bottom: 0.5rem;
  }

  .meta-key {
    margin-bottom: 0.1rem;
  }
  
  .meta-val {
    margin-bottom: 0.5rem;
  }

  @media (max-width: 900px) {
    .forensic-grid {
      grid-template-columns: 1fr;
    }
  }
</style>
