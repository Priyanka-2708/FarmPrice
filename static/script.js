/**
 * Farmer Market Price Information System — script.js
 * Handles: filter dropdowns, dashboard rendering with category & location filters
 */

const EMOJIS = {
  tomato:'🍅',potato:'🥔',onion:'🧅',brinjal:'🍆',carrot:'🥕',cabbage:'🥬',
  rice:'🌾',wheat:'🌿',maize:'🌽',soybean:'🫘',barley:'🌱',
  banana:'🍌',mango:'🥭',papaya:'🍈',grapes:'🍇',
  sugarcane:'🎋',cotton:'🌸',turmeric:'🟡'
};
const emoji = n => EMOJIS[n.toLowerCase()] || '🌱';

const BADGE = {
  'Vegetable':'badge-vegetable','Grain':'badge-grain',
  'Fruit':'badge-fruit','Cash Crop':'badge-cash'
};

// Load filter options from backend
async function loadFilters() {
  try {
    const res  = await fetch('/filters');
    const data = await res.json();

    const catSel   = document.getElementById('filterCategory');
    const stateSel = document.getElementById('filterState');

    data.categories.forEach(c => {
      const o = document.createElement('option');
      o.value = c; o.textContent = c;
      catSel.appendChild(o);
    });
    data.states.forEach(s => {
      const o = document.createElement('option');
      o.value = s; o.textContent = s;
      stateSel.appendChild(o);
    });
  } catch(e) { console.error('Filter load error:', e); }
}

// Apply filters & fetch prices
async function applyFilters() {
  const category = document.getElementById('filterCategory').value;
  const state    = document.getElementById('filterState').value;
  await loadPrices(category, state);
}

// Reset filters
function resetFilters() {
  document.getElementById('filterCategory').value = '';
  document.getElementById('filterState').value    = '';
  loadPrices('', '');
}

// Load & render price cards
async function loadPrices(category = '', state = '') {
  const grid = document.getElementById('priceGrid');
  const count = document.getElementById('resultCount');

  // Show skeletons while loading
  grid.innerHTML = Array(6).fill('<div class="skeleton-card"></div>').join('');
  count.textContent = 'Loading prices…';

  try {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (state)    params.append('state', state);

    const res  = await fetch('/all_prices?' + params.toString());
    const data = await res.json();

    grid.innerHTML = '';

    if (!data.success || !data.data.length) {
      grid.innerHTML = `
        <div class="no-results">
          <div class="no-results-icon">🔍</div>
          <p>No crops found for the selected filters.<br>Try a different category or location.</p>
        </div>`;
      count.textContent = '0 crops found';
      return;
    }

    count.textContent = `Showing ${data.data.length} crop${data.data.length !== 1 ? 's' : ''}`;

    data.data.forEach((crop, i) => {
      const badgeClass = BADGE[crop.category] || 'badge-grain';
      const card = document.createElement('div');
      card.className = 'crop-card';
      card.style.animationDelay = `${i * 0.06}s`;
      card.innerHTML = `
        <div class="card-top">
          <span class="crop-emoji">${emoji(crop.crop_name)}</span>
          <span class="category-badge ${badgeClass}">${crop.category}</span>
        </div>
        <div class="crop-name">${crop.crop_name}</div>
        <div class="crop-price"><sup>₹</sup>${crop.price_per_kg.toFixed(2)}<sub>/kg</sub></div>
        <div class="crop-location">📍 ${crop.market_location}</div>
        <span class="crop-state">📌 ${crop.state}</span>
      `;
      grid.appendChild(card);
    });

  } catch(e) {
    grid.innerHTML = '<div class="no-results"><div class="no-results-icon">⚠️</div><p>Failed to load prices. Please refresh.</p></div>';
    count.textContent = 'Error loading data';
    console.error('Price load error:', e);
  }
}

// Boot
loadFilters();
loadPrices();
fetch('/search_live?crop=Tomato')
  .then(res => res.json())
  .then(data => console.log(data));
  // Fetch live data for Tomato
fetch('/search_live?crop=Tomato')
  .then(res => res.json())
  .then(data => {
      if(data.success){
          let container = document.getElementById('tomato-info');
          container.innerHTML = ''; // Clear previous
          
          data.data.results.forEach(item => {
              let title = document.createElement('h4');
              title.textContent = item.title;
              
              let content = document.createElement('p');
              content.textContent = item.content;
              
              container.appendChild(title);
              container.appendChild(content);
          });
      }
  });
  function fetchLivePrice(crop) {
    fetch(`/search_live?crop=${crop}`)
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            console.log("Live Market Data:", data.data);
            // Display in your HTML
            document.getElementById("live-price").innerText = JSON.stringify(data.data, null, 2);
        } else {
            alert(data.message);
        }
    })
    .catch(err => console.error(err));
}
function fetchLivePrice(crop) {
    fetch(`/search_live?crop=${crop}`)
        .then(res => res.json())
        .then(data => {
            if(data.success){
                const display = `
                    Crop: ${crop}
                    Database Price: ₹${data.data.database_price}
                    Market: ${data.data.market_location}
                    Live Price: ${data.data.live_price ?? "Not available"}
                `;
                document.getElementById("live-price").innerText = display;
            } else {
                alert(data.message);
            }
        });
}function applyFilters() {
    const category = document.getElementById("filterCategory").value;
    const state    = document.getElementById("filterState").value;

    fetch(`/all_prices?category=${category}&state=${state}`)
        .then(res => res.json())
        .then(data => {
            const grid = document.getElementById("priceGrid");
            grid.innerHTML = "";

            if (data.success && data.data.length) {
                data.data.forEach(crop => {
                    grid.innerHTML += `
                        <div class="price-card">
                            <h3>${crop.crop_name}</h3>
                            <p>Category: ${crop.category}</p>
                            <p>Price: ₹${crop.price_per_kg}</p>
                            <p>Market: ${crop.market_location}</p>
                            <p>State: ${crop.state}</p>
                        </div>
                    `;
                });
                document.getElementById("resultCount").innerText = `${data.data.length} crops found`;
            } else {
                grid.innerHTML = `<p>No crops found for selected filters</p>`;
                document.getElementById("resultCount").innerText = `0 crops found`;
            }
        });
}
fetch(`/all_prices?category=${category}&state=Tamil Nadu`)