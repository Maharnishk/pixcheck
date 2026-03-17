<script>
  import { createEventDispatcher } from 'svelte';
  
  const dispatch = createEventDispatcher();
  let isDragging = false;
  let fileInput;

  function handleDrop(e) {
    isDragging = false;
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) dispatch('fileSelected', { file });
  }

  function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) dispatch('fileSelected', { file });
  }
</script>

<div 
  class="upload-zone {isDragging ? 'dragging' : ''}"
  on:dragenter|preventDefault={() => isDragging = true}
  on:dragleave|preventDefault={() => isDragging = false}
  on:dragover|preventDefault
  on:drop|preventDefault={handleDrop}
  role="button"
  tabindex="0"
  on:click={() => fileInput.click()}
  on:keydown={e => e.key === 'Enter' && fileInput.click()}
>
  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" class="icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
  
  <h3>Select Image File</h3>
  <p>Drag & drop or click to browse files system.</p>
  
  <input type="file" accept="image/*" bind:this={fileInput} on:change={handleFileSelect} class="hidden" />
</div>

<style>
  .upload-zone {
    border: 2px dashed #cbd5e1;
    border-radius: var(--radius-lg);
    background: var(--surface-color);
    padding: 4rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
  }

  .upload-zone:hover, .upload-zone.dragging {
    border-color: var(--primary-color);
    background: #f0fdf4;
  }

  .icon {
    color: #94a3b8;
    margin-bottom: 1rem;
  }

  .upload-zone:hover .icon {
    color: var(--primary-color);
  }

  h3 {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
  }

  p {
    color: var(--text-secondary);
    font-size: 0.95rem;
  }

  .hidden { display: none; }
</style>
